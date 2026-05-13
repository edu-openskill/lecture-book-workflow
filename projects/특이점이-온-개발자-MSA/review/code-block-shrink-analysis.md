# 코드 블록 압축 분석 리포트

> 분석 대상: `chapters/01~05-*-v3.md` 5개 챕터
> 분석 일자: 2026-05-13
> 목적: KEEP / SHRINK / TABLE / REMOVE 4단계 분류로 압축 가능 코드 식별

---

## 코드 블록 카운트 기준

본 리포트의 "코드 블록" 정의:
- 트리플 백틱(```) 으로 감싼 모든 블록 (java, yaml, properties, gradle, dockerfile, nginx, sql, bash, json, javascript, text)
- HTML 다이어그램(`<div class="svg-figure">`), `:::box`, terminal-log(`<div class="terminal-log">`)은 제외 (이미 시각 컴포넌트)
- 본문 인용 컨텍스트가 있는지 직접 Read로 확인

---

## 챕터별 코드 블록 인벤토리

### 챕터 1 — 2개 코드 블록 (개념서, 코드 최소)

| # | 위치 | 종류 | 길이 | 태그 | 분류 | 압축 방식 |
|---|------|------|------|------|------|-----------|
| 1-1 | 1.1.2 백화점의 한계 (L67-78) | text 박스 | 12줄 | (텍스트 박스) | KEEP | 비유 박스. 이미지가 아니라 ASCII 콘솔 박스로 백화점 한계 3건 정리. 본문 흐름 유지에 기여 |
| 1-2 | 1.4.1 모놀리식 트랜잭션 (L253-262) | java | 10줄 | [참고] | KEEP | "모놀리식에서는 @Transactional 하나로 끝난다"는 핵심 대비를 시각화. 분산 트랜잭션 도입부의 핵심 비교 자료. REMOVE 시 본문 흐름 깨짐 |

**합계: KEEP 2건 / SHRINK 0건 / TABLE 0건 / REMOVE 0건**

### 챕터 2 — 22개 코드 블록 (실습 챕터, 압축 여지 다수)

| # | 위치 | 종류 | 길이 | 태그 | 분류 | 압축 방식 |
|---|------|------|------|------|------|-----------|
| 2-1 | 2.prep (L20) | bash | 2줄 | [터미널] | KEEP | git clone — prep 필수 |
| 2-2 | 2.prep (L27) | text | 7줄 | 디렉토리 트리 | KEEP | ex01 디렉토리 구조 — prep 필수 |
| 2-3 | 2.prep (L38) | text | 28줄 | 패키지 트리 | KEEP | order 서비스 패키지 구조. [참고]/[작성] 마킹 — outline 역할로 필수 |
| 2-4 | 2.6.1 Order 엔티티 (L190) | java | 45줄 | (태그 없음) | **TABLE** | 이미 압축된 2.3~2.5와 동일 패턴. 본문 "사용자(`userId`)와 상품 한 건(`productId`, `quantity`, `price`)을 담습니다. 상태는 `PENDING → COMPLETED` 또는 `PENDING → CANCELLED`로 전이..." 가 이미 모든 정보 포함. 코드는 필드·메서드 표로 압축 가능 |
| 2-5 | 2.6.2 더미 데이터 SQL (L242) | sql | 4줄 | (태그 없음) | **REMOVE** | 본문에서 "사용자별 주문 3건(완료·취소·대기)을 등록합니다" 한 줄로 이미 설명. INSERT 3줄은 GitHub에 있어도 됨 |
| 2-6 | 2.6.3 OrderRequest (L252) | java | 7줄 | (태그 없음) | **TABLE** | record 필드 4개만 있는 단순 DTO. 본문 위에 이미 "상품 정보(`productId`, `quantity`, `price`)와 배달 주소(`address`)" 명시. 필드 표로 대체 가능 |
| 2-7 | 2.6.3 OrderResponse (L263) | java | 20줄 | (태그 없음) | **TABLE** | from() 정적 팩토리만 다른 record. 본문 "저장된 Order의 필드를 그대로 펼쳐서 반환합니다" 가 다 설명. 필드 표 + from() 한 줄 언급으로 압축 가능 |
| 2-8 | 2.6.8 RestClientConfig (L375) | java | 22줄 | **[실습 1]** | **KEEP** | 인터셉터 핵심 — 실습 |
| 2-9 | 2.6.9 ProductClient (L410) | java | 29줄 | **[실습 2]** | **KEEP** | 실습 — 본문에서 "재고 감소·복구 API를 호출합니다" 인용 |
| 2-10 | 2.6.9 DeliveryClient (L444) | java | 28줄 | **[실습 3]** | **KEEP** | 실습 — ProductClient와 같은 패턴이지만 실습이라 둘 다 유지 필요 |
| 2-11 | 2.6.10 OrderService.createOrder (L483) | java | 40줄 | **[실습 4]** | **KEEP** | 챕터 2의 하이라이트. 본문에서 "두 플래그 추적", "try-catch" 인용 |
| 2-12 | 2.6.10 OrderService.findById+cancelOrder (L528) | java | 27줄 | (태그 없음) | **SHRINK** | 본문 "재고 복구 → 배달 취소 → 주문 상태 변경 순서로 처리" 이미 풀어줌. findById는 표준 패턴이므로 제거하고 cancelOrder만 핵심 부분 (재고 복구 → 배달 취소 → cancel) 짧게 남기기 |
| 2-13 | 2.7.1 Dockerfile (L567) | dockerfile | 9줄 | (태그 없음) | **REMOVE** | 표준 Spring Boot 도커파일. 본문에서 인용 없음 ("4개 서비스 모두 아래와 같습니다" 한 줄). GitHub 참조로 충분. 도커&쿠버네티스 책에서 이미 다룬 패턴 |
| 2-14 | 2.7.1 docker-compose.yml (L581) | yaml | 14줄 | (태그 없음) | **SHRINK** | "주문 서비스만 예시로 보여줍니다"라 이미 1개로 축약된 상태. 그러나 본문 "msa-network로 묶여 있기 때문에..." 가 핵심 — networks 부분만 6-7줄로 더 압축 가능. 또는 KEEP 유지 후 networks 강조 |
| 2-15 | 2.7.1 docker compose up (L601) | bash | 3줄 | [터미널] | KEEP | 독자 실행 명령 |
| 2-16 | 2.7.3-5 시나리오 JSON 6건 (L660~749) | json | 각 2~9줄 | (태그 없음) | **KEEP** | 시나리오 요청 페이로드. 본문에서 직접 인용("MacBook Pro 1개 주문", "iPhone 15 품절"). 결과 화면 캡처와 짝을 이룸 |
| 2-17 | 2.7.5 docker compose down (L760) | bash | 2줄 | [터미널] | KEEP | 정리 명령 |

**합계: KEEP 14건 / SHRINK 2건 / TABLE 3건 / REMOVE 2건**

### 챕터 3 — 23개 코드 블록 (개념서, [참고] 코드 위주)

| # | 위치 | 종류 | 길이 | 태그 | 분류 | 압축 방식 |
|---|------|------|------|------|------|-----------|
| 3-1 | 3.prep (L19) | bash | 3줄 | [터미널] | KEEP | git clone — prep 필수 |
| 3-2 | 3.2 의존 구조 비교 (L83) | text 박스 | 16줄 | (텍스트 박스) | **REMOVE** | 바로 위 그림 3-2 (의존 다이어그램)와 100% 중복. 본문 "구현체 → 인터페이스" 가 다 설명. 텍스트 박스 ASCII는 다이어그램의 노이즈 |
| 3-3 | 3.2.1 OrderController 비교 (L107) | java | 7줄 | (태그 없음) | **KEEP** | "2장 vs 3장 의존 대상" 핵심 비교. 코드가 짧고 본문 흐름의 정수 |
| 3-4 | 3.3.1 패키지 구조 (L124) | text | 24줄 | 디렉토리 트리 | KEEP | ex02 패키지 구조 — prep 역할 |
| 3-5 | 3.3.2 UseCase 3종 (L162) | java | 12줄 | (태그 없음) | **TABLE** | 인터페이스 3개가 단순한 메서드 시그니처 하나씩. 본문 "주문 생성·조회·취소를 각각 별도 인터페이스" 가 이미 설명. 인터페이스명·메서드 시그니처 표로 압축 가능 (3.3.6에 이미 동일 형식 표가 있음) |
| 3-6 | 3.3.3 Order.validateCancelable (L180) | java | 11줄 | (태그 없음) | **SHRINK** | "주문이 이미 취소되었습니다" 검증 메서드 하나만 보여주려는 의도. "2장 Order.java 참조"가 있어 보일러플레이트 절반. validateCancelable() 5줄만 남기고 클래스 외피는 한 줄 코멘트로 축약 |
| 3-7 | 3.3.4 OrderService 구현 (L202) | java | 14줄 | (태그 없음) | **SHRINK** | 이미 핵심만 발췌되어 있으나 "쓰기 메서드만 오버라이드", "cancel() 내부에서 검증" 같은 표시점 본문 1~2와 중복. 본문 텍스트에서 다루는 핵심 변경점(@Transactional readOnly + implements 3개 + cancel() 호출)이 짧으니 코드 8줄로 더 축약 가능 |
| 3-8 | 3.3.5 OrderController (L222) | java | 17줄 | (태그 없음) | **SHRINK** | 본문 "API는 챕터 2와 동일합니다(POST·GET·PUT)" + 3-3 비교 코드가 이미 핵심을 보여줌. POST 본체와 GET/PUT 주석 라인 정도로 축약 가능 (현재는 메서드 1개 + 주석 2개) |
| 3-9 | 3.4 프로파일 분리 (L266) | text | 5줄 | 디렉토리 트리 | KEEP | 파일 구조 시각화 — 3줄짜리 트리. 본문 흐름에 필수 |
| 3-10 | 3.4 application-prod.properties (L275) | properties | 11줄 | (태그 없음) | **KEEP** | `${DB_URL}` 환경변수 참조 패턴이 핵심. 본문에서 "플레이스홀더 사용하면..." 직접 인용 |
| 3-11 | 3.4 build.gradle MySQL 드라이버 (L289) | gradle | 7줄 | (태그 없음) | **SHRINK** | "// 생략..." 두 줄 + 의존성 한 줄. 본문 "build.gradle에 드라이버 의존성을 추가해야 합니다" 한 줄로 이미 충분. 한 줄 inline 코드로 축약 가능 |
| 3-12 | 3.5.1 gateway/ 트리 (L307) | text | 5줄 | 디렉토리 트리 | KEEP | 디렉토리 구조 — 필수 |
| 3-13 | 3.5.1 gateway/Dockerfile (L315) | dockerfile | 6줄 | (태그 없음) | **REMOVE** | 표준 Nginx Dockerfile. 본문 "Nginx를 설치하고, 우리가 작성한 설정 파일을 넣어주는 역할" 한 줄로 충분. GitHub 참조로 대체 |
| 3-14 | 3.5.1 nginx.conf 라우팅 (L324) | nginx | 27줄 | (태그 없음) | **SHRINK** | "user-service만 보여주고 나머지는 동일" 패턴. upstream 1개 + location 1개로 더 축약 가능 (현재 약 27줄). 본문 표가 라우팅 규칙 다 풀어줌 |
| 3-15 | 3.5.2 db/ 트리 (L364) | text | 4줄 | 디렉토리 트리 | KEEP | 필수 |
| 3-16 | 3.5.2 db/Dockerfile MySQL (L370) | dockerfile | 4줄 | (태그 없음) | **REMOVE** | 표준 MySQL Dockerfile. 본문 "Dockerfile에 직접 박지 않고 K8s db-secret.yml에서..." 가 핵심이고, Dockerfile 자체는 정보 가치 없음. GitHub 참조로 충분 |
| 3-17 | 3.5.2 db/init.sql (L380) | sql | 9줄 | (태그 없음) | **SHRINK** | CREATE TABLE 4개를 표 형태로 축약. 본문 "MySQL은 자동으로 테이블을 만들어주지 않으므로 CREATE TABLE도 포함합니다" 한 줄로 이미 핵심. 테이블 4개·컬럼 핵심 필드만 표로 |
| 3-18 | 3.6.1 k8s/ 트리 (L455) | text | 17줄 | 디렉토리 트리 | KEEP | K8s 매니페스트 구조 — 챕터 핵심 |
| 3-19~3.6.6 ConfigMap/Secret/Deployment/Service/Ingress 5종 YAML (L487, 501, 516, 533, 568, 586) | yaml | 8~30줄씩, 총 6개 | (태그 없음) | **KEEP** | 챕터 3의 본질 = K8s 매니페스트 학습. 본문이 각 리소스 역할을 풀어줌. db-secret 1개는 SHRINK 후보로 검토 가능하나 "양쪽에 같은 비밀이 적힌다"는 본문 인용과 함께 보여줘야 의미 있음. → 6개 모두 KEEP |
| 3-20 | 3.7 Minikube/배포 bash 5건 (L621, 649, 681, 726, 820, 834) | bash | 각 1~16줄 | [터미널] | KEEP | 독자 실행 명령 — 모두 필수 |

**합계: KEEP 16건 / SHRINK 5건 / TABLE 1건 / REMOVE 3건**

### 챕터 4 — 18개 코드 블록 (실습 챕터)

| # | 위치 | 종류 | 길이 | 태그 | 분류 | 압축 방식 |
|---|------|------|------|------|------|-----------|
| 4-1 | 4.prep (L20) | bash | 3줄 | [터미널] | KEEP | git clone |
| 4-2 | 4.4.1 order-service 트리 (L414) | text | 21줄 | 디렉토리 트리 | KEEP | [참고]/[작성] 마킹 outline |
| 4-3 | 4.4.2 Kafka 의존성 (L446) | gradle | 3줄 | (태그 없음) | **SHRINK** | 한 줄 코드. 본문 "spring-boot-starter-kafka 한 줄을 추가합니다" 가 이미 인라인. inline code로 충분 (현재 3줄 블록 → 1줄 inline) |
| 4-4 | 4.4.3 application-prod Kafka 설정 (L458) | properties | 6줄 | (태그 없음) | **SHRINK** | "bootstrap-servers", "consumer.group-id" 2줄이 핵심. 본문 "Kafka 주소는 환경변수로 주입받습니다" 가 다 설명. 4줄로 축약 가능 (`# 생략` 줄 제외) |
| 4-5 | 4.4.4 KafkaConfig JSON 변환 (L471) | java | 10줄 | (태그 없음) | **SHRINK** | RecordMessageConverter 빈 하나. 본문 "JacksonJsonMessageConverter 빈이 이 변환을 자동으로 처리합니다" 가 이미 설명. 핵심 빈 한 줄(`return new JacksonJsonMessageConverter()`) 강조하고 클래스 외피 줄임 가능. 또는 KEEP — 모든 Kafka 서비스 공통이라 한 번은 보여줘야 |
| 4-6 | 4.4.5 OrderCreatedEvent DTO (L486) | java | 10줄 | (태그 없음) | **TABLE** | record 1개 + 필드 6개. 본문 "record 한 줄짜리 단순한 형태"가 이미 설명. 8개 토픽 DTO 표(4.5.2 L600-611)에 이미 동일 정보 등장. **재중복. TABLE 4.5.2와 합칠 수 있음** |
| 4-7 | 4.4.6 OrderEventProducer (L504) | java | 12줄 | **[실습 1]** | KEEP | 실습 |
| 4-8 | 4.4.7 OrderService.createOrder Kafka (L528) | java | 15줄 | **[실습 2]** | KEEP | 실습 — 챕터 핵심 차이 |
| 4-9 | 4.4.8 OrderCommandConsumer (L554) | java | 20줄 | **[실습 3]** | KEEP | 실습 |
| 4-10 | 4.5.1 product-service 트리 (L584) | text | 11줄 | 디렉토리 트리 | KEEP | outline 역할 |
| 4-11 | 4.5.2 DTO 표 (L600-611) | (마크다운 표) | — | (이미 표) | KEEP | 8개 토픽 DTO 일괄 표 — 이미 압축 완료 형태 |
| 4-12 | 4.6.1 orchestrator 트리 (L626) | text | 14줄 | 디렉토리 트리 | KEEP | outline |
| 4-13 | 4.6.2 orchestrator build.gradle (L645) | gradle | 6줄 | (태그 없음) | **SHRINK** | 한 줄짜리 의존성 추가. 본문 "spring-boot-starter-kafka를 추가합니다" 인라인으로 충분. 또는 inline code 한 줄로 축약 |
| 4-14 | 4.6.3 WorkflowState 골격 (L668) | java | 19줄 | **[실습 4]** | KEEP | 실습 |
| 4-15 | 4.6.4 orderCreated 리스너 (L720) | java | 19줄 | **[실습 5]** | KEEP | 실습 |
| 4-16 | 4.6.5 productDecreased 리스너 (L775) | java | 26줄 | **[실습 6]** | KEEP | 실습 |
| 4-17 | 4.6.6 deliveryCreated 리스너 (L841) | java | 32줄 | **[실습 7]** | KEEP | 실습 |
| 4-18 | 4.7.1 kafka-service.yml (L965) | yaml | 13줄 | (태그 없음) | **SHRINK** | Service 정의 12줄. 본문 "Service는 9092만 노출"이 핵심. 메타데이터 줄 제거하면 6-7줄로 가능 — 하지만 챕터 3에서 이미 Service 패턴 학습했으므로 SHRINK 가능 |
| 4-19 | 4.7.3 order-configmap.yml (L992) | yaml | 11줄 | (태그 없음) | **SHRINK** | 챕터 3에서 ConfigMap 학습 완료 상태. "SPRING_KAFKA_BOOTSTRAP_SERVERS 추가"만 보여주면 됨. data 섹션 3줄만 inline diff 형태로 압축 가능. 또는 SHRINK 후 핵심 1줄(`SPRING_KAFKA_BOOTSTRAP_SERVERS: kafka-service:9092`)만 |
| 4-20 | 4.8 bash 명령 4건 (L1010, 1024, 1071, 1283) | bash | 각 3~21줄 | [터미널] | KEEP | 독자 실행 |
| 4-21 | 4.8.4-5 JSON 시나리오 4건 (L1206, 1223, 1238, 1254) | json | 각 2~9줄 | (태그 없음) | KEEP | 시나리오 페이로드 |

**합계: KEEP 13건 / SHRINK 5건 / TABLE 1건 / REMOVE 0건**

### 챕터 5 — 16개 코드 블록 (실습 챕터)

| # | 위치 | 종류 | 길이 | 태그 | 분류 | 압축 방식 |
|---|------|------|------|------|------|-----------|
| 5-1 | 5.prep (L21) | bash | 3줄 | [터미널] | KEEP | git clone |
| 5-2 | 5.4.1 delivery-service 트리 (L152) | text | 14줄 | 디렉토리 트리 | KEEP | outline |
| 5-3 | 5.4.2 Delivery 엔티티 (L172) | java | 22줄 | (태그 없음) | **SHRINK** | "2장 Delivery.java 참조 — 필드 동일" 표시 있음. 본문 "이전에는 생성과 동시에 complete()를 호출했지만, 이제는 명시적인 API 호출이..." 가 이미 핵심 변경 설명. validateAddress / create() / complete() 3개 메서드만 핵심 한 줄씩 보여주면 됨. 현재 22줄 → 12줄 정도로 축약 가능 |
| 5-4 | 5.4.2 DeliveryService.completeDelivery (L202) | java | 10줄 | **[실습 1]** | KEEP | 실습 |
| 5-5 | 5.4.3 DeliveryController PUT (L220) | java | 5줄 | **[실습 2]** | KEEP | 실습 |
| 5-6 | 5.4.4 DeliveryEventProducer (L235) | java | 4줄 | **[실습 3]** | KEEP | 실습 |
| 5-7 | 5.5.1 deliveryCreated 수정 (L251) | java | 12줄 | **[실습 4]** | KEEP | 실습 — 챕터 4 대비 변경 핵심 |
| 5-8 | 5.5.2 deliveryCompleted 추가 (L271) | java | 10줄 | **[실습 5]** | KEEP | 실습 |
| 5-9 | 5.6.1 order-service 트리 (L310) | text | 11줄 | 디렉토리 트리 | KEEP | outline |
| 5-10 | 5.6.2 WebSocket 의존성 (L327) | gradle | 3줄 | (태그 없음) | **SHRINK** | 한 줄 의존성. 본문 "build.gradle에 websocket이 추가됩니다" 가 다 설명. inline code 한 줄로 축약 |
| 5-11 | 5.6.3 WebSocketConfig (L339) | java | 18줄 | **[실습 6]** | KEEP | 실습 |
| 5-12 | 5.6.4 JwtAuthenticationFilter (L365) | java | 9줄 | **[실습 7]** | KEEP | 실습 |
| 5-13 | 5.6.5 OrderService.completeOrder + Push (L387) | java | 11줄 | **[실습 8]** | KEEP | 실습 — 챕터 5 하이라이트 |
| 5-14 | 5.6.6 frontend/+gateway/ 트리 (L405) | text | 8줄 | 디렉토리 트리 | KEEP | outline |
| 5-15 | 5.6.7 index.html WebSocket (L418) | javascript | 12줄 | (태그 없음) | KEEP | SockJS+STOMP 핵심. 본문 "이 코드가 핵심" 직접 인용. javascript 등장 유일 지점 |
| 5-16 | 5.6.8 frontend/nginx.conf (L445) | nginx | 9줄 | (태그 없음) | **SHRINK** | proxy_set_header 4줄이 핵심. 본문 "upgrade 헤더를 설정하여..." 가 다 설명. 핵심 3줄만 (`Upgrade $http_upgrade` + `Connection upgrade`)으로 압축 가능. 또는 KEEP — Upgrade 헤더 패턴이 처음 등장하므로 그대로 두는 게 안전 |
| 5-17 | 5.6.8 gateway/nginx.conf 추가분 (L457) | nginx | 8줄 | (태그 없음) | **REMOVE** | 바로 위 frontend/nginx.conf와 100% 동일 패턴. 본문 "gateway-service의 nginx 설정도 동일하게 upgrade 헤더를 추가합니다" 가 모든 정보. 코드 자체는 frontend/nginx.conf 반복 |
| 5-18 | 5.7 bash 4건 (L485, 500, 526, 559) | bash | 각 3~22줄 | [터미널] | KEEP | 독자 실행 |
| 5-19 | 5.7.5 JSON 시나리오 6건 (L571, 585, 610, 625, 637, 650) | json | 각 1~9줄 | (태그 없음) | KEEP | 시나리오 페이로드 |
| 5-20 | 5.7.6 전체 흐름 (L679) | text | 31줄 | (태그 없음) | KEEP | "최종 완성 시스템 전체 흐름" 텍스트 다이어그램 — 챕터 5 클로징 정수 |

**합계: KEEP 18건 / SHRINK 3건 / TABLE 0건 / REMOVE 1건**

---

## 분류별 후보 정리

### KEEP — 그대로 유지 63건

- 모든 `[실습 N]` 태그 코드 (CH02·CH04·CH05 합계 17개) — 절대 건드리지 않음
- 디렉토리 트리 (각 챕터 prep) — outline 역할
- bash 터미널 명령 — 독자 실행 필수
- JSON 시나리오 페이로드 — 본문 직접 인용
- K8s 매니페스트 5종(CH03) — 챕터 본질
- 챕터 1 모놀리식 `@Transactional` 비교 코드 — 분산 트랜잭션 도입 정수

### SHRINK — 축약 15건 (Before / After)

**SH-01. CH02 2-12: OrderService.findById+cancelOrder (L528, 27줄 → 15줄)**
- Before: findById 6줄 + cancelOrder 17줄 + 주석
- After: cancelOrder 핵심 5줄만 (재고 복구 → 배달 취소 → cancel() 호출). findById는 "주문 한 건을 조회합니다" 본문 한 줄로 대체, 코드 생략
- 근거: 본문이 이미 "재고 복구(increaseQuantity) → 배달 취소(cancelDelivery) → 주문 상태 변경(cancel()) 순서로 처리" 라고 풀어줌

**SH-02. CH02 2-14: docker-compose.yml (L581, 14줄 → 8줄)**
- Before: services / build / ports / networks 풀세트
- After: services 1개 + networks 블록만. ports 줄에 한 줄 주석으로 패턴 설명
- 근거: 본문에서 "msa-network로 묶여 있기 때문에..." 핵심만 인용

**SH-03. CH03 3-6: Order.validateCancelable (L180, 11줄 → 6줄)**
- Before: 클래스 외피 + 주석 + 메서드
- After: 클래스 외피 한 줄 코멘트로 ("// Order.java — 2장 필드 그대로") + validateCancelable() 5줄
- 근거: "2장 Order.java 참조 — 필드 및 create()/complete()/cancel() 동일" 표시가 이미 있음

**SH-04. CH03 3-7: OrderService 구현 (L202, 14줄 → 8줄)**
- Before: 클래스 외피 + 주석 3개 + cancelOrder 본체
- After: 핵심만 (`@Transactional(readOnly = true)` + `implements 3개 인터페이스` + `cancelOrder`에 @Transactional override)
- 근거: 본문 1, 2 표시점이 이미 핵심 변경 다 풀어줌

**SH-05. CH03 3-8: OrderController (L222, 17줄 → 10줄)**
- Before: 클래스 외피 + 필드 3개 + POST 메서드 + GET/PUT 주석
- After: 필드 3줄 + POST 본체 한 줄 (이미 3-3 비교 코드가 핵심을 보여줌)
- 근거: 본문 "API는 챕터 2와 동일합니다(POST·GET·PUT)" + 3-3 비교 코드 중복

**SH-06. CH03 3-11: build.gradle MySQL 드라이버 (L289, 7줄 → 1줄 inline)**
- Before: dependencies 블록 + 생략 주석 2줄
- After: 본문에 inline code "`runtimeOnly 'com.mysql:mysql-connector-j'`"
- 근거: 한 줄 변경이라 블록 불필요

**SH-07. CH03 3-14: gateway/nginx.conf 라우팅 (L324, 27줄 → 15줄)**
- Before: events + http + upstream user-service + 주석 + location /login + /api/users + 주석
- After: upstream + location 1쌍 + 동일 패턴 주석
- 근거: 이미 "동일 패턴" 주석 있고, 본문 표가 다 풀어줌

**SH-08. CH03 3-17: db/init.sql (L380, 9줄 → 표 + 4줄)**
- Before: CREATE TABLE 4건 (각 칼럼 풀세트) + 더미 INSERT 안내
- After: 4테이블 표 (테이블명·핵심 필드·인덱스) + CREATE TABLE 1개만 패턴 예시
- 근거: 본문 "테이블도 4개입니다" + "더미 데이터 (2장과 동일)" 두 줄이 다 설명

**SH-09. CH04 4-3: Kafka 의존성 (L446, 3줄 → 1줄 inline)**
- Before: 코드블록 3줄
- After: 본문 inline code
- 근거: 본문 "spring-boot-starter-kafka 한 줄을 추가합니다" 가 이미 줄 단위 인라인

**SH-10. CH04 4-4: application-prod Kafka (L458, 6줄 → 4줄)**
- Before: `# ===== Kafka =====` 헤더 + bootstrap-servers + group-id + 생략
- After: 핵심 2줄만 (헤더·생략 줄 제거)

**SH-11. CH04 4-5: KafkaConfig (L471, 10줄 → 6줄) 또는 KEEP**
- Before: 클래스 외피 + @Bean + return
- After: `@Bean public RecordMessageConverter recordMessageConverter() { return new JacksonJsonMessageConverter(); }` 한 메서드 + 클래스 외피
- 절충: "이 설정은 모든 Kafka 서비스에 동일" 본문이 있어 한 번은 풀어 보여주는 게 안전. 신중 검토 필요

**SH-12. CH04 4-13: orchestrator build.gradle (L645, 6줄 → 1줄 inline)**
- Before: dependencies 블록 6줄
- After: 본문 inline code

**SH-13. CH04 4-18: kafka-service.yml (L965, 13줄 → 7줄)**
- Before: 풀 매니페스트 12줄
- After: spec.ports 핵심부 + 한 줄 주석
- 근거: 챕터 3에서 Service 패턴 학습 완료

**SH-14. CH04 4-19: order-configmap.yml (L992, 11줄 → 4줄)**
- Before: 풀 매니페스트
- After: data 섹션 핵심 1줄 (`SPRING_KAFKA_BOOTSTRAP_SERVERS: kafka-service:9092`) + 한 줄 주석. 또는 본문 inline code

**SH-15. CH05 5-3: Delivery 엔티티 (L172, 22줄 → 12줄)**
- Before: 클래스 외피 + validateAddress + create + complete + 주석
- After: "2장 필드 그대로" 한 줄 코멘트 + 3개 메서드 5줄씩
- 근거: 본문 "이전에는 생성과 동시에 complete()를..."이 핵심 변경 설명

**SH-16. CH05 5-10: WebSocket 의존성 (L327, 3줄 → 1줄 inline)**
- Before: 코드블록 3줄
- After: 본문 inline code

### TABLE — 표로 압축 5건

**TB-01. CH02 2-4: Order 엔티티 (L190, 45줄 → 표 + 메서드 시그니처 3줄)**

압축 시안:

| 필드 | 타입 | 역할 |
|------|------|------|
| id | int | PK, AUTO_INCREMENT |
| userId | int | 주문자 |
| productId, quantity, price | int, int, Long | 단일 상품 |
| status | OrderStatus | PENDING/COMPLETED/CANCELLED |
| createdAt, updatedAt | LocalDateTime | 타임스탬프 |

메서드: `create()`, `complete()`, `cancel()` (각 상태 캡슐화)

전체 코드는 GitHub `ex01/order/Order.java` 참조.

- 근거: 2.3~2.5에서 이미 동일 패턴(메서드 표 + GitHub 참조)으로 압축한 상태

**TB-02. CH02 2-6: OrderRequest (L252, 7줄 → 표)**

| 필드 | 타입 | 역할 |
|------|------|------|
| productId | int | 상품 ID |
| quantity | int | 수량 |
| price | Long | 단가 |
| address | String | 배달 주소 |

전체 record 정의는 GitHub 참조.

**TB-03. CH02 2-7: OrderResponse (L263, 20줄 → 표)**

OrderResponse는 Order의 필드(id, userId, productId, quantity, price, status, createdAt, updatedAt)를 그대로 펼친 record + `from(Order)` 정적 팩토리. 전체 정의는 GitHub 참조.

**TB-04. CH03 3-5: UseCase 3종 (L162, 12줄 → 표)**

| UseCase | 시그니처 |
|---------|---------|
| CreateOrderUseCase | `OrderResponse createOrder(int userId, int productId, int quantity, Long price, String address)` |
| GetOrderUseCase | `OrderResponse findById(int orderId)` |
| CancelOrderUseCase | `OrderResponse cancelOrder(int orderId)` |

- 근거: 3.3.6에 이미 4개 서비스의 UseCase 인터페이스가 표로 정리되어 있음. 형식 통일

**TB-05. CH04 4-6: OrderCreatedEvent (L486, 10줄 → 4.5.2 DTO 표에 흡수)**

이미 4.5.2 (L600-611)에 8개 토픽·DTO·필드가 표로 정리되어 있음. OrderCreatedEvent 코드 블록 자체는 제거하고 표 한 줄에 위임. "Kafka 메시지로 전송할 데이터를 DTO로 정의합니다" 한 줄로 도입 후 바로 4.6 KafkaTemplate으로 진행.

### REMOVE — 제거 6건

**RM-01. CH02 2-5: 주문 더미 데이터 SQL (L242, 4줄)**
- 이유: 본문 "사용자별 주문 3건(완료·취소·대기)을 등록합니다. 한 행에 상품 정보까지 함께 들어갑니다" 한 문장으로 충분. INSERT 3건은 GitHub 참조 가능.
- 본문 영향: 없음. 더미 데이터 내용은 이후 시나리오에서 별도로 언급됨

**RM-02. CH02 2-13: Dockerfile 4개 서비스 공통 (L567, 9줄)**
- 이유: 표준 Spring Boot Dockerfile. 본문 "각 서비스의 Dockerfile은 동일한 구조입니다" 한 줄 + "스프링 프로젝트를 컨테이너 내에서 실행하는 Dockerfile입니다" 도 GitHub 참조로 충분. 도커&쿠버네티스 책에서 이미 학습한 패턴
- 본문 영향: 미미. "JDK 21 베이스" 정보가 사라지나, prep 환경 표(L74-78)에서 다룸

**RM-03. CH03 3-2: 의존 구조 비교 ASCII 박스 (L83, 16줄)**
- 이유: 바로 위 그림 3-2(`02_usecase-deps.png`) 다이어그램과 100% 중복. 본문 "OrderController → OrderService 직접 의존 → UseCase 인터페이스 의존"이 다 설명
- 본문 영향: 없음. 시각화는 이미지로 충분

**RM-04. CH03 3-13: gateway/Dockerfile (L315, 6줄)**
- 이유: 표준 Nginx Dockerfile (FROM nginx:alpine + COPY + EXPOSE + CMD). 학습 가치 0
- 본문 영향: "Dockerfile은 Nginx를 설치하고, 우리가 작성한 설정 파일을 넣어주는 역할입니다" 본문 한 줄 + GitHub 참조로 충분

**RM-05. CH03 3-16: db/Dockerfile MySQL (L370, 4줄)**
- 이유: 표준 MySQL Dockerfile (FROM mysql + COPY init.sql + CMD options). 핵심은 본문에 있는 "Dockerfile에 직접 박지 않고 K8s db-secret.yml에서 환경변수로 주입합니다" 메시지
- 본문 영향: utf8mb4 정보가 사라지지만, 학습 흐름에 비핵심

**RM-06. CH05 5-17: gateway/nginx.conf WebSocket 추가분 (L457, 8줄)**
- 이유: 바로 위 frontend/nginx.conf(5-16)와 같은 4줄 패턴 반복. 본문 "gateway-service의 nginx 설정도 동일하게 upgrade 헤더를 추가합니다" 가 다 설명
- 본문 영향: 없음. 동일 코드 반복 제거

---

## 일괄 적용 전략

### 권장 순서 (Phase 1 → Phase 4)

**Phase 1. REMOVE 6건 (가장 안전, 즉시 적용 가능)**
1. RM-01: CH02 더미 SQL → 본문 한 줄로 대체
2. RM-02: CH02 Dockerfile → 본문 한 줄 + GitHub 참조 안내
3. RM-03: CH03 ASCII 의존 박스 → 그림 3-2로 대체
4. RM-04: CH03 gateway/Dockerfile → 본문 한 줄로 대체
5. RM-05: CH03 db/Dockerfile → 본문 한 줄로 대체
6. RM-06: CH05 gateway/nginx.conf 중복 → 한 문장으로 대체

각 항목 모두 본문 인용 끊김 없음을 확인 완료. 압축 효과: 약 47줄 감소.

**Phase 2. TABLE 5건 (CH02 2.6.1~2.6.3 + CH03 UseCase + CH04 DTO)**
- TB-01·02·03 (CH02 Order 엔티티·DTO 3종) → 2.3~2.5 압축 패턴 재사용. 가장 큰 효과 (45 + 7 + 20 = 72줄 → 표 3개 약 20줄)
- TB-04 (CH03 UseCase 3종) → 3.3.6 패턴과 통일
- TB-05 (CH04 OrderCreatedEvent) → 4.5.2 표에 흡수

압축 효과: 약 75줄 감소. 본문 영향 없음 (이미 본문이 모든 필드·메서드를 풀어줌).

**Phase 3. SHRINK 16건 (개별 검토 필요)**
- 우선순위 A (효과 큼·안전): SH-01, SH-02, SH-07, SH-08, SH-15
- 우선순위 B (한 줄짜리 inline 전환): SH-06, SH-09, SH-12, SH-16 — 본문에 자연스럽게 녹임
- 우선순위 C (신중): SH-03, SH-04, SH-05, SH-10, SH-11, SH-13, SH-14 — 학습 흐름 손상 여부 케이스별 확인

압축 효과: 약 65~80줄 감소. 본문 흐름 영향: 케이스 B의 inline 전환은 오히려 본문 가독성 향상.

**Phase 4. KEEP 63건 (수정 금지)**
- 모든 [실습 N] 태그 코드
- 디렉토리 트리
- bash 명령
- JSON 시나리오 페이로드
- K8s 매니페스트 (CH03 5종)
- 챕터 1 비교 코드

### GitHub 참조로 대체 가능한 항목

| 항목 | 현재 | 대체 |
|------|------|------|
| CH02 OrderRequest/Response 풀 코드 | 인라인 | GitHub `ex01/order/.../web/dto/` + 필드 표 |
| CH02 Order 엔티티 풀 코드 | 인라인 | GitHub `ex01/order/.../orders/Order.java` + 필드·메서드 표 |
| CH02 더미 데이터 SQL | 인라인 | GitHub `ex01/order/.../db/data.sql` |
| CH02 4개 서비스 공통 Dockerfile | 인라인 | GitHub `ex01/*/Dockerfile` |
| CH03 gateway/Dockerfile | 인라인 | GitHub `ex02/gateway/Dockerfile` |
| CH03 db/Dockerfile | 인라인 | GitHub `ex02/db/Dockerfile` |
| CH03 UseCase 인터페이스 3종 풀 코드 | 인라인 | GitHub `ex02/order/.../usecase/` + 시그니처 표 |
| CH03 db/init.sql CREATE TABLE | 인라인 | GitHub `ex02/db/init.sql` + 테이블 4개 표 |
| CH04 모든 DTO 풀 코드 | 4.4.5 OrderCreatedEvent 인라인 | 4.5.2 8개 토픽 표에 흡수 |

### 본문 흐름 영향 평가

| 분류 | 압축 후 영향 | 위험도 |
|------|------------|--------|
| REMOVE 6건 | 본문 한 줄 대체로 충분, 인용 끊김 없음 | 낮음 |
| TABLE 5건 | 본문이 이미 모든 정보 풀어줌. 표는 시각 정리 | 낮음 |
| SHRINK 우선순위 A·B 9건 | 가독성 오히려 향상 | 낮음 |
| SHRINK 우선순위 C 7건 | 케이스별 본문 인용 재확인 필요 | 중간 |

---

## 종합

### 챕터별 압축 효과 추정

| 챕터 | 현재 줄수 | 코드블록 차지 | 압축 후 예상 | 감소량 |
|------|----------|------------|------------|--------|
| CH01 | 442 | 약 20줄 (2건) | 442 (변경 없음) | 0 |
| CH02 | 785 | 약 290줄 (22건) | 약 700 | -85 (-11%) |
| CH03 | 855 | 약 310줄 (23건) | 약 760 | -95 (-11%) |
| CH04 | 1302 | 약 430줄 (18건) | 약 1250 | -52 (-4%) |
| CH05 | 729 | 약 290줄 (16건) | 약 700 | -29 (-4%) |
| **합계** | **4113** | — | **약 3852** | **-261 (-6.3%)** |

### 가장 큰 압축 효과가 기대되는 곳

1. **CH02 2.6.1~2.6.3 Order 엔티티+DTO 2종 (TB-01·02·03)** — 단일 변경으로 약 60줄 감소. 2.3~2.5와 패턴 통일 효과까지
2. **CH03 3.5 Dockerfile 3건 + ASCII 박스 (RM-02·03·04·05)** — 본문 흐름 영향 없이 약 35줄 감소
3. **CH02 OrderService.findById+cancelOrder (SH-01)** — 챕터 핵심 createOrder 다음에 오는 보조 메서드. SHRINK로 핵심 노출

### 1차 권장 작업 단위

**1차 (낮은 위험·큰 효과)**: Phase 1 REMOVE 6건 + Phase 2 TABLE 5건 = 11건. 약 120줄 감소. 본문 영향 거의 없음.

**2차 (검토 필요)**: Phase 3 SHRINK A·B 9건. 약 50~70줄 감소. 본문 자연스러움 향상 부분도 있음.

**3차 (개별 결정)**: Phase 3 SHRINK C 7건. 본문 인용 재확인이 필요한 케이스.

### 일괄 적용 가능성 평가

**일괄 적용 가능**: Phase 1·Phase 2 (16건)
- 본문 인용 끊김 없음 확인 완료
- 모두 본문이 이미 모든 정보 풀어준 상태에서 코드만 시각 압축

**개별 적용 권장**: Phase 3 SHRINK 16건
- A·B 9건은 그룹 작업 가능
- C 7건은 케이스별 본문 인용 재확인 필요

**절대 건드리지 말 것**: KEEP 63건 (모든 [실습 N] + 디렉토리 트리 + bash + JSON 페이로드 + K8s 매니페스트 + CH02 2.3~2.5 이미 압축분)

---

## 부록: 분석 메모

- CH02 2.3~2.5 (회원·상품·배달 서비스) 는 이미 메서드 표 + GitHub 참조 패턴으로 압축 완료된 상태. 같은 패턴을 2.6.1~2.6.3에 적용하면 챕터 전반 톤 통일성도 확보.
- CH04는 [실습] 비중이 높아 압축 여지가 상대적으로 적음. yaml 매니페스트 압축이 주 효과.
- CH05는 [실습] 비중이 가장 높음. SHRINK는 작은 의존성 블록·반복 nginx 설정 위주.
- 챕터별 시각 컴포넌트(SVG figure, terminal-log, :::box)는 분석 대상이 아니며 모두 KEEP 처리.
