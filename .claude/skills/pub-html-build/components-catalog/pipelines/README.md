# Pipelines

> 순차 흐름·타임라인·파이프라인. 단계가 있고 방향이 있는 구조를 보여준다.

## 속함

- `.rag-pipeline-box` + `.rag-*` / `.s-*` 계열 (CH01 RAG 3단계)
- `.rc-timeline` (CH07 비용·시간 타임라인) — `rc-*` 접두어를 CH03 reindex-compare와 공유하지만 별개
- `.ec-cabinet` (CH07 임베딩 캐시 캐비닛)
- `.wrapper-arch` (CH07 래퍼 아키텍처)
- `.journey-forward` + `.jf-*` (CH01 여정 맵)
- `.journey-roadmap` + `.roadmap-*`, `.node-*` (CH01 노드 기반 로드맵)
- `.qr-flow` + `.qr-*` (CH06 QueryRouter 3단계 분기 플로우차트)
- `.evolve-flow` + `.ev-*` (CH01 단계별 좌→우 진화 — 도커·쿠버네티스 책)

## 속하지 않음

- 책 전체 구성도 → [`../fullmap/`](../fullmap/)
- 비교형 정적 대조 → [`../comparisons/`](../comparisons/)

## 주의

`rc-*` 접두어는 CH03 `reindex-compare`와 CH07 `rc-timeline` **두 곳에서 사용** 중. 같은 접두어가 두 컴포넌트에 걸쳐 있으므로:

- 신규 컴포넌트에 `rc-*` 추가 금지 (충돌 위험)
- `.rc-timeline` 내부 자식은 반드시 `.rc-tl-*` 접두어 사용 (`rc-tl-head`, `rc-tl-event`, `rc-tl-tag`). `.rc-card` / `.rc-doc` / `.rc-stage` 등 짧은 `rc-*`는 CH03 `reindex-compare` 소유
- 한 페이지 안에서 `.reindex-compare`와 `.rc-timeline`을 동시에 쓸 때 클래스 이름만 보고 헷갈리지 말 것. 항상 부모(`.reindex-compare` vs `.rc-timeline`)로 컨텍스트를 확인

## 컴포넌트 목록

### .rag-pipeline-box

**언제 쓰는가**: 3~5단계 순차 파이프라인을 박스 + 화살표로 도식화. 각 단계는 `.rag-step` 카드(번호·제목·기술 설명·비유 메타 4요소)이고, 단계 사이는 `.rag-arrow`(`→`)로 연결. 챕터 서두에서 "이 책에서 만들 파이프라인"을 한 장면으로 선언할 때 유효.

**사용 챕터**: CH01

**HTML 사용 예**:
```html
<div class="rag-pipeline-box">
  <div class="rag-pipeline-title">RAG 파이프라인. 사서가 일하는 순서</div>
  <div class="rag-pipeline">
    <div class="rag-step">
      <div class="s-num">1</div>
      <div class="s-title">문서 저장</div>
      <div class="s-desc">문서를 벡터로 변환<br>ChromaDB에 저장</div>
      <div class="s-meta">서가에 책 꽂기</div>
    </div>
    <div class="rag-arrow">→</div>
    <div class="rag-step">
      <div class="s-num">2</div>
      <div class="s-title">문서 검색</div>
      <div class="s-desc">질문과 가장 비슷한<br>문서를 자동으로 찾기</div>
      <div class="s-meta">사서가 책 찾기</div>
    </div>
    <div class="rag-arrow">→</div>
    <div class="rag-step">
      <div class="s-num">3</div>
      <div class="s-title">답변 생성</div>
      <div class="s-desc">찾은 문서를 LLM에<br>넘겨서 답변 생성</div>
      <div class="s-meta">AI가 읽고 답하기</div>
    </div>
  </div>
</div>
```

**렌더 CSS**: `styles/diagrams.css:20-28` (`.rag-pipeline-box`, `.rag-pipeline-title`, `.rag-pipeline`, `.rag-step`, `.rag-step .s-num`, `.s-title`, `.s-desc`, `.s-meta`, `.rag-arrow`)

**변형**: 단계 수 3~5 권장. `.s-meta`는 비유 한 줄 전용(예: "서가에 책 꽂기"), `.s-desc`는 기술 설명 전용. 두 줄 이상은 `<br>`로 끊는다. `.rag-arrow`는 단계 사이마다 필수.

**피해야 할 것**
- 단계 2개: 비교 의도라면 `.annotated-compare`(LLM vs 진실) 또는 `.reindex-compare`로 대체. 파이프라인은 "흐름"이 보여야 함
- 단계 6개 이상: 한 화면에 담기 어려움. 표(table) 또는 섹션 분할 권장
- `.s-meta`에 기술 용어 직접 기재(`embedding_model_name` 등) 금지 → `.s-meta`는 비유 회수 자리. 기술은 `.s-desc`로
- `.rag-arrow` 생략하고 박스만 나열 금지 → 순차성이 사라짐

### .rc-timeline

**언제 쓰는가**: 같은 입력이 시간 순서로 다른 결과(MISS/HIT/EXPIRED)를 내는 동작을 시간축 + 이벤트 카드로 도식화. 응답 캐시처럼 "TTL 안에 다시 오면 즉시 반환, 만료되면 다시 계산" 같은 시간 의존 동작을 한 장면에 담을 때 유효. 이벤트 카드(`.rc-tl-event`)는 modifier(`.rc-tl-miss` / `.rc-tl-hit` / `.rc-tl-expired`)로 색·점 색이 갈린다.

**사용 챕터**: CH07

