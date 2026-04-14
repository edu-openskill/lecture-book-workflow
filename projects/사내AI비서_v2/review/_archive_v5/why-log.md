# Why Log

## 2026-03-15-1: CH08 캡처 이미지 — 색상/여백 문제

**증상**: 캡처 이미지에 ANSI 색상(cyan, green, yellow)이 그대로 남아있고, 양쪽 여백이 과도함

**5 Whys**:

1. 왜 실패? → ANSI 색상이 그대로 HTML 색상으로 변환됨
2. 왜? → terminal_screenshot.py가 터미널 색상 보존 설계이고, rich_capture.py가 그대로 재사용
3. 왜 오버라이드 안 했나? → 서적용 캡처의 "블랙 텍스트 + 볼드만" 규칙이 어디에도 없음
4. 왜 규칙이 없나? → screenshot 스킬이 "터미널 재현" 목적으로만 설계됨
5. **근본 원인** → 서적 캡처 시 스타일 규칙(블랙/볼드/여백)이 부재

**수정**:

- `.claude/rules/style.md` — "ANSI 색상 변환 금지" + "불필요한 공백 금지" 규칙 2줄 추가
- `rich_capture.py` — `ansi_to_html()` 결과에서 모든 `color:` 값을 `#222222`로 치환
- `terminal_screenshot.py` — CSS: `min-width: auto`, `padding: 12px 16px`

**참조**: CH08 5개 캡처 (08_chunk-size, 08_overlap, 08_strategy-comparison, 08_reranker, 08_hybrid-search)

## 2026-03-15-2: CH08 캡처 이미지 — 오른쪽 여백 과다

**증상**: 색상/padding 수정 후에도 오른쪽에 큰 빈 공간이 남아있음

**5 Whys**:

1. 왜 오른쪽 여백? → `.terminal` 컨테이너가 테이블보다 넓음
2. 왜 넓음? → `white-space: pre`가 trailing 공백을 그대로 보존
3. 왜 trailing 공백? → `COLUMNS=100` 환경변수 → Rich가 100칸에 맞춰 줄 끝을 공백으로 채움
4. 왜 `width: fit-content`로 안 줄었나? → `pre` 모드에서 trailing 공백도 "콘텐츠"
5. **근본 원인** → Rich 출력의 각 줄 trailing 공백을 제거하지 않음

**수정**:

- `rich_capture.py` — HTML 변환 전 `line.rstrip()` + `run_and_capture(columns=80)` 으로 Rich 테이블 폭 축소
- `terminal_screenshot.py` — `run_and_capture()`에 `columns` 파라미터 추가 (기본값 100 유지)
- `.claude/rules/style.md` — "trailing 공백 제거" 규칙 추가

## 2026-03-15-3: 목차에 소제목 누락

**증상**: PDF 목차에 1.1, 1.2 등 소제목이 표시되지 않음. h1과 "기술 파트"(h2)만 나옴

**5 Whys**:

1. 왜 소제목이 목차에 없나? → `outline(depth: 2)`가 h1+h2만 표시
2. 왜 depth:2로 부족? → 소제목이 `###` (h3) 레벨
3. 왜 h3인가? → `## 이야기 파트`/`## 기술 파트`가 h2를 차지, 실제 소제목은 h3
4. 왜 소제목 번호 추가할 때 depth를 안 바꿨나? → heading 레벨과 목차 depth의 연관을 점검하지 않음
5. **근본 원인** → 마크다운 heading 구조 변경 시 Typst 목차 설정을 연동 점검하지 않음

**수정**:

- `book_base.typ` — `outline(depth: 2)` → `outline(depth: 3)`
- `pub-typst-design/SKILL.md` — "heading 레벨 변경 시 outline depth 점검" 규칙 추가

## 2026-03-15-4: 목차 depth 수정이 반영 안 됨

**증상**: `book_base.typ`에서 `depth: 3`으로 수정했는데 PDF 목차에 여전히 소제목 없음

**5 Whys**:

1. 왜 depth:3이 반영 안 됐나? → 빌드가 프로젝트 `templates/book_base.typ`을 사용
2. 왜 프로젝트 파일이 depth:2인가? → 스킬 원본의 **복사본**이라 동기화 안 됨
3. 왜 복사본인가? → 최초 설정 시 심볼릭 링크 대신 파일 복사로 생성
4. 왜 스킬 원본만 수정했나? → 스킬 파일을 수정하면 프로젝트에 자동 반영될 것으로 착각
5. **근본 원인** → 프로젝트 `book_base.typ`이 스킬 원본의 복사본이라 수정이 전파되지 않음

