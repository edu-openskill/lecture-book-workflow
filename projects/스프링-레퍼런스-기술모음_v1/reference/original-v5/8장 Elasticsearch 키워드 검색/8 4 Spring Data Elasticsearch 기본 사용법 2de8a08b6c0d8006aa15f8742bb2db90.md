# 8.4 Spring Data Elasticsearch 기본 사용법

## **8.4 Spring Data Elasticsearch 기본 사용법**

Spring Data Elasticsearch는 “문서(Document) 저장 + 검색”을 스프링 방식으로 다루기 위한 모듈입니다. 이번 절에서는 실습에서 바로 쓰는 범위만 정리합니다.

---

## **1)@Document,@Field 핵심 어노테이션**

Elasticsearch는 RDB처럼 “테이블/행”이 아니라 “인덱스/문서” 구조로 저장합니다. Spring에서는 문서 모델을 자바 클래스로 만들고, 어노테이션으로 인덱스와 필드 성격을 지정합니다.

### **1. @Document**

- 이 클래스가 **어떤 인덱스에 저장되는 문서인지** 지정합니다.
- RDB 관점으로는 “테이블 이름 지정”과 비슷합니다.

```java
@Document(indexName = "devices")
public class DeviceDocument {
    ...
}
```

### **2. @Field**

- 각 필드를 Elasticsearch의 **필드 타입**으로 매핑합니다.
- 실습에서는 검색이 목적이므로 Text만 사용해도 충분합니다.

```java
@Field(type = FieldType.Text)
private String title;

@Field(type = FieldType.Text)
private String content;
```

Text는 **분석기(analyzer)** 를 통해 토큰화되어 **full-text 검색**에 적합합니다.

이 절에서는 타입을 최소로 유지하고, “검색 가능하게 매핑한다” 수준만 이해하면 됩니다.

---

## **2) ElasticsearchRepository vs 커스텀 Query**

Spring Data Elasticsearch는 크게 2가지 방식으로 검색을 구현합니다.

### **1. ElasticsearchRepository: 빠르게 CRUD + 간단 검색**

JPA Repository처럼 기본 기능을 바로 쓸 수 있습니다.

```java
public interface DeviceSearchRepository
        extends ElasticsearchRepository<DeviceDocument, Long> {
}
```

장점은 구현이 가장 간단합니다. save(), findById() 같은 기본 기능을 바로 사용합니다. 하지만 복잡한 검색 조건(가중치, 멀티필드, fuzziness 등)은 표현이 어렵습니다.

### **2. 커스텀 Query: ElasticsearchOperations로 DSL 구성**

검색 조건이 복잡해지면 ElasticsearchOperations를 사용해 **NativeQuery(DSL)** 로 직접 구성합니다.

- 예: title 가중치, multi_match, fuzziness, bool should 같은 조건

```java
public List<DeviceEntity> searchAll(String keyword) {
    NativeQuery query = NativeQuery.builder()
            .withQuery(q -> q.bool(b -> b
                    .should(s -> s.multiMatch(m -> m
                            .fields("title^3", "content")
                            .query(keyword)
                            .fuzziness("AUTO")))
                    .minimumShouldMatch("1")))
            .build();

    var deviceHits = operations.search(query, DeviceDocument.class);
    ...
}
```

장점은 검색 품질을 올리는 조건을 자유롭게 넣을 수 있습니다. **단순 저장/조회는 Repository**, **검색 최적화는 ElasticsearchOperations(커스텀 Query)** 로 접근합니다.

---

## **3) 인덱스/매핑**

Elasticsearch에서 인덱스는 문서들이 저장되는 공간이고, 매핑은 “필드 타입이 무엇인지”를 의미합니다. 실습에서는 아래 수준만 기억하면 됩니다.

- @Document(indexName="devices") → devices 인덱스에 저장됩니다.
- @Field(type=Text) → title, content는 검색 가능한 텍스트 필드로 매핑됩니다.

실행 시점에 인덱스/매핑은 설정에 따라 자동 생성될 수도 있고, 미리 만들어둘 수도 있습니다. 이 실습 범위에서는 “최소 매핑으로 검색이 되게 만든다”가 목표입니다.

---