**HTML 사용 예**:
```html
<div class="rc-timeline">
  <div class="rc-tl-head">
    <span class="rc-tl-kind">ResponseCache</span>
    <span class="rc-tl-sub">같은 질문을 시간 순서로 추적</span>
  </div>
  <div class="rc-tl-axis">
    <div class="rc-tl-time">09:00</div>
    <div class="rc-tl-time">09:30</div>
    <div class="rc-tl-time">10:01</div>
    <div class="rc-tl-bar"></div>
  </div>
  <div class="rc-tl-events">
    <div class="rc-tl-event rc-tl-miss">
      <div class="rc-tl-q">"병가 증빙?"</div>
      <div class="rc-tl-tag">MISS</div>
      <div class="rc-tl-action">서가 가서 찾음<br>→ 메모장 기록<br><span class="rc-tl-latency">20초</span></div>
      <div class="rc-tl-ttl">⏱ TTL 시작</div>
    </div>
    <div class="rc-tl-event rc-tl-hit">
      <div class="rc-tl-q">"병가 증빙?"</div>
      <div class="rc-tl-tag">HIT</div>
      <div class="rc-tl-action">메모장 확인<br>→ 즉시 반환<br><span class="rc-tl-latency">0.1초</span></div>
      <div class="rc-tl-ttl">⏱ 잔여 30분</div>
    </div>
    <div class="rc-tl-event rc-tl-expired">
      <div class="rc-tl-q">"병가 증빙?"</div>
      <div class="rc-tl-tag">EXPIRED</div>
      <div class="rc-tl-action">메모장 만료<br>→ 다시 서가로<br><span class="rc-tl-latency">20초</span></div>
      <div class="rc-tl-ttl">⏱ 새 TTL 시작</div>
    </div>
  </div>
  <div class="rc-tl-store">
    <code>self._store = {hash: (answer, expires_at)}</code>
  </div>
  <div class="cf-caption">그림 7-4. ResponseCache는 <b>유통기한이 있는 메모장</b>. 같은 질문이 TTL 안에 다시 오면 서가(LLM)를 건너뜁니다</div>
</div>
```

**렌더 CSS**: `styles/diagrams.css:930-1073` (`.rc-timeline`, `.rc-tl-head`, `.rc-tl-kind`, `.rc-tl-sub`, `.rc-tl-axis`, `.rc-tl-time`, `.rc-tl-bar`, `.rc-tl-events`, `.rc-tl-event`, `.rc-tl-event::before`, `.rc-tl-miss/.hit/.expired`, `.rc-tl-q`, `.rc-tl-tag`, `.rc-tl-action`, `.rc-tl-latency`, `.rc-tl-ttl`, `.rc-tl-store`)

**변형**: 시간 슬롯 3개(`.rc-tl-time` × 3)와 이벤트 카드 3개(`.rc-tl-event` × 3) 1:1 대응이 기본. 이벤트 modifier는 `.rc-tl-miss` / `.rc-tl-hit` / `.rc-tl-expired` 세 가지. `.rc-tl-store`는 선택(자료구조 한 줄 코드 표시). 캡션은 `.cf-caption`(공용 캐시 캡션)을 그대로 사용한다.

**피해야 할 것**
- **`rc-*` 네임스페이스 충돌**: `.rc-card` / `.rc-doc` / `.rc-stage` 등 CH03 `reindex-compare` 클래스를 `.rc-timeline` 자식으로 끌어와 쓰지 말 것. `.rc-timeline` 내부는 항상 `.rc-tl-*` 접두어
- 시간 슬롯 4개 이상: 한 줄 그리드(3 컬럼)가 전제. 늘리면 그리드 깨짐 → `.rc-tl-axis` / `.rc-tl-events` `grid-template-columns` 동시 수정 필요
- modifier 누락(`.rc-tl-event`만 있고 `.rc-tl-miss/.hit/.expired` 없음): 점 색이 기본 accent로만 찍혀 사건 종류가 구분 안 됨
- 시간 진행이 없는 정적 비교에 사용 금지 → `.cache-compare` 또는 `.annotated-compare` 사용

### .ec-cabinet

**언제 쓰는가**: 키-파일 매핑이 미리 저장돼 있고, 새 입력이 들어오면 HIT/MISS로 갈리는 **상태 시각화**. 임베딩 캐시처럼 "텍스트 → 파일" 서랍이 이미 채워져 있고 새 텍스트 도착 시 서랍을 뒤지는 구조를 한 장에 담을 때 유효. 위쪽 `.ec-cab-shelf`(저장된 서랍), 아래쪽 `.ec-cab-lookup`(신규 조회 결과) 2층 구조.

**사용 챕터**: CH07

**HTML 사용 예**:
```html
<div class="ec-cabinet">
  <div class="ec-cab-head">
    <span class="ec-cab-kind">EmbeddingCache</span>
    <span class="ec-cab-sub">outputs/embedding_cache/</span>
  </div>
  <div class="ec-cab-shelf">
    <div class="ec-cab-file ec-exists">
      <div class="ec-file-text">"연차 규정"</div>
      <div class="ec-file-arrow">→</div>
      <div class="ec-file-name">a1f3c7.pkl</div>
    </div>
    <div class="ec-cab-file ec-exists">
      <div class="ec-file-text">"휴가 절차"</div>
      <div class="ec-file-arrow">→</div>
      <div class="ec-file-name">d9e2b5.pkl</div>
    </div>
  </div>
  <div class="ec-cab-lookup">
    <div class="ec-lookup-title">새 텍스트가 들어오면</div>
    <div class="ec-lookup-rows">
      <div class="ec-lookup-row ec-hit-row">
        <div class="ec-lookup-text">"연차 규정"</div>
        <div class="ec-lookup-tag">HIT</div>
        <div class="ec-lookup-action">파일 존재 → <code>pickle.load</code> → 벡터 반환 <span class="ec-latency">즉시</span></div>
      </div>
      <div class="ec-lookup-row ec-miss-row">
        <div class="ec-lookup-text">"근태 관리"</div>
        <div class="ec-lookup-tag">MISS</div>
        <div class="ec-lookup-action">파일 없음 → 임베딩 계산 → <b>새 파일 저장</b> <span class="ec-latency">약 0.5초</span></div>
      </div>
    </div>
  </div>
  <div class="cf-caption">그림 7-5. EmbeddingCache는 <b>텍스트별 전용 서랍</b>. 서랍이 있으면 파일을 그대로 꺼내고, 없으면 계산 후 서랍 하나를 추가합니다</div>
</div>
```

