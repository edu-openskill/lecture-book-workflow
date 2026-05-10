
# 챕터 1. MSA란 무엇인가?

### 학습 목표

- 모놀리식 아키텍처의 한계를 이해한다.
- 마이크로서비스 아키텍처가 어떤 방식으로 문제를 해결하는지 이해한다.
- 이 책에서 만들 쇼핑몰 주문 시스템의 전체 구조를 파악한다.
- MSA의 핵심 과제인 분산 트랜잭션과 Saga 패턴을 이해한다.
- 챕터 2~5의 학습 흐름을 파악한다.


## 1.1 모놀리식 — 쇼핑몰을 하나의 서버로 만들면 어떻게 될까?

### 1.1.1 처음에는 아무 문제가 없었다

백화점을 떠올려 보세요. 수십 개의 매장이 한 건물 안에 모여 있습니다. 고객은 한 곳에서 모든 것을 해결할 수 있고, 운영사 입장에서는 전기·냉방·보안·고객 데이터를 한 곳에서 통합 관리합니다. 이 구조는 단순하고 효율적입니다.

<!-- image-prompt: Minimal black line drawing on white background, icon-like simplicity, 4:3 aspect ratio, 800x600px. A large department store building with Korean label "백화점". Inside the building, multiple small shop icons (clothing, electronics, food, cosmetics) are visible through windows, all sharing one roof. Label above: "모든 매장이 한 건물에". Simple, clean, no colors. -->
![백화점 - 모든 매장이 한 건물에](images/chap01-1.png)
*그림 1-1: 백화점 — 모든 매장이 한 건물에 모여 있다*

소프트웨어도 같은 이야기입니다. 처음에는 하나의 서버에 모든 기능을 넣는 **모놀리식** 구조가 단순하고 빠릅니다.

### 1.1.2 성장하면서 균열이 생긴다

백화점이 잘 돼서 방문객이 열 배로 늘었습니다. 이제 문제가 보이기 시작합니다.

```
[백화점의 한계]

  문제1: 한 매장에서 화재 발생
         → 스프링클러 작동·대피령으로 전 층 영업 중단

  문제2: 전자제품 세일로 3층에 사람이 몰림
         → 3층만 확장 불가, 건물 전체를 새로 지어야 함

  문제3: 건물 전기 배선 전면 교체
         → 공사 기간 동안 전 층 영업 중단
```

소프트웨어 세계에서도 똑같은 일이 벌어집니다. 회원 10만 명, 하루 주문 1만 건이 되었을 때, 모놀리식 구조의 균열이 드러납니다.

<!-- image-prompt: Minimal black line drawing on white background, icon-like simplicity, 4:3 aspect ratio, 800x600px. A tower server case shape as the outer container — rounded top corners, a small power button circle on the top-right, and small LED indicator dots on the front panel, making it clearly recognizable as a computer server, not a plain box. Label "모놀리식 서버" at the top inside the server case. Inside, four module boxes stacked vertically with equal spacing: "회원", "상품", "주문", "배달". No DB icon. No external elements. Just one server case containing four modules. -->
![모놀리식 쇼핑몰](images/chap01-2.png)
*그림 1-2: 모놀리식 쇼핑몰 — 모든 기능이 하나의 서버에*

**배포가 두렵다** — 주문 기능 하나를 수정해도 배포 시 회원·상품·배달까지 전부 재시작해야 합니다.

**장애가 전파된다** — 배달 기능 버그로 서버가 느려지면 배달과 무관한 회원 로그인도 함께 느려집니다.

**확장이 어렵다** — 블랙프라이데이에 주문 기능만 서버를 늘리고 싶어도 모놀리식에서는 전체 서버를 복제해야 합니다.

**팀이 커지면 충돌이 잦아진다** — 10명이 하나의 코드베이스를 동시에 수정하면 하루에도 수십 번 충돌이 발생합니다.


## 1.2 마이크로서비스 — 역할을 나눈다

### 1.2.1 백화점 vs 개별 상점

개별 상점 방식은 백화점과 구조 자체가 다릅니다. 각 매장이 독립된 건물로 운영되어, 자신만의 전기·냉방·입구를 가집니다.

<!-- image-prompt: Minimal black line drawing on white background, icon-like simplicity, 4:3 aspect ratio, 800x600px. ONLY four separate small shop buildings standing independently with clear gaps between them. Each shop has its own small door, roof, and sign. Labels: "의류점", "전자제품점", "식품점", "화장품점". Do NOT draw a department store or any other large building. Only the four independent small shops. -->
![개별 상점 - 각 매장이 독립된 건물](images/chap01-3.png)
*그림 1-3: 개별 상점 — 각 매장이 독립된 건물로 운영*

백화점 구조와 비교하면 차이가 분명합니다.

