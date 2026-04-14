# Comparisons

> 비교형 시각 요소. "A vs B", "before / after", "취소선으로 오류 표시" 같은 **대조**가 핵심인 컴포넌트.

## 속함

- `.annotated-compare` + `.ac-*` (LLM 환각 vs 사내규정, CH01)
- `.overlap-text-demo` + `.otd-*` (청크 오버랩 시각화, CH03)
- `.reindex-compare` + `.rc-arrow`, `.rc-badge-full`, `.rc-badge-inc` (전체 vs 증분 재인덱싱, CH03)
- `.cache-diff` (캐시 전후 시간선, CH07)
- `.dual-image` + `figure`/`figcaption` (2분할 이미지, CH04)

## 속하지 않음

- 순차 흐름 타임라인(`.rc-timeline`) → [`../pipelines/`](../pipelines/) — 같은 `rc-*` 접두어지만 별도
- 청크 단위 카드 → [`../cards/`](../cards/)

## 주의

`rc-*` 접두어는 이 카테고리(CH03 reindex-compare)와 pipelines 카테고리(CH07 rc-timeline) **두 곳에서 사용** 중이다. 신규 `rc-*` 클래스 추가 금지.

## 컴포넌트 목록

_Task 6에서 작성됨._
