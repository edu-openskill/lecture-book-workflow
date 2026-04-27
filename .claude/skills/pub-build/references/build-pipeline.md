# 빌드 파이프라인 상세 규칙

## 전처리 순서 (반드시 지켜야 함)

```
1. clean_comments()         — HTML 주석 제거
2. fix_image_paths()        — 상대경로 → 절대경로
3. render_mermaid_diagrams() — Mermaid → PNG (먼저!)
4. fix_br_tags()            — <br> → 줄바꿈 (나중에!)
```

**중요**: Mermaid 렌더링을 `fix_br_tags()` 보다 먼저 실행해야 함.
Mermaid 코드 내 `<br>`은 다이어그램 줄바꿈이므로 보존해야 한다.

## fix_br_tags 규칙

코드 블록(```) 내부의 `<br>`은 변환하지 않는다.
`re.split(r'(```.*?```)', text, flags=re.DOTALL)`로 코드 블록을 분리한 뒤,
코드 블록이 아닌 부분만 `<br>` → `  ` 변환.

## 이미지 경로 변환

| 소스 위치 | 마크다운 경로 | 변환 결과 |
|----------|-------------|----------|
| `book/body/01-*.md` | `../../assets/CH01/img.png` | `/absolute/path/assets/CH01/img.png` |
| `chapters/01-*.md` | `../assets/CH01/img.png` | `/absolute/path/assets/CH01/img.png` |

`fix_image_paths()`가 소스 파일의 디렉토리 기준으로 절대경로를 계산.
파일이 없으면 `*[이미지: alt]*` 텍스트로 대체.

## Pandoc 옵션

```
-f markdown+pipe_tables+fenced_code_blocks+backtick_code_blocks-citations
-t typst
--wrap=none
```

- `-citations`: 인용 파싱 비활성화 (`[@ref]` 패턴이 깨지지 않도록)
- `--wrap=none`: 줄 바꿈 없이 출력 (한국어 텍스트 보존)

## Typst 후처리 규칙

### 이미지 변환

Pandoc 출력 패턴 → auto-image 변환:

```
!#link("path")[alt]  →  #auto-image("path", alt: [alt], max-width: 0.6)
#box(image("path"))  →  #auto-image("path", max-width: 0.6)
```

### 수평선 처리

| 위치 | 처리 |
|------|------|
| heading 직전 | 제거 (heading이 이미 여백 생성) |
| 그 외 | `#v(4pt) + #block(height: 0.5pt, fill: gray) + #v(4pt)` |

### 한국어 라벨 제거

Pandoc이 생성하는 `<한국어-라벨>` 앵커 제거:
`re.sub(r'<[가-힣a-zA-Z0-9.\-_]+>\n', '\n', text)`

## Typst 컴파일 옵션

```bash
typst compile output.typ output.pdf --font-path ~/Library/Fonts --root /
```

- `--root /`: 절대경로 이미지 접근을 위해 루트를 `/`로 설정
- `--font-path`: RIDIBatang, D2Coding 등 사용자 폰트 경로