| | 백화점 | 개별 상점 |
|---|---|---|
| 한 매장 화재 발생 | 스프링클러·대피령으로 전 층 영업 중단 | 해당 매장만 소방 처리, 나머지 정상 영업 |
| 전자제품 수요 폭증 | 건물 전체를 확장해야 함 | 전자제품점만 확장 |
| 건물 전기 배선 교체 | 공사 기간 동안 전 층 영업 중단 | 해당 매장만 임시 폐쇄, 나머지 정상 영업 |

마이크로서비스 아키텍처가 바로 이 방식입니다. 하나의 큰 서버 대신, 기능별로 작은 서비스들을 분리합니다.

<!-- image-prompt: Minimal black line drawing on white background, icon-like simplicity, 4:3 aspect ratio, 800x600px. Four separate tower server case shapes arranged horizontally with gaps between them. Each server has rounded top corners, a small power button circle, and LED indicator dots to look like a physical server, not a plain rectangle. Labels inside each server: "회원 서비스", "상품 서비스", "주문 서비스", "배달 서비스". No arrows, no connections, no DB cylinders. Just four independent servers standing side by side. -->
![마이크로서비스 쇼핑몰](images/chap01-4.png)
*그림 1-4: 마이크로서비스 쇼핑몰 — 기능별로 서비스를 분리*

이제 각 서비스는 독립적으로 배포하고, 독립적으로 확장할 수 있습니다. 주문 서비스에 버그가 생겨도 회원 서비스는 영향을 받지 않습니다.

### 1.2.2 MSA vs 모놀리식

| 특성 | 모놀리식 | 마이크로서비스 |
|---|---|---|
| 배포 | 전체 재배포 | 해당 서비스만 배포 |
| 장애 격리 | 전체 영향 | 해당 서비스만 영향 |
| 확장 | 전체 복제 | 필요한 서비스만 확장 |
| 팀 분리 | 하나의 코드베이스 | 서비스별 독립 개발 |


## 1.3 시스템 설계 : 우리가 만들 서비스 구조

문제를 이해했으니, 이제 직접 만들어볼 시스템을 설계해보겠습니다. 이 책의 쇼핑몰 주문 시스템은 4개의 마이크로서비스로 구성됩니다.

| 서비스 | 포트 | 역할 |
|---|---|---|
| 회원 서비스 | 8083 | 로그인, JWT 발급, 사용자 조회 |
| 상품 서비스 | 8082 | 상품 목록, 재고 조회 및 증감 |
| 주문 서비스 | 8081 | 주문 생성·조회·취소 (핵심) |
| 배달 서비스 | 8084 | 배달 생성·조회·취소 |


### 1.3.1 챕터 2~3 아키텍처 (동기 통신)

챕터 2와 챕터 3에서 만들 시스템입니다. 주문 서비스가 중심에서 다른 서비스를 직접 REST API로 호출합니다.

![챕터 2~3 아키텍처 — 동기 REST 통신](images/fig-1-5.png)
*그림 1-5: 챕터 2~3 아키텍처 — 동기 REST 통신*

사용자가 주문을 생성하면 주문 서비스가 상품 서비스와 배달 서비스를 RestClient로 차례로 호출합니다. 응답을 받을 때까지 기다리는 동기 방식입니다. 이 구조를 먼저 직접 구현해보면, 나중에 비동기 방식으로 전환했을 때 그 차이가 더 명확하게 느껴집니다.


### 1.3.2 챕터 4~5 아키텍처 (비동기 통신)

챕터 4와 챕터 5에서는 직접 호출을 걷어내고 Kafka를 도입합니다. 중앙의 오케스트레이터가 전체 흐름을 조율하고, 각 서비스는 Kafka를 통해 재고 차감, 배달 생성 메시지를 주고받습니다.

![챕터 4~5 아키텍처 — Kafka 비동기 통신](images/fig-1-6.png)
*그림 1-6: 챕터 4~5 아키텍처 — Kafka 비동기 통신*

주문 서비스는 주문을 저장하고 Kafka에 이벤트만 발행한 뒤 즉시 응답합니다. 오케스트레이터가 나머지 흐름을 이어받아 처리하므로, 서비스 간 직접 연결이 사라집니다. 이 구조의 장점은 챕터 4에서 직접 체험합니다.


## 1.4 분산 트랜잭션 : MSA의 핵심 과제

서비스를 분리하면 좋은 점이 많지만, 동시에 새로운 문제가 생깁니다. 바로 **분산 트랜잭션**입니다. 이 개념을 이해하는 것이 이 책의 핵심입니다.

### 1.4.1 모놀리식에서는 쉬웠던 것

