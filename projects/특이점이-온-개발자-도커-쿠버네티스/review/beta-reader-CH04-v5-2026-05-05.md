# Beta Reader 리포트: CH04 — Kubernetes 시작하기 (v5)

**대상 파일**: `chapters/04-Kubernetes-시작하기-v5.md` (~1180줄, 닫기 단락 추가됨)
**검수 일자**: 2026-05-05
**라운드**: 적극 리라이트(v5) + 일괄 검수 후 첫 베타 리딩

## 페르소나 10명

| # | 이름 | 이야기 | 기술 | 실습 | 전체 |
|---|------|:----:|:----:|:----:|:----:|
| 1 | 신입 백엔드 | 4 | 3.5 | 3.5 | 3.5 |
| 2 | 클라우드 입문 엔지니어 | 4 | 3 | 4 | 3.5 |
| 3 | iOS 개발자 | 4 | 3 | 3 | 3.5 |
| 4 | ML 엔지니어 | 4 | 3 | 4 | 3.5 |
| 5 | PM/서비스 기획자 | 4 | 3.5 | 2.5 | 3.5 |
| 6 | 테크 PM | 4 | 4 | 4 | 4 |
| 7 | DevOps 시니어 | 4.5 | 4.3 | 4.6 | 4.5 |
| 8 | 풀스택 CTO | 4 | 3 | 3 | 3 |
| 9 | 부트캠프 수료생 | 4 | 3 | 3 | 3 |
| 10 | CS 학생 | 4 | 3 | 4 | 3.5 |

**평균**: 이야기 4.05 / 기술 3.33 / 실습 3.56 / 전체 3.55 (CH01~CH03 중 가장 높음)

## 요약
- 도입(팀장 세 질문) → 4.4 자동복구·스케일링·롤링업데이트·롤백 → 4.4.6 IP 흔들림 → CH05 다리, 큰 호 단단함
- 본사·가맹점 비유의 일관성·실습 흐름 광범위 호평
- **4.1.4 컨트롤 플레인 부서 폭격 + 4.4 캐릭터 부재 + maxSurge 4/0 기본값 오해**가 공통 지적

## 공통 피드백 (3명 이상 동일 의견)

| # | 피드백 | 페르소나 | 심각도 |
|---|--------|--------|:----:|
| 1 | **4.1.4 컨트롤 플레인 부서 6개 + 그림 4-3·4-4·4-5 중복감** | P1,P3,P5,P8,P9 | 높음 |
| 2 | **4.4 캐릭터 부재 (4.1.2 선배 이후 ~800줄간 0건)** | P1,P6,P8,P9 | 높음 |
| 3 | **그림 4-21 롤링 업데이트 결과 해석 부재 + maxUnavailable:0 ↔ 동시 Terminating 모순처럼 보임** | P1,P3,P7,P8,P10 | 높음 |
| 4 | **selector·matchLabels·template.metadata.labels 매칭 제약 명시 부족** | P3,P5,P7,P9 | 중간 |
| 5 | **maxSurge:4/maxUnavailable:0이 기본값처럼 보이는 위험** (실제 default 25%/25%) | P6,P7,P8 | 중간 |
| 6 | **ReplicaSet 정의 위치 어색** — 그림 4-14(4.4.2)에 등장하는데 정의는 4.4.3 | P1,P3,P6,P9 | 중간 |
| 7 | **4.1.3 핵심 리소스 표 6종이 일찍 나오는데 ConfigMap/Secret은 이번 챕터 안 나옴** + 챕터 매핑 한 줄 부재 | P1,P6,P8 | 중간 |
| 8 | **`:::prep` 블록 누락 + ex08~ex10 폴더 이동 안내 부재** | P3,P9 | 낮음 |
| 9 | **kubectl rollout history 출력 부재** (undo만 보여줌) | P1,P9 | 낮음 |
| 10 | **iptables/CNI 한 줄이 입문자에게 무거움** | P3,P9 | 낮음 |

## 단독 페르소나 핵심 지적

### P7 DevOps 시니어 (정확성 12건, 전체 4.5/5)
- **워커 노드 박스에 container runtime(containerd/runc) 누락** — kubelet이 직접이 아니라 CRI 통해 위임
- **maxSurge: 4 = replicas와 같은 극단값** — default 25%/25% 부연 한 줄 필요
- **kube-proxy iptables 모드 외 ipvs/nftables/eBPF 분화** — 입문서에선 OK이지만 "기본 모드는 iptables" 단서
- **그림 4-3에 API Server만 컨트롤 플레인 박스에 있어 부정확** — 4-5에서야 부서 4개. 캡션에 "단순화" 한 줄
- **Pod = "스케줄링 단위, 공유 네트워크/스토리지 단위"** — 입문서로는 OK
- **`set image` = 새 ReplicaSet 생성 + 기존 0으로 줄임** 메커니즘 본문에 없음
- **readinessProbe·Ready 상태와 무중단 핵심** — Ready 카운트로 종료가 무중단 핵심

