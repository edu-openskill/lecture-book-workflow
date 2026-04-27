# 8.8 검색 실습(기본 + Fuzzy)

해당 실습은 제공된 깃 주소로 서버를 실행하며 Kibana로 elasticsearch 조회, 포스트맨으로 spring DB 조회를 실습합니다.

---

## **1) 실행 환경 준비**

### **1. Docker Compose 실행 (ES + Kibana + Spring app)**

![image.png](8%208%20%EA%B2%80%EC%83%89%20%EC%8B%A4%EC%8A%B5(%EA%B8%B0%EB%B3%B8%20+%20Fuzzy)/image.png)

`docker compose up -d`로 ES/Kibana/Spring app이 함께 올라오며, Spring은 `http://localhost:8080`에서 동작합니다. ES가 준비될 때까지 잠시 대기 후 브라우저에서 healthCheck 하여 연결성공 메세지를 확인합니다.

---

### **2. Elasticsearch 응답 확인**

이미지

![image.png](8%208%20%EA%B2%80%EC%83%89%20%EC%8B%A4%EC%8A%B5(%EA%B8%B0%EB%B3%B8%20+%20Fuzzy)/image%201.png)

`http://localhost:9200` 에서 클러스터 정보가 JSON으로 반환되면 ES가 정상 동작 중인걸 확인할 수 있습니다.

---

## **2) 데이터 저장 (샘플 입력)**

---

**(확인) 경로: src/main/java/com/metacoding/spring_elasticsearch/ElasticSearch/ElasticSearchSearchController.java**

### **1. 여러 건 저장 API 확인**

```java
...
@PostMapping("/devices")
public List<DeviceDocument> saveDevices(@RequestBody List<DeviceDocument> docs) {
    return elasticSearchService.saveDeviceList(docs);
}
...

```

---

### **2. 샘플 데이터 저장 요청**

**샘플 데이터** json은 실습 깃헙 `README.md` 파일을 확인해주세요.

![image.png](8%208%20%EA%B2%80%EC%83%89%20%EC%8B%A4%EC%8A%B5(%EA%B8%B0%EB%B3%B8%20+%20Fuzzy)/image%202.png)

`POST http://localhost:8080/devices` 요청합니다. RDB와 ES에 동시에 저장되며, 이후 검색에 바로 사용됩니다. 

![image.png](8%208%20%EA%B2%80%EC%83%89%20%EC%8B%A4%EC%8A%B5(%EA%B8%B0%EB%B3%B8%20+%20Fuzzy)/image%203.png)

RDB(h2)에서 정상적으로 확인할 수 있습니다.

---

## **3) Kibana에서 확인하기**

키바나는 Elasticsearch에 저장된 인덱스와 문서를 브라우저에서 바로 확인할 수 있는 관리·디버그 도구입니다. 이 실습에서는 Spring이 Elasticsearch에 데이터를 제대로 저장했는지 빠르게 검증하고, 검색 쿼리를 직접 실행해 결과가 정상인지 확인하는 용도로 사용합니다. 

Kibana에서 검색이 정상인데 Spring API에서만 결과가 안 나오면 Elasticsearch 자체는 정상 동작 중이므로, Spring의 연결 주소 설정(localhost vs elasticsearch)이나 쿼리 구성 문제로 원인을 좁혀 디버그할 수 있습니다.

---

### **3.1 Kibana 접속**

![image.png](8%208%20%EA%B2%80%EC%83%89%20%EC%8B%A4%EC%8A%B5(%EA%B8%B0%EB%B3%B8%20+%20Fuzzy)/image%204.png)

브라우저에서 Kibana에 접속합니다.

- http://localhost:5601

---

### **3.2 Dev Tools 열기**

![image.png](8%208%20%EA%B2%80%EC%83%89%20%EC%8B%A4%EC%8A%B5(%EA%B8%B0%EB%B3%B8%20+%20Fuzzy)/image%205.png)

Kibana에서 검색바에서 **Dev Tools**를 엽니다.

---

![image.png](8%208%20%EA%B2%80%EC%83%89%20%EC%8B%A4%EC%8A%B5(%EA%B8%B0%EB%B3%B8%20+%20Fuzzy)/image%206.png)

 Dev Tools는 Elasticsearch에 쿼리를 직접 실행할 수 있는 콘솔입니다.

---

### **3.3 기본 검색 Multi Match**

