# Superpowers 워크플로우 규칙

구현 작업 시 반드시 superpowers 스킬 워크플로우를 따른다.

## 필수 스킬 체인

| 단계 | 스킬 | 조건 |
|------|------|------|
| 1 | `superpowers:brainstorming` | 새 기능/변경 시작 전 |
| 2 | `superpowers:writing-plans` | 3개 이상 파일 수정 예상 시 |
| 3 | `superpowers:subagent-driven-development` | 플랜 실행 시 (서브에이전트 사용 가능 환경) |
| 4 | `superpowers:verification-before-completion` | 작업 완료 선언 전 |
| 5 | `superpowers:finishing-a-development-branch` | 브랜치 마무리 시 |

## 예외

- 단일 파일 수정, 오타 수정, 질문 답변 등 단순 작업은 스킬 없이 진행
- 디버깅 시 `superpowers:systematic-debugging` 사용