### P8 풀스택 CTO (구조 결함, 3.0/5)
- **챕터 분량 1180줄·그림 22장·새 용어 ~15개 = 신입 첫 K8s 만남으로 과적**
- **4.1.3 표 6종과 4.1.3 끝 "Pod·Deployment만"의 모순** — 5장 도입으로 옮기는 안
- **4.4가 챕터의 42% (자동복구·스케일링·롤링·롤백·IP)** — 4.4·4.5·4.6 분리 또는 롤링/롤백을 다음 챕터로

### P10 CS 학생 (정식 용어 매핑 부재)
- **"Reconciliation Loop / Control Loop" 정식 용어 0회** — 비유는 정확한데 학술 다리 부재
- **etcd가 "기록실"로만 끝남** — Raft·분산 KV 한 줄 부재 (학생에게 가장 매력적인 부분)
- **사이드카 패턴 0회 언급** — Pod가 "하나 이상" 컨테이너인 동기 부재
- **imperative vs declarative 정식 용어 부재** (`kubectl run` vs `apply -f`)
- **service discovery 단어 0회** — 4.4.6 IP 흔들림 = service discovery 문제

### P3 iOS 개발자
- **SwiftUI = 선언형 가교 부재** — "원하는 상태 선언"과 SwiftUI의 선언형 매핑
- **Phased Release vs RollingUpdate 한 줄 부재** — 모바일 카나리 vs 일괄 교체

### P2 클라우드 입문
- **AWS ASG·EKS·CodeDeploy 매핑 0회** — `desired_capacity`와 K8s 본질이 같다는 한 줄 부재
- **EKS 매니지드 모델 한 줄 부재** — control plane = AWS / data plane = EC2 매핑

### P4 ML 엔지니어
- **GPU 자원 요청(`resources.requests`·`nvidia.com/gpu`) 0회**
- **Job/CronJob 표에 누락** — ML 워크로드의 절반은 단발성
- **사이드카 ML 활용(추론 + 모니터링) 부재**

### P6 테크 PM
- **팀장 세 질문 회수 부족** — 4.4.2/4.4.3/4.4.4 직후 "팀장 질문 N번 해결" 콜백 부재
- **4.1.3 표에 챕터 매핑 컬럼** — Service·Ingress→CH05, ConfigMap·Secret→CH06

## 페르소나별 핵심 한 줄

| # | 한 줄 |
|---|------|
| 1 신입 백엔드 | "도입·새벽 2시 강력. 4.1.4 etcd 너무 빨리 등장, ex09→ex10 strategy 점프 급함" |
| 2 클라우드 입문 | "ASG/EKS/CodeDeploy 매핑 0회. 비유는 EKS 모델 그대로인데 회수 안 됨" |
| 3 iOS | "SwiftUI 선언형·Phased Release 가교 부재. 4.1.4 부서 6개 폭격이 가장 큰 미끄러짐" |
| 4 ML | "GPU·Job/CronJob·`resources` 0회. 비유·실습은 우수" |
| 5 PM | "본사·가맹점 비유 PM 머리에 박힘. 따라갈 비율 60% (이야기 90% / YAML 30%)" |
| 6 테크 PM | "팀장 세 질문 회수가 명시되면 PM 시연 자료로 만점. 신입 OJT용 4점" |
| 7 DevOps 시니어 | "정확성·구조·서사 모두 상위권. container runtime 누락·maxSurge default 보강 권장" |
| 8 풀스택 CTO | "1180줄 + 22장 그림 = 과적. 챕터 분할 또는 4.1.4 5장으로 미루는 안" |
| 9 부트캠프 | "본사·가맹점 일관성 좋음. 4.1.4·4.4.4 strategy 두 곳에서 책 덮을 위험" |
| 10 CS | "비유 정확. 학술 용어(Reconciliation·etcd-Raft·namespace·service discovery) 다리 부재" |

## 심각도별 이슈

### 높음 (다수 페르소나 일치)
1. **4.1.4 분량/그림 압축** — 그림 4-3·4-4·4-5 중 하나로 압축, etcd/Scheduler/Controller Manager는 5장 또는 부록으로 미루기
2. **4.4 캐릭터 한 번 더 등장** — 롤링 업데이트 직전 또는 4.4.6 IP 발견 직후에 팀장/동료 한마디
3. **maxSurge 4/0 default 오해 방지** — ":::tip 기본값은 25%/25%, 본 예제는 무중단 강조 위해 4/0 극단" 박스
4. **그림 4-21 캡처 해석 한 줄** — "Pending 4 동시 = maxSurge 작동 / Terminating 4 동시 = 새 4 Ready 직후"