**렌더 CSS**: `styles/diagrams.css:1076-1204` (`.ec-cabinet`, `.ec-cab-head`, `.ec-cab-kind`, `.ec-cab-sub`, `.ec-cab-shelf`, `.ec-cab-file`, `.ec-file-text`, `.ec-file-arrow`, `.ec-file-name`, `.ec-cab-lookup`, `.ec-lookup-title`, `.ec-lookup-rows`, `.ec-lookup-row`, `.ec-hit-row`, `.ec-miss-row`, `.ec-lookup-text`, `.ec-lookup-tag`, `.ec-lookup-action`, `.ec-latency`)

**변형**: `.ec-cab-shelf` 안 `.ec-cab-file`은 2~3개 권장. `.ec-cab-lookup` 안 `.ec-lookup-row`는 HIT/MISS 한 쌍이 기본. `.ec-lookup-row`는 `.ec-hit-row` 또는 `.ec-miss-row` modifier로 색이 갈리고, 이에 맞춰 `.ec-lookup-tag` / `.ec-latency` 색도 자동 분기.

**피해야 할 것**
- `.rc-*` 네임스페이스에 끌려가 `.ec-tl-*` 같이 변형 짓지 말 것. 캐시 시간축이 필요하면 `.rc-timeline`을 따로 사용
- `.ec-cab-shelf`에 5개 이상 파일 나열 금지 → 서가 비유 강조점이 흐려짐. 대표 2~3개로 압축
- HIT 행만 또는 MISS 행만 단독 배치 금지 → "둘이 갈린다"가 핵심. 한 쌍을 이뤄 대비
- 캡션은 `.cf-caption`(공용)을 사용. 별도 `.ec-caption` 만들지 말 것

### .wrapper-arch

**언제 쓰는가**: 기존 코어를 건드리지 않고 바깥에 운영 기능을 두른 **계층 래핑 구조**를 보여줄 때. CH07처럼 "챕터 6의 IntegratedAgent는 그대로 두고, 바깥을 캐시·추적·재시도로 감쌌다"는 메시지를 한 장에 담는다. `.wa-outer`(이번 챕터 래퍼) → `.wa-middle`(추가 기능 카드 3개) → `.wa-inner`(이전 챕터 코어) 3층 중첩.

**사용 챕터**: CH07

**HTML 사용 예**:
```html
<div class="wrapper-arch">
  <div class="wa-title">ConnectHRAgent — 운영용 래퍼 구조</div>
  <div class="wa-outer">
    <div class="wa-outer-label">
      <span class="wa-tag">이번 챕터</span>
      ConnectHRAgent (운영 래퍼)
    </div>
    <div class="wa-middle">
      <div class="wa-feature wa-cache">
        <div class="wa-feature-title">ResponseCache</div>
        <div class="wa-feature-sub">TTL 메모장</div>
      </div>
      <div class="wa-feature wa-monitor">
        <div class="wa-feature-title">TokenTracker</div>
        <div class="wa-feature-sub">업무 일지</div>
      </div>
      <div class="wa-feature wa-retry">
        <div class="wa-feature-title">Retry 루프</div>
        <div class="wa-feature-sub">3회 재시도</div>
      </div>
    </div>
    <div class="wa-inner">
      <div class="wa-inner-label">
        <span class="wa-tag wa-tag-inner">챕터 6 그대로</span>
        IntegratedAgent
      </div>
      <div class="wa-inner-core">
        <div class="wa-core-item">QueryRouter</div>
        <div class="wa-core-sep">→</div>
        <div class="wa-core-item">AgentExecutor<br><span class="wa-core-hint">(ReAct)</span></div>
        <div class="wa-core-sep">→</div>
        <div class="wa-core-item">MCP Tools</div>
      </div>
    </div>
  </div>
  <div class="wa-caption">그림 7-6. 챕터 6의 에이전트는 그대로 두고, 바깥을 <b>운영 래퍼 3종</b>(캐시·추적·재시도)으로 감쌉니다</div>
</div>
```

**렌더 CSS**: `styles/diagrams.css:734-845` (`.wrapper-arch`, `.wa-title`, `.wa-outer`, `.wa-outer-label`, `.wa-inner-label`, `.wa-tag`, `.wa-tag-inner`, `.wa-middle`, `.wa-feature`, `.wa-feature-title`, `.wa-feature-sub`, `.wa-cache`, `.wa-monitor`, `.wa-retry`, `.wa-inner`, `.wa-inner-core`, `.wa-core-item`, `.wa-core-hint`, `.wa-core-sep`, `.wa-caption`)

**변형**: `.wa-middle` 안 `.wa-feature`는 3개가 그리드(`grid-template-columns: 1fr 1fr 1fr`) 전제. modifier는 `.wa-cache`(녹색) / `.wa-monitor`(노랑) / `.wa-retry`(빨강). `.wa-inner-core`의 `.wa-core-item`은 좌→우 흐름을 `.wa-core-sep`(`→`)로 연결. `.wa-tag` vs `.wa-tag-inner`로 "신규 vs 기존" 라벨 색이 갈린다.

**피해야 할 것**
- 래퍼가 1층뿐이면 의미 없음. `.wa-outer` 안에 반드시 `.wa-inner`(이전 코어)가 들어가야 "감싼 구조"가 성립
- `.wa-feature` 4개 이상: 그리드가 깨짐. 3개 이상 보여주려면 `.wa-middle`을 두 줄로 분할하거나 `.cache-compare` 같은 다른 컴포넌트 검토
- `.wa-cache` / `.wa-monitor` / `.wa-retry` 외 임의 modifier 추가: 색·의미 매핑 일관성 깨짐. 추가 색이 필요하면 CSS에 정식 modifier로 등록
- 시간 흐름 표현(MISS → HIT)에 사용 금지 → `.rc-timeline` 사용. `.wrapper-arch`는 정적 구조 전용

### .journey-forward

**언제 쓰는가**: 책 전체 또는 챕터군의 여정을 **좌→우 진행**으로 그룹별 펼쳐 보여줄 때. 챕터 1 마무리에서 "PART 1~4까지 이런 순서로 간다"를 안내하는 자리에 사용. 그룹(`.jf-group`)은 PART 단위, 항목(`.jf-item`)은 챕터 단위. 각 항목은 `.jf-ch`(챕터 번호) + `.jf-desc` 안 `.jf-title`(챕터 제목) + `.jf-hint`(부제) 조합.

