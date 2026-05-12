# MSA 책 이미지 → HTML 컴포넌트 마이그레이션 계획 v1

## 목적

MSA 책 5개 챕터의 PNG 이미지를 사내AI비서(`pub-html-build` 카탈로그) 표준에 맞춘 HTML 컴포넌트로 재구현한다. 추상 비유 일러스트(gemini/) 11장은 PNG로 유지한다.

## 범위 요약

| 분류 | 매수 | 처리 |
|---|---|---|
| gemini/ (비유 일러스트) | 11 | **PNG 유지** |
| diagram/ (D2 다이어그램) | 18 | HTML 컴포넌트 |
| terminal/ (실행 결과 캡처) | 32 | HTML 컴포넌트 (UI 캡처 포함) |
| **합계** | **61** | (HTML화 50 / PNG 11) |

## 카탈로그 기존 컴포넌트 활용 가능 목록

| 카탈로그 컴포넌트 | 적합한 상황 |
|---|---|
| `.terminal-log` + `.tl-*` | kubectl/docker compose/minikube/orchestrator 로그 |
| `.annotated-compare` | A vs B 진실값 비교 (취소선) |
| `.dual-image` | 2분할 이미지 비교 |
| `.proc-compare` | 프로세스 경계 비교 |
| `.rag-pipeline-box` | 3~5단계 순차 파이프라인 |
| `.evolve-flow` | 단계별 좌→우 진화 (도커-쿠버네티스 책) |

## 신규 MSA 전용 컴포넌트 (카탈로그 추가 필요)

기존 카탈로그로 커버 못하는 MSA 고유 패턴.

| 신규 컴포넌트 | 용도 | 사용 예 |
|---|---|---|
| `.svc-arch` + `.sa-*` | 4개 서비스(주문·상품·배달·회원) 박스 + REST/Kafka 화살표 아키텍처 | 그림 1-5, 1-6 |
| `.saga-flow` + `.sf-*` | Choreography/Orchestration Saga 흐름. 서비스 + 보상 화살표 | 그림 1-8, 1-9, 4-5, 4-6 |
| `.seq-diagram` + `.sd-*` | 시퀀스 다이어그램. 가로 lifeline + 가로 메시지 | 그림 2-1, 2-2, 4-7, 4-8, 4-9 |
| `.kafka-topic-flow` + `.ktf-*` | Producer → Topic → Consumer 흐름 + 메시지 칸 | 그림 4-2, 4-3 |
| `.kafka-cluster` + `.kc-*` | CLUSTER_ID로 묶인 브로커 + Listener 주소 | 그림 4-10, 4-11 |
| `.k8s-resources` + `.kr-*` | ConfigMap/Secret/Deployment/Service/Ingress 관계도 | 그림 3-3 |
| `.state-lifecycle` + `.sl-*` | 배달 상태 전이 (PENDING → COMPLETED) | 그림 5-2, 5-3 |
| `.hoppscotch-mock` + `.hm-*` | Hoppscotch UI 모사 (메서드·URL·Bearer 토큰·응답) | CH02~05 API 호출 캡처 |
| `.browser-console-mock` + `.bc-*` | 브라우저 DevTools Console 출력 모사 | 그림 5-7, 5-13 |
| `.browser-page-mock` + `.bp-*` | index.html 등 브라우저 페이지 모사 | 그림 5-5, 5-6, 5-12 |

## 챕터별 매핑

### CH01 (10장 → diagram 4장 HTML화)

| 그림 | 파일 | 분류 | 매핑 컴포넌트 | 비고 |
|---|---|---|---|---|
| 1-1 | gemini/01_department-store | gemini | PNG 유지 | 비유 일러스트 |
| 1-2 | gemini/02_monolith-shop | gemini | PNG 유지 | 비유 일러스트 |
| 1-3 | gemini/03_individual-shops | gemini | PNG 유지 | 비유 일러스트 |
| 1-4 | gemini/04_microservices-shop | gemini | PNG 유지 | 비유 일러스트 |
| 1-5 | diagram/05_arch-sync | diagram | **`.svc-arch` 신규** | 동기 REST 4서비스 |
| 1-6 | diagram/06_arch-async | diagram | **`.svc-arch` 신규** | Kafka 비동기 4서비스 |
| 1-7 | gemini/07_isolated-databases | gemini | PNG 유지 | 비유 일러스트 (서비스별 DB) |
| 1-8 | diagram/08_choreography-saga | diagram | **`.saga-flow` 신규** | Choreography Saga |
| 1-9 | diagram/09_orchestration-saga | diagram | **`.saga-flow` 신규** | Orchestration Saga |
| 1-10 | gemini/10_book-journey | gemini | PNG 유지 | 비유 일러스트 (학습 흐름 맵) |

### CH02 (13장 → 모두 HTML화)

