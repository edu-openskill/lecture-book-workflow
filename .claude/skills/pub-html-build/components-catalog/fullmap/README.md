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
