# 디자인 선택 가이드

인쇄소(publisher) 첫 빌드 시, 유저에게 `component-catalog.pdf`를 보여주고 컴포넌트별 디자인 번호를 받는다.

## 진행 예시

### 1단계: 카탈로그 안내

```
인쇄소: component-catalog.pdf를 열어드렸습니다.
       각 컴포넌트마다 1번(클래식 블루)과 2번(컴팩트 모노) 디자인이 있습니다.
       컴포넌트별로 원하는 번호를 골라주세요.
       전체 1번으로 통일하셔도 됩니다.
```

### 2단계: 유저 선택

```
유저: 본문 1번, 제목 1번, 코드블록 2번, 인용 1번, 표 2번, 나머지는 1번
```

### 3단계: 변환 + 빌드

인쇄소가 유저의 한글 선택을 `--design` 인자로 변환한다.

```bash
python3 book/build_pdf_typst.py --design "body=1,heading=1,code=2,quote=1,table=2"
```

### 4단계: 저장

선택 결과를 `progress.json`에 저장한다. 이후 빌드에서 재사용.

```json
{
  "design": "body=1,heading=1,code=2,quote=1,table=2"
}
```

## 컴포넌트 이름 매핑

| 유저가 말하는 이름 | --design 키 | 카탈로그 페이지 |
|------------------|-------------|---------------|
| 본문 | body | p3 |
| 제목 | heading | p4 |
| 코드블록 | code | p5 |
| 인라인코드 | inline_code | p5 |
| 인용 | quote | p6 |
| 표 | table | p7 |
| 목차 | toc | p7 |

## 이미지 설정 (별도)

이미지 테두리와 레이아웃은 `--design`이 아니라 별도 설정으로 제어한다.

| 유저가 말하는 이름 | 설정 키 | 옵션 |
|------------------|--------|------|
| 이미지 테두리 | image_border_preset | plain / clean-border / shadow / primary-shadow / minimal |
| 이미지 레이아웃 | (함수 파라미터) | auto-image / side-image / dual-image |

```
유저: 이미지 테두리는 shadow로 해주세요
인쇄소: CONFIG["image_border_preset"] = "shadow" 적용
```

## 프리셋 단축 선택

전체를 한 번에 선택할 수도 있다.

```
유저: 전체 1번으로 해주세요
인쇄소: --design 1

유저: 전체 2번
인쇄소: --design 2
```