모놀리식에서는 데이터베이스 트랜잭션이 간단합니다. 주문, 재고 변경, 배달 생성을 하나의 `@Transactional` 블록 안에 넣으면, 하나라도 실패하면 전부 자동 롤백됩니다.

모놀리식에서 단일 트랜잭션으로 처리하는 예시입니다.

**[참고]** 동작 이해용입니다. Java 코드를 모르더라도 주석만 읽으면 흐름을 이해할 수 있습니다.

```java
// 모놀리식: 하나의 트랜잭션으로 처리 가능
@Transactional
public void createOrder() {
    decreaseStock();    // 재고 감소
    createDelivery();   // 배달 생성
    saveOrder();        // 주문 저장
    // 실패 시 세 가지 모두 자동 롤백
}
```

### 1.4.2 MSA에서는 불가능하다

하지만 MSA에서는 각 서비스가 **독립된 데이터베이스**를 가집니다. DB를 공유하면 한 서비스의 테이블 변경이 다른 서비스에 영향을 주고, 배포와 확장도 함께 묶이기 때문입니다. 상품 서비스의 DB와 배달 서비스의 DB가 물리적으로 분리되어 있으므로, 하나의 트랜잭션으로 묶을 방법이 없습니다.

> 이 책에서는 학습 편의를 위해 하나의 MySQL 인스턴스를 공유합니다. 실무에서는 서비스별로 DB를 분리하는 것이 원칙입니다.

이것은 서로 다른 은행 간 송금과 비슷합니다. 같은 은행 안에서 이체하면 A 계좌에서 빠진 돈이 B 계좌로 즉시 들어가고, 문제가 생기면 자동으로 원상 복구됩니다. 하지만 다른 은행으로 송금할 때는 이야기가 달라집니다. A 은행에서 돈은 빠졌는데 B 은행에 입금이 실패하면, A 은행이 자동으로 알 수 없습니다. 별도의 확인과 복구 절차가 필요합니다.

> **분산 트랜잭션(Distributed Transaction)**: 여러 독립된 데이터베이스에 걸친 작업을 하나의 논리적 단위로 처리해야 하는 상황입니다. MSA에서는 서비스마다 DB가 분리되어 있으므로 단일 트랜잭션이 불가능하고, 별도의 전략이 필요합니다.

배달 생성이 실패했을 때, 이미 감소된 재고를 어떻게 되돌릴까요? 상품 서비스와 배달 서비스의 DB가 분리되어 있으므로, 자동 롤백이 불가능합니다.

<!-- image-prompt: Minimal black line drawing on white background, icon-like simplicity, 4:3 aspect ratio, 800x600px. Three separate service boxes arranged horizontally: "주문 서비스", "상품 서비스", "배달 서비스". Each has its own "DB" cylinder directly below it, clearly separated.  Label above: "서비스별 독립 데이터베이스". Dotted line with "트랜잭션으로 묶을 수 없다." showing transaction boundary cannot span across services. -->
![서비스별 독립 데이터베이스](images/chap01-5.png)
*그림 1-7: 서비스별 독립 데이터베이스*

### 1.4.3 해결 방법: Saga 패턴

이 문제를 어떻게 해결할까요? 다시 은행 비유로 돌아가 봅시다. 타행 송금이 실패하면 은행은 "송금 실패 → 출금액 환불"이라는 정해진 절차를 밟습니다. 자동 롤백은 안 되지만, 실패를 감지하면 단계별로 되돌리는 것입니다. 이 책에서는 이 접근법을 **Saga 패턴**으로 구현합니다.

> **Saga 패턴**: 분산 트랜잭션을 여러 개의 로컬 트랜잭션으로 나누고, 중간에 실패가 발생하면 이전 단계를 역순으로 취소(보상)하여 전체 정합성을 맞추는 패턴입니다.

두 가지 방식을 순서대로 배웁니다.

**Choreography Saga — 챕터 2, 챕터 3**

동네 가게들이 서로 전화로 직접 소통하는 방식입니다. 꽃집이 케이크 가게에 직접 전화해서 "케이크 취소해주세요"라고 말하듯, 실패가 발생하면 이전 단계 서비스에 직접 복구를 요청합니다. 주문 서비스가 직접 상품 서비스에 "재고 돌려줘"라고 요청합니다.

> **Choreography Saga(코레오그래피 사가)**: 중앙 조율자 없이 각 서비스가 서로 직접 호출하여 트랜잭션을 이어가고, 실패 시 이전 서비스에 직접 보상(복구)을 요청하는 방식입니다.

![Choreography Saga — 서비스 간 직접 호출과 보상](images/fig-1-8.png)
*그림 1-8: Choreography Saga — 서비스 간 직접 호출과 보상*

서비스끼리 서로 직접 호출해서 복구하는 방식입니다. 단순하지만, 서비스 수가 늘어날수록 복잡해집니다.