**사용 챕터**: CH01

**HTML 사용 예**:
```html
<div class="journey-forward">
  <h2>본격 여정은 여기서부터</h2>
  <p class="jf-sub">챕터 1에서 맛본 RAG 원리를 기반으로, 챕터 2부터 <b>커넥트HR 에이전트</b>를 한 단계씩 쌓아갑니다.</p>

  <div class="jf-group">
    <div class="jf-group-label">PART 1 · 사내 시스템 만들기</div>
    <p class="jf-part-desc">AI 비서가 조회할 데이터를 먼저 마련합니다. FastAPI로 직원, 연차, 매출 CRUD API를 만들고, 어떤 문서를 어떻게 정리해서 넣을지 설계합니다.</p>
    <div class="jf-items">
      <div class="jf-item">
        <div class="jf-ch">챕터 2</div>
        <div class="jf-desc"><span class="jf-title">사내 시스템 API</span><span class="jf-hint">FastAPI · PostgreSQL · 직원·연차·매출 CRUD</span></div>
      </div>
      <div class="jf-item">
        <div class="jf-ch">챕터 3</div>
        <div class="jf-desc"><span class="jf-title">문서 설계와 메타데이터</span><span class="jf-hint">어떤 문서를 어떤 형식으로 넣을지, 재인덱싱 전략까지</span></div>
      </div>
    </div>
  </div>

  <div class="jf-group">
    <div class="jf-group-label">PART 2 · RAG 엔진 만들기</div>
    <p class="jf-part-desc">챕터 1의 맛보기를 실전 수준으로 끌어올립니다.</p>
    <div class="jf-items">
      <div class="jf-item">
        <div class="jf-ch">챕터 4</div>
        <div class="jf-desc"><span class="jf-title">벡터 DB 구축</span><span class="jf-hint">PDF·DOCX 파싱, 한국어 임베딩, ChromaDB 영구 저장</span></div>
      </div>
    </div>
  </div>
</div>
```

**렌더 CSS**: `styles/components.css:131-178` (`.journey-forward`, `.journey-forward h2`, `.journey-forward .jf-sub`, `.jf-group`, `.jf-group-label`, `.jf-items`, `.jf-item`, `.jf-item .jf-ch`, `.jf-item .jf-desc`, `.jf-title`, `.jf-hint`, `.jf-part-desc`)

**변형**: `.journey-forward` 내부는 H2 + `.jf-sub` 도입부 + `.jf-group` 반복 구조. 각 그룹은 `.jf-group-label`(PART 라벨) + `.jf-part-desc`(파트 한 줄 설명) + `.jf-items` 안 `.jf-item` 2~3개. `.jf-item`은 60px(`.jf-ch`) + 1fr(`.jf-desc`) 그리드. `.jf-hint`는 부제로 같은 줄에 `margin-left: 6px`로 붙는다.

**피해야 할 것**
- `.journey-forward` 외부에 `.jf-*`만 단독 사용 금지 → 배경·여백 토큰이 적용되지 않아 시각이 무너짐
- `.jf-item`을 3개 이상 한 그룹에 넣지 말 것 → 한 PART는 2챕터 단위가 시각 균형에 맞음. 3챕터 이상이면 그룹을 나누기
- `.jf-title`과 `.jf-hint`를 별도 줄로 끊으면 디자인이 어긋남 → 같은 `<span>` 형제로 한 줄 유지
- 챕터 번호(`.jf-ch`)에 "Chapter 02" 같이 길게 쓰지 말 것 → 60px 그리드 칼럼 깨짐. "챕터 N" 짧게
- **노드형 진행이 필요하면** `.journey-forward` 대신 `.journey-roadmap` 사용

### .journey-roadmap

**언제 쓰는가**: 책 전체 여정을 **노드 + 점선 라인**으로 한 장에 압축할 때. `.journey-forward`가 그룹 단위 좌→우 펼침이라면, `.journey-roadmap`은 노드 한 줄로 PART 경계와 챕터 진행을 동시에 보여준다. 각 노드는 `.node-dot`(번호 동그라미) + `.node-icon`(이모지/심볼) + `.node-title` + `.node-story`(한 줄 비유) 조합. PART 경계는 `.roadmap-part[data-part="PART N"]`의 `::before` 라벨로 자동 표시.

**사용 챕터**: CH01

**HTML 사용 예**:
```html
<div class="journey-roadmap">
  <div class="roadmap-line"></div>

  <div class="roadmap-part" data-part="PART 1">
    <div class="roadmap-node">
      <div class="node-dot">2</div>
      <div class="node-icon">🗄️</div>
      <div class="node-title">대시보드</div>
      <div class="node-story">"데이터가 여기 들어온다"</div>
    </div>
    <div class="roadmap-node">
      <div class="node-dot">3</div>
      <div class="node-icon">📄</div>
      <div class="node-title">문서 설계</div>
      <div class="node-story">"어떤 문서를 넣을까"</div>
    </div>
  </div>

  <div class="roadmap-part" data-part="PART 2">
    <div class="roadmap-node">
      <div class="node-dot">4</div>
      <div class="node-icon">🧲</div>
      <div class="node-title">벡터 DB</div>
      <div class="node-story">"진짜 문서를 담는다"</div>
    </div>
    <div class="roadmap-node">
      <div class="node-dot">5</div>
      <div class="node-icon">💬</div>
      <div class="node-title">RAG 엔진</div>
      <div class="node-story">"출처까지 달아 답한다"</div>
    </div>
  </div>

  <div class="roadmap-part" data-part="PART 3">
    <div class="roadmap-node finish">
      <div class="node-dot">7</div>
      <div class="node-icon">🚀</div>
      <div class="node-title">운영 안정화</div>
      <div class="node-story">"실서비스에 올린다"</div>
    </div>
  </div>
</div>
```

**렌더 CSS**: `styles/components.css:180-261` (`.journey-roadmap`, `.roadmap-line`, `.roadmap-part`, `.roadmap-part::before`, `.roadmap-node`, `.roadmap-node.finish`, `.node-dot`, `.node-icon`, `.node-title`, `.node-story`)

