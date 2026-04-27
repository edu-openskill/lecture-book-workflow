# chapters v3/v4 개념도 검수 보고서

작성일: 2026-04-17
대상: v3/v4 6개 챕터 본문이 참조하는 **개념도(이론 설명 이미지)**
제외: 실제 실행 스크린샷(`docker ps`, `kubectl get`, vim 화면, 터미널 출력 등)
방식: Explore 에이전트 3개 병렬 디스패치. Read 멀티모달로 이미지 판독 + 본문 섹션 대조

---

## 1. 한 줄 총평

**대부분의 기술 다이어그램은 Docker/Kubernetes 공식 문서 기준으로 정확하고 비유와의 매핑도 우수**하다. 다만 **CH05-v3가 참조하는 개념도 7장이 실제 파일로 존재하지 않는 깨진 링크**가 가장 큰 이슈다.

---

## 2. 종합 판정

| 항목 | 판정 |
|------|------|
| 기술 정확성 (존재하는 개념도) | **A** |
| 본문-그림 매핑 | **A-** |
| 비유-기술 매핑 | **A** |
| **이미지 자산 완결성** | **C (7장 깨진 링크)** |
| 캡션 일치 | A- (1건 경미한 불일치) |
| **종합** | **B+** (깨진 링크 때문에 감점) |

검수 대상: 약 45장
- PASS: 약 35장 (78%)
- 경미 수정: 3장 (7%)
- **깨진 링크 (심각)**: 7장 (15%)

---

## 3. 가장 시급한 이슈 — CH05-v3 깨진 이미지 링크 (Critical)

### 3.1 문제

CH05-v3 본문이 참조하는 **7개 개념도가 `assets/CH05/` 폴더에 없음**. PDF 빌드 시 이미지 누락으로 렌더링 실패.

| 본문 라인 | 참조 파일 | 섹션 | 역할 |
|---------|---------|------|------|
| 05-v3:46 | `k8s-step3.png` | 5.1.1 Service 필요성 | Service 기본 개념 |
| 05-v3:108 | `label-selector-matching.png` | 5.1.3 Label-Selector | 매칭 메커니즘 |
| 05-v3:161 | `kube-proxy-dual-role.png` | 5.1.5 kube-proxy | NodePort/ClusterIP 처리 |
| 05-v3:180 | `endpoint-controller.png` | 5.1.5 Endpoint Controller | Pod IP 감시 → iptables 갱신 |
| 05-v3:263 | `l4-vs-l7.png` | 5.2.1 L4/L7 비교 | 계층별 역할 |
| 05-v3:298 | `k8s-step4c.png` | 5.2 Ingress | Ingress 구조 |
| 05-v3:321 | `full-traffic-flow.png` | 5.3.1 전체 흐름 | 브라우저→Pod 통합 |

### 3.2 원인 추정

CH05 v3 작성 시 writer 에이전트가 "이런 개념도가 있으면 좋겠다"는 판단으로 가상의 파일명을 본문에 넣었으나, 실제 이미지 제작은 아직 이뤄지지 않음. v2에서도 동일 구조였을 가능성.

### 3.3 영향도

- PDF 빌드 시 해당 페이지 렌더링 실패 또는 `![]()` 깨진 링크 표시
- CH05의 기술적 핵심(kube-proxy, Endpoint Controller, 전체 흐름)이 **시각 자료 없이 텍스트로만** 전달
- v3 흐름 검수에서 CH05를 A 등급으로 평가했던 근거(매핑 표, 다이어그램)가 일부 무효

### 3.4 권장 조치 (우선순위)

**최우선 (책 신뢰성에 직결)**
1. `kube-proxy-dual-role.png` — CH02.4.2 iptables DNAT 다이어그램을 K8s 규모로 확장한 그림 (ClusterIP 10.96.x → 실제 Pod IP 10.244.x DNAT 변환)
2. `endpoint-controller.png` — 순서도: (1) Pod IP 변화 → (2) Endpoint Controller 감지 → (3) Endpoints 리소스 갱신 → (4) kube-proxy가 iptables 규칙 자동 업데이트
3. `full-traffic-flow.png` — 브라우저 → Ingress(L7) → Service → kube-proxy(iptables) → Pod 5단계 통합 흐름

**차순위**
4. `label-selector-matching.png` — Service selector `app: web` ↔ Pod labels `app: web` 매칭 메커니즘
5. `l4-vs-l7.png` — 고속도로 분기점 vs 안내 데스크 비유 + 기술 대응표
6. `k8s-step3.png` — Service 기본 개념 (콜센터 대표 전화번호 시각화)
7. `k8s-step4c.png` — Ingress 리소스 vs Ingress Controller 구분

