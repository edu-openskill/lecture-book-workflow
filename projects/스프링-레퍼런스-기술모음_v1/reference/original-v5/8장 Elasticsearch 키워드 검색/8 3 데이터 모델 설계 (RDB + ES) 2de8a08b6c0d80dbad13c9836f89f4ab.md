# 8.3 데이터 모델 설계 (RDB + ES)

---

## **1) RDB Entity 설계**

---

**(확인) 경로: src/main/java/com/metacoding/spring_elasticsearch/device/DeviceEntity.java**

### **JPA 엔티티 정의**

```java
@Entity
@Getter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class DeviceEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String title;
    private String content;
}

```

RDB에는 정합성과 트랜잭션을 보장해야 하므로 JPA 엔티티로 데이터를 저장합니다.

---

## **2) ES Document 설계**

---

**(확인) 경로: src/main/java/com/metacoding/spring_elasticsearch/device/DeviceDocument.java**

### **Elasticsearch 문서 정의**

```java
@Document(indexName = "devices")
public class DeviceDocument {

    private Long id; // RDB PK와 동일하게 사용

    @Field(type = FieldType.Text)
    private String title;

    @Field(type = FieldType.Text)
    private String content;
}

```

`@Document`로 인덱스를 지정하고, `@Field(type = Text)`로 full-text 검색 가능한 필드를 설정합니다.

---

## **3) RDB PK를 ES 문서 식별자로 쓰는 이유**

---

**(확인) 경로: src/main/java/com/metacoding/spring_elasticsearch/ElasticSearch/ElasticSearchService.java**

### **저장 시 동일한 ID 매핑**

```java
public DeviceDocument saveDevices(DeviceDocument doc) {
    ...
    DeviceEntity saved = deviceJpaRepository.save(entity);

    DeviceDocument savedDoc = new DeviceDocument(
            saved.getId(),
            saved.getTitle(),
            saved.getContent());

    deviceSearchRepository.save(savedDoc);
    ...
}
```

RDB PK를 ES 문서 ID로 맞추면 검색 결과에서 ID만 추출해도 바로 RDB를 재조회할 수 있어 데이터 결합이 단순해집니다.

---