**수정**:

- 프로젝트 `book/templates/book_base.typ` → 스킬 원본 심볼릭 링크로 교체
- `pub-typst-design/SKILL.md`에 "심볼릭 링크 사용" 규칙이 이미 명시되어 있었으나 미준수

## 2026-03-15-5: 페이지 하단 대형 공백

**증상**: 페이지 5 하단에 큰 공백. 이미지가 남은 공간에 안 들어가 다음 페이지로 밀림

**5 Whys**:

1. 왜 공백? → 이미지가 남은 공간에 안 들어가서 다음 페이지로 밀림
2. 왜 안 들어갔나? → `auto-image()` 축소 시도했으나 이미지+캡션이 남은 공간보다 큼
3. 왜 축소 안 됐나? → 최소 비율 0.5 (50% 미만이면 원래 크기로 다음 페이지 이동)
4. 왜 0.5? → 너무 작으면 읽기 어렵다는 보수적 설정
5. **근본 원인** → 최소 축소 비율이 높아서 중간 크기 공백을 활용하지 못함 + 빌드 후 공백 검수 부재

**수정**:

- `book_base.typ` — `auto-image()` 최소 비율 0.5 → 0.35
- publisher 에이전트에 "빌드 후 1/3 이상 공백 페이지 감지 → 이미지 크기 또는 텍스트 재배치" 지침 추가

## 2026-03-15-6: D2 다이어그램 샘플 디자인 미적용

**증상**: CH01 D2 다이어그램이 기본 스타일로 작성됨. 샘플에 있는 classes/shadow/border-radius/프라이머리 컬러 미사용

**5 Whys**:

1. 왜 샘플 디자인을 안 썼나? → D2 생성 시 샘플을 참조하라는 규칙이 없음
2. 왜 규칙이 없나? → 샘플 파일은 `book/output/`과 스킬 `references/samples/`에 있었지만 "반드시 참조" 지침 부재
3. 왜 지침을 안 넣었나? → 샘플 파일 관리를 스킬에 옮기는 작업만 했고 사용 강제 규칙을 빠뜨림
4. **근본 원인** → D2 디자인 시스템(classes)을 재사용하라는 규칙이 에이전트/스킬 어디에도 없었음

**수정**:

- `publisher/AGENT.md` — "새 D2 생성 시 샘플 classes 복사 필수" 규칙 추가
- CH01 D2 파일 → 샘플 디자인 시스템으로 교체

## 2026-03-15-7: D2 다이어그램에 빨강/초록 강조색 사용