각각 `[GEMINI PROMPT]` 플레이스홀더로 본문에 먼저 마크업 → illustrator 에이전트 + Gemini/D2로 일괄 생성 권장.

---

## 4. 챕터별 개념도 검수 결과

### 4.1 CH01-v3 — 5장 검수 (1장 경미 수정)

| 이미지 | 판정 | 비고 |
|-------|------|------|
| chap01-1.png (수작업 하역) | PASS | 비유 성공 |
| chap01-2.png (컨테이너 크레인) | PASS | 효율성 대조 우수 |
| chap01-3.png (환경 불일치) | PASS | 개발자 공감 장면 |
| **chap01-4.png (소프트웨어 컨테이너)** | **경미 수정** | 컨테이너 박스 내부에 **"OS 기본 라이브러리" 요소 미표시**. 본문은 "라이브러리/설정/OS 파일까지"라고 4요소를 말하나 그림은 3개만 |
| chap01-roadmap.png | PASS | 학습 지도 명확 |

### 4.2 CH02-v3 — 15장 검수 (2장 경미 수정)

| 이미지 | 판정 | 비고 |
|-------|------|------|
| chap01-5/6/7 (주방 비유 3장) | PASS | chap01-7 "공용+개별 조리대"가 컨테이너 개념 최고 수준 비유 |
| **chap02-container.png** | **경미 수정** | "Host OS" 박스에 **"Kernel(공유)" 부분 명시적 표현 부족**. 좌측 라벨 가독성 개선 필요 |
| chap01-9.png (docker run 흐름) | PASS | 5단계 중 3단계로 단순화 적절 |
| chap01-13.png (이미지→컨테이너) | PASS | 붕어빵 틀 비유 시각화 탁월 |
| **fig-1-bp-0.png (Docker 전체 흐름)** | **경미 수정** | "내려받기/올리기/실행/저장" 4동작이 **화살표에 명확히 라벨되지 않음**. 순환 순서 모호 |
| ch2-step1-namespace1 / diagram/ch2-step1-namespace | PASS | 푸드코트 비유 + Namespace/veth/docker0 기술 다이어그램 모두 우수 |
| ch2-step2-dnat1 / diagram/ch2-step2-dnat | PASS | 키오스크 비유 + iptables DNAT 기술 매핑 정확 |
| ch2-step3-dns1 / diagram/ch2-step3-dns | PASS | 안내 지도 비유 + Docker DNS (127.0.0.11) 정확 |
| bind-mount.png / volume-mount.png | PASS | 두 마운트 방식 대조 명확 |

### 4.3 CH03-v4 — 약 12장 검수 (전부 PASS)

| 이미지 | 판정 | 비고 |
|-------|------|------|
| chap02-provisioning.png | PASS | 프로비저닝 비유 |
| upstream.png | PASS | NGINX upstream 개념 |
| ex01-lb-to-host.png | PASS | host.docker.internal 우회 |
| net-04-host-routing / net-05-docker-dns / net-06-compose-network | PASS | 네트워크 진화 3단계 |
| session-problem / session-redis | PASS | 문제-해결 대조 명확 |
| cache-miss / cache-hit | PASS | 캐싱 개념 |
| fig-1-v2.png | PASS | Docker 흐름 |

### 4.4 CH04-v3 — 약 15장 검수 (2장 경미 수정)

| 이미지 | 판정 | 비고 |
|-------|------|------|
| chap03-k8s-architecture.png | PASS | **K8s 전체 리소스 한 장 요약 — 우수** |
| chap04-node.png | PASS | 컨테이너 vs 노드 계층 차이 명확 |
| ch4-overview-1a-cluster / 1b-node / 3-layers | PASS | 기본 구조 |
| **ch4-overview-2-flow.png** | **경미 수정** | Endpoint Controller 역할이 점선으로만 표시되어 애매. **캡션에 "Service와 Pod를 자동 연결" 설명 추가** 권장 |
| fig-3-1 ~ fig-3-5 | PASS | Pod/Deployment/ReplicaSet/Scheduler 각 단계 정확 |
| k8s-step1 ~ k8s-step2 | PASS | 컨트롤 플레인 단계 |
| pod-creation.png | PASS (경미 개선 여지) | pause 컨테이너 역할이 "네트워크 네임스페이스"로만 표시. 캡션 보강 가능 |
| selector-labels.png | PASS | Label-Selector 매칭 **탁월한 시각화** |
| replicaset.png | PASS | 실선/회색/점선으로 상태 구분 — 우수 |
| net-07-pod-namespace.png | PASS | Pod Network Namespace |
| ch4-service-1-clusterip / 2-nodeport / 3-loadbalancer | PASS + **경미 수정(LoadBalancer)** | LoadBalancer는 **클라우드 전용이며 Minikube 미지원**이라는 주석 추가 권장 |