### 중간 (정확성·흐름)
5. **selector ↔ template.metadata.labels 매칭 제약** — "두 라벨이 같아야 매칭"·"selector immutable" 한 줄
6. **ReplicaSet 정의를 4.4.2 그림 4-14 등장 시점으로 끌어오기** — "Deployment가 내부적으로 만드는 ReplicaSet" 한 줄
7. **4.1.3 표에 "이번 챕터에서 다루는 것" 굵게 표시** + 챕터 매핑 (Service·Ingress→CH05 등)
8. **`:::prep` 블록 추가** — ex08~ex10 폴더 진입 안내
9. **kubectl rollout history 출력 캡처 추가** — undo 직전에 이력 보여주기
10. **iptables 한 줄을 비유로 부드럽게** — "패킷 길 안내. 5장에서 다룸"

### 낮음 (개선)
11. **container runtime(containerd) 워커 노드 박스에 추가** + "kubelet이 CRI 통해 위임" 한 줄
12. **CS 학생용 정식 용어 :::term-box** — Reconciliation Loop·imperative vs declarative·service discovery
13. **AWS/iOS/ML 페르소나 :::tip** — ASG·SwiftUI·GPU 한 줄씩
14. **팀장 세 질문 회수 콜백** — 4.4.2/4.4.3/4.4.4 직후
15. **`kubectl rollout status` 한 줄 추가** — set image와 -w 사이
16. **kubectl get pod -w 종료 안내** — Ctrl+C로 빠지기

## 수정 제안 (우선순위)

| # | 위치 | 제안 | 심각도 |
|---|------|------|:----:|
| 1 | 4.1.4 | 그림 4-4 삭제 또는 4-3·4-4 합치기 + etcd/Scheduler/Controller Manager는 ":::tip 자세한 내부 구조" 박스로 강등 | 높음 |
| 2 | 4.4.4 또는 4.4.6 | 팀장/동료 한마디 추가 (롤링 업데이트 직후 칭찬 / IP 발견 시 동료 등장) | 높음 |
| 3 | 4.4.4 strategy 코드블록 위 | ":::tip 기본값 25%/25%, 본 예제는 4/0 극단" 박스 | 높음 |
| 4 | 그림 4-21 위·아래 | "Pending 4 동시 = maxSurge 작동 / Terminating 4 동시 = 새 4 Ready 직후" 해석 1~2줄 | 높음 |
| 5 | 4.4.2 selector 코드블록 직후 | "selector.matchLabels와 template.metadata.labels는 같아야 매칭" 한 줄 + selector immutable 안내 | 중간 |
| 6 | 4.4.2 그림 4-14 직후 | ReplicaSet 한 줄 정의 (정식 정의는 4.4.3에서 확장) | 중간 |
| 7 | 4.1.3 표 직후 | 챕터 매핑 ("이번 챕터: Pod·Deployment / Service·Ingress: CH05 / ConfigMap·Secret: CH06") | 중간 |
| 8 | 4장 도입 | `:::prep` 블록 추가 — Minikube 사전 조건 + 폴더 안내 | 중간 |
| 9 | 4.4.5 rollout undo 직전 | rollout history 결과 캡처 추가 | 중간 |
| 10 | 4.1.4 끝 | iptables 한 줄을 "패킷 길 안내" 비유로 부드럽게 + container runtime 추가 한 줄 | 낮음 |
| 11 | 4.4.3 끝 | ":::tip Reconciliation Loop = closed-loop control" CS 학생용 매핑 | 낮음 |
| 12 | 본문 곳곳 | AWS ASG/EKS·SwiftUI 선언형·GPU 한 줄 :::tip | 낮음 |
| 13 | 4.4.2/4.4.3/4.4.4 직후 | "팀장 첫 번째 질문 해결" 콜백 한 줄 | 낮음 |

## 결론
CH04 v5는 베타리더 평균 3.55로 CH01~CH03 중 가장 높음 (DevOps 시니어 4.5, 테크 PM 4.0이 견인). 도입 호·실습 흐름·비유 일관성·다음 챕터 다리는 단단. 다음 라운드 핵심은 **4.1.4 부서 폭격 압축**, **4.4 캐릭터 한 번 더 등장**, **maxSurge default 오해 방지**, **그림 4-21 해석 보강** 네 가지가 가장 임팩트 큼.
