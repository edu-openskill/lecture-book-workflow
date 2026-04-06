# pub-studio 리팩토링 스펙 — Typst SVG 실시간 프리뷰 + Pretext

## 목표
CSS 근사치 프리뷰를 제거하고, Typst SVG를 유일한 프리뷰로 사용.
디자인 변경 → 즉시 Typst 렌더링 → "보이는 것 = PDF 결과".

## 현재 문제
- CSS 프리뷰와 Typst 결과가 다름 (행간, 문단간격, 여백 불일치)
- 두 렌더링 엔진 유지 비용 → 새 컴포넌트 추가 시 CSS + Typst 양쪽 수정
- 표 열 너비를 Python 문자 수로 추정 → 실제 렌더링과 다름

## 아키텍처

### Phase 1: Typst CLI 실시간 프리뷰 (방식 B)
```
[HTML UI 사이드바] → 설정 변경
  ↓ (300ms 디바운스)
[서버] → design_state로 .typ 조립 → typst compile --format svg
  ↓
[브라우저] → SVG 페이지 표시
```

- 현재 탭 2(PDF 프리뷰)가 이미 이 구조
- CSS 카탈로그 탭은 이미 제거됨 (완료)
- Stage 2 캐시 활용: 디자인만 변경 시 ~200ms로 SVG 재생성

### Phase 2: Pretext 도입 — 표 열 너비 정밀 계산
```
[빌드 완료] → 표 셀 텍스트 + 폰트 정보 추출
  ↓
[브라우저] → Pretext prepare() + layout()으로 실제 텍스트 폭 측정
  ↓
[서버] → tableOverrides에 최적 열 비율 반영 → 리빌드
```

- GitHub: https://github.com/chenglou/pretext
- npm: @myriaddreamin/typst.ts (참고용)
- 한글/영문 혼합, 인라인코드 등 정확한 폭 측정
- 현재 Python `_vlen` 문자 수 추정을 대체

### Phase 3: typst.ts WASM (방식 A, 장기)
```
[브라우저] → 설정 변경 → JS로 .typ 소스 조합
  ↓
[WASM 컴파일러] → 밀리초 단위 컴파일
  ↓
[WASM 렌더러] → SVG/Canvas 즉시 렌더링
```

- 서버 불필요, 완전 클라이언트 사이드
- typst.ts: https://github.com/Myriad-Dreamin/typst.ts
- 폰트 임베딩/로딩 해결 필요
- 오프라인 동작 가능

### Phase 4: 블록 에디터
```
[블록 에디터] → 드래그/속성 편집 → MD + blockOverrides 저장
  ↓
[Typst 실시간 렌더링] → 블록 클릭 시 해당 영역 하이라이트
```

- 현재 imageOverrides/tableOverrides를 blockOverrides로 일반화
- 각 블록(heading, paragraph, code, image, table, quote)에 개별 여백/스타일 오버라이드
- 블록 순서 드래그 → MD 파일에 반영
- 에이전트가 생성한 콘텐츠를 유저가 수동 조정하는 인터페이스

## 수정 대상 파일

### Phase 1 (완료됨)
- [x] preview_editor.html — CSS 카탈로그 탭 제거
- [x] state.js — 기본값 pt 단위로 변경
- [x] renderer.js — CSS line-height 계산 수정

### Phase 2
- [ ] static/js/에 pretext 라이브러리 추가 (CDN 또는 로컬)
- [ ] tables.js — Pretext 기반 열 너비 계산 함수 추가
- [ ] build_pipeline.py — 표 메타데이터(셀 텍스트, 폰트) API 확장
- [ ] builder.js — 빌드 후 Pretext로 열 너비 재계산 → 자동 리빌드

### Phase 3
- [ ] typst.ts WASM 번들 추가
- [ ] renderer.js — Typst WASM 컴파일러/렌더러 초기화
- [ ] design.js — 설정 변경 시 WASM 직접 호출 (서버 우회)
- [ ] 폰트 로딩 전략 (RIDIBatang, D2Coding 등)

### Phase 4
- [ ] static/js/block-editor.js — 블록 파싱, 드래그, 속성 편집
- [ ] preview_server.py — /api/block-override 엔드포인트
- [ ] models.py — BlockOverride 데이터 클래스
- [ ] 85-image.typ — 블록별 오버라이드 적용

## 의존성
- Phase 1 → 2: 독립 (병렬 가능)
- Phase 2 → 3: Pretext는 WASM과 무관하게 사용 가능
- Phase 3 → 4: WASM이 있으면 블록 편집 실시간 반영이 쾌적

## 참고 자료
- Pretext: https://github.com/chenglou/pretext
- typst.ts: https://github.com/Myriad-Dreamin/typst.ts
- tinymist (VS Code Typst preview): https://github.com/Myriad-Dreamin/tinymist
- Typst --input 플래그: sys.inputs로 외부 변수 주입
- Typst HTML export (실험적): typst watch --format html --features html