### 4.5 CH05-v3 — 깨진 링크 7장 + 기존 개념도 (CH05 폴더)

**CH05-v3 본문이 직접 참조하는 다이어그램 중 7장이 없음** (§3 참조). 이것이 이 검수 보고서의 최대 이슈.

기존 파일로 존재하는 개념도는 다음과 같이 CH06-v4에서 주로 사용됨:

| 이미지 (assets/CH05 폴더) | 현재 사용처 | 판정 |
|---------|-----------|------|
| fig-3-6.png | CH06-v4:206 (ConfigMap 재시작) | **캡션 애매** (§5 참조) |
| fig-3-7-v2.png | CH06-v4:469 (종합 아키텍처) | PASS — 4개 서비스 통합 구조 정확 |
| k8s-step4a / 4b | CH06-v4 ConfigMap / PV 섹션 | PASS |
| net-09-coredns.png | CH06-v4:262 | PASS — CoreDNS 쿼리 흐름 |
| net-10a-full-path / net-10b-full-path | CH06-v4:966~970 | PASS — Ingress/Service/kube-proxy 흐름 분리 표현 |
| k8s-namespace.png | CH06-v4:568 | PASS — 다중 네임스페이스 |
| 13_secret-env.png | CH06-v4:164 | PASS — Secret 환경변수 주입 |
| 42_volume-pod-preserved.png | CH06-v4:425 | PASS — PV 데이터 보존 증명 |

### 4.6 CH06-v4 — 별도 개념도 없음 (assets/CH05 참조)

CH06-v4는 자체 이미지를 가지지 않고 assets/CH05 폴더 이미지를 참조. 위 4.5 참조.

---

## 5. 기술 정확성 특별 검증

### 5.1 kube-proxy / Endpoint Controller (CH05.1.5 — v3 최대 개선 구간)

**본문(CH05-v3:130~185)의 기술적 정확도**: **매우 높음**

| 항목 | 본문 설명 | Kubernetes 공식 기준 | 판정 |
|------|---------|-----------------|------|
| ClusterIP | "어느 장비에도 할당되지 않은 가상 IP" | 정확 | ✓ |
| iptables DNAT | "목적지 IP를 실제 Pod IP로 바꿔치기" | 정확 (kube-proxy의 기본 모드) | ✓ |
| Endpoint | "Service 뒤의 실제 Pod IP 목록" | 정확 | ✓ |
| Endpoint Controller | "Pod IP 변화 감시 → Endpoints 리소스 갱신" | 정확 | ✓ |
| 3단계 흐름 | Service 선언 → Endpoint Controller → kube-proxy | 정확 | ✓ |

**단, 이 구간의 시각 자료 2장(`kube-proxy-dual-role.png`, `endpoint-controller.png`)이 누락**되어 있어 독자가 글로만 이해해야 함. §3 권장 조치가 시급.

### 5.2 기타 기술 다이어그램 샘플 검증

- **diagram/ch2-step2-dnat.png** (Docker iptables DNAT) — ✓ 정확
- **diagram/ch2-step3-dns.png** (Docker DNS 127.0.0.11) — ✓ 정확 (Docker 기본 DNS 주소)
- **chap03-k8s-architecture.png** (K8s 전체 리소스) — ✓ 공식 구조와 일치
- **fig-3-3.png** (컨트롤 플레인 내부) — ✓ API Server/etcd/Controller Manager/Scheduler 관계 정확
- **selector-labels.png** — ✓ Label-Selector 매칭 메커니즘 정확

---

## 6. 캡션 불일치 (1건)

### 6.1 fig-3-6.png — CH06-v4:206

**본문 캡션 (현재)**:
> "ConfigMap을 수정한 뒤에는 Pod를 재시작해야 값이 환경 변수로 반영됩니다."

**실제 이미지 내용**: ConfigMap → Pod, Secret → Pod의 **초기 주입 흐름** (일방향 화살표, "일반 설정 주입" / "비밀 설정 주입" 라벨)

**문제**: 캡션은 "변경 → 재시작 → 반영" 프로세스를 암시하지만, 이미지는 최초 주입 순간만 표현. 불일치는 크진 않지만 혼동 가능.