**변형**: `.roadmap-line`은 `.journey-roadmap` 첫 자식으로 1개만(점선 가로축). `.roadmap-part`는 PART 단위 그룹이고 `data-part` 속성으로 라벨이 자동 표시(`::before`). `.roadmap-node.finish` modifier는 마지막 노드 점을 녹색으로 강조. `.node-icon`은 이모지 권장(필터 `grayscale(0.2)`로 톤 다운).

**피해야 할 것**
- `.roadmap-line` 누락: 노드만 떠 있고 흐름선이 사라짐 → 항상 첫 자식으로 1회 삽입
- `data-part` 속성 누락: PART 라벨이 비어 보임. `data-part="PART 1"` 형식 필수
- `.node-title`을 두 줄(긴 문장)로 작성 금지 → `white-space: nowrap`이 적용되어 잘림. 4~6자 권장
- `.node-story`에 코드/긴 문장 넣지 말 것 → 큰따옴표로 감싼 8~12자 비유 한 줄이 디자인 의도
- **그룹 단위 펼침 설명**이 필요하면 `.journey-roadmap` 대신 `.journey-forward` 사용. 두 컴포넌트는 한 페이지에 동시 등장할 수 있으나 의미가 다르므로 역할을 섞지 말 것
- `rc-*` 네임스페이스(CH03/CH07)와는 무관하지만, `.node-*` 클래스를 다른 컴포넌트가 재사용하지 못하게 항상 `.journey-roadmap` 자식 컨텍스트 안에서만 사용

---

### .qr-flow

**언제 쓰는가**: **"단계별 분기 + 공통 결과 풀" 플로우차트**. 여러 단계(stage)가 순서대로 흐르고, 각 단계에서 "조건 충족 시 결과 반환(실선 ↑)" / "미충족 시 다음 단계로 fall-through(점선 ⇢)"가 동시에 존재할 때. 출력 후보가 단계마다 공통이면 위쪽 `.qr-pool` 박스에 묶고, 각 단계 성공 경로는 `.qr-up` 수직 stem + 라벨로 박스 전체를 가리킨다. CH06 `QueryRouter` 3단계(키워드→컬럼→LLM) 분류기처럼 **단순→정교 단계 fall-through 구조**에 쓴다.

**사용 챕터**: CH06

**HTML 사용 예** (`projects/사내AI비서_v2/chapters/06-연차도-규정도-한번에.md` CH06 §6.4):

```html
<div class="qr-flow">
  <div class="qr-pool">
    <span class="qr-pool-label">route 반환</span>
    <span class="qr-out">structured</span>
    <span class="qr-out">unstructured</span>
    <span class="qr-out">hybrid</span>
  </div>

  <div class="qr-up qr-up-1">
    <span class="qr-up-stem"></span>
    <span class="qr-up-label">명확</span>
    <span class="qr-up-stem"></span>
  </div>
  <div class="qr-up qr-up-2">
    <span class="qr-up-stem"></span>
    <span class="qr-up-label">있음</span>
    <span class="qr-up-stem"></span>
  </div>

  <div class="qr-node qr-input qr-input-col">질문 입력</div>
  <div class="qr-arrow-h qr-arrow-1"><span>→</span></div>
  <div class="qr-node qr-stage-1">
    <span class="qr-stage-num">STAGE 1</span>키워드 매칭
  </div>
  <div class="qr-arrow-h dashed qr-arrow-2">
    <span>⇢</span><span class="qr-arrow-lbl">불명확</span>
  </div>
  <div class="qr-node qr-stage-2">
    <span class="qr-stage-num">STAGE 2</span>컬럼명 매칭
  </div>
  <div class="qr-arrow-h dashed qr-arrow-3">
    <span>⇢</span><span class="qr-arrow-lbl">없음</span>
  </div>
  <div class="qr-node qr-stage-3">
    <span class="qr-stage-num">STAGE 3</span>LLM 판단
  </div>
  <div class="qr-arrow-h qr-arrow-4"><span>→</span></div>
  <div class="qr-node qr-final qr-final-col">최종 결정</div>
</div>
```

**렌더 CSS**: `styles/diagrams.css` — 9컬럼 × 3행 CSS Grid. Row1 = `.qr-pool`(3~7열 span), Row2 = `.qr-up`(3, 5열), Row3 = stages 가로 흐름. 색상은 `--color-success`(pool), `--color-info`(입력), `--color-accent`(최종), `--color-border-strong`(stage).

**변형**:
- `.qr-node` 기본 변형: `.qr-input`(info 블루), `.qr-final`(accent 인디고, 대시 테두리)
- `.qr-arrow-h` modifier: `.dashed`(점선 + 뮤티드 컬러, fall-through 전용)
- `.qr-up-N` / `.qr-stage-N` / `.qr-arrow-N`의 `N`은 CSS에 명시적으로 grid-column 지정돼 있음. 단계 수가 달라지면 CSS 확장 필요 (현재 3단계 고정)
- 출력 풀(`.qr-pool`) 내부 `.qr-out` 칩 개수는 3개 기준. 더 많으면 `grid-column` span 조정

**피해야 할 것**
- 단계 수가 3개와 다르면 `qr-up-N` / `qr-stage-N` 수동 확장 필요. 4단계 이상은 **새 컴포넌트로 분기**를 고려. 기본 그리드 9열 구조는 "질문→3단계→최종"에 특화
- `.qr-up` stem 상·하 양쪽에 두는 게 필수. stem 하나만 두면 연결선이 중간에 끊겨 보임
- `.qr-up-label`에 긴 문장 금지. "명확"/"있음" 같은 2~4자 조건 라벨만. 더 길면 라벨이 넓어져 outputs pool 컬럼을 초과
- `.qr-pool`을 비교(A vs B)에 사용 금지. 결과 **풀**(pool)을 표현하는 단일 목적지이며, 2분할이 필요하면 `../comparisons/`의 `.annotated-compare`나 `.reindex-compare`를 쓴다
- 단계 내부에서 "여러 output 중 하나만 반환되는 경우"(예: CH06 STAGE 2 있음 → structured 단일)를 강조해야 하면 `.qr-pool` 옆에 별도 `.qr-out` 단일 칩을 배치하거나 본문으로 보충 설명. 단계마다 output 차이를 시각화하려면 수직 자기완결 레이아웃이 더 적합

