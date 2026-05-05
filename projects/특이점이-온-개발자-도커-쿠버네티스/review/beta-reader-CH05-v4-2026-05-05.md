# Beta Reader 리포트: CH05 — Kubernetes 네트워킹 (v4)

**대상 파일**: `chapters/05-Kubernetes-네트워킹-v4.md` (1215줄, :::note 박스 가독성 수정 후)
**검수 일자**: 2026-05-05
**라운드**: 적극 리라이트(v4) + 일괄 검수 후 첫 베타 리딩

## 페르소나 10명

| # | 이름 | 이야기 | 기술 | 실습 | 전체 |
|---|------|:----:|:----:|:----:|:----:|
| 1 | 신입 백엔드 | 4 | 4 | 3.5 | 4 |
| 2 | 클라우드 입문 엔지니어 | 4 | 3 | 3.5 | 3.5 |
| 3 | iOS 개발자 | 4 | 3 | 4 | 3.5 |
| 4 | ML 엔지니어 | 4 | 4 | 3 | 4 |
| 5 | PM/서비스 기획자 | 4 | 4 | 3 | 3.5 |
| 6 | 테크 PM | 4 | 5 | 4 | 4.5 |
| 7 | DevOps 시니어 | 4 | 3 | 3.5 | 3.5 |
| 8 | 풀스택 CTO | 4 | 3.5 | 3 | 3.5 |
| 9 | 부트캠프 수료생 | 4.5 | 3.5 | 3 | 3.7 |
| 10 | CS 학생 | 4.5 | 3.5 | 4 | 4 |

**평균**: 이야기 4.1 / 기술 3.65 / 실습 3.45 / 전체 **3.77** (CH01~CH04 중 최고)

## 요약
- 도입(동료 "어떻게 들어가요?") + 콜센터 비유 일관성 + Pod 삭제 후 재접속 검증 실험은 광범위하게 호평
- 5.3 "브라우저에서 Pod까지" 3단계 분해는 칭찬·우려 양극화 — 깊이는 좋으나 분량(~450줄)·시나리오 섞임·캐릭터 부재
- ingress-nginx 실제 동작과 본문 비유 모순이 시니어 그룹 가장 큰 정확성 결함

## 공통 피드백 (3명 이상 동일 의견)

| # | 피드백 | 페르소나 | 심각도 |
|---|--------|--------|:----:|
| 1 | **비유 위계 균열** — 5.1 "집/방문/정문" → 5.2·5.3 "콜센터/부서". 같은 "대표번호"가 5.1=Service, 5.2=Ingress | P3,P5,P6,P8 | 높음 |
| 2 | **5.3 시나리오 ex11/ex12 섞임** — 그림 5-19/5-21에 "30080" 박혀 있는데 ex12 흐름은 LoadBalancer 80 | P7,P9 | 높음 |
| 3 | **ingress-nginx 비유와 실제 동작 모순** — DNS 조회 비유 → :::note에서 "사실 API Server watch" 정정. 비유와 그림이 부정확 모델 강화 | P5,P6,P7,P9 | 높음 |
| 4 | **kube-proxy "1차/2차" 명명** — 같은 컴포넌트의 두 규칙인데 두 개로 오해 위험. 5.3 도입에 예고 한 줄 부재 | P1,P7,P8,P9 | 중간 |
| 5 | **minikube tunnel 함정 안내 부족** — Windows UAC / 80 포트 충돌 / 터미널 살려두기 / 별도 터미널 강조 | P5,P8,P9 | 중간 |
| 6 | **5.3 분량 + 비유/IT 다이어그램 쌍 6개 반복** — 부트캠프·iOS·PM 후반 책 덮을 위험 | P3,P5,P9 | 중간 |
| 7 | **ingressClassName: nginx 의미 부족** — 어디서 왔는지, 여러 컨트롤러 공존 가능성 | P4,P7,P9 | 중간 |
| 8 | **그림 5-19 L7 색대 영역에 ClusterIP Service까지 포함됨** — Service는 L4인데 L7 박스 안 | P7,P10 | 중간 |
| 9 | **그림 5-16 출력 `frontend-ingress` ↔ 실제 ex12-ingress 이름 불일치** | P1,P8 | 낮음 |
| 10 | **NodePort 30080 vs minikube service --url 임의 포트** 의문 한 줄 부재 | P7,P9 | 낮음 |