**권장**: 캡션을 "**ConfigMap과 Secret이 환경 변수로 주입되는 경로. 값이 바뀐 뒤에는 Pod를 재시작해야 반영됩니다.**"처럼 두 의미를 합치거나, 별도 재시작 흐름 이미지 생성.

---

## 7. 긍정 평가 (유지할 우수 그림 10선)

1. **chap01-7.png** — 주방 공유+개별 조리대가 컨테이너 개념의 최고 수준 비유
2. **chap01-13.png** — 붕어빵 틀 비유로 이미지→컨테이너 정확 시각화
3. **diagram/ch2-step1-namespace.png** — Namespace/veth/docker0 기술적 정확
4. **diagram/ch2-step2-dnat.png** — iptables DNAT 흐름 명확
5. **session-problem.png + session-redis.png** — 문제/해결 대조 최고
6. **chap03-k8s-architecture.png** — K8s 전체 한 장 요약 **책의 백미**
7. **fig-3-1.png** — 클러스터 계층 구조 가장 상세하고 정확
8. **selector-labels.png** — Label-Selector 매칭 매우 직관적
9. **replicaset.png** — 상태 표현(실선/회색/점선)으로 복구 메커니즘 시각화
10. **fig-3-7-v2.png** — 종합 아키텍처 4계층 + 서비스 간 통신 경로 명확

---

## 8. 권장 조치 (우선순위)

### Tier A (책 신뢰성 필수, 즉시)

1. **CH05-v3 깨진 이미지 7장 생성** (§3.4 목록)
   - 최우선: `kube-proxy-dual-role.png`, `endpoint-controller.png`, `full-traffic-flow.png`
   - 방식: `[GEMINI PROMPT]` 플레이스홀더로 본문 수정 → illustrator 에이전트로 Gemini/D2 일괄 생성

### Tier B (개선 권장)

2. **chap01-4.png** 컨테이너 박스에 OS 파일시스템 요소 추가
3. **chap02-container.png** "Host OS" 내 "Kernel(공유)" 명시
4. **fig-1-bp-0.png** 화살표에 "내려받기/올리기/실행/저장" 라벨
5. **ch4-overview-2-flow.png** 캡션에 "Endpoint Controller가 Service와 Pod 자동 연결" 보강
6. **ch4-service-3-loadbalancer.png** 캡션에 "클라우드 전용, Minikube 미지원" 주석
7. **fig-3-6.png** (CH06.1.4) 캡션 재작성

### Tier C (선택 개선)

8. **pod-creation.png** 캡션에 pause 컨테이너 역할 보강
9. **k8s-namespace.png** 다중 네임스페이스 간 통신(FQDN) 예시 추가

---

## 9. 최종 결론

**현 상태**: 기존 개념도는 양호. 하지만 **CH05-v3 깨진 링크 7장이 최우선 해결 과제**.

**조치 후 예상 등급**: 
- Tier A 완료 → **A**
- Tier A + Tier B 완료 → **A+**

**출판 준비도**: Tier A 없이는 PDF 빌드 시 문제 발생. **Tier A는 필수**.

### 9.1 다음 단계 제안

깨진 이미지 7장을 GEMINI PROMPT로 먼저 본문에 마크업하고, 이후 illustrator 에이전트로 일괄 생성 작업이 합리적. Tier B/C는 여유 있을 때 일괄 정리.

---

## 10. 부록

### 10.1 실제 검수한 이미지 목록

- CH01: 5장 (전부 개념도)
- CH02: 15장 (비유 + 기술 다이어그램)
- CH03: 12장 (NGINX, Redis, Compose 아키텍처)
- CH04: 15장 (K8s 구조, Service 3타입, Pod/Deployment)
- CH05 참조 존재 파일: 8장 (fig-3-6, fig-3-7-v2, net-09/10a/10b, k8s-step4a/4b/4c, k8s-namespace 등)
- CH05 참조 누락: **7장** (§3 목록)
- CH06: 자체 이미지 없음, assets/CH05 참조

**총 분석 대상**: 약 55장
**판정**: PASS 약 43장 / 경미 수정 약 5장 / **깨진 링크 7장**

### 10.2 분석 방법

- Explore 에이전트 3개 병렬 디스패치 (A: CH01-02, B: CH03-04, C: CH05-06)
- 각 에이전트가 Read 멀티모달로 이미지 직접 판독
- 6가지 체크리스트 (라벨/구성/방향/비유/오해/캡션)로 본문과 대조
- 크로스 체크: 에이전트 C 판정이 가상의 파일명 기반이었으므로, 메인 세션에서 Grep으로 실제 참조 여부 재검증 → 7장 깨진 링크 확정