multi_match는 여러 필드를 동시에 검색하는 쿼리입니다. title^3은 제목이 더 중요하므로 점수를 더 크게 주겠다는 의미입니다.

```sql
GET /devices/_search
{
  "query": {
    "multi_match": {
      "query": "갤럭시",
      "fields": ["title^3", "content"]
    }
  }
}
```

- query: 검색어
- fields: 검색 대상 필드
- title^3: 제목 매칭에 가중치 부여

---

### **3.4 Kibana에서 삽입하면 Spring 서버에는 저장되지 않습니다**

Kibana Dev Tools에서 실행하는 삽입 요청은 **Elasticsearch에 직접 저장**하는 방식입니다. 이 요청은 Spring 서버를 거치지 않으므로, Spring이 사용하는 RDB에는 저장되지 않습니다.

- Kibana에서 저장하면: Elasticsearch에만 반영됩니다.
- Spring API로 저장하면: RDB에 저장한 뒤 Elasticsearch에도 저장하는 구조(dual write)로 만들 수 있습니다.

### **Kibana에서 문서 삽입**

![image.png](8%208%20%EA%B2%80%EC%83%89%20%EC%8B%A4%EC%8A%B5(%EA%B8%B0%EB%B3%B8%20+%20Fuzzy)/image%207.png)

```
POST /devices/_doc
{
  "id": 11,
  "title": "갤럭시 S25",
  "content": "신형 갤럭시 모델"
}
```

![image.png](8%208%20%EA%B2%80%EC%83%89%20%EC%8B%A4%EC%8A%B5(%EA%B8%B0%EB%B3%B8%20+%20Fuzzy)/image%208.png)

문서를 삽입 후 RDB(h2)를 확인하면 DB에는 인덱스가 여전히 10까지만 있는 걸 확인할 수 있습니다.

---

### **3.5 Fuzzy 검색 확인**

Fuzzy는 오타를 허용하는 검색 방식입니다. 아래 예시는 갈럭시처럼 오타가 있어도 결과가 나오는지 확인합니다.

### **오타 키워드(Fuzzy) 검색**

![image.png](8%208%20%EA%B2%80%EC%83%89%20%EC%8B%A4%EC%8A%B5(%EA%B8%B0%EB%B3%B8%20+%20Fuzzy)/image%209.png)

```sql
GET /devices/_search
{
  "query": {
    "multi_match": {
      "query": "갈럭시",
      "fields": ["title^3", "content"],
      "fuzziness": "AUTO"
    }
  }
}
```

- 오타 검색에서도 결과가 나오면 Elasticsearch의 Fuzzy 동작이 정상입니다.
- Kibana에서는 되는데 Spring에서는 안 되면, Spring의 ES 연결 주소 또는 쿼리 구성을 먼저 점검합니다.

다양한 검색어는 `README.md`를 확인해주세요.

---

## **4) Postman 실습**

---

### **1. 정상 키워드 검색**

![image.png](8%208%20%EA%B2%80%EC%83%89%20%EC%8B%A4%EC%8A%B5(%EA%B8%B0%EB%B3%B8%20+%20Fuzzy)/image%2010.png)

`http://localhost:8080/search?keyword=스마트폰`정상 키워드로 검색했을 때 관련 검색어가 나오면 기본 검색이 정상입니다.

---

### **2. 오타 검색 테스트**

![image.png](8%208%20%EA%B2%80%EC%83%89%20%EC%8B%A4%EC%8A%B5(%EA%B8%B0%EB%B3%B8%20+%20Fuzzy)/image%2011.png)

`http://localhost:8080/search?keyword=스마크폰` 응답이 정상 검색과 동일하게 나오면 Fuzzy가 정상 동작하는 것입니다.

---

## **5) 결과 비교 포인트**

---

- **정상 키워드 vs 오타 키워드**: 정상 검색과 유사한 결과가 나오면 Fuzzy 효과가 확인됩니다.
- **정확도**: 필요 이상으로 결과가 늘어나면 Fuzzy 적용 범위를 좁힙니다.
- **응답 지연**: 오타 허용은 비용이 있으니 응답 시간이 늘어나는지 확인합니다.

---

## **6) 결과가 안 나올 때 체크리스트**

---

- ES가 실행 중인지 확인: `http://localhost:9200`
- Spring 설정 확인: Docker 실행 시 `spring.elasticsearch.uris=http://elasticsearch:9200`, 로컬 실행 시 `http://localhost:9200`
- 데이터 저장이 정상인지 확인: `/devices` 저장 응답

---