### .eng-pipe

**언제 쓰는가**: **6개 단계의 파이프라인**을 입력·챔버·출력 블루프린트 스타일로 표현할 때. CH11 §11.2 "커넥트HR 엔진"처럼 RAG 파이프라인 6 스테이지(파싱·청킹·쿼리 확장·검색·리랭킹·부모/LLM)를 한 그림에 담음. 좌측 입력(accent-warm 아웃라인) · 중앙 2×3 챔버 그리드 · 우측 출력(success 아웃라인) 3-zone 구조.

**사용 챕터**: CH11

**HTML 사용 예**:
```html
<div class="eng-pipe">
  <div class="ep-head">
    <span class="ep-tag">pipeline</span>
    <span class="ep-name">커넥트HR 엔진</span>
    <span class="ep-tag">6 stages</span>
  </div>

  <div class="ep-body">
    <div class="ep-port in">
      <div class="ep-port-lbl">INPUT</div>
      <div class="ep-port-rule"></div>
      <div class="ep-port-name">질문</div>
      <div class="ep-port-arrow">▶</div>
    </div>

    <div class="ep-chambers">
      <div class="ep-stages">
        <div class="ep-stage"><span class="ep-stage-num">01</span><span class="ep-stage-name">파싱</span><div class="ep-stage-fn">parse_pdf_hybrid</div></div>
        <div class="ep-stage"><span class="ep-stage-num">02</span><span class="ep-stage-name">청킹</span><div class="ep-stage-fn">semantic_chunking</div></div>
        <div class="ep-stage"><span class="ep-stage-num">03</span><span class="ep-stage-name">쿼리 확장</span><div class="ep-stage-fn">QueryExpander</div></div>
        <div class="ep-stage"><span class="ep-stage-num">04</span><span class="ep-stage-name">검색</span><div class="ep-stage-fn">EnsembleRetriever</div></div>
        <div class="ep-stage"><span class="ep-stage-num">05</span><span class="ep-stage-name">리랭킹</span><div class="ep-stage-fn">CrossEncoderReranker</div></div>
        <div class="ep-stage"><span class="ep-stage-num">06</span><span class="ep-stage-name">부모·LLM</span><div class="ep-stage-fn">ParentDoc + Agent</div></div>
      </div>
    </div>

    <div class="ep-port out">
      <div class="ep-port-lbl">OUTPUT</div>
      <div class="ep-port-rule"></div>
      <div class="ep-port-name">답변</div>
      <div class="ep-port-arrow">▶</div>
    </div>
  </div>

  <div class="ep-caption">그림 11-10. 질문이 들어와 6단계 파이프라인을 지나 답변이 나가기까지</div>
</div>
```

**렌더 CSS**: `styles/diagrams.css` 의 `/* Engine Pipeline (CH11 §11.2) */` 블록 (`.eng-pipe`, `.ep-head`, `.ep-tag`, `.ep-name`, `.ep-body`, `.ep-port`, `.ep-port.in/.out`, `.ep-port-lbl/-rule/-name/-arrow`, `.ep-chambers`, `.ep-stages`, `.ep-stage`, `.ep-stage-num/-name/-fn`, `.ep-caption`)

**변형**: 스테이지 개수는 6개 기준(2×3 그리드). 5 이하면 `.ep-stages`의 grid-template-columns를 1fr·반복 개수로 조정. 7 이상은 세로가 길어져 `.rag-pipeline-box`를 쓰거나 새 컴포넌트로 분리. 포트 색:
- `.ep-port.in` — `--color-accent-warm` 아웃라인 (INPUT, 질문)
- `.ep-port.out` — `--color-success` 아웃라인 (OUTPUT, 답변)
스테이지 번호 색은 `--color-accent` 인디고 고정.

**피해야 할 것**
- 스테이지 4개 이하: 6칸 그리드가 비게 되어 공백이 크다. 3~5단계는 `.rag-pipeline-box`(가로 flex) 사용
- `.ep-port`를 3개 이상 두기 금지: INPUT · OUTPUT 두 쌍이 기본 구조. 제3의 포트가 필요하면 별도 컴포넌트
- `.ep-stage-fn`에 2줄 이상 텍스트: 셀 높이가 부풀어 그리드 균형이 깨짐. 함수명 한 줄로
- 입력·출력 포트를 같은 색으로 쓰기: 입력·출력 구분이 색으로 되어 있으므로 `.in`·`.out` modifier로 반드시 구분

### .evolve-flow

**언제 쓰는가**: 책 전체 챕터(또는 챕터군) 흐름을 **좌→우 카드 + 화살표** 한 줄로 압축할 때. 챕터 1의 학습 로드맵에서 "한 단계씩 다음 챕터로 진화"하는 흐름을 보여주는 자리에 사용. `.journey-forward`가 PART 단위 그룹 펼침이고 `.journey-roadmap`이 노드+점선이라면, `.evolve-flow`는 **카드 5개 좌→우 균등 배치**로 단계 간 진화 의미를 강조.

**사용 챕터**: CH01 (도커·쿠버네티스 책)

**HTML 사용 예**:
```html
<div class="evolve-flow">
  <div class="ev-card">
    <div class="ev-step">1</div>
    <div class="ev-meta">CH02 · Docker</div>
    <div class="ev-name">이해하기</div>
    <div class="ev-add">컨테이너를 띄운다</div>
  </div>
  <div class="ev-arrow">→</div>
  <div class="ev-card">
    <div class="ev-step">2</div>
    <div class="ev-meta">CH03 · Docker</div>
    <div class="ev-name">다루기</div>
    <div class="ev-add">여러 개를 한 번에 묶는다</div>
  </div>
  <!-- ... 단계 5까지 동일 패턴 -->
</div>
```

**렌더 CSS**: `styles/components.css`의 `/* evolve-flow */` 블록 (`.evolve-flow`, `.ev-card`, `.ev-step`, `.ev-meta`, `.ev-name`, `.ev-add`, `.ev-arrow`, `.ev-caption`)

