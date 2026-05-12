# Fullmap

> 책 전체 구성도. 각 챕터가 시스템의 어디에 해당하는지 보여주는 최상위 시각 요소.

## 속함

- `.arch-fullmap` (컨테이너) + `.arch-fullmap-title`
- `.afm-row` / `.afm-box` / `.afm-zone` 계열 전체
- modifier: `.afm-faint`, `.afm-on`, `.afm-dashed`, `.afm-round`, `.afm-three`, `.afm-ext`, `.afm-user`
- 라벨: `.afm-tag`, `.afm-label`, `.afm-sub`, `.afm-note`, `.afm-zone-ch`, `.afm-zone-label`

## 속하지 않음

- 개별 파이프라인 도식 → [`../pipelines/`](../pipelines/)
- 청크·임베딩 카드 → [`../cards/`](../cards/)

## 컴포넌트 목록

### `.arch-fullmap` (컨테이너)

**언제 쓰는가**: 각 챕터 끝에 "## N.N 전체 구성도에서 챕터 N의 자리" H2 아래 삽입. 이번 챕터가 만든 박스는 `.afm-on`(진함)으로, 앞뒤 챕터는 `.afm-faint`(흐림)로 표시해 전체 책 진행도를 시각화.

**사용 챕터**: CH02, CH03, CH04, CH05, CH07, CH10

**HTML 스켈레톤**:

```html
<div class="arch-fullmap">
  <div class="arch-fullmap-title">전체 구성도. 짙은 박스가 챕터 N 범위</div>

  <div class="afm-row afm-user">
    <div class="afm-box afm-faint afm-round">
      <div class="afm-label">사내 직원 · 관리자</div>
    </div>
  </div>

  <div class="afm-zone">
    <span class="afm-zone-ch">챕터 N</span>
    <span class="afm-zone-label">{영역명}</span>
    <div class="afm-row">
      <div class="afm-box afm-on">
        <div class="afm-tag">오늘 만든 부분</div>
        <div class="afm-label">{기술 이름}</div>
        <div class="afm-sub">{한 줄 요약}</div>
      </div>
    </div>
  </div>

  <!-- 다른 챕터 zone은 .afm-faint -->
  <div class="afm-zone">
    <span class="afm-zone-ch">챕터 M</span>
    <span class="afm-zone-label">{영역명}</span>
    <div class="afm-row afm-three">
      <div class="afm-box afm-faint">
        <div class="afm-label">{박스1}</div>
        <div class="afm-sub">{설명}</div>
      </div>
      <div class="afm-box afm-faint">
        <div class="afm-label">{박스2}</div>
        <div class="afm-sub">{설명}</div>
      </div>
      <div class="afm-box afm-faint afm-dashed">
        <div class="afm-label">{미구현/외부 박스}</div>
        <div class="afm-sub">{설명}</div>
      </div>
    </div>
  </div>

  <div class="afm-row afm-ext">
    <div class="afm-box afm-faint afm-dashed">
      <div class="afm-label">Ollama LLM (외부)</div>
    </div>
  </div>

  <div class="afm-note">
    오늘 띄운 건 <b>{핵심 박스}</b> 입니다. 나머지는 챕터 N+1부터 하나씩 채워집니다.
  </div>
</div>
```

**렌더 CSS**: `styles/diagrams.css:227-327` (`.arch-fullmap` ~ `.afm-note b` 블록)

**변형(Variants)**: 아래 `.afm-*` 요소별 규칙 표 참조.

**피해야 할 것**
- `.afm-on`을 2개 이상: "오늘 만든 부분"은 한 챕터당 1~2 박스까지. 3개 넘어가면 "이번 챕터 범위"가 흐려진다
- zone 6개 초과: 세로로 길어져 한 페이지에 안 들어가고 가독성이 붕괴된다
- `.afm-zone-ch` 영문 표기("Chapter 6"): 책 전체에서 "챕터 N" 한글 표기로 통일
- `.afm-note` 없이 끝내기: 하단 요약 노트 없이 박스만 나열하면 독자가 "오늘 뭘 만들었지"를 다시 찾아봐야 한다
- `.afm-row.afm-user` / `.afm-row.afm-ext` 누락: 최상단(사용자) / 최하단(외부 의존)이 없으면 시스템 경계가 모호해진다

