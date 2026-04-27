# Beta Reader 리포트: CH04 — Kubernetes 시작하기 (v6)

## 프로젝트
- 대상 파일: `chapters-v2/04-Kubernetes-시작하기-v6.md`
- 분량: 480줄 / 4개 절 / 그림 4-1~4-20

## 페르소나 10명

| # | 이름 | 이야기 | 기술 | 실습 |
|---|------|:----:|:----:|:----:|
| 1 | 신입 백엔드 | 4 | **5** | 4 |
| 2 | 프론트엔드 | 4.5 | 4 | 4.5 |
| 3 | SI 개발자 | **5** | 4 | **5** |
| 4 | 데이터 엔지니어 | 4 | **5** | 4 |
| 5 | PM/기획자 | 4.5 | 4 | 4.5 (스킵 가능) |
| 6 | 비전공 전직자 | 4 | 4 | 2.5 |
| 7 | DevOps 주니어 | 4 | 4 | 4 |
| 8 | CS 학생 | 4 | 4 | 4 |
| 9 | CTO/시니어 | 4.5 | 3.5 | — |
| 10 | 게임 개발자 | 4.5 | 4 | 3.5 |

**평균**: 이야기 4.3/5 · 기술 4.15/5 · 실습 4.0/5

## 요약
- 통과: 10/10 (P9 조건부 — 비유 과부하/Control Plane 깊이/maxSurge 해석 보강 시 추천)
- 공통 지적: 5건 (3명 이상)
- 총평: **챕터 전체에서 가장 높은 점수. 오프닝 훅과 프랜차이즈 비유 일관성이 압도적**

## 공통 피드백 (3명 이상)

| 영역 | 피드백 | 언급 | 심각도 |
|------|--------|------|--------|
| Minikube 설치 전제 | Chocolatey 미설치자 탈출구 없음. Docker Desktop 필수, kubectl 별도 설치 여부, WSL2/Hyper-V 활성화 안내 부재 | 2, 3, 6 | **높음** |
| YAML 오타 | `spec: # pod에 대한 하는 상태 지정` 주석 오타 | 1, 8 | 중 |
| maxSurge 극단값 | `replicas:4, maxSurge:4, maxUnavailable:0`이 왜 이 숫자인지 해석 부족. 일시적 8 Pod 뜨는 의미 | 1, 5, 9 | **높음** (CTO) |
| selector.matchLabels 중복 | selector와 template.labels가 왜 같아야 하는지 그림만 있고 본문 한 번 더 짚어주지 않음 | 2, 6, 10 | 중 |
| Rollback 얕음 | `revisionHistoryLimit`, `rollout undo --to-revision` 부재. 두 줄로 끝나 허무 | 1, 9 | 중 |

## 강점 (다수 언급)

| 강점 | 언급 |
|------|------|
| "하나 죽으면 누가 살려?" 팀장 오프닝 훅 | 1, 2, 3, 4, 5, 7, 10 (7명) |
| 본사/가맹점 프랜차이즈 비유 일관성 (Ingress=안내데스크, Service=대표번호, Pod=주방) | 1, 2, 3, 5, 7, 10 |
| "Compose=지금 이대로 / K8s=이 상태 유지해라" 한 줄 정의 | 1, 4, 7 |
| Pod 직접 생성 → delete → 사라짐 → Deployment 자동 복구 Try/Fail | 1, 3, 6, 8, 10 |
| 4.4.6 Pod IP 문제 + 동료 메시지 "왜 자꾸 끊기지?" → CH05 훅 | 1, 3, 6, 7, 9, 10 |
| 컨트롤 플레인 참고박스로 분리, 본문 흐름 유지 | 1, 7, 10 |
| 선언형 vs 명령형 SQL SELECT 비유 | 2, 3, 4, 7, 8 |
| selector-labels 그림 4-12 | 3, 9 |

## 심각도별 이슈

### 높음
1. **Minikube 환경 전제 부족** (3명) — Chocolatey/Docker Desktop/WSL2/kubectl 설치 안내. P6(부트캠프) 첫 관문 탈락 위험
2. **maxSurge:4 극단값 해석** (3명, CTO 포함) — 일시적 8 Pod, 실무 기본값 25%/25% 주석 필요

