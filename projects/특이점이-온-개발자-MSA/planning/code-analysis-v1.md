# 코드 분석

## 완성 코드 정보
- 경로: projects/처음-만나는-MSA/code/chap01~chap04
- 언어/프레임워크: Java 21, Spring Boot 4.0.1, Gradle

## 전체 구조

4단계로 진화하는 쇼핑몰 MSA 프로젝트.

```
chap01/ — 동기 REST MSA (4개 서비스)
├── user/         (8083)
├── product/      (8082)
├── order/        (8081)
├── delivery/     (8084)
└── docker-compose.yml

chap02/ — 클린 아키텍처 + K8s 배포
├── user/product/order/delivery/  (domain/usecase/web 구조로 리팩토링)
├── gateway/      (Nginx)
├── db/           (MySQL + init.sql)
└── k8s/          (서비스별 deploy/service/configmap)

chap03/ — Kafka 비동기 + 사가 패턴
├── user/product/order/delivery/  (+producer/consumer/message 추가)
├── orchestrator/ (NEW — 사가 오케스트레이터)
├── gateway/db/
└── k8s/kafka/    (KRaft 단일 노드)

chap04/ — WebSocket 실시간 알림 + 프론트엔드
├── user/product/order/delivery/orchestrator/
├── frontend/     (NEW — HTML + SockJS/STOMP)
├── gateway/db/
└── k8s/frontend/
```

## 핵심 기능 (의도 안)

| 기능 | 관련 코드 | 주요 기술 | 챕터 |
|------|----------|----------|------|
| 서비스 분리 | user/product/order/delivery 각 독립 프로젝트 | Spring Boot, JPA, H2 | chap01 |
| 동기 REST 통신 | OrderService → ProductClient, DeliveryClient | RestClient, HTTP | chap01 |
| 보상 트랜잭션 | OrderService에서 실패 시 재고 복원 | try-catch 보상 로직 | chap01 |
| JWT 인증 | JwtAuthenticationFilter, JwtProvider | Auth0 JWT 4.4.0 | chap01 |
| 클린 아키텍처 리팩토링 | domain/usecase/web/repository 레이어 분리 | UseCase 인터페이스, DIP | chap02 |
| API 게이트웨이 | gateway/nginx.conf (경로 기반 라우팅) | Nginx | chap02 |
| MySQL 연동 | db/init.sql, application-prod.properties | MySQL 5.7, Spring Data JPA | chap02 |
| Docker 빌드 | 각 서비스 Dockerfile (Gradle multi-stage) | Docker | chap02 |
| K8s 배포 | k8s/ (deploy, service, configmap, secret) | Kubernetes, Minikube | chap02 |
| Kafka 비동기 통신 | producer/consumer/message 패키지 | Spring Kafka, Jackson JSON | chap03 |
| 사가 오케스트레이터 | orchestrator/handler/OrderOrchestrator.java | @KafkaListener, 상태 추적 | chap03 |
| 사가 보상 흐름 | 실패 시 IncreaseProductCommand + CancelOrderCommand | 토픽 기반 롤백 | chap03 |
| WebSocket 실시간 알림 | WebSocketConfig, SimpMessagingTemplate | STOMP, SockJS | chap04 |
| 프론트엔드 | frontend/index.html (JWT 입력 → 주문 → 실시간 알림) | Vanilla JS, SockJS | chap04 |

## 의도 밖 기능 (제외)

| 기능 | 관련 코드 | 제외 이유 |
|------|----------|----------|
| Kafka 내부 동작 (파티션, 오프셋) | kafka-deploy.yml KRaft 설정 | seed.md 의도 밖 — 사용법만 다룸 |
| K8s 운영 (오토스케일링, Helm) | — | seed.md 의도 밖 |
| 테스트 코드 | test/ 폴더 (비어있음) | seed.md 의도 밖 |
| CI/CD | — | seed.md 의도 밖 |
| 보안 심화 (OAuth2, mTLS) | JWT 기본만 사용 | seed.md 의도 밖 |

## 기술 스택 정리 (의도 안)

| 분류 | 기술 | 용도 |
|------|------|------|
| 언어 | Java 21 | 백엔드 전체 |
| 프레임워크 | Spring Boot 4.0.1 | 서비스 기반 |
| 빌드 | Gradle (Kotlin DSL) | 의존성 관리 |
| ORM | Spring Data JPA | DB 접근 |
| DB (개발) | H2 | 인메모리 개발 환경 |
| DB (운영) | MySQL 5.7 | 영구 저장 |
| 인증 | JWT (Auth0 4.4.0) | 서비스 간 인증 |
| 게이트웨이 | Nginx | HTTP 라우팅 |
| 메시지 브로커 | Apache Kafka (KRaft) | 비동기 통신 |
| 실시간 | WebSocket (STOMP/SockJS) | 클라이언트 알림 |
| 컨테이너 | Docker | 이미지 빌드 |
| 오케스트레이션 | Kubernetes (Minikube) | 배포/관리 |
| 프론트엔드 | HTML + Vanilla JS | 주문 UI |

## Kafka 토픽 구조 (chap03~04)

```
주문 성공 흐름:
  order-created → orchestrator
    → decrease-product-command → product-service
      → product-decreased → orchestrator
        → create-delivery-command → delivery-service
          → delivery-created → orchestrator
            → complete-order-command → order-service
              → WebSocket 알림 (chap04)

주문 실패 흐름 (보상):
  product-decreased (실패) → orchestrator
    → increase-product-command (이미 차감된 재고 복원)
    → cancel-order-command → order-service
```

## 기술 의존성 메모

| 선행 개념 | 필요한 곳 | 비고 |
|----------|----------|------|
| REST API 기본 | chap01 전체 | 독자 배경지식 가정 |
| Spring Boot 기본 | chap01 전체 | 독자 배경지식 가정 |
| JPA 기본 | chap01 엔티티 | @Entity, Repository 패턴 |
| Docker 기본 | chap02 빌드/배포 | Dockerfile, docker-compose |
| K8s 기본 | chap02 배포 | Pod, Deployment, Service, ConfigMap |
| 인터페이스/DIP | chap02 UseCase | 클린 아키텍처 리팩토링 시 필요 |
| 메시지 큐 개념 | chap03 Kafka | Producer/Consumer, Topic |
| HTTP vs WebSocket | chap04 실시간 | 폴링 vs 푸시 차이 |
