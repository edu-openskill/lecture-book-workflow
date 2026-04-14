# Captions

> 인라인 라벨·캡션·태그. 다른 컴포넌트의 보조 텍스트 또는 단독 캡션.

## 속함

- 이미지 캡션: Markdown 이탤릭 `*그림 N-N. 설명*` (이 프로젝트는 Typst 미경유 전자책이라 수동 번호 유지)
- `.caption` (일반 캡션)
- `.eer-caption` (임베딩 예시 전용)
- `.cwm-note` (청크 카드 보조 설명)
- `.rl-caption` (CH06 ReAct 루프 캡션)
- 태그/뱃지: `.afm-tag`, `.afm-zone-ch`, `.afm-zone-label`, `.afm-note`
- `.api-tag`, `.rag-tag`, `.agent-tag`, `.tune-tag`
- `.num-badge`

## 속하지 않음

- 박스 컨테이너 자체 → [`../boxes/`](../boxes/)
- 카드 본체 → [`../cards/`](../cards/)

## 톤 규칙

- 캡션은 **존댓말**. 반말 종결(`-다`/`-이다`) 금지.
- 그림 번호 접두어 `그림 N-N:` (콜론) 금지. `그림 N-N.` (마침표)는 이 프로젝트 허용.

## 컴포넌트 목록

### 군 1. Markdown 이미지 캡션 (Markdown 규칙)

#### Markdown 이미지 캡션

**언제 쓰는가**: 모든 이미지 바로 아래. `![](경로)` 다음 줄에 이탤릭으로 `*그림 N-N. 설명*`. 이 프로젝트는 Typst를 경유하지 않는 전자책 파이프라인이라 번호를 수동으로 유지한다.

**사용 챕터**: CH01~CH10 (전 챕터)

**Markdown 사용 예**:
```markdown
![](../assets/CH04/gemini/04_chapter-opening.png)
*그림 4-1. 문서를 지식으로 바꾸는 주방. 손질, 다지기, 양념, 냉장고*
```

**렌더 CSS**: `base.css:32` (`.chapter-image .caption` 기본 스타일) + `print.css:151`, `print.css:229` (인쇄 변형). markdown-it가 이탤릭 단락을 캡션으로 인식.

**변형(Variants)**: 없음. 형식 고정.

**피해야 할 것**
- 콜론 접두어 `그림 N-N:` 사용 금지 (마침표만 허용)
- 반말 종결(`-다`/`-이다`) 사용 금지 — 존댓말만
- 캡션 2줄 이상 금지 — 1줄에 담을 것
- `![](alt)` alt 텍스트 채우지 말 것 (alt는 비워두고 캡션으로 대체)
- `그림 N-N` 번호 누락 금지 (Typst 자동 부여 아님. 수동 관리)

### 군 2. HTML 캡션 클래스

#### .caption (일반 캡션)

**언제 쓰는가**: 이미지를 `<figure class="chapter-image">` 등 HTML 구조에 담을 때. Markdown 이탤릭이 불가능한 구성(그리드/듀얼 이미지)에서 사용.

**사용 챕터**: 전 챕터 (HTML로 이미지를 감쌀 때)

**HTML 사용 예**:
```html
<figure class="chapter-image">
  <img src="../assets/CH04/gemini/04_chapter-opening.png" alt="">
  <div class="caption">그림 4-1. 문서를 지식으로 바꾸는 주방</div>
</figure>
```

**렌더 CSS**: `base.css:32` (`.chapter-image .caption`), `print.css:151`, `print.css:229`

**변형**: 없음

**피해야 할 것**
- Markdown 이탤릭으로 충분한 자리에 HTML `.caption` 남용 금지
- `.chapter-image` 바깥에서 단독 사용 금지 (스코핑 CSS)

#### .eer-caption (임베딩 예시 캡션)

**언제 쓰는가**: CH04 임베딩 예시 박스(`.eer-*`) 바로 아래. 좌/우 2열 구성의 이중 이미지에 공통 캡션이 필요할 때.

**사용 챕터**: CH04 (문서를 지식으로 바꾸다)

**HTML 사용 예**:
```html
<div class="eer-grid">
  <div class="eer-left">...</div>
  <div class="eer-right">...</div>
</div>
<div class="eer-caption">그림 4-5. 왼쪽(문장 임베딩 벡터 예시. 앞 몇 자리만 봐도 비슷/다름이 드러남), 오른쪽(임베딩 공간에 찍힌 좌표. 의미가 가까운 문서가 한 곳에 모임)</div>
```

**렌더 CSS**: `diagrams.css:1918`

**변형**: 없음

**피해야 할 것**
- 단일 이미지에 사용 금지 (좌/우 2열 전용)
- 임베딩 박스 바깥에서 사용 금지

#### .cwm-note (청크 카드 보조 설명)

**언제 쓰는가**: CH04 청크 카드(`.cwm-*`) 하단에 "이 데이터가 실제로 어디에 저장되는지" 같은 보조 설명이 필요할 때.

**사용 챕터**: CH04

