"""ex06 — 통합 에이전트 모듈."""

from rich.console import Console
from rich.rule import Rule

from src.llm_factory import build_llm
from src.agent_helpers import (
    parse_agent_result,
    serialize_steps,
    clean_think_tags,
    fallback_response,
)
from src.mcp_tools import ALL_TOOLS

_console = Console(highlight=False)

STRUCTURED_TOOLS = {"leave_balance", "sales_sum", "list_employees"}
UNSTRUCTURED_TOOLS = {"search_documents"}


def _summarize_observation(obs):
    """도구 관찰 결과를 한 줄 요약 문자열로 축약한다."""
    if isinstance(obs, dict):
        if "name" in obs and "remaining_days" in obs:
            return (f"{obs.get('name')}({obs.get('emp_no')}, {obs.get('department')}) "
                    f"총 {obs.get('total_days')}일 · 사용 {obs.get('used_days')}일 · "
                    f"잔여 {obs.get('remaining_days')}일")
        if "results" in obs:
            n = obs.get("total_found", len(obs.get("results", [])))
            top = obs.get("results", [])[:1]
            if top:
                src = top[0].get("source", "?")
                sc = top[0].get("score", 0)
                return f"{n}건 수신 · 최상위 {src} (score={sc:.3f})"
            return f"{n}건 수신"
    text = str(obs)
    return text[:80] + ("..." if len(text) > 80 else "")


def _classify_by_tools(steps):
    """에이전트가 실제 호출한 도구 종류로 query_type을 사후 판정한다."""
    called = {getattr(a, "tool", "") for a, _ in steps}
    has_s = bool(called & STRUCTURED_TOOLS)
    has_u = bool(called & UNSTRUCTURED_TOOLS)
    if has_s and has_u:
        return "hybrid"
    if has_s:
        return "structured"
    if has_u:
        return "unstructured"
    return "unstructured"


# ---------------------------------------------------------------------------
# 시스템 프롬프트
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """당신은 사내 HR 및 업무 질문에 답변하는 AI 어시스턴트입니다.

사용 가능한 도구:
- leave_balance: 직원 연차 잔여 조회 (emp_no 또는 이름으로 검색)
- sales_sum: 매출 합계 조회 (부서, 기간 필터 가능)
- list_employees: 직원 목록 조회 (부서 필터 가능)
- search_documents: 사내 문서 검색 (절차, 정책, 안내 등)

**핵심 규칙 — 사전 지식 금지**:
- 사내 고유 정보(직원·연차·매출·규정·정책)는 모른다는 전제로 답하세요.
- 자기 지식으로 추측 금지. 반드시 도구 결과만 인용.
- 문서에 없으면 "문서에서 찾을 수 없습니다", DB에 없으면 "해당 정보를 찾을 수 없습니다"로 솔직히 답하세요.

**질문 유형별 도구 호출**:

1. **정형 질문**(이름·연차일수·매출·직원목록): DB 도구 호출.
   - 예: "김민준 연차" → leave_balance
   - 예: "영업부 매출" → sales_sum
   - 예: "개발부 직원 목록" → list_employees

2. **비정형 질문**(규정·정책·절차·방법·안내): search_documents 호출.
   - 예: "연차 신청 절차" → search_documents
   - 예: "출장 비용 규정" → search_documents

3. **복합 질문**(정형 + 비정형이 한 문장에 섞인 경우): **반드시 두 도구 모두 호출**.
   - 질문에 이름·숫자·목록 같은 DB 대상이 있으면 → DB 도구 호출
   - 질문에 규정·정책·절차 같은 문서 대상이 있으면 → search_documents 호출
   - 한쪽만 호출하고 끝내지 마세요. 정확히 하나씩 최소 두 번 호출한 후에 답변을 합칩니다.
   - 예: "정시우 연차 + 연차 사용 규정"
     → ① leave_balance(emp_no="정시우") 호출
     → ② search_documents(query="연차 사용 규정") 호출
     → ③ 둘의 결과를 합쳐 "정시우님의 연차 잔여는 N일입니다. 연차 사용 규정은 다음과 같습니다: ..." 형식으로 답변

4. 답변은 반드시 한국어로, 도구 결과만 바탕으로 작성하세요. 원본 JSON/딕셔너리는 그대로 출력하지 마세요."""