## 단독 페르소나 핵심 지적

### P7 DevOps 시니어 (정확성 12건, 3.5/5)
- **그림 5-5 LoadBalancer SVG에 "kube-proxy (NodePort)" 라벨 → 본문 설명 부재** (LoadBalancer가 내부적으로 NodePort+ClusterIP 자동 생성)
- **EndpointSlice Controller vs 레거시 Endpoint Controller** — 1.21+ 표준은 EndpointSlice Controller, 본문 호명 점검
- **Headless Service / pathType: Prefix / sessionAffinity** 한 줄 :::note 권장
- **kube-proxy iptables/IPVS/eBPF 모드 분화** — "기본은 iptables 모드 기준" 단서
- **`kubectl delete pod --all`이 default ns만임** 안내

### P10 CS 학생 (학술 용어 매핑)
- **kube-proxy = control plane(룰 설치) vs netfilter = data plane(패킷 변환)** 분리 누락
- **service discovery·virtual IP·reverse proxy·reconciliation loop·stale endpoint** 정식 학술 용어 0회
- **ClusterIP가 NIC에 바인딩되지 않은 가상 IP라는 본질** 부재
- **EndpointSlice 실습(`kubectl get endpointslices -o wide`) 0회**
- **5.1에 :::term-box 부재** (Ingress엔 있는데)

### P8 풀스택 CTO (구조)
- **L4/L7 위치 부적절** — 5.3.4 마지막 회수보다 5.1.3·5.2.1에 분산 도입 권장
- **5.3 캐릭터 부재 450줄** — 가장 어려운 절에서 인적 가이드 끊김
- **CAPTURE NEEDED placeholder 미해결** (744·749줄)
- **포트 흐름 표 "생략 시" 컬럼 정확도** — `targetPort` 기본값 = `port`로 정교화

### P2 클라우드 입문
- **AWS LoadBalancer Controller·ALB Ingress·NLB·Route 53 매핑 0회** — :::tip 한 줄씩
- **EKS에서 `type: LoadBalancer`가 무엇 발급(CLB→NLB)** 한 줄 부재
- **minikube tunnel ↔ EKS LoadBalancer Service 다리** 부재

### P4 ML 엔지니어
- **모델 버전 라우팅(`/v1`·`/v2`)·카나리(canary annotation)·gRPC** 0회
- **kube-proxy 부하 분산 알고리즘 (라운드로빈/sessionAffinity)** 한 줄 부재 — 모델 워밍업 sticky 중요
- **추론 서버 readinessProbe 콜드 스타트** 한 줄

### P3 iOS 개발자
- **클라이언트(iOS·web) 관점 매핑 부재** — "앱이 호출하는 건 LoadBalancer Service" 한 줄
- **`kubectl get pod -w` 결과 해석 / 5-22~5-25 비유/IT 쌍 6장 시각 피로**

### P6 테크 PM (4.5/5)
- **5.2.2 표 "쿠버네티스 철학" 컬럼 본문 보강 부족** — 선언/집행 분리 한 줄
- **그림 5-19 "클러스터 DNS" 시선 흐름 약함** — 우측 끝에 외따로 + 색 동일
- **CH06 다리 데이터 영속성 강화** — "Pod 죽으면 데이터 같이" 한 단락

### P9 부트캠프 수료생 (3.7/5)
- **5.1.1 분산 방식(라운드로빈) 한 줄 누락** — "이것만은 기억하자"에서야 등장
- **5.1.4 첫 시도 실패 해결 너무 빠름** — "번뜩 어제 메시지" 한 줄. 미니큐브 별도 네트워크 본문 한 문장 박기
- **5.3 도입 "이름은 다 들어봤는데"가 독자 경험과 어긋남** — EndpointSlice·CoreDNS 처음 듣는 부트캠프생
- **챕터 도입 `:::prep` 블록 누락**

### P1 신입 백엔드 (4/5)
- **그림 5-5에 kube-proxy가 5.3 학습 전에 등장 = 정보 과잉**
- **닫기 단락이 세 번 반복** (5.3 끝 / 이것만은 기억하자 / 다음 챕터 예고) — 페이지 피로

## 페르소나별 핵심 한 줄