**변형**: `.evolve-flow`는 5개 카드 + 4개 화살표 = 9칸 그리드(`1fr 24px 1fr 24px 1fr 24px 1fr 24px 1fr`) 고정. 단계 수가 다르면 `grid-template-columns`만 비율 조정. 카드 내부 4요소(`.ev-step`·`.ev-meta`·`.ev-name`·`.ev-add`)는 모두 필수 — 빠지면 카드 균형이 무너짐.

**피해야 할 것**
- 카드 6개 이상: 카드 폭이 너무 좁아져 텍스트 잘림. 6단계 이상은 `.journey-forward` 또는 `.journey-roadmap`으로
- 카드 1~2개: 카드가 너무 넓게 퍼져 진화 의미가 사라짐. 3단계 이상에서 사용
- 마지막 카드만 강조색으로 칠하기: 전체가 한 흐름이라 마지막만 다르면 시각이 깨진다. 모든 카드 같은 스타일
- `.ev-arrow`에 `→` 외 다른 기호: `▶`·`>` 등은 시각 무게가 달라 카드와 어긋난다. 항상 `→`
- `.ev-meta`에 챕터 번호만(예: "CH02") 적기: 기술 컨텍스트(`Docker`·`Kubernetes`)가 빠지면 PART 구분이 사라진다. `CH02 · Docker` 형식 유지

---

### `.state-lifecycle`

**언제 쓰는가**: 도메인 객체의 상태 전이(예: 배달 PENDING → COMPLETED)를 좌→우 흐름으로. 각 상태 박스 사이의 화살표 위에 트리거(자동 전이 / API 호출 / 외부 이벤트)를 라벨로 표시. 2~5단계 전이에 적합.

**사용 챕터**: MSA 책 CH05 §5.3 (그림 5-2 챕터 4 흐름, 그림 5-3 챕터 5 흐름)

**HTML 사용 예**:

```html
<div class="state-lifecycle">
  <div class="sl-title">챕터 5의 배달 흐름</div>
  <div class="sl-flow">
    <div class="sl-state">
      <div class="sl-tag">생성</div>
      <div class="sl-desc">배달 생성 요청</div>
    </div>
    <div class="sl-arrow">
      <span class="sl-arrow-line">→</span>
      <span class="sl-arrow-lbl">자동 전이</span>
    </div>
    <div class="sl-state">
      <div class="sl-tag">PENDING</div>
      <div class="sl-desc">배달 대기 상태</div>
    </div>
    <div class="sl-arrow">
      <span class="sl-arrow-line">→</span>
      <span class="sl-arrow-lbl">배달 기사<br>완료 API 호출</span>
    </div>
    <div class="sl-state sl-final">
      <div class="sl-tag">COMPLETED</div>
      <div class="sl-desc">배달 완료</div>
    </div>
  </div>
</div>
```

**렌더 CSS**: `styles/diagrams.css` MSA 블록 (`.state-lifecycle`, `.sl-title`, `.sl-flow`, `.sl-state`, `.sl-state.sl-final`, `.sl-tag`, `.sl-desc`, `.sl-arrow`, `.sl-arrow-line`, `.sl-arrow-lbl`)

**변형**: `.sl-state.sl-final` modifier로 종료 상태를 인디고 채움 + 흰 글씨 태그로 강조. 화살표 라벨은 두 줄까지 가능(`<br>`로 끊기).

**피해야 할 것**
- 6단계 이상 전이: 가로 폭이 모자라 줄바꿈 발생. 5단계 이하 권장. 더 많은 단계는 `.evolve-flow`나 `.rag-pipeline-box`로
- 양방향 화살표: 상태 전이는 단방향(시간순)이 원칙. 되돌리는 흐름이 있으면 별도 도식
- `.sl-final`을 중간 상태에 적용 금지: 종료 상태(최종 도달) 전용

---

### `.saga-flow`

**언제 쓰는가**: 분산 트랜잭션의 Saga 패턴 두 가지(Choreography 직선형 / Orchestration 허브-스포크)를 한 컴포넌트로 표현. Choreography는 서비스 박스 가로 일렬 + 박스 사이 양방향 화살표(순행/보상). Orchestration은 가운데 hub(`.sf-hub`)에 명령/이벤트가 모이는 구조.

**사용 챕터**: MSA 책 CH01 §1.4.3, CH04 §4.3

**HTML 사용 예** (Choreography):

```html
<div class="saga-flow">
  <div class="sf-title">Choreography Saga — 서비스 간 직접 호출과 보상</div>
  <div class="sf-row">
    <div class="sf-node"><div class="sf-tag">Order</div><div class="sf-desc">주문 생성</div></div>
    <div class="sf-arrow">
      <span class="sf-fwd">→ 재고 감소</span>
      <span class="sf-bwd">← 재고 복구 (보상)</span>
    </div>
    <div class="sf-node"><div class="sf-tag">Product</div><div class="sf-desc">재고 차감</div></div>
    <div class="sf-arrow">
      <span class="sf-fwd">→ 배달 생성</span>
      <span class="sf-bwd">← 배달 취소 (보상)</span>
    </div>
    <div class="sf-node"><div class="sf-tag">Delivery</div><div class="sf-desc">배달 생성</div></div>
  </div>
  <div class="sf-note">중앙 조율자 없이 서비스끼리 직접 호출. 실패 시 이전 서비스에 직접 보상 요청.</div>
</div>
```

Orchestration 변형은 `.sf-stack`(세로) + `.sf-node.sf-hub`(가운데 오렌지) + `.sf-arrow.sf-arrow-line`(↕ + command/event 라벨)으로.

**렌더 CSS**: `styles/diagrams.css` MSA 블록 (`.saga-flow`, `.sf-title`, `.sf-row`, `.sf-stack`, `.sf-node`, `.sf-node.sf-hub`, `.sf-tag`, `.sf-desc`, `.sf-arrow`, `.sf-fwd`, `.sf-bwd`, `.sf-arrow-line`, `.sf-arrow-lbl`, `.sf-note`)

**변형**: `.sf-fwd`(인디고)는 순행 호출, `.sf-bwd`(오렌지 warm)는 보상 흐름. 색만 봐도 진행 vs 롤백이 구분된다. `.sf-hub`는 Orchestration 패턴 전용 — Choreography에서는 hub 없음.