| 그림 | 파일 | 분류 | 매핑 컴포넌트 | 비고 |
|---|---|---|---|---|
| 2-1 | diagram/01_order-success | diagram | **`.seq-diagram` 신규** | 주문 성공 시퀀스 |
| 2-2 | diagram/02_order-rollback | diagram | **`.seq-diagram` 신규** | 주문 실패 + 보상 시퀀스 |
| 2-3 | terminal/03_docker-compose-up | terminal | `.terminal-log` (기존) | docker compose 로그 |
| 2-4 | terminal/04_hoppscotch-main | terminal | **`.hoppscotch-mock` 신규** | Hoppscotch 초기 UI |
| 2-5 | terminal/05_hoppscotch-extension | terminal | **`.hoppscotch-mock` 신규** | Browser Extension 설정 |
| 2-6 | terminal/06_login-result | terminal | **`.hoppscotch-mock` 신규** | POST /login 응답 |
| 2-7 | terminal/07_bearer-token | terminal | **`.hoppscotch-mock` 신규** | Bearer 토큰 설정 |
| 2-8 | terminal/08_order-create | terminal | **`.hoppscotch-mock` 신규** | POST /api/orders 응답 |
| 2-9 | terminal/09_stock-decreased | terminal | **`.hoppscotch-mock` 신규** | GET /products/1 응답 |
| 2-10 | terminal/10_delivery-created | terminal | **`.hoppscotch-mock` 신규** | GET /deliveries/4 응답 |
| 2-11 | terminal/11_stockout-error | terminal | **`.hoppscotch-mock` 신규** | 재고 부족 에러 |
| 2-12 | terminal/12_empty-address-error | terminal | **`.hoppscotch-mock` 신규** | 주소 누락 에러 |
| 2-13 | terminal/13_stock-restored | terminal | **`.hoppscotch-mock` 신규** | 재고 원복 확인 |

### CH03 (8장 → 6장 HTML화)

| 그림 | 파일 | 분류 | 매핑 컴포넌트 | 비고 |
|---|---|---|---|---|
| 3-1 | gemini/01_power-adapter | gemini | PNG 유지 | 비유 일러스트 |
| 3-2 | gemini/02_usecase-deps | gemini | PNG 유지 | 비유 일러스트 (의존 도식) |
| 3-3 | diagram/03_k8s-resources | diagram | **`.k8s-resources` 신규** | K8s 리소스 관계도 |
| 3-4 | terminal/04_minikube-start | terminal | `.terminal-log` (기존) | minikube start 로그 |
| 3-5 | terminal/05_image-build | terminal | `.terminal-log` (기존) | minikube image build 로그 |
| 3-6 | terminal/06_kubectl-apply | terminal | `.terminal-log` (기존) | kubectl apply 로그 |
| 3-7 | terminal/07_pod-status | terminal | `.terminal-log` (기존) | kubectl get pods 출력 |
| 3-8 | terminal/08_order-result | terminal | **`.hoppscotch-mock` 신규** | K8s에서 주문 결과 |

### CH04 (17장 → 15장 HTML화)

| 그림 | 파일 | 분류 | 매핑 컴포넌트 | 비고 |
|---|---|---|---|---|
| 4-1 | gemini/01_sync-vs-async | gemini | PNG 유지 | 카운터 대기 vs 진동벨 |
| 4-2 | diagram/02_message-queue | diagram | **`.kafka-topic-flow` 신규** | 프로듀서 → 토픽 → 컨슈머 |
| 4-3 | diagram/03_consumer-group | diagram | **`.kafka-topic-flow` 신규** | 컨슈머 그룹 |
| 4-4 | gemini/04_orchestra | gemini | PNG 유지 | 오케스트라 비유 |
| 4-5 | diagram/05_saga-success | diagram | **`.saga-flow` 신규** | Orchestration 성공 흐름 |
| 4-6 | diagram/06_saga-rollback | diagram | **`.saga-flow` 신규** | Orchestration 롤백 흐름 |
| 4-7 | diagram/07_step1-order-created | diagram | **`.seq-diagram` 신규** | orchestrator 1단계 |
| 4-8 | diagram/08_step2-product-decreased | diagram | **`.seq-diagram` 신규** | orchestrator 2단계 |
| 4-9 | diagram/09_step3-delivery-created | diagram | **`.seq-diagram` 신규** | orchestrator 3단계 |
| 4-10 | diagram/10_kafka-cluster-id | diagram | **`.kafka-cluster` 신규** | CLUSTER_ID 묶음 |
| 4-11 | diagram/11_kafka-advertised-listener | diagram | **`.kafka-cluster` 신규** | Advertised Listener |
| 4-12 | terminal/12_kafka-deploy | terminal | `.terminal-log` (기존) | kubectl apply 로그 |
| 4-13 | terminal/13_pod-status | terminal | `.terminal-log` (기존) | get pods 출력 |
| 4-14 | terminal/14_order-pending | terminal | **`.hoppscotch-mock` 신규** | 주문 PENDING 응답 |
| 4-15 | terminal/15_order-completed | terminal | **`.hoppscotch-mock` 신규** | 주문 COMPLETED 응답 |
| 4-16 | terminal/16_stockout-order | terminal | **`.hoppscotch-mock` 신규** | 품절 주문 |
| 4-17 | terminal/17_orchestrator-rollback | terminal | `.terminal-log` (기존) | orchestrator 롤백 로그 |