**HTML 사용 예**:
```html
<div class="cwm-note">이 라벨들이 ChromaDB에 <code>metadata</code> 필드로 같이 저장됩니다. 검색할 때 "HR 폴더의 3페이지 근처 문서만"처럼 필터링도 가능합니다.</div>
```

**렌더 CSS**: `diagrams.css:1824`, `diagrams.css:1832` (내부 `code` 규칙)

**변형**: 없음

**피해야 할 것**
- 그림 캡션 용도로 사용 금지 (번호를 매기지 않음. 보조 설명 전용)
- 청크 카드 바깥에서 사용 금지

#### .rl-caption (CH06 ReAct 루프 캡션)

**언제 쓰는가**: CH06 ReAct 루프 시퀀스(`.rl-*`) 하단에 그림 번호가 붙은 캡션이 필요할 때. Markdown 이탤릭으로 표현할 수 없는 HTML 다이어그램의 전용 캡션.

**사용 챕터**: CH06 (연차도 규정도 한번에)

**HTML 사용 예**:
```html
<div class="rl-exit">최종 답이 충분하면 루프 종료 → 자연어 답변 생성</div>
<div class="rl-caption">그림 6-4. ReAct 루프는 충분한 정보를 모을 때까지 같은 순환을 반복하며, 매 Observe 단계의 결과가 다음 Reason의 입력이 됩니다</div>
```

**렌더 CSS**: `diagrams.css:1531`

**변형**: 없음

**피해야 할 것**
- 일반 이미지 캡션은 Markdown 이탤릭 사용 (HTML 남용 금지)
- ReAct 루프 바깥에서 사용 금지 — 범용 HTML 캡션이 필요하면 `.caption` 사용

### 군 3. 인라인 태그 & 뱃지

**언제 쓰는가**: 박스·트리·다이어그램 내부에 짧은 분류 라벨이나 번호를 붙일 때. 단독 사용이 아니라 상위 컨테이너에 종속된다.

**태그 목록**:

| 클래스 | 용도 | 색상 의도 | 상위 컨테이너 |
|-------|------|----------|-------------|
| `.afm-tag` | fullmap 박스 상단 "오늘 만든 부분" 태그 | 강조 (박스 상단) | `.afm-box` |
| `.afm-zone-ch` | "챕터 N" 뱃지 | 중립 (zone 식별) | `.afm-zone` |
| `.afm-zone-label` | zone 역할명 | 중립 | `.afm-zone` |
| `.afm-note` | fullmap 하단 요약 텍스트 | 회색 | `.full-architecture-map` |
| `.api-tag` | arch-tree API 분류 태그 | 파랑 (`#fef3c7` 배경) | `.at-part-tag` |
| `.rag-tag` | arch-tree RAG 분류 태그 | 초록 (`#dbeafe` 배경) | `.at-part-tag` |
| `.agent-tag` | arch-tree 에이전트 분류 태그 | 보라 (`#e9d5ff` 배경) | `.at-part-tag` |
| `.tune-tag` | arch-tree 튜닝 분류 태그 | 주황 (`#fecaca` 배경) | `.at-part-tag` |
| `.num-badge` | 번호 원형 뱃지 | 중립 (`--color-info` 배경) | 자유 (prep-item 등) |

**HTML 사용 예 (fullmap)**:
```html
<div class="afm-box afm-on">
  <div class="afm-tag">오늘 만든 부분</div>
  <div class="afm-label">LCEL Chain</div>
</div>
```

**HTML 사용 예 (arch-tree)**:
```html
<div class="at-branch">
  <span class="at-line">├─</span>
  <span class="at-folder">rag/</span>
  <span class="at-part-tag rag-tag">RAG</span>
</div>
```

**렌더 CSS**:
- `.afm-tag` → `diagrams.css:300`
- `.afm-zone-ch` → `diagrams.css:247`
- `.afm-zone-label` → `diagrams.css:258`
- `.afm-note` → `diagrams.css:319`, `diagrams.css:327` (`b` 강조)
- `.api-tag` → `components.css:355`
- `.rag-tag` → `components.css:356`
- `.agent-tag` → `components.css:357`
- `.tune-tag` → `components.css:358`
- `.num-badge` → `components.css:407` (독립), `components.css:38` (`.prep-item-title` 내부)

**피해야 할 것**
- 태그 텍스트에 긴 문장 금지 (1~6자 권장)
- 같은 요소에 2개 이상 태그 중첩 금지 (한 박스에 `.afm-tag`와 `.api-tag` 동시 사용 금지)
- `.api-tag` 등 컬러 태그를 fullmap에 쓰지 말 것 (fullmap은 `.afm-*` 전용)
- `.afm-tag`를 arch-tree에 쓰지 말 것 (arch-tree는 `.at-part-tag` + `.{api,rag,agent,tune}-tag` 조합)
- `.num-badge`를 2자리 이상 숫자에 사용 금지 (원형 22px이라 1자리 기준)
- 반말·명령조 라벨 금지 — 태그도 톤 규칙 적용(`완료`, `RAG`, `오늘 만든 부분`처럼 명사형)