**피해야 할 것**
- Choreography에서 hub 사용 금지: hub 없음이 Choreography의 정의
- Orchestration에서 양방향 화살표(`.sf-fwd`/`.sf-bwd`) 직접 사용 금지: Orchestration은 hub-spoke이므로 `↕`(command/event) 하나로 표현
- 4개 이상 서비스 가로 나열: 가로 폭 부족. 3~4개 이하 권장

---

### `.seq-diagram`

**언제 쓰는가**: 다수 actor 사이의 시간순 메시지 교환을 표 형식으로. UML 시퀀스 다이어그램의 단순화 버전(생명선·활성 박스 없이 번호 + From→To + 메시지). 주문 성공 / 실패 / 단계별 처리 흐름 등 시간 흐름이 핵심일 때.

**사용 챕터**: MSA 책 CH02 §2.6 (그림 2-1, 2-2), CH04 §4.3 (그림 4-5, 4-6), §4.6 (그림 4-7, 4-8, 4-9)

**HTML 사용 예**:

```html
<div class="seq-diagram">
  <div class="sd-title">주문 성공 흐름 — Orchestration Saga</div>
  <div class="sd-lifelines">
    <div class="sd-actor"><div class="sd-tag">Order</div></div>
    <div class="sd-actor sd-hub"><div class="sd-tag">Orchestrator</div></div>
    <div class="sd-actor"><div class="sd-tag">Product</div></div>
    <div class="sd-actor"><div class="sd-tag">Delivery</div></div>
  </div>
  <div class="sd-steps">
    <div class="sd-step">
      <div class="sd-num">1</div>
      <div class="sd-from-to">Order → Orch.</div>
      <div class="sd-msg">order-created 발행</div>
    </div>
    <div class="sd-step sd-fail">
      <div class="sd-num">2</div>
      <div class="sd-from-to">Delivery → Orch.</div>
      <div class="sd-msg">delivery-created {success: false}</div>
    </div>
  </div>
</div>
```

**렌더 CSS**: `styles/diagrams.css` MSA 블록 (`.seq-diagram`, `.sd-title`, `.sd-lifelines`, `.sd-actor`, `.sd-actor.sd-hub`, `.sd-tag`, `.sd-steps`, `.sd-step`, `.sd-step.sd-fail`, `.sd-num`, `.sd-from-to`, `.sd-msg`)

**변형**:
- `.sd-actor.sd-hub` — 중심 조율자(Orchestrator) actor를 오렌지 태그로 강조
- `.sd-step.sd-fail` — 실패·롤백 단계를 warm 배경 + 번호도 오렌지로
- `.sd-num`에 `2a`·`2b` 형식 허용 (분기 표시)

**피해야 할 것**
- actor 5명 초과: 가로 폭이 줄어 lifeline 라벨 잘림. 4명 이하 권장
- 단계 10개 초과: 한 시퀀스가 너무 길면 절을 나눠 별도 도식으로
- 단계 번호 없이 메시지만 나열: 시간 순서가 핵심이므로 번호 필수

---

### `.kafka-topic-flow`

**언제 쓰는가**: Kafka 메시지 큐 개념(Producer → Topic → Consumer)을 한 줄로. 토픽 내부에 메시지 셀(`.ktf-msg`)이 일렬로 쌓여 있는 모습을 보여줘 "큐"임을 시각적으로 전달. 컨슈머 그룹 변형은 `.ktf-group` + `.ktf-instance`(active / skip)로 라우팅 패턴을 보여준다.

**사용 챕터**: MSA 책 CH04 §4.2.1 (그림 4-2 메시지 큐 개념, 그림 4-3 컨슈머 그룹)

**HTML 사용 예** (기본 흐름):

```html
<div class="kafka-topic-flow">
  <div class="ktf-title">메시지 큐 개념 — Producer · Topic · Consumer</div>
  <div class="ktf-row">
    <div class="ktf-node"><div class="ktf-tag">Producer</div><div class="ktf-desc">order-service</div></div>
    <div class="ktf-arrow">→</div>
    <div class="ktf-topic">
      <div class="ktf-tag">Topic</div>
      <div class="ktf-name">order-created</div>
      <div class="ktf-msgs">
        <span class="ktf-msg">msg1</span>
        <span class="ktf-msg">msg2</span>
        <span class="ktf-msg">…</span>
      </div>
    </div>
    <div class="ktf-arrow">→</div>
    <div class="ktf-node"><div class="ktf-tag">Consumer</div><div class="ktf-desc">orchestrator</div></div>
  </div>
</div>
```

컨슈머 그룹 변형은 `.ktf-node` 자리에 `.ktf-group`(점선 박스 + `.ktf-group-lbl` 그룹 이름 + `.ktf-group-row` 안에 `.ktf-instance.ktf-active`/`.ktf-skip`).

**렌더 CSS**: `styles/diagrams.css` MSA 블록 (`.kafka-topic-flow`, `.ktf-title`, `.ktf-row`, `.ktf-node`, `.ktf-topic`, `.ktf-tag`, `.ktf-name`, `.ktf-desc`, `.ktf-msgs`, `.ktf-msg`, `.ktf-arrow`, `.ktf-group`, `.ktf-group-lbl`, `.ktf-group-row`, `.ktf-instance`, `.ktf-instance.ktf-active`, `.ktf-instance.ktf-skip`)

**변형**: 토픽 박스는 오렌지(`.ktf-topic` — Kafka 색 통일). 메시지 셀(`.ktf-msg`)은 모노스페이스로 작은 칸. 컨슈머 그룹의 `.ktf-skip`은 취소선으로 "전달 안 됨"을 표현.

**피해야 할 것**
- 토픽 박스에 메시지를 8개 이상 나열: 가로 폭 초과. 3~4개 + `…`로 생략
- `.ktf-active` 없이 `.ktf-skip`만 표시: 그룹 라우팅의 핵심은 "어디로 전달되는지". active와 skip을 함께 표시해야 의미 전달
- Producer·Consumer 양쪽에 오렌지 색 적용 금지: 오렌지는 Kafka 토픽 전용. 클라이언트(서비스)는 인디고
