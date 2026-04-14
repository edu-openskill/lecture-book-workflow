# Pipelines

> 순차 흐름·타임라인·파이프라인. 단계가 있고 방향이 있는 구조를 보여준다.

## 속함

- `.rag-pipeline-box` + `.rag-*` / `.s-*` 계열 (CH01 RAG 3단계)
- `.rc-timeline` (CH07 비용·시간 타임라인) — `rc-*` 접두어를 CH03 reindex-compare와 공유하지만 별개
- `.ec-cabinet` (CH07 임베딩 캐시 캐비닛)
- `.wrapper-arch` (CH07 래퍼 아키텍처)
- `.journey-forward` + `.jf-*` (CH01 여정 맵)
- `.journey-roadmap` + `.roadmap-*`, `.node-*` (CH01 노드 기반 로드맵)

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