### `.afm-*` 요소별 규칙 표

| 클래스 | 레이어 | 역할 | 언제 쓰는가 |
|-------|-------|------|------------|
| `.arch-fullmap` | 컨테이너 | 최상위 래퍼 | 항상 1개 |
| `.arch-fullmap-title` | 컨테이너 | 상단 제목 한 줄 | "전체 구성도. 짙은 박스가 챕터 N 범위" 형태로 1개 |
| `.afm-row` | 레이아웃 | 가로 한 줄 묶음 | zone 안 또는 단독으로 사용 |
| `.afm-row.afm-three` | 레이아웃 | 3칸 그리드 | 한 레이어에 박스 3개가 나란히 놓일 때 (`flex: 1`) |
| `.afm-row.afm-user` | 레이아웃 | 사용자 레이어 | 맨 위에 사용자/관리자 박스를 배치할 때 (1개만) |
| `.afm-row.afm-ext` | 레이아웃 | 외부 의존 레이어 | 맨 아래 외부 LLM / 외부 API 박스 (1개만) |
| `.afm-zone` | 그룹 | 챕터 단위 묶음 | 한 챕터에 해당하는 박스들을 묶을 때 |
| `.afm-zone-ch` | 그룹 라벨 | "챕터 N" 뱃지 | `.afm-zone` 좌측 상단. 한글 "챕터 N" 고정 |
| `.afm-zone-label` | 그룹 라벨 | 영역 역할명 | "대시보드", "검색", "데이터" 등 해당 zone이 담당하는 기능 영역 |
| `.afm-box` | 박스 | 기본 박스 단위 | 기술 컴포넌트 한 덩어리 |
| `.afm-box.afm-on` | 박스 modifier | "오늘 만든 부분" 진한 스타일 | 이번 챕터에서 새로 만든 박스에만 (한 챕터당 1~2개) |
| `.afm-box.afm-faint` | 박스 modifier | 흐린 스타일 | 앞뒤 챕터의 박스. 전체 구성도에서 "아직/이미" 구역을 표시 |
| `.afm-box.afm-dashed` | 박스 modifier | 대시 테두리 | 외부 의존 / 아직 구현 전 / 이 책 범위 밖 박스 |
| `.afm-box.afm-round` | 박스 modifier | 둥근 테두리 (pill) | 사용자 레이어 박스 (`.afm-row.afm-user` 안에서 주로 사용) |
| `.afm-tag` | 박스 내부 | 상단 태그 라인 | "오늘 만든 부분", "오늘 띄운 DB" 같은 강조 태그 (주로 `.afm-on`과 함께) |
| `.afm-label` | 박스 내부 | 메인 라벨 | 기술 이름 / 박스 제목 (필수) |
| `.afm-sub` | 박스 내부 | 서브 설명 | 한 줄 요약 / 역할 설명 (선택) |
| `.afm-note` | 컨테이너 | 하단 요약 노트 | 컨테이너 맨 아래 1개. `<b>` 태그로 핵심 박스명 강조 가능 |

**modifier 조합 규칙**
- `.afm-box.afm-faint.afm-round`: 사용자 레이어에서 "아직 이 챕터 범위 아님"을 둥근 모양으로 표시
- `.afm-box.afm-faint.afm-dashed`: 외부 의존 / 미구현 박스 (예: Ollama LLM, 다음 챕터에서 만들 컴포넌트)
- `.afm-box.afm-on`에는 `.afm-faint` / `.afm-dashed` 조합 금지 (진함과 흐림이 충돌)

### `.arch11` (최종 완성 구성도)

**언제 쓰는가**: 책 **마지막 챕터의 완성 시스템 전체 구성도**를 한 장으로 선언할 때. `.arch-fullmap`이 "이 챕터가 전체에서 어디에 해당하는가"를 보여준다면, `.arch11`은 "11개 챕터 전체가 어떻게 한 시스템으로 조립됐는가"를 보여주는 **최종 조립도** 전용. 3행 2열 스택(사용자·Runtime / LLM·Tools / Vector·PG) 구조로 A4 세로 폭에 맞음. d1-tokens 에디토리얼 스타일 계승(LLM 박스 브라켓 장식 `::before/::after`, accent-bg 인디고 core, col-t 앰버/RAG 뱃지).

**사용 챕터**: CH11

