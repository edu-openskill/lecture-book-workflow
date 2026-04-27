---
name: image-analyzer
description: "참고 이미지를 분석하여 교육용 Gemini 프롬프트를 자동 생성"
allowed-tools: Read, Edit, Glob, Grep
---

# image-analyzer -- 참고 이미지 → Gemini 프롬프트

## 역할

저자가 챕터 MD에 삽입한 참고 이미지(인터넷/외부 출처)를 멀티모달로 분석하고, 해당 이미지의 교육적 의도를 파악하여 저작권 없는 새 이미지를 생성할 Gemini 프롬프트를 자동으로 만든다.

## 입출력

| 입력 | 출력 |
|------|------|
| 챕터 MD 파일 경로 | `[GEMINI PROMPT]` 플레이스홀더가 삽입된 챕터 MD |
| (또는) 특정 이미지 경로 | 해당 이미지에 대한 Gemini 프롬프트 |

## 실행 절차

### 1. 대상 식별

챕터 MD 파일을 읽고 이미지 태그를 스캔한다.

```
![캡션](../assets/CH{N}/{subfolder}/{파일명})
```

다음 조건의 이미지를 분석 대상으로 식별한다.
- `[GEMINI PROMPT]` HTML 주석이 **없는** 이미지 (이미 프롬프트가 있으면 건너뜀)
- `gemini/` 서브폴더에 있거나, 실제 이미지 파일이 존재하는 이미지

### 2. 이미지 분석

각 대상 이미지에 대해 순서대로 수행한다.

**a) 이미지 파일 읽기**
- Read 도구로 이미지 파일을 멀티모달로 읽음
- 이미지의 구도, 색상, 요소, 텍스트, 레이아웃을 파악

**b) 캡션 확인**
- `![캡션]` 부분에서 의도된 설명을 확인

**c) 문맥 파악**
- 이미지 태그 기준 **위 3문단 + 아래 2문단** 읽기
- 해당 문맥에서 이미지가 어떤 역할을 하는지 파악

**d) 교육적 의도 분류**

| 분류 | 설명 | Style 태그 |
|------|------|-----------|
| 비유 | 추상 개념을 일상적 사물로 비유한 이미지 | `metaphor-infographic` |
| 아키텍처 | 시스템 구조, 컴포넌트 관계도 | `architecture-infographic` |
| 프로세스 | 단계별 흐름, 파이프라인 | `process-infographic` |
| 비교 | A vs B, 전후 대비 | `comparison-infographic` |
| 결과 | 실행 결과, 데이터 시각화 | `result-infographic` |

### 3. Gemini 프롬프트 생성

**a) 베이스 스타일 적용**
- `visual/references/image.md` Section 3의 Gemini 베이스 스타일을 기반으로 한다
- 공통 심볼 패턴(사람, 서버, DB 등)을 활용

**b) 저작권 회피 전략**
- 원본의 **핵심 교육 의도**는 유지하되, 시각적 표현은 완전히 재해석
- 미니멀 B&W 라인아트 스타일로 변환
- 원본의 구도와 배치를 참고하되, 동일하게 복사하지 않음
- 원본에 영어 텍스트가 있으면 한국어로 변환
- 원본의 색상 체계를 무시하고 프로젝트 스타일(B&W) 적용

**c) 프롬프트 구조**
```
{베이스 스타일}
{이미지 의도에 맞는 구체적 프롬프트}
- 핵심 요소와 배치 설명
- 라벨 텍스트 (한국어)
- 연결선/화살표 설명
```

### 4. 플레이스홀더 삽입

방식 C 형식으로 챕터에 삽입한다.

```markdown
<!-- [GEMINI PROMPT: {NN}_{identifier}]
path: assets/CH{N}/gemini/{NN}_{identifier}.png
reference: assets/CH{N}/gemini/{원본파일명}
context: {문맥 요약 1줄}
{생성된 Gemini 프롬프트}
Style: {style-tag}
-->
![{캡션}](../assets/CH{N}/gemini/{NN}_{identifier}.png)
*그림 {N}-{순번}: {캡션}*
```

**reference 필드**: 원본 참고 이미지의 경로를 보존. 나중에 프롬프트를 개선할 때 원본을 다시 참조할 수 있도록 한다.

### 5. 유저 확인

생성된 프롬프트를 유저에게 보여주고 확인을 받은 후 최종 반영한다.
수정 요청이 있으면 반영 후 다시 확인.

## 참조

- [analysis-guide.md](references/analysis-guide.md) -- 분석 상세 가이드
- `skills/visual/references/image.md` Section 3 -- Gemini 베이스 스타일
- `skills/visual/references/image.md` Section 0.5 -- 경로 규칙