### CH05 (13장 → 12장 HTML화)

| 그림 | 파일 | 분류 | 매핑 컴포넌트 | 비고 |
|---|---|---|---|---|
| 5-1 | gemini/01_polling-vs-websocket | gemini | PNG 유지 | 폴링 vs 초인종 비유 |
| 5-2 | diagram/02_delivery-ch4 | diagram | **`.state-lifecycle` 신규** | 챕터 4 배달 상태 전이 |
| 5-3 | diagram/03_delivery-ch5 | diagram | **`.state-lifecycle` 신규** | 챕터 5 배달 상태 전이 |
| 5-4 | terminal/04_pod-status | terminal | `.terminal-log` (기존) | get pods 출력 |
| 5-5 | terminal/05_index-html-initial | terminal | **`.browser-page-mock` 신규** | index.html 초기 |
| 5-6 | terminal/06_token-order | terminal | **`.browser-page-mock` 신규** | 토큰 입력 후 |
| 5-7 | terminal/07_websocket-connect | terminal | **`.browser-console-mock` 신규** | DevTools Console |
| 5-8 | terminal/08_order-pending | terminal | **`.hoppscotch-mock` 신규** | 주문 PENDING |
| 5-9 | terminal/09_delivery-pending | terminal | **`.hoppscotch-mock` 신규** | 배달 PENDING |
| 5-10 | terminal/10_delivery-completed | terminal | **`.hoppscotch-mock` 신규** | 배달 COMPLETED API |
| 5-11 | terminal/11_order-completed | terminal | **`.hoppscotch-mock` 신규** | 주문 COMPLETED |
| 5-12 | terminal/12_websocket-notification | terminal | **`.browser-page-mock` 신규** | 알림 수신 |
| 5-13 | terminal/13_console-log | terminal | **`.browser-console-mock` 신규** | Console 메시지 로그 |

## 신규 컴포넌트 작업량 추산

| 컴포넌트 | 사용 횟수 | 작업 단계 |
|---|---|---|
| `.svc-arch` | 2 | CSS 정의 + chap01 적용 |
| `.saga-flow` | 4 | CSS 정의 + chap01·chap04 적용 |
| `.seq-diagram` | 5 | CSS 정의 + chap02·chap04 적용 |
| `.kafka-topic-flow` | 2 | CSS 정의 + chap04 적용 |
| `.kafka-cluster` | 2 | CSS 정의 + chap04 적용 |
| `.k8s-resources` | 1 | CSS 정의 + chap03 적용 |
| `.state-lifecycle` | 2 | CSS 정의 + chap05 적용 |
| `.hoppscotch-mock` | 18 | CSS 정의 + chap02~05 적용 |
| `.browser-console-mock` | 2 | CSS 정의 + chap05 적용 |
| `.browser-page-mock` | 3 | CSS 정의 + chap05 적용 |

**총 10개 신규 컴포넌트**. CSS는 `pub-html-build/styles/diagrams.css`에 추가하거나, MSA 책 전용 `.build/components-msa.css`를 별도 두는 두 가지 옵션.

## 권장 작업 순서

1. **카탈로그 신규 컴포넌트 10개 설계** (HTML + CSS 명세) — 사용자 확인
2. **CSS 추가 위치 결정** — 스킬 카탈로그(`diagrams.css`)에 추가 vs MSA 전용 파일
3. **챕터별 적용 (CH01 → CH05)** — 챕터당 빌드·검수
4. **이미지 파일 정리** — HTML로 대체된 PNG는 `assets-archive/`로 이동(필요 시 보존)

## 작업 양

- 신규 컴포넌트: 10개 (CSS + HTML 템플릿 작성)
- 챕터 본문 수정: 50개 이미지 블록을 HTML 블록으로 교체
- 빌드·검수: 5개 챕터

작은 작업이 아니므로 챕터 1개 끝낼 때마다 사용자 검수를 권장.

## 결정 필요 사항

1. **CSS 추가 위치**: 스킬의 `diagrams.css`에 합칠지(다른 책이 못 씀) vs MSA 책 전용(`.build/components-msa.css` 등)
2. **신규 컴포넌트 카탈로그 등록 여부**: `components-catalog/`에 새 카테고리(예: `msa-services/`)를 만들고 README 작성할지
3. **첫 컴포넌트부터 시작**: 작업량이 가장 적은 `.k8s-resources`(CH03 한 곳)부터 시작 vs 사용 빈도 높은 `.hoppscotch-mock`(18곳)부터 시작
