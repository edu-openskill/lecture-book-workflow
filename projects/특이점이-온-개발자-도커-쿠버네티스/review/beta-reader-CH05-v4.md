# Beta Reader 리포트: CH05 — Kubernetes 네트워킹 (v4)

## 프로젝트
- 책: 특이점이 온 개발자 — 도커·쿠버네티스
- 대상 파일: `chapters/05-Kubernetes-네트워킹.md` (515 라인)
- 독자 상수: 입사 3~6개월차 주니어
- 평가 일자: 2026-04-27

## 페르소나 목록

| # | 이름 | 이야기 | 기술 | 실습 | 통과 |
|---|------|:----:|:----:|:----:|:----:|
| 1 | 신입 백엔드 | 4 | 3 | 4 | O |
| 2 | 데이터 엔지니어 | 4 | 5 | 3 | O |
| 3 | 프론트엔드 | 4 | 5 | 3 | O |
| 4 | SI 개발자 | 4 | 3.5 | 3 | O (조건부) |
| 5 | PM/기획자 | 4 | 3 | 3.5 | O (조건부) |
| 6 | 비전공 전직자 | 4 | 3 | 3 | O |
| 7 | DevOps 엔지니어 | 4 | 2 | 3 | **X (운영 부정확성)** |
| 8 | 임베디드 개발자 | 4 | 3 | 4 | O |
| 9 | CS 학생 | 4 | 2 | 4 | O (조건부) |
| 10 | CTO/리드 | 5 | 4 | 3 | O (MOCK 차단) |

**평균**: 이야기 4.1/5 · 기술 3.4/5 · 실습 3.3/5
**통과**: 9/10 (조건부 3명, 비통과 1명)

## 요약

- **최대 강점**: §5.3 "요청의 여정" 다섯 단계 + Docker→K8s 대응표(§5.3.3) — 거의 전 페르소나 백미로 호평
- **최대 약점**:
  1. **MOCK 캡처 3장 차단 이슈** (그림 5-14, 5-16, 5-17) — 4명 지적
  2. **ClusterIP 가상 IP 정의 모호** — 임베디드·CS 학생 두 페르소나 정밀도 지적
  3. **DevOps 시각의 운영 부정확성** — iptables/IPVS 모드, EndpointSlice, ingress-nginx 경로 등 5종 함정
- 콜센터 직통 전화번호·프랜차이즈 공식 앱·톨게이트 vs 안내데스크 비유 — 입문~PM 페르소나 전원 강한 호평
- §5.3.3 대응표가 CH02·CH03 회수 효과 — CTO·데이터·프론트·임베디드·SI 모두 호평

## 공통 피드백 (3명 이상 동일 의견)

| 영역 | 피드백 | 언급 페르소나 | 심각도 |
|------|--------|-------------|--------|
| MOCK 캡처 3장 | 그림 5-14·5-16·5-17이 mock 상태. 출간 전 반드시 실측 교체 | 2, 3, 4, 10 | **높음 (차단)** |
| 5.3.2 kube-proxy 1차/2차 명료성 | 같은 프로그램이 두 노드에서 도는지 모호 | 1, 2 | 중간 |
| 포트 3종 흐름 다이어그램 부재 | nodePort/port/targetPort 표만 있고 패킷 흐름 그림 없음 | 1, 6 | 중간 |
| ClusterIP 가상 IP 명시 부재 | "어느 인터페이스에도 바인딩되지 않은 가상 IP" 한 줄 누락. ping 안 되는 이유 못 풀림 | 8, 9 | 중간 |
| L4/L7 박스 위치 | 5.3.2 표 *뒤*에 정의 박스가 있어 역순. 표 *앞*으로 이동 또는 본문 승격 | 6, 9 | 중간 |

## 강점 (다수 또는 전원 언급)

- 도입부 "IP 외워 두고 쓰려는 거 아니지?" 팀장 트리거 — **9명 호평**
- 직통 전화번호(Service) + 공식 앱(Ingress) 비유 — **전 페르소나 호평**
- 톨게이트(L4) vs 안내데스크(L7) 비유 — 입문~숙련 매핑 우수
- §5.3.1 "이름→ClusterIP→Pod IP, 두 단계 변환" — 프론트 강한 호평 (axios fetch 멘탈 모델 보강)
- §5.3.3 Docker→K8s 대응표 — CTO 즉시 인용 가능, CH02·CH03 완벽 회수
- L4/L7 참고 박스의 "봉투 겉면 vs 안쪽" 비유 — 비유 자체는 우수 (위치만 조정 필요)

## 심각도별 이슈