**HTML 사용 예** (요약):

```html
<div class="arch11">
  <div class="header">
    <div class="sub">시스템 아키텍처 (System Architecture)</div>
    <div class="title">커넥트HR 에이전트</div>
    <div class="desc">11개 챕터에 걸쳐 완성한 RAG 시스템</div>
  </div>

  <!-- Row 1: 사용자·Gateway ┃ Runtime -->
  <div class="row-client">
    <div class="col-c">
      <div class="user">…</div>
      <div class="flow">…</div>
      <div class="api">…</div>
    </div>
    <div class="flow-arrows">…</div>
    <div class="col-a">
      <div class="title">통합 에이전트 · 운영 (Runtime)</div>
      <div class="ops">…</div>
      <div class="core">
        <div class="l">…</div><div class="n">…</div><div class="s">…</div>
        <div class="loop-inner">…</div>
        <div class="engine-inner">…</div>
      </div>
    </div>
  </div>

  <div class="lvl-lbl">↑ 프롬프트·도구 호출 · ↓ 응답·결과</div>

  <!-- Row 2: LLM ┃ Tools -->
  <div class="row-ext">
    <div class="llm"><div class="box">…</div></div>
    <div class="flow-arrows">…</div>
    <div class="col-t">…</div>
  </div>

  <div class="lvl-lbl">↑ 조회·도구 실행 · ↓ 레코드·문서</div>

  <!-- Row 3: Stores -->
  <div class="stores">
    <div class="st">ChromaDB</div>
    <div class="st">PostgreSQL</div>
  </div>

  <div class="caption">그림 11-11. 커넥트HR 에이전트의 시스템 아키텍처</div>
</div>
```

전체 샘플은 `projects/사내AI비서_v2/chapters/11-커넥트HR-에이전트의-완성.md` §11.5 참조.

**렌더 CSS**: `styles/diagrams.css` 의 `/* System Architecture (arch11, CH11 §11.5) */` 블록

**변형**: Row별 grid-template-columns 비율은 콘텐츠 양에 맞게 고정:
- `.row-client`: `180px 36px 1fr` (사용자 좁음 · 화살표 · Runtime 넓음)
- `.row-ext`: `280px 36px 1fr` (LLM 중간 · 화살표 · Tools 넓음)
- `.stores`: `1fr 1fr` (동일 저장소 2개)

Runtime `.col-a` 내부는 `.core > .loop-inner + .engine-inner` 중첩 구조(통합 에이전트가 ReAct Loop와 RAG Engine을 부품으로 포함). `.engine-inner .stages-6`은 3×2 grid(6 stages).

**피해야 할 것**
- 행·열 개수 변경 금지 (3행 2열 고정 구조). 늘리려면 별도 컴포넌트
- `.col-a .core` 내부에 `.loop-inner`·`.engine-inner` 외 다른 요소 추가 금지 (Executor 안 "부품"만)
- Row별 `.flow-arrows` 누락: Row 1·Row 2는 요청/응답 화살표가 시각 흐름의 핵심. 생략하면 3행 2열이 단순 표처럼 보임
- `.arch11`을 `.arch-fullmap`과 동일한 위치(각 챕터 끝)에 쓰기 금지: 최종 챕터 한 번만. 중간 챕터는 `.arch-fullmap`으로

---

### `.k8s-resources`

**언제 쓰는가**: Kubernetes 핵심 리소스(Pod·Deployment·Service·Ingress·ConfigMap·Secret)의 관계를 한 장에 정리할 때. 클러스터 박스 안에 리소스들이 들어가고 외부 클라이언트가 진입점으로 들어오는 구조를 보여준다. K8s 입문 챕터 도입부에 "이번 챕터에서 다룰 리소스의 전체 그림" 위치 권장.

**사용 챕터**: MSA 책 CH03 §3.6.1 (또한 도커-쿠버네티스 책 CH04 §4.1.3에서 같은 SVG 패턴)

**HTML 사용 예** (수평 흐름형, 시리즈 톤은 인라인 SVG 권장):