### 중간
3. YAML 주석 오타 "pod에 대한 하는 상태 지정"
4. selector/matchLabels/template.labels 중복 구조 설명
5. Rollback `revisionHistoryLimit`, `--to-revision` 언급
6. `apiVersion: v1` vs `apps/v1` 차이 (P2)

### CTO 전용 지적 (P9)
7. **프랜차이즈 비유 과부하** — 4.1.2/4.1.3/4.1.4/4.2.1/4.3.1/4.4.1/4.4.6 거의 전 섹션에 반복. "페이지당 3개 이하" 규칙 경계
8. **Control Plane 깊이 과함** — etcd/Scheduler/CM/kubelet/kube-proxy 한 박스에 나열, 실습에 안 쓰임
9. **Minikube 한계 설명 얕음** — LoadBalancer/PodAntiAffinity/tunnel 등 실제 클러스터 차이. kind/k3d 대안 한 줄
10. **deploy-ex01.yml replicas:1** — ReplicaSet "개수 맞춤" 증명 약함. replicas:3으로 시작해 하나 지우면 2→3 복구가 더 효과적 (P9 제안)
11. **describe 출력 해석 가이드 부재** (P7 지적) — Events/ImagePullBackOff 같은 실패 메시지 어떻게 봐야 하는지

### 특정 페르소나
- P2: `apiVersion` 차이
- P4: Airflow Job/CronJob 한 줄 언급
- P6: YAML 들여쓰기 에러 시 대처
- P8: etcd Raft 합의, Pod Network = Linux namespace 키워드 한 줄
- P10: 게임 서버 stateful 세션 → StatefulSet 예고 한 줄

## 페르소나별 주요 반응

- **P1 신입 백엔드** (기술 5/5): "본사 지침서=Deployment 비유가 replicas/selector/template에 자연스럽게 달라붙음"
- **P3 SI 10년** (이야기 5, 실습 5): "WAS 수동 재기동 기억 직격. Rollback 두 줄 vs 배포 롤백 절차서 3장의 대비"
- **P4 데이터 엔지니어** (기술 5/5): "KubernetesExecutor 근거가 여기서 납득. Job/CronJob 한 줄 있으면 완성"
- **P5 PM** (스킵 4.5): "본사 비유 일관성 + 4.4.6 IP→동료 메시지 마무리로 Service 필요성 납득"
- **P9 CTO**: "조건부 추천. 입문용으론 훌륭하지만 실무 운영 맥락 몇 줄 필요"

## 수정 제안 (우선순위순)

| # | 위치 | 제안 | 심각도 |
|---|------|------|--------|
| 1 | 4.2.2 Minikube 설치 | Chocolatey/Homebrew 미설치자용 직접 다운로드 링크 + Docker Desktop 사전 실행 + kubectl 설치 여부(minikube 자동) 한 문단 | 높음 |
| 2 | 4.4.3~4.4.4 | `replicas:4, maxSurge:4, maxUnavailable:0`이 "100% 돌파 허용, 무중단 강제"이며 실무 기본 25%/25%라는 주석 | 높음 |
| 3 | 4.3.3 YAML | `spec: # pod에 대한 하는 상태 지정` 오타 수정 ("Pod의 원하는 상태 지정") | 중 |
| 4 | 4.4.2 | selector와 template.labels가 같아야 하는 이유 본문 한 줄 (그림 4-12 이전에) | 중 |
| 5 | 4.4.5 Rollback | `revisionHistoryLimit`, `rollout undo --to-revision <N>` 한 줄 추가 | 중 |
| 6 | 4.1.4 Control Plane 박스 | 참고박스 tone 다운 — "이름만 훑기" 분위기 강조 | 중 (CTO) |
| 7 | 4.2.1 | Minikube vs 실제 클러스터 차이 2~3줄(LoadBalancer/tunnel, kind/k3d 대안 한 줄) | 중 (CTO) |
| 8 | 4.4.4 describe 명령 뒤 | "Events 섹션에 ImagePullBackOff/CrashLoopBackOff 이런 메시지" 한 줄 | 중 (P7) |

## 결론
- **챕터 전체 중 가장 높은 점수** (4.15 평균)
- 오프닝 훅 + 프랜차이즈 비유 + Compose→K8s 대비 + 4.4.6 훅까지 서사 완성도 최고
- 환경 설정 안내와 실무 감각 두 축 보강 시 거의 완벽
- **P9 CTO 조건부 추천 → 수정 후 추천 확정 예상**