| # | 한 줄 |
|---|------|
| 1 신입 백엔드 | "도입 + 5.1 + 5.2 흐름 좋음. 그림 5-16 이름 불일치·5.3 닫기 세 번 반복" |
| 2 클라우드 입문 | "K8s 네트워킹 자체는 탄탄. AWS 매핑 0회로 다리 끊김" |
| 3 iOS | "콜센터 비유 좋음. 5.3 비유/IT 다이어그램 두 번 그리기 부담" |
| 4 ML | "모델 버전 라우팅·gRPC·canary 0회. 페르소나 폭이 통합 사이트에 묶임" |
| 5 PM 비개발 | "5.1 90% / 5.2 70% / 5.3 30%. 9명 등장인물이 한 절에 다 옴" |
| 6 테크 PM | "PM 시연용으로 가장 잘 빠진 챕터. 4.5/5" |
| 7 DevOps 시니어 | "ex11/ex12 시나리오 섞임이 핵심 결함. ingress-nginx 실제 동작 본문 모순" |
| 8 풀스택 CTO | "구조·:::note 정직성 칭찬. 5.3 캐릭터 부재·minikube tunnel 함정 미언급" |
| 9 부트캠프 | "5.1 만점. 5.2.3 minikube tunnel 함정에서 책 덮을 위험 1순위" |
| 10 CS | "비유 일관성 좋음. service discovery·virtual IP·reverse proxy 학술 용어 0회" |

## 심각도별 이슈

### 높음 (정확성·구조)
1. **5.3 ex11/ex12 시나리오 분리 명확화** — 그림 5-19/5-21의 "30080"을 ex12 흐름(LoadBalancer 80)에 맞게 교체 또는 일반화
2. **그림 5-19 L7 색대 영역** — Ingress Controller만 L7, Service는 L4 영역으로 재배치
3. **5.3.2 비유와 실제 모순 해소** — "DNS 조회"가 ingress-nginx 실제 동작이 아니라는 점을 :::note 한 줄이 아닌 본문 비유 자체에서 정직하게 풀기 (또는 비유를 "상담원이 미리 받아둔 부서별 직원 명단" 톤으로 통일)
4. **5.3 캐릭터 한 번 등장** — 옥상에서 만난 선배가 "그거 세 단계로 잘라봐요" 또는 5.3.4 끝에 동료 검증
5. **5.1·5.2 비유 위계 다리** — 선배 대사("Service는 매장 대표번호, Ingress는 그 위 본사 콜센터") 한 줄로 매핑 명시

### 중간 (정확성·실습 막힘)
6. **kube-proxy "1차/2차" 예고 + 같은 컴포넌트의 두 규칙임 :::note**
7. **minikube tunnel 함정 :::tip** — Windows UAC / 80 포트 충돌 / 터미널 살려두기 / 별도 터미널 강조
8. **ingressClassName: nginx 한 줄 보강** — 미니큐브 ingress 애드온 = nginx-ingress 매핑
9. **그림 5-16 출력 이름을 실제 ex12-ingress로 교체**
10. **NodePort 30080 ↔ minikube service --url 임의 포트** 한 줄 — "왜 30080이 아니라 임의 포트인지"
11. **챕터 도입 `:::prep` 블록 추가** — ex11/ex12 폴더 진입 안내
12. **5.1.4 미니큐브 별도 네트워크 본문 한 문장** — 첫 시도 실패 직후 깨달음 강화
13. **L4/L7 분산 도입** — 5.3.4 회수만이 아니라 5.1.3 NodePort 설명 직후·5.2.1 Service 한계 자리에 한 줄씩
14. **5.1.4 그림 5-9 자산 경로** — `assets/CH04/chap03-44.png` 참조를 CH05 자산으로 이동

### 낮음 (개선)
15. **EndpointSlice Controller 명칭 정확화** + **Endpoints 레거시 분리** :::note
16. **kube-proxy = control plane·netfilter = data plane** 정확화 한 줄
17. **5.1에 :::term-box 추가** — Service 정식 정의 (CS 학생용 학술 용어)
18. **AWS·ML·iOS 페르소나 :::tip** — ALB/NLB/Route 53·canary·`/v1`·`/v2`·앱 클라이언트 관점
19. **CH06 다리 데이터 영속성 강화** — "Pod 죽으면 데이터 같이" 한 단락
20. **CAPTURE NEEDED placeholder 처리** — 744·749줄 ex12 결과 캡처
21. **EndpointSlice 실습 `kubectl get endpointslices -o wide`** 한 줄

