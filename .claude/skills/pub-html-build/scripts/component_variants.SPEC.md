# component_variants.py 스펙

## 역할

[`../modes/design-explore.md`](../modes/design-explore.md)의 Step 3에서 신규 컴포넌트의 4축 변형을 HTML 프리뷰 페이지로 생성한다. 표지 위자드(`pub-studio/cover_generator.py`)와 동일한 패턴.

**상태**: 스펙만 정의됨. 실구현은 후속 PR에서 진행.

## 인자

| 플래그 | 의미 | 필수/선택 | 기본값 |
|-------|------|----------|-------|
| `--component NAME` | 컴포넌트 클래스명 (예: `chapter-note`) | 필수 | — |
| `--axes A,B,C,D` | 생성할 변형 축 (쉼표 구분) | 선택 | `A,B,C,D` 전체 |
| `--out PATH` | 결과 HTML 파일 경로 | 필수 | — |
| `--sample-text TEXT` | 컴포넌트 내부 샘플 텍스트 | 선택 | `"샘플 본문입니다."` |
| `--select A\|B\|C\|D` | 변형 선택. 지정 시 CSS를 `components.css`에 append | 선택 | (없으면 프리뷰만) |

## 4 변형 축 (고정 프리셋)

| 축 | 이름 | 디자인 언어 |
|----|------|------------|
| A | Editorial | 여백 크게, 세리프 제목(Noto Serif KR), 단색 액센트, 최소 장식 |
| B | Playful | 둥근 코너(radius 14px+), 파스텔 배경, 손글씨 느낌 강조, 친근한 이모지 아이콘 (프로젝트 규칙상 실제 이모지 대신 ::before 도형) |
| C | Technical | 격자 정렬, 모노스페이스(JetBrains Mono) 라벨, 고대비(흑/백), 얇은 보더 |
| D | Bold | 블록 컬러 배경, 굵은 산세리프, drop-shadow, 큰 타이포 |

각 축은 공통 템플릿에 대해 CSS 변수만 다르게 치환한다 (아래 산출물 구조 참조).

## 산출물

### `--select` 없을 때 (프리뷰 모드)

단일 HTML 파일. 4 변형을 **가로 2×2 그리드**로 배치.

```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <title>Component Variants: {component}</title>
  <style>
    /* Reset + grid layout */
    body { font-family: 'Pretendard', sans-serif; padding: 40px; background: #f7fafc; }
    .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 32px; }
    .cell { background: white; padding: 32px; border-radius: 12px; }
    .cell h2 { margin-top: 0; font-size: 13px; letter-spacing: 1px; color: #718096; }

    /* Variant A — Editorial */
    .a-{component} {
      padding: 24px 28px;
      border-left: 2px solid #2d3748;
      font-family: 'Noto Serif KR', serif;
      background: #fffefb;
    }

    /* Variant B — Playful */
    .b-{component} {
      padding: 20px 24px;
      border-radius: 16px;
      background: linear-gradient(135deg, #fef5e7, #fed7aa);
      border: 2px solid transparent;
    }

    /* Variant C — Technical */
    .c-{component} {
      padding: 16px 20px;
      border: 1px solid #111;
      background: white;
      font-family: 'JetBrains Mono', monospace;
      font-size: 13px;
    }

    /* Variant D — Bold */
    .d-{component} {
      padding: 28px 32px;
      background: #dd6b20;
      color: white;
      font-weight: 800;
      box-shadow: 8px 8px 0 #2d3748;
    }
  </style>
</head>
<body>
  <h1>Component: {component}</h1>
  <p>샘플 텍스트: {sample_text}</p>
  <div class="grid">
    <div class="cell">
      <h2>A — EDITORIAL</h2>
      <div class="a-{component}">{sample_text}</div>
    </div>
    <div class="cell">
      <h2>B — PLAYFUL</h2>
      <div class="b-{component}">{sample_text}</div>
    </div>
    <div class="cell">
      <h2>C — TECHNICAL</h2>
      <div class="c-{component}">{sample_text}</div>
    </div>
    <div class="cell">
      <h2>D — BOLD</h2>
      <div class="d-{component}">{sample_text}</div>
    </div>
  </div>
  <p><em>선택: <code>python component_variants.py --component {component} --select A --out ...</code></em></p>
</body>
</html>
```

### `--select X` 지정 시

1. 프리뷰 HTML은 **생성하지 않음**
2. 선택된 변형(예: A)의 CSS 블록만 추출
3. 클래스 이름을 `.{component}` (접두어 없는 최종 이름)로 변경
4. `../styles/components.css` 파일 끝에 **append**
5. 터미널에 "✓ `.{component}` 추가됨 (components.css:{NNN})" 출력

## 구현 요구사항

- Python 3.10+
- 외부 의존 없음 (stdlib + Jinja2만)
- 실행 시간 1초 이내 목표
- 파일 이름 충돌 검증: `--component` 값이 이미 `components.css`에 있으면 에러

## 테스트 시나리오

```bash
# 프리뷰 생성
python component_variants.py \
  --component chapter-note \
  --out /tmp/variants.html
# → 4 변형이 2×2 그리드로 렌더됨

# 축 선택 (A만)
python component_variants.py \
  --component chapter-note \
  --axes A \
  --out /tmp/variants-A-only.html
# → 1개만 렌더됨

# 선택 후 CSS 추가
python component_variants.py \
  --component chapter-note \
  --select A
# → components.css 끝에 .chapter-note 블록 추가
# → stdout: "✓ .chapter-note 추가됨 (components.css:1234)"

# 충돌 검증
python component_variants.py \
  --component goal-box \
  --select A
# → 에러: ".goal-box가 이미 components.css:22-26에 있습니다"
```

## 확장 (Future)

- `--select` 후 변형 **미세조정** 모드 (색상·radius 슬라이더)
- 변형 **조합** 모드 (A의 타이포 + C의 레이아웃)
- 선택 이력을 `projects/<책>/planning/design-decisions.md`에 자동 기록