**Orchestration Saga — 챕터 4, 챕터 5**

이번에는 웨딩 플래너를 떠올려 봅시다. 결혼식에는 꽃집, 케이크 가게, 사진작가, 밴드 등 여러 업체가 참여합니다. 신랑 신부가 각 업체에 일일이 전화하는 대신, 웨딩 플래너가 전체 일정을 조율합니다. 한 업체에 문제가 생기면 플래너가 나머지 업체에 변경 사항을 알립니다.

별도의 오케스트레이터가 이 웨딩 플래너 역할을 합니다. 전체 흐름을 조율하고, 각 서비스는 자신의 일만 하고 Kafka로 결과를 발행합니다. 오케스트레이터가 결과를 받아 다음 단계를 결정합니다.

> **Orchestration Saga(오케스트레이션 사가)**: 중앙의 조율자(오케스트레이터)가 전체 트랜잭션 흐름을 관리하고, 각 서비스에 명령을 내리고 결과를 받아 다음 단계를 결정하는 방식입니다. 실패 시 오케스트레이터가 자동으로 보상 명령을 내립니다.

![Orchestration Saga — 오케스트레이터가 흐름을 조율](images/fig-1-9.png)
*그림 1-9: Orchestration Saga — 오케스트레이터가 흐름을 조율*

오케스트레이터가 전체 흐름을 알고 있기 때문에, 실패 시 자동으로 롤백 명령을 내립니다.

두 방식을 모두 직접 구현해보면, 각각의 장단점이 자연스럽게 체감됩니다.


## 1.5 이 책의 학습 흐름

이제 전체 그림이 보입니다. 이 책은 하나의 시스템이 단계별로 진화하는 여정입니다. 각 챕터는 이전 챕터의 한계를 느끼는 것에서 시작합니다.

<!-- image-prompt: Minimal black line drawing on white background, 16:9 aspect ratio, 1280x400px. A winding path/road from left to right, like a journey map. Starting point on the far left: a small flag icon labeled "시작". Four stops along the path, each marked with a milestone marker. Stop 1: signpost "챕터 2", below it "동기 REST + 보상 트랜잭션", a small speech bubble pointing forward saying "동기 호출이 전부 묶여있어...". Stop 2: signpost "챕터 3", below it "Clean Architecture + Kubernetes", speech bubble "운영 환경이 필요해...". Stop 3: signpost "챕터 4", below it "Kafka + Orchestration Saga", speech bubble "서비스를 완전히 분리하자!". Stop 4 (destination): signpost "챕터 5", below it "WebSocket + 실시간 알림", a finish flag icon. The path gets slightly wider/bolder as it progresses, suggesting growth. No colors, no fill, just clean black lines. -->
![이 책의 학습 흐름](images/chap01-6.png)
*그림 1-10: 이 책의 학습 흐름*

**챕터 2** — 4개 서비스를 REST로 연결하고 보상 트랜잭션을 구현합니다. MSA의 뼈대를 직접 손으로 만드는 챕터입니다.

**챕터 3** — 챕터 2 코드의 아쉬운 점을 클린 아키텍처로 개선하고, Kubernetes에 올려 운영 환경을 경험합니다.

**챕터 4** — 동기 REST 호출의 한계를 Kafka로 해결합니다. 서비스가 완전히 분리되는 경험을 합니다.

**챕터 5** — 배달 기사가 완료 API를 호출하는 순간, 사용자 화면에 실시간 알림이 뜨는 시스템을 완성합니다.


## 이것만은 기억하자

- **모놀리식**은 처음에는 단순하지만, 서비스가 커지면 배포·장애·확장 문제가 생깁니다.
- **마이크로서비스**는 기능별로 서비스를 분리하여 각자 독립적으로 배포하고 확장할 수 있게 합니다.
- MSA의 핵심 과제는 **분산 트랜잭션**입니다. 각 서비스의 DB가 분리되어 있어 단일 트랜잭션으로 묶을 수 없습니다.
- **Saga 패턴**으로 분산 트랜잭션을 해결합니다. Choreography Saga(챕터 2~3)와 Orchestration Saga(챕터 4~5) 두 가지를 이 책에서 배웁니다.
- 이 책은 하나의 쇼핑몰 주문 시스템이 챕터 2부터 챕터 5까지 단계적으로 진화하는 이야기입니다.

이제 직접 코드를 작성할 시간입니다. 챕터 2에서는 4개의 서비스를 REST로 연결하고, 보상 트랜잭션을 구현해봅니다. 처음에는 단순하게 시작합니다. 그 단순함이 나중에 어떤 문제를 만드는지 직접 느껴보는 것이 챕터 2의 핵심입니다.