```html
<div class="k8s-resources">
  <div class="kr-title">Kubernetes 리소스 관계</div>
  <div class="kr-stack">
    <div class="kr-node">
      <div class="kr-tag">Ingress</div>
      <div class="kr-desc">외부 요청 라우팅</div>
    </div>
    <div class="kr-arrow">↓</div>
    <div class="kr-node">
      <div class="kr-tag">Service</div>
      <div class="kr-desc">Pod에 고정 DNS 부여</div>
    </div>
    <div class="kr-arrow">↓</div>
    <div class="kr-row">
      <div class="kr-node">
        <div class="kr-tag">Pod</div>
        <div class="kr-desc">컨테이너 실행 단위</div>
      </div>
      <div class="kr-arrow kr-h">←</div>
      <div class="kr-node">
        <div class="kr-tag">Deployment</div>
        <div class="kr-desc">Pod 생명주기 관리</div>
      </div>
    </div>
    <div class="kr-arrow"><span>↑</span><span class="kr-arrow-lbl">envFrom</span></div>
    <div class="kr-row">
      <div class="kr-node"><div class="kr-tag">ConfigMap</div><div class="kr-desc">일반 환경변수</div></div>
      <div class="kr-node"><div class="kr-tag">Secret</div><div class="kr-desc">민감 정보</div></div>
    </div>
  </div>
</div>
```

**렌더 CSS**: `styles/diagrams.css` "MSA 책 다이어그램 컴포넌트" 블록 (`.k8s-resources`, `.kr-title`, `.kr-stack`, `.kr-row`, `.kr-node`, `.kr-tag`, `.kr-desc`, `.kr-arrow`, `.kr-arrow-lbl`)

**변형**: 시리즈 톤을 더 살리려면 인라인 SVG(`.svg-figure`)로 교체 가능. 색 의미는 Pod 오렌지(`#ff7849`), Deployment 인디고(`#4f46e5`), 보조 리소스(Service/Ingress/ConfigMap/Secret) 회색을 시리즈 전반에서 통일.

**피해야 할 것**
- 클라이언트(외부 요청 발신자)를 클러스터 박스 안에 두지 말 것. 클라이언트는 항상 외부.
- ConfigMap/Secret을 본 흐름(Ingress→Service→Pod) 색과 같은 진한 색으로 칠하기 금지. 보조 리소스이므로 회색.
- 리소스 종류 5개 초과: Volume·StatefulSet·DaemonSet 등 더 넣으면 한 장에 담기 어려움. 분리된 도식으로.

---

### `.svc-arch`

**언제 쓰는가**: 4~5개 마이크로서비스의 통신 구조를 한 장에. 동기 REST(직선형) 또는 비동기 Kafka(허브-스포크) 두 토폴로지를 같은 컴포넌트로 표현 가능. 시스템 설계 도입 절에서 "이 챕터의 시스템 그림"을 한 장면으로 선언할 때 유효.

**사용 챕터**: MSA 책 CH01 §1.3 (그림 1-5 동기 REST, 그림 1-6 Kafka 비동기)

**HTML 사용 예** (동기 REST 토폴로지):

```html
<div class="svc-arch">
  <div class="sa-title">동기 REST 통신</div>
  <div class="sa-layout">
    <div class="sa-row">
      <div class="sa-node">
        <div class="sa-tag">Client</div>
        <div class="sa-desc">브라우저·앱</div>
      </div>
      <div class="sa-arrow">
        <span class="sa-arrow-line">→</span>
        <span class="sa-arrow-lbl">POST /api/orders</span>
      </div>
      <div class="sa-node sa-primary">
        <div class="sa-tag">Order</div>
        <div class="sa-desc">주문 서비스</div>
      </div>
    </div>
    <div class="sa-arrow"><span class="sa-arrow-line">↓</span><span class="sa-arrow-lbl">RestClient</span></div>
    <div class="sa-row">
      <div class="sa-node"><div class="sa-tag">Product</div><div class="sa-desc">재고 차감</div></div>
      <div class="sa-node"><div class="sa-tag">Delivery</div><div class="sa-desc">배달 생성</div></div>
    </div>
  </div>
  <div class="sa-note">주문 서비스가 상품·배달 서비스를 직접 호출. User 서비스는 JWT 발급으로 별도.</div>
</div>
```

비동기 Kafka 토폴로지는 `.sa-node.sa-hub`로 Kafka 박스(오렌지)를 가운데 두고 위아래로 Order·Orchestrator·서비스들을 배치한다.