## 수정 제안 (우선순위)

| # | 위치 | 제안 | 심각도 |
|---|------|------|:----:|
| 1 | 그림 5-19/5-21 | "30080" 제거 또는 "ingress-nginx Service의 NodePort"로 일반화 | 높음 |
| 2 | 그림 5-19 | L7 색대를 Ingress Controller까지만 좁히고 Service는 L4 영역으로 | 높음 |
| 3 | 5.3.2 비유 본체 | "DNS 조회" 대신 "상담원이 미리 받아둔 부서별 직원 명단을 보고 직접 연결"로 톤 통일 | 높음 |
| 4 | 5.3 도입 또는 5.3.4 끝 | 선배/동료 한마디 추가 — 비유 촉발 또는 검증 | 높음 |
| 5 | 5.1.3 또는 5.2.2 | "Service는 매장 대표번호, Ingress는 본사 콜센터" 비유 위계 다리 한 줄 | 높음 |
| 6 | 5.3 도입 | "kube-proxy는 이 흐름에 두 번 등장한다" 예고 + 같은 컴포넌트의 두 규칙 :::note | 중간 |
| 7 | 5.2.3 minikube tunnel 직전 | ":::tip Windows UAC·80 포트 충돌·터미널 살려두기·별도 터미널" 박스 | 중간 |
| 8 | 5.2.3 ingressClassName | "미니큐브 ingress 애드온 = nginx-ingress라서 nginx로 지정. 여러 컨트롤러 공존 가능" 한 줄 | 중간 |
| 9 | 5.2.3 그림 5-16 | 출력 이름을 실제 ex12-ingress로 교체 | 중간 |
| 10 | 5.1.4 직후 | "왜 30080이 아니라 임의 포트인지(미니큐브 docker 드라이버 임시 터널)" 한 줄 | 중간 |
| 11 | 챕터 도입 | `:::prep` 블록 — ex11/ex12 폴더 안내 | 중간 |
| 12 | 5.1.4 첫 시도 실패 직후 | "미니큐브는 별도 네트워크라서 호스트와 분리" 본문 한 문장 | 중간 |
| 13 | 5.1.3 NodePort / 5.2.1 Service 한계 | L4/L7 분산 도입 — 한 줄씩 | 중간 |
| 14 | 그림 5-9 경로 | `assets/CH04/chap03-44.png` → CH05 자산으로 이동 | 낮음 |
| 15 | 5.3.3 Endpoint Controller | "1.21+ EndpointSlice Controller가 표준" :::note | 낮음 |
| 16 | 5.3.1 kube-proxy 직후 | "kube-proxy는 룰 작성, 실제 NAT은 노드 커널 netfilter" 한 줄 | 낮음 |
| 17 | 5.1.1 끝 | Service `:::term-box` 추가 (CS 학생용 학술 용어 포함) | 낮음 |
| 18 | 본문 곳곳 | AWS/ML/iOS :::tip 박스 페르소나별 1~2개 | 낮음 |
| 19 | 5.3 끝 또는 CH06 다리 | "Pod 죽으면 데이터 같이" 한 단락 | 낮음 |
| 20 | 744·749줄 | CAPTURE NEEDED placeholder 처리 | 낮음 |
| 21 | 5.1.4 검증 실험 직후 | `kubectl get endpointslices -o wide` 한 줄 추가 | 낮음 |

## 결론
CH05 v4는 베타리더 평균 3.77로 CH01~CH04 중 최고 (테크 PM 4.5, 부트캠프·CS 학생·신입·ML·CTO·DevOps 모두 3.5~4 안정). 콜센터 비유 일관성·5.1 도입·검증 실험은 책 전체에서도 상위. 다음 라운드 핵심은 **5.3 시나리오 섞임 정리**, **그림 5-19 L7 색대 재배치**, **ingress-nginx 비유와 실제 동작 일치**, **5.3 캐릭터 한 번 등장**, **5.1·5.2 비유 위계 다리** 다섯 가지가 가장 임팩트 큼.