# ---------------------------------------------------------------------------
# 통합 에이전트 클래스
# ---------------------------------------------------------------------------

class IntegratedAgent:
    """정형 + 비정형 통합 ReAct 에이전트."""

    def __init__(self, llm=None):
        """에이전트를 초기화한다."""
        self._llm = llm or build_llm()
        self._agent_executor = self._build_agent_executor()

    def _build_agent_executor(self):
        """LangChain AgentExecutor를 생성한다."""
        try:
            from langchain.agents import AgentExecutor, create_tool_calling_agent
            from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

            # 1. 프롬프트 구성 (system + history + input + scratchpad)
            prompt = ChatPromptTemplate.from_messages([
                ("system", SYSTEM_PROMPT),
                MessagesPlaceholder(variable_name="chat_history", optional=True),
                ("human", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ])

            # 2. Tool Calling Agent 생성
            agent = create_tool_calling_agent(
                llm=self._llm,
                tools=ALL_TOOLS,
                prompt=prompt,
            )

            # 3. AgentExecutor 래핑 (중간 단계 반환 활성화)
            return AgentExecutor(
                agent=agent,
                tools=ALL_TOOLS,
                verbose=False,
                return_intermediate_steps=True,
                max_iterations=10,
                handle_parsing_errors=True,
            )
        except Exception as e:
            print(f"[경고] AgentExecutor 초기화 실패: {e}. 폴백 모드로 동작합니다.")
            return None

    def run(self, query):
        """질문을 처리하고 통합 응답을 반환한다."""
        _console.print(Rule("[bold]IntegratedAgent.run()[/bold]", style="grey50"))
        _console.print(f"[bold]질문:[/bold] {query}\n")

        # 1. 에이전트 실행
        if self._agent_executor is None:
            return fallback_response(self._llm, query, "unstructured")

        try:
            result = self._agent_executor.invoke({"input": query})
            answer = result.get("output", "답변을 생성하지 못했습니다.")
            steps = list(result.get("intermediate_steps", []))

            # 2. DeepSeek-R1 <think> 태그 제거
            answer = clean_think_tags(answer)

            # 3. 각 도구 호출 단계별 로그
            for i, (action, obs) in enumerate(steps, start=1):
                tool = getattr(action, "tool", "?")
                args = getattr(action, "tool_input", {})
                _console.print(f"[bold cyan][{i}단계][/bold cyan] 도구 호출: [bold]{tool}[/bold]")
                _console.print(f"  → 인자: {args}")
                _console.print(f"  → 결과: {_summarize_observation(obs)}\n")

            # 4. 사후 분류 — 실제 호출된 도구 종류로 질문 유형 확정
            query_type = _classify_by_tools(steps)

            # 5. 최종 답변 로그
            final_step = len(steps) + 1
            _console.print(f"[bold cyan][{final_step}단계][/bold cyan] LLM 최종 답변 생성 "
                           f"(분류: [bold]{query_type}[/bold])")
            _console.print(Rule("[bold green]최종 답변[/bold green]", style="green"))
            _console.print(answer)

            # 6. 응답 구조 반환
            structured_data, unstructured_data = parse_agent_result(steps)
            return {
                "answer": answer,
                "query_type": query_type,
                "structured_data": structured_data,
                "unstructured_data": unstructured_data,
                "steps": serialize_steps(steps),
            }
        except Exception as e:
            _console.print(f"[bold red]오류:[/bold red] {e}")
            return {
                "answer": f"처리 중 오류가 발생했습니다: {e}",
                "query_type": "unstructured",
                "structured_data": {},
                "unstructured_data": [],
                "steps": [],
            }


if __name__ == "__main__":
    import sys
    from src.db_helper import get_vectorstore

    DEFAULT_QUERY = "정시우 사원의 연차 잔여와 휴가 규정을 설명해주세요"
    query = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_QUERY

    get_vectorstore()
    IntegratedAgent().run(query)
