# Spike: LaTeX → Typst 수식 변환 결과 (S2)

Date: 2026-06-24
Pandoc: 3.10

## 샘플 수식 변환 결과 (pandoc -f markdown -t typst)

| LaTeX | Typst 출력 | 상태 |
|-------|-----------|------|
| `$x = \frac{-b \pm \sqrt{b^2-4ac}}{2a}$` | `$x = frac(- b plus.minus sqrt(b^2 - 4 a c), 2 a)$` | 정상 |
| `$$L = \frac{1}{n}\sum_{i=1}^{n}(y_i - \hat{y}_i)^2$$` | `$ L = 1 / n sum_(i = 1)^n\(y_i - hat(y)_i\)^2 $` | 정상* |
| `$e^{i\pi} + 1 = 0$` | `$e^(i pi) + 1 = 0$` | 정상 |
| `$y = Wx + b$` | `$y = W x + b$` | 정상 |

*주의: Pandoc이 `\(` `\)` (escaped parens)을 emit하나, Typst math mode에서 컴파일 오류 없이 처리됨. 실제 typst 컴파일 확인 완료.

## 추가 fixup 필요 없음

`\begin{aligned}` 및 `\xrightarrow` 두 가지 보정 외에 추가 매크로 깨짐 없음.
모든 샘플 수식이 `fix_math_typst()` 없이도 Pandoc→Typst 변환 후 컴파일 가능.
`fix_math_typst()`는 더 복잡한 aligned 블록이나 화살표 매크로가 등장할 때를 위해 유지.

## 구현된 보정 규칙

1. `\begin{aligned}...\end{aligned}` → `&`와 `\\` 제거 (단순 인라인 수식으로 변환)
2. `\xrightarrow{...}` → `arrow.r` (라벨 손실 허용)