### 높음 (차단)

1. **MOCK 캡처 3장 — 4명 지적, 출간 차단 이슈**
   - 위치: 그림 5-14, 5-16, 5-17 (§5.2.3 Ingress 실습)
   - 증상: `mock-ingress-get.png`, `mock-order-page.png`, `mock-stores-page.png` 3장이 모두 mock
   - 영향: 독자가 실습 후 "내 결과가 책과 같은가?" 검증 불가 — 신뢰도 직접 타격
   - 제안: **출간 전 반드시 실측 교체** (또는 캡션에 "예시 화면" 명시 + 실제 캡처 추가)

### 중간

2. **ClusterIP 가상성 정의 모호 — 2명 (숙련)**
   - 위치: §5.3.1 L391~L393 "가상 주소(ClusterIP)" 첫 등장
   - 증상: "어느 인터페이스에도 바인딩되지 않은 iptables 규칙으로만 존재하는 가상 IP" 핵심 누락
   - 영향: "왜 ping이 안 되는데 통신은 되지?" 의문 영구 미해결
   - 제안: §5.3.1 첫 의문 끝에 `:::term-box` 추가 — ClusterIP·Endpoints·DNAT 3개 정식 정의 + `iptables -t nat -L KUBE-SERVICES -n` 출력 한 컷

3. **L4/L7 박스 위치 — 2명**
   - 위치: §5.3.2 다섯 단계 표 *뒤*
   - 증상: 톨게이트/안내데스크 비유는 본문에 먼저 등장, 정의 박스는 표 후
   - 제안: **L4/L7 정의 박스를 §5.3.2 표 직전으로 이동** 또는 본문 승격(2~3문장으로 녹임)

4. **kube-proxy 1차/2차 명료성 — 2명**
   - 위치: §5.3.2 4단계 "kube-proxy(2차)"
   - 제안: "같은 kube-proxy 프로그램이 모든 노드에 떠 있어 들어가는 노드와 나가는 노드 양쪽에서 두 번 일합니다" 1줄

5. **포트 3종 흐름 다이어그램 부재 — 2명**
   - 위치: §5.1.3 표 직전
   - 제안: `[브라우저]→nodePort 30080→[Service]port 80→[Pod]targetPort 80` HTML inline 1줄 도식

6. **NodePort 운영 적합성 (SI 특유)**
   - 위치: §5.1.3 끝
   - 제안: "온프레는 외장 L4 + NodePort(VIP→nodePort:30080)" 패턴 + MetalLB 한 줄 박스. SI 90% 안도

7. **sessionAffinity·Readiness Probe 연결 (SI 특유)**
   - 위치: §5.1.4 또는 §5.3.1 Endpoint Controller
   - 제안: "JSESSIONID 쓰던 분은 `sessionAffinity: ClientIP` 옵션" 1단락 + "살아있다 = Readiness Probe 통과한 Pod만 Endpoint에 들어감" 1줄

8. **kube-proxy iptables 모드·IPVS/eBPF (DevOps 특유)**
   - 위치: §5.3.1
   - 제안: 참고박스 "kube-proxy 모드: iptables(소규모, O(n) 룰 체인) / IPVS(대규모 표준) / eBPF(Cilium)" 한 줄 비교

9. **EndpointSlice 누락 (DevOps 특유)**
   - 위치: §5.3.1 Endpoint Controller
   - 제안: "K8s 1.21+ 기본은 EndpointSlice. 구 Endpoints는 deprecated" 1줄

10. **§5.3.2 4단계 ingress-nginx 부정확 (DevOps 특유)**
    - 위치: §5.3.2 4단계
    - 제안: "Controller에 따라 ClusterIP 경유(일반) 또는 Pod IP 직결(ingress-nginx)" 분기 서술

11. **Ingress Controller 운영 함정 (DevOps 특유)**
    - 위치: §5.2.3 끝
    - 제안: 운영 함정 박스 — TLS Secret 연결, Annotation 의존성, Controller별 CRD 차이 3줄

12. **Pod 네트워크(CNI) 매핑 — 1명 (데이터)**
    - 위치: §5.1.1 또는 §5.3.1
    - 제안: "CH02 docker0가 같은 호스트, K8s는 노드 넘나드는 Pod 통신을 CNI 플러그인이 담당" 1단락

13. **응답 경로 conntrack — 1명 (임베디드)**
    - 위치: §5.3.2 5단계 다음
    - 제안: "conntrack이 NAT 매핑을 기억해 응답이 자동 역변환" 1단락

### 낮음

