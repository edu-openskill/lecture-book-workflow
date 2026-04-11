# 다음 세션: JointJS 다이어그램 마이그레이션

## 목표
D2 시퀀스/플로우 다이어그램을 JointJS(무료, MPL 2.0)로 전환. D2의 디자인 컨셉(색상, 폰트, 스타일)을 승계하면서 간격 조절이 가능한 렌더링 파이프라인 구축.

## 배경
- D2 sequence_diagram은 세로 간격이 고정(하드코딩)이라 조절 불가
- D2 flowchart는 `--layout elk`로 꺾인선 적용 가능하지만, 시퀀스는 별도 엔진이라 elk 무시
- PlantUML은 간격 조절 가능하나 디자인이 90년대 수준
- GoJS는 디자인 최고지만 유료(워터마크)
- **JointJS**: 무료 + 시퀀스 데모 있음 + px 단위 커스텀 + SVG 출력

## D2 현재 디자인 컨셉 (승계 대상)
```
- process 박스: fill=#eef2ff, stroke=#2563eb, border-radius=8, font=#1e40af
- storage(cylinder): fill=#f8fafc, stroke=#c5cee0, font=#374151
- 화살표: stroke=#2563eb, stroke-width=2
- 점선 응답: stroke-dash=5
- 그룹 박스: stroke=#2563eb, stroke-dash=5, fill=#ffffff
- 폰트: bold, 14~18px
```

## 만들어야 할 것
1. **JointJS 렌더링 스크립트** (`scripts/render_diagram.js`)
   - JSON 입력 → SVG → PNG 출력
   - Node.js + Puppeteer(또는 headless) 기반
   - D2 스타일 프리셋 내장
2. **시퀀스 다이어그램 JSON 형식** 정의
3. **플로우 다이어그램 JSON 형식** 정의  
4. **CH06 다이어그램 마이그레이션** (4개)
   - 06_react-flow (flowchart) → JointJS
   - 06_tool-vs-mcp (비교 다이어그램) → JointJS
   - 06_sequence-crud (시퀀스) → JointJS
   - 06_exercise-flow (flowchart) → JointJS

## 참고
- JointJS 시퀀스 데모: https://www.jointjs.com/demos/sequence-diagram
- JointJS GitHub: https://github.com/clientIO/joint
- 현재 D2 소스: `assets/CH06/diagram/*.d2`
- D2 빌드 규칙: `.claude/skills/visual/references/image.md` (--layout elk --theme 0)
- PlantUML도 설치됨 (`brew install plantuml` 완료)

## 이번 세션에서 완료한 것
- CH04: 터미널 캡처 2건 생성
- CH05: 캡션 존댓말, 실습 번호, 코드블록 설명 보강, response_parser CH01 비교
- CH06: 캡션 존댓말, 실습 번호, 상수 설명, 코드블록 보강, 보조함수 테이블, "ReAct 에이전트" → "통합 에이전트 (ReAct 패턴)" 11건
- 전체: "이야기 파트" 메타라벨 제거 15곳, "권장합니다"→"바랍니다" 8건, 소스코드 준비 축약 8개 파일
- 규칙 추가: 캡션 존댓말, 다이어그램 실습 번호, 코드블록 친절 설명, 소스코드 준비 축약, 메타라벨 금지, 비유 회수 필수, D2 빌드(elk+theme 0)
- D2 다이어그램 CH06 4개 elk+theme 0 재빌드
- Compound Engineering 워크플로우 메모리 저장