**증상**: CH01 `01_llm-vs-rag.d2`의 `danger` 클래스가 빨강(#dc2626), `success` 클래스가 초록(#16a34a)으로 렌더링됨

**5 Whys**:

1. 왜 빨강/초록? → `danger`/`success` 클래스에 의미 색상(red/green)을 적용함
2. 왜 의미 색상을 넣었나? → 환각=위험(빨강), RAG=성공(초록)이라는 직관적 표현 의도
3. 왜 화이트 규칙이 없었나? → "모든 도형 배경 화이트" 규칙은 있었으나 danger/success 같은 시맨틱 클래스는 예외로 인식
4. **근본 원인** → "강조색 금지" 규칙이 명시적이지 않아 시맨틱 클래스에서 색상 사용

**수정**:

- `01_llm-vs-rag.d2` — `danger`/`success` 클래스 fill/stroke/font-color를 화이트(start-end 스타일)로 변경
- `publisher/AGENT.md` — "빨강/초록/노랑 등 강조색 금지" 규칙 추가

## 2026-03-15-8: 빌드 후 레이아웃 자동 검수 미실행

**증상**: `pub-layout-check` 스킬이 존재하지만 빌드 후 자동으로 실행되지 않음. 사용자가 매번 수동 요청해야 함

**5 Whys**:

1. 왜 자동 실행 안 됐나? → `build_chapter()` 함수에 layout-check 호출이 없음
2. 왜 호출이 없나? → 스킬을 만들었지만 빌드 파이프라인에 통합하지 않음
3. 왜 통합 안 했나? → 스킬 생성과 파이프라인 통합을 별개 작업으로 처리, 통합 단계를 빠뜨림
4. **근본 원인** → 스킬 생성 시 "어디서 호출할 것인가"를 함께 정의하지 않음

**수정**:

- `typst_builder.py`의 `build_chapter()` 마지막에 `pdf_layout_checker.py` subprocess 호출 추가
- 이슈 있으면 출력, 없으면 조용히 통과

## 2026-03-15-9: PDF 조판 세부 규칙 부재 (6개 이슈)

**증상**: CH01 PDF에서 (1) 인용 디자인이 이야기/기술 파트 구분 없음 (2) 터미널 실행결과 이미지가 좁음 (3) 코드 블록 간 문단 간격 부족 (4) 그림 1-2가 커서 p5 공백 (5) 그림 1-4가 작음 (6) 용어 정리 표 열 균등으로 가독성 저하

**5 Whys**:

1. 왜 6가지 이슈? → Typst 템플릿과 후처리 파이프라인에 세부 조판 규칙이 부재
2. 왜 부재? → "기본값으로 충분하다"고 가정하고 PDF 출력물을 검토하지 않음
3. 왜 검토 안 했나? → 빌드 후 시각적 검토 프로세스가 없고 layout-check는 공백만 감지
4. **근본 원인** → 조판 규칙이 "콘텐츠 유형별"로 세분화되지 않음. 이미지 경로, 인용 위치, 테이블 구조에 따른 차별화 규칙 부재

**수정**:

- `book_base.typ` — 코드 블록 상하 v(6pt) 여백 추가, 테이블 par justify:false
- `typst_builder.py` — terminal/ 이미지 0.95, 가로형 diagram 0.85, 세로형 0.35, 3열+ 테이블 마지막 열 2fr, 기술파트 blockquote→callout-box
- `publisher/AGENT.md` + `style.md` — 관련 규칙 보강

## 2026-03-15-10: 실습순서 Mermaid 미변환 + callout 하이픈 + 공백 자동 해소 없음

**증상**: (1) 2.4 실습순서에 Mermaid 코드블록이 그대로 남아있어 PDF에서 텍스트로 출력 (2) callout-box에 불필요한 `-` 구분자 표시 (3) layout-check가 공백을 감지만 하고 자동 수정하지 않음

**5 Whys**:

1. 왜 Mermaid가 남아있나? → D2 교체가 `diagram/` 폴더의 이미지만 대상, 마크다운 내 코드블록은 놓침
2. 왜 callout에 `-`? → `book_base.typ`에 `\-` 구분자가 하드코딩됨
3. 왜 공백을 자동 해소 안 했나? → layout-check가 감지 전용이고 수정 로직이 없음
4. **근본 원인** → (1) D2 전환 체크리스트에 "인라인 mermaid 코드블록" 항목 부재 (2) 디자인 템플릿의 구분자가 하드코딩 (3) 감지→수정→재빌드 루프가 구현되지 않음

**수정**:

- CH01 Mermaid 코드블록 → D2 파일 생성 + 이미지 교체
- `book_base.typ` callout-box에서 `-` 제거, 라벨 없으면 본문만 표시
- `typst_builder.py`에 자동 공백 해소 루프 구현 (최대 3회 이미지 축소 + 재빌드)
- `publisher/AGENT.md`에 이미지 위치 이동 허용 규칙 추가

## 2026-03-15-11: D2 다이어그램 텍스트 잘림 + 박스 크기 부족

**증상**: CH01 실습순서 D2(`01_exercise-flow.d2`)에서 step3_no 파일명이 잘리고 전체 다이어그램이 너무 작게 렌더링됨

**5 Whys**:

1. 왜 텍스트 잘림? → step3_no 박스 width(160px)가 `step3_rag_no_chunking.py` 텍스트에 비해 좁음
2. 왜 좁았나? → 모든 박스를 동일 width(160)로 설정, 텍스트 길이 미고려
3. 왜 다이어그램이 작았나? → `_detect_image_max_width()`에 exercise-flow 패턴이 없어 기본 diagram 비율(0.4~0.7) 적용
4. **근본 원인** → D2 박스 크기가 텍스트 길이를 고려하지 않음 + flow 다이어그램 전용 이미지 비율 부재

**수정**:

- `01_exercise-flow.d2` — width 160→220, height 55→70, font-size 16→20, step3_no width 280
- `typst_builder.py` `_detect_image_max_width()` — `exercise-flow`/`flow` 패턴 → 0.95 추가

## 2026-03-15-12: 그림 1-2(context-overflow) 이미지 비정상 확대

**증상**: `01_context-overflow.png`가 0.95(좌우 꽉 채움)로 렌더링되어 비정상적으로 커짐

**5 Whys**:

1. 왜 0.95? → `_detect_image_max_width()`에서 `'flow' in path` 조건에 매칭
2. 왜 매칭? → `context-overflow`의 `overflow`에 `flow` 부분 문자열이 포함
3. 왜 부분 문자열 매칭? → exercise-flow 전용으로 `'exercise-flow' in path or 'flow' in path`를 사용, `flow` 단독이 너무 넓은 패턴
4. **근본 원인** → 부분 문자열 패턴 `'flow'`가 `overflow`, `workflow` 등에 오탐

**수정**:

- `typst_builder.py` L192 — `'exercise-flow' in path or 'flow' in path` → `'exercise-flow' in path`로 축소

## 2026-03-15-13: p13 공백(56%) 미감지 + 터미널 이미지 과대

**증상**: p13이 56% 사용률인데 layout-check가 이슈로 감지하지 않음. 그림 1-7(터미널 이미지)이 0.95로 과대

**5 Whys**:

1. 왜 p13 공백 미감지? → `low_usage` 기준이 `< 45%`라 56%는 통과
2. 왜 45%? → 초기 설정 시 "절반 이하만 문제"라는 보수적 기준
3. 왜 보수적? → 오탐을 피하려 했으나 실제로는 50~60%도 시각적으로 공백이 눈에 띔
4. **근본 원인** → `low_usage` 감지 기준이 너무 보수적(45%). 터미널 이미지 0.95가 공백 밀림 유발

**수정**:

- `pdf_layout_checker.py` L115 — `< 45` → `< 60`으로 감지 기준 완화
- `typst_builder.py` — 터미널 이미지 비율 0.95 → 0.75로 축소
- publisher 에이전트 규칙: "터미널 이미지도 공백 밀림 유발 가능" → why-log.md#2026-03-15-13

## 2026-03-15-14: 마지막 페이지 공백 — 자동 해소 불가

**증상**: p17(마지막 페이지)이 87%인데 이미지 축소로는 해결 불가. 콘텐츠 분량 자체가 문제

**근본 원인**: 마지막 페이지 공백은 이미지 축소 루프로 해결할 수 없는 유형. 콘텐츠 양 자체를 줄이거나 늘려야 함

**수정**: "더 알아보기" 섹션 제거 → "이것만은 기억하세요"에 1줄로 통합 → 17p → 16p

## 2026-03-15-15: CH02 Mermaid 미변환 + 이미지 폴더 분류 오류

**증상**: (1) CH02에 Mermaid 코드블록 2개 잔존 (그림 2-1 API 웨이터, 실습순서) (2) `02_crud-menu.png`(Gemini 개념도)이 `terminal/`에 분류되어 0.75 적용 → 과대

**5 Whys**:

1. 왜 Mermaid가 남아있나? → CH01에서만 Mermaid→D2 변환 수행, CH02 이후 챕터 점검 누락
2. 왜 crud-menu가 terminal에? → 캡처 생성 시 이미지 유형(개념도 vs 터미널)을 구분하지 않고 terminal/에 일괄 저장
3. **근본 원인** → (1) Mermaid→D2 변환이 프로젝트 전체가 아닌 챕터 단위로만 수행 (2) 이미지 폴더 분류 기준(gemini/diagram/terminal) 미준수

**수정**:

- CH02 Mermaid 2개 → D2 파일 생성 + 이미지 교체
- `02_crud-menu.png` → `gemini/`로 이동
- 13p → 11p

## 2026-03-15-16: autocrop이 Gemini 이미지 여백을 못 자름

**증상**: `02_crud-menu.png`(Gemini 개념도)의 넓은 여백이 autocrop으로 제거되지 않음

**5 Whys**:

1. 왜 autocrop 안 됐나? → `getbbox()`가 전체 이미지를 콘텐츠로 인식
2. 왜 전체가 콘텐츠? → `ImageChops.difference(img, white_bg)`에서 배경색 차이 감지
3. 왜 차이? → Gemini 이미지 배경이 순백(255,255,255)이 아닌 연한 회색(252-254)
4. **근본 원인** → `autocrop_image()`가 정확히 #FFFFFF만 빈 공간으로 판단, 허용 오차(tolerance)가 없음

**수정**:

- `typst_builder.py` `autocrop_image()` — `tolerance` 파라미터 추가 (기본값 10)
- `diff.point(lambda x: 0 if x <= tolerance else x)` 적용하여 ±10 이내 차이는 배경 처리
- 적용 결과: 23개 이미지 추가 crop 성공

## 2026-03-15-17: 이미지 크기 경로별 제각각 + layout-check 사용률 불일치

**증상**: (1) `_detect_image_max_width()`에 7가지 패턴별 비율 → 이미지 크기 비일관 (2) `print_page_usage`는 p05=42% 표시하는데 `analyze_layout`은 이슈 0개 → 자동 수정 루프 미작동

**5 Whys**:

1. 왜 이미지 크기가 제각각? → 경로별 패턴(terminal/0.75, diagram/AR기반, step/0.6 등) 7가지 분기
2. 왜 이렇게 많나? → 개별 이슈 대응 시 패턴을 하나씩 추가하면서 복잡해짐
3. 왜 layout-check가 감지 못 했나? → `print_page_usage`는 `max_y - min_y`, `analyze_layout`은 `max_y - content_top` 사용
4. **근본 원인** → (1) 기본값 통일 없이 경로별 예외를 늘림 (2) 두 함수의 사용률 계산 공식이 달라 시각화와 감지가 불일치

**수정**:

- `_detect_image_max_width()` → chapter-opening(0.4), exercise-flow(0.85), 나머지 전부 0.6으로 단순화
- `print_page_usage` → `max_y - min_y` 대신 `max_y - content_top` (analyze_layout과 동일)
- 결과: 전 페이지 87% 균일

## 2026-03-15-19: 챕터 헤더 blockquote — CH01만 정상 출력

**증상**: PDF에서 챕터 상단 요약 블록(버전/요약/핵심개념)이 CH01만 깔끔하게 나오고 나머지는 깨짐

**5 Whys**:
1. 왜 CH01만 잘 나왔나? → CH01은 `<br>` 태그로 blockquote 내 줄바꿈 강제
2. 왜 CH02~는 안 되나? → `<br>` 없이 `>` 줄만 나열, Pandoc이 하나의 블록으로 합침
3. 왜 `<br>`가 빠졌나? → CH02 이후 작성 시 CH01 패턴을 따르지 않음
4. **근본 원인** → 챕터 헤더 blockquote 형식 규칙이 명시되지 않음

**수정**:
- 전 챕터 blockquote에 `<br>` 추가하여 CH01 형식과 통일
- 규칙 추가: auto-chapters.md

## 2026-03-15-20: 인라인 코드 □ 깨짐 — 폰트 글리프 누락

**증상**: PDF p88/p90/p104/p109에서 인라인 코드 `"""`, `->` 등이 □로 표시

**5 Whys**:
1. 왜 □로 나오나? → 해당 글리프가 렌더링 폰트에 없음
2. 왜 폰트에 없나? → 인라인 코드에 모노스페이스 폰트가 미지정
3. 왜 미지정? → `raw.where(block: false)` show rule에서 `it.text`를 일반 텍스트로 출력
4. **근본 원인** → `it.text`가 raw 요소를 해제하여 Typst smart quotes/ligature 적용 + 본문 폰트 사용

**수정**:
- `book_base.typ`: `it.text` → `it` + `font: ("Menlo", "KoPubDotum_Pro")` 추가
- 규칙 추가: `.claude/rules/style.md`

## 2026-03-15-21: 시퀀스 다이어그램 — 플로우차트로 작성됨

**증상**: PDF p93에서 "시퀀스 다이어그램"이라 했는데 좌→우 플로우차트 형태

**5 Whys**:
1. 왜 플로우차트인가? → D2 변환 시 `direction: right` 일률 적용
2. 왜 구분 안 했나? → 본문 맥락(시퀀스/플로우/구조)을 확인하지 않음
3. **근본 원인** → D2 변환 시 본문의 다이어그램 유형 설명을 반영하는 규칙 없음

**수정**:
- `06_sequence-crud.d2`: `shape: sequence_diagram` 으로 재작성
- `09_sequence-pipeline.d2`: 동일 적용

## 2026-03-15-22: "이번 버전:" 텍스트 — 챕터에 불필요 정보

**증상**: 모든 챕터 blockquote에 "이번 버전: exNN → exNN" 라인 포함

**5 Whys**:
1. 왜 들어갔나? → 작가 에이전트가 챕터 작성 시 버전 추적용으로 삽입
2. 왜 문제인가? → 독자에게 불필요한 메타데이터, PDF 지면 낭비
3. **근본 원인** → 작가 에이전트에 금지 규칙 없음

**수정**:
- 전 챕터(01~10)에서 해당 줄 삭제
- 규칙 추가: `.claude/agents/writer/AGENT.md`

## 2026-03-15-23: 실습 순서 — 다이어그램 대신 목록

**증상**: 실습 순서가 D2 다이어그램으로 표시되어 다른 다이어그램과 디자인 불일치

**5 Whys**:
1. 왜 다이어그램인가? → 일러스트레이터가 모든 순서를 다이어그램화
2. 왜 문제인가? → 3~5 단계 단순 순서는 번호 목록이 더 간결하고 지면 효율적
3. **근본 원인** → "실습 순서는 텍스트 목록으로" 규칙 없음

**수정**:
- 전 챕터 exercise-flow 이미지 → 번호 목록 교체
- 규칙 추가: `.claude/agents/writer/AGENT.md`

## 2026-03-15-24: D2 다이어그램 디자인 — 파란 배경 불일치

**증상**: 일부 D2 다이어그램이 `fill: "#3b82f6"` 파란 배경 + 흰 글자로 렌더링

**5 Whys**:
1. 왜 디자인이 다른가? → D2 변환 시 일률적 스타일 대신 각각 다른 스타일 적용
2. **근본 원인** → D2 스타일 가이드(흰배경 `#eef2ff`, 파란 테두리 `#2563eb`) 미준수

**수정**:
- `09_ch08-vs-ch09.d2`, `09_sequence-pipeline.d2` 스타일 통일
- 규칙 참고: 일러스트레이터 D2 스타일 가이드

## 2026-03-15-25: 줄바꿈이 너무 많다 — 문단 구성 원칙 부재

**증상**: 전 챕터에서 같은 맥락의 문장이 빈 줄로 불필요하게 분리. 한 줄짜리 문장이 나열되어 가독성 저하

**5 Whys**:
1. 왜 줄바꿈이 많았나? → 작가 에이전트가 문장마다 독립 문단으로 작성
2. 왜 문장마다 끊었나? → "빈 줄 삽입" 규칙만 있고 "같은 맥락은 이어쓰기" 규칙이 없었음
3. **근본 원인** → 문단 구성 원칙이 명시되지 않음

**수정**:
- 전 챕터(CH00~CH10) 약 90건 문단 합치기
- 규칙 추가: `.claude/rules/style.md` L23-24 (문단 구성 + 숨돌리기 빈 줄)

## 2026-03-15-26: 캡처 이미지에 장식선(═══) 포함

**증상**: book_capture.py로 캡처한 이미지에 `═══ step 1-1: 청크 크기 실험 ═══` 장식선이 포함됨. 기존 정상 캡처(08_chunk-experiment-2.png)에는 없던 장식선.

**5 Whys**:
1. 캡처에 장식선이 왜 나왔나? → 실험 스크립트가 `console.rule()` 사용
2. 왜 스크립트가 rule()을 쓰나? → 작성 시 code.md "장식선 금지" 규칙 미적용
3. 왜 미적용? → 캡처 전 스크립트 출력 규칙 준수 여부 점검 절차 없음
4. **근본 원인** → 캡처 실행 전 사전 점검 규칙 부재

**수정**:
- ex08/ex09/ex10 전체 tuning 스크립트에서 `console.rule()` → `console.print("[bold]...[/bold]")` 교체 (총 31건)
- "실험 완료" 장식선은 삭제 (불필요)
- 규칙 추가: `.claude/rules/code.md` "캡처 전 console.rule() 잔존 여부 grep 점검"