14. **CS 학생 정밀도 (P9)**
    - L483 "ClusterIP가 적힌 짐을 Pod IP로 다시 붙여서" → "DNAT(Destination NAT)" 명시
    - L498 비교표 캡션에 "iptables DNAT 메커니즘 동일성" 추가
    - L413 DNS 설명에 "Pod CIDR ≠ Service CIDR" 한 줄

15. **selector CH04 회수 — 1명 (비전공)**
    - 위치: §5.1.2 코드블록 위
    - 제안: "CH04에서 Deployment가 라벨로 Pod를 묶었듯, Service도 같은 라벨 매칭" 1줄

16. **5.3 도입 Try/Fail 한 컷 — 1명 (프론트)**
    - 제안: "오픈이가 흐름도를 그려보다 화살표 하나에서 펜이 멈췄다" 같은 막힘 장면 1컷

17. **axios.baseURL/CORS 연결 — 1명 (프론트)**
    - 위치: §5.2.2 "공식 앱" 비유 직후
    - 제안: "프론트 입장에선 도메인 하나에 `/api/order`, `/api/stores` 동시 호출, CORS 단순화" 1줄

18. **Mock 캡처에 host 필드 부재 — 1명 (CTO)**
    - 위치: §5.2.3 Ingress 규칙
    - 제안: `host: shop.local` + `/etc/hosts` 1줄 추가, TLS 한 줄 보강

19. **5.1.3 6개 개념 분할 — 1명 (PM)**
    - 위치: §5.1.3
    - 제안: 타입 3종 본문 → 포트 3종은 별도 박스로 분리

20. **5.3 도입 난이도 안내 — 1명 (PM)**
    - 위치: §5.3 시작
    - 제안: "이 절은 운영자·개발자가 장애 대응 시 참고. 비개발자는 톨게이트·안내데스크 비유만 읽어도 OK" 우회로

21. **`kubectl get endpoints` 시각화 — 1명 (CTO)**
    - 위치: §5.1.4 Pod 삭제 실험 직후
    - 제안: `kubectl get endpoints nginx-service` 1줄로 §5.3.1 미리 시각화

22. **이것만은 기억하자 강화 — 1명 (CTO)**
    - 제안: "kube-proxy iptables = Docker iptables DNAT의 진화형" 명시

## 페르소나별 상세 (요약)

### 1. 신입 백엔드 — 4/3/4
직통 전화 비유 5.1까지 막힘 없음. §5.3 kube-proxy/iptables/DNAT가 한꺼번에 등장하면서 막힘. Spring 인터셉터 비유와 selector CH04 회수 1줄 권장.

### 2. 데이터 엔지니어 — 4/5/3
§5.3.1 Endpoint+kube-proxy+DNS 삼각 구도 압권 (Airflow Scheduler/Executor/Worker 동형). MOCK 캡처 + Pod 네트워크(CNI) 한 단락 + minikube tunnel vs --url 차이 보강.

### 3. 프론트엔드 — 4/5/3
"이름→ClusterIP→Pod IP" 두 단계 변환이 axios fetch 멘탈 모델 보강. MOCK 캡처 + axios.baseURL/CORS 연결 + Try/Fail 한 컷 + replicas 수치 명기.

### 4. SI 개발자 — 4/3.5/3 (조건부)
L4/L7 톨게이트/안내데스크 매핑 탁월. **운영 적합성 4종 누락** (NodePort+L4 패턴, sessionAffinity, Readiness Probe, MOCK).

### 5. PM/기획자 — 4/3/3.5 (조건부)
콜센터·공식 앱 비유 효과적. §5.1.3 "타입 3 + 포트 3" 6개 개념 한 절은 부담. §5.3 난이도 안내·iptables/DNAT 박스 격리.

### 6. 비전공 전직자 — 4/3/3
직통 전화 비유와 §5.3 셋의 협력 결론은 머리에 박힘. NodePort 30080 패킷 흐름 다이어그램 + selector CH04 회수 + L4/L7 본문 승격 필요.

### 7. DevOps 엔지니어 — 4/2/3 — **비통과**
"Minikube에서만 맞는 책" 평가. iptables 모드·IPVS/eBPF·EndpointSlice·Ingress Controller TLS·§5.3.2 ingress-nginx 부정확 5종이 결정타.

### 8. 임베디드 개발자 — 4/3/4
L4/L7 구분 늦음 + ClusterIP 가상성 + iptables -t nat 출력 예시 + conntrack 응답 경로 보강 필요. OSI는 임베디드 모국어.