**렌더 CSS**: `styles/diagrams.css` MSA 블록 (`.svc-arch`, `.sa-title`, `.sa-layout`, `.sa-row`, `.sa-node`, `.sa-node.sa-primary`, `.sa-node.sa-hub`, `.sa-tag`, `.sa-desc`, `.sa-arrow`, `.sa-arrow-line`, `.sa-arrow-lbl`, `.sa-note`)

**변형**: `.sa-primary`(인디고 강조)는 흐름의 중심 서비스(Order, Orchestrator)에. `.sa-hub`(오렌지)는 메시지 브로커(Kafka)에만. 화살표 라벨은 모노스페이스로 REST 메서드 또는 Kafka 토픽 이름.

**피해야 할 것**
- 6개 이상 서비스 나열: 박스가 좁아져 텍스트 잘림. 5개 이하 권장
- 화살표 라벨 누락: REST 메서드(`POST /api/orders`)나 Kafka 토픽 이름이 없으면 흐름의 의미가 사라짐
- `.sa-hub` 색을 일반 서비스에 적용 금지: 오렌지는 메시지 브로커 전용

---

### `.kafka-cluster`

**언제 쓰는가**: Kafka 브로커 클러스터의 구조 + Listener 주소 관계. CLUSTER_ID로 묶인 브로커들과 클라이언트가 접근하는 ADVERTISED_LISTENERS 주소를 한 장에. KRaft 모드 단일 브로커부터 멀티 브로커 확장 시점 설명까지.

**사용 챕터**: MSA 책 CH04 §4.7.1 (그림 4-10 클러스터 식별, 그림 4-11 Advertised Listener)

**HTML 사용 예** (단일 브로커 + Quorum Voter):

```html
<div class="kafka-cluster">
  <div class="kc-title">CLUSTER_ID로 Kafka 브로커들을 하나의 클러스터로 묶다</div>
  <div class="kc-cluster">
    <div class="kc-cluster-id">CLUSTER_ID: AbijZYk0QOm5p852kOMSIg</div>
    <div class="kc-brokers">
      <div class="kc-broker">
        <div class="kc-tag">Broker #1</div>
        <div class="kc-desc">KAFKA_NODE_ID = 1<br>실습용 단일 브로커</div>
      </div>
    </div>
    <div class="kc-listeners">
      <div class="kc-listener">
        <span class="kc-listener-lbl">CONTROLLER_QUORUM_VOTERS</span>
        <span class="kc-listener-val">1@localhost:9093 (자기 자신)</span>
      </div>
    </div>
  </div>
  <div class="kc-note">단일 브로커이므로 컨트롤러가 자기 자신과만 통신. 멀티 브로커 시 같은 CLUSTER_ID 노드끼리 동기화.</div>
</div>
```

클라이언트 진입 토폴로지(`.kc-clients` → `.kc-arrow` → `.kc-cluster`)로 ADVERTISED_LISTENERS 주소를 보여주는 변형 가능.

**렌더 CSS**: `styles/diagrams.css` MSA 블록 (`.kafka-cluster`, `.kc-title`, `.kc-cluster`, `.kc-cluster-id`, `.kc-brokers`, `.kc-broker`, `.kc-tag`, `.kc-desc`, `.kc-listeners`, `.kc-listener`, `.kc-listener-lbl`, `.kc-listener-val`, `.kc-clients`, `.kc-client`, `.kc-arrow`, `.kc-note`)

**변형**: 클러스터 컨테이너는 오렌지 점선 테두리(Kafka 시각 표식). 클라이언트 진입을 보여줄 때 `.kc-clients` 행을 위에, `.kc-arrow ↓`로 클러스터에 연결. 멀티 브로커 시 `.kc-broker`를 3개 이상 가로로 배치 가능.

**피해야 할 것**
- CLUSTER_ID·NODE_ID 같은 식별자를 코드블록 안에 따로 넣지 말 것. 이 컴포넌트 내부 `.kc-cluster-id`·`.kc-tag`로 표현해야 시각적으로 묶임
- 환경변수 4개 이상 나열: Listener 다이어그램은 핵심 1~2개(LISTENERS, ADVERTISED_LISTENERS, QUORUM_VOTERS 중)만. 전체 환경변수는 코드블록으로
- 브로커 박스를 인디고 색으로: 시리즈 톤에서 Kafka는 오렌지로 통일