### 9. CS 학생 — 4/2/4 (조건부)
정의 정밀도 5종 누락 — L4/L7 위치 오류, NAT/DNAT 매핑, ClusterIP 가상성, Endpoints 오브젝트, IP 대역 분리.

### 10. CTO/리드 — 5/4/3
§5.3 다섯 단계 + §5.3.3 대응표 팀 온보딩 자료로 즉시 인용 가능. **MOCK 캡처 3건은 차단 이슈**. 분량 515라인 적정.

## 수정 제안 (우선순위순)

| # | 위치 | 제안 | 심각도 | 관련 페르소나 |
|---|------|------|--------|-------------|
| 1 | 그림 5-14·5-16·5-17 | MOCK 캡처 3건 실측 교체 (출간 전 차단 이슈) | **높음** | 2, 3, 4, 10 |
| 2 | §5.3.1 첫 의문 끝 | term-box: ClusterIP(가상 IP, iptables 규칙으로만)·Endpoints·DNAT 3개 정식 정의 + `iptables -t nat -L KUBE-SERVICES` 출력 한 컷 | **높음** | 8, 9 |
| 3 | §5.3.2 다섯 단계 표 *직전* | L4/L7 정의 박스 이동 또는 본문 승격 | 중간 | 6, 9 |
| 4 | §5.3.2 4단계 | "같은 kube-proxy가 두 노드에서 두 번 일함" 1줄 명시 | 중간 | 1, 2 |
| 5 | §5.1.3 표 직전 | 포트 3종 흐름 다이어그램 (nodePort→port→targetPort) | 중간 | 1, 6 |
| 6 | §5.1.3 끝 | 온프레 NodePort+L4(MetalLB) 패턴 박스 | 중간 | 4 |
| 7 | §5.1.4 또는 §5.3.1 | sessionAffinity 1단락 + Readiness Probe 1줄 | 중간 | 4 |
| 8 | §5.3.1 참고박스 | kube-proxy 모드 (iptables/IPVS/eBPF) 1줄 비교 | 중간 | 7 |
| 9 | §5.3.1 Endpoint Controller | EndpointSlice (K8s 1.21+) 1줄 | 중간 | 7 |
| 10 | §5.3.2 4단계 | "Controller에 따라 ClusterIP 경유 또는 Pod IP 직결(ingress-nginx)" 분기 서술 | 중간 | 7 |
| 11 | §5.2.3 끝 | Ingress 운영 함정 박스 (TLS·Annotation·CRD 차이) | 중간 | 7 |
| 12 | §5.1.1 또는 §5.3.1 | Pod 네트워크(CNI) 한 단락 — CH02 docker0 → 노드 간 CNI | 중간 | 2 |
| 13 | §5.3.2 5단계 다음 | 응답 경로 conntrack 1단락 | 중간 | 8 |
| 14 | §5.1.2 코드블록 위 | "CH04 selector와 동일" 회수 1줄 | 낮음 | 6 |
| 15 | §5.3 도입 | Try/Fail 한 컷 (펜이 멈춤) | 낮음 | 3 |
| 16 | §5.2.2 "공식 앱" 비유 직후 | axios.baseURL/CORS 단순화 1줄 | 낮음 | 3 |
| 17 | §5.2.3 Ingress 규칙 | `host: shop.local` + `/etc/hosts` 1줄, TLS 1줄 | 낮음 | 10 |
| 18 | §5.1.3 | 타입 3종/포트 3종 분할 | 낮음 | 5 |
| 19 | §5.3 시작 | 비개발자 우회로 안내 1줄 | 낮음 | 5 |
| 20 | §5.1.4 Pod 삭제 직후 | `kubectl get endpoints nginx-service` 미리 시각화 | 낮음 | 10 |
| 21 | "이것만은 기억하자" | "kube-proxy iptables = Docker DNAT 진화형" 명시 | 낮음 | 10 |
| 22 | L498 비교표 | "iptables DNAT 메커니즘 동일성" 캡션 | 낮음 | 9 |

## 결론

- §5.3 다섯 단계와 §5.3.3 대응표는 책 전체 백미. CTO 추천 수준. 입문~PM 비유 매핑 강력
- v4 결정타 3개:
  1. **MOCK 캡처 3건 실측 교체 (출간 차단)**
  2. **ClusterIP 가상 IP + iptables DNAT term-box** (숙련 페르소나 정밀도)
  3. **L4/L7 박스 위치 정정** (역순 → 정순)
- DevOps 운영 정확성 5종은 본문 흐름 유지하되 참고박스 한 줄씩 추가. 추가 시 4년차 신뢰도 회복
- 통과율 9/10 — 운영 정밀도 보강 시 10/10 가능
