# 4장. Postman ↔ Spring 이미지 업로드 (Base64)

4장에서는 Spring 서버로 이미지 업로드시 사용하는 포멧 Base64에 대해서 알아봅니다. 

이번 실습은 깃주소를 git clone 하고 직접 서버를 실행하여 실습합니다.

---

## **4.1 Postman 테스트 시나리오**

상세 로직을 확인하기 전 Postman으로 테스트 시나리오를 통해 전체 흐름을 먼저 확인합니다.

테스트 시나리오는 수행할 동작과 기대 결과를 정리한 목록이므로, 순서를 따라가며 검증하면 됩니다.

```java
https://github.com/metacoding-11-spring-reference/spring-base64
```

위 spring-base64 깃을 클론하여 서버를 실행합니다.

---

![image.png](4%EC%9E%A5%20Postman%20%E2%86%94%20Spring%20%EC%9D%B4%EB%AF%B8%EC%A7%80%20%EC%97%85%EB%A1%9C%EB%93%9C%20(Base64)/image.png)

### 1) Base64로 인코딩하기

파일을 Base64로 변환하는 작업이 필요합니다.

![image.png](4%EC%9E%A5%20Postman%20%E2%86%94%20Spring%20%EC%9D%B4%EB%AF%B8%EC%A7%80%20%EC%97%85%EB%A1%9C%EB%93%9C%20(Base64)/image%201.png)

1. [https://www.base64decode.org/](https://www.base64decode.org/) 웹사이트로 이동합니다.

---

![image.png](4%EC%9E%A5%20Postman%20%E2%86%94%20Spring%20%EC%9D%B4%EB%AF%B8%EC%A7%80%20%EC%97%85%EB%A1%9C%EB%93%9C%20(Base64)/image%202.png)

1. 아래로 드래그 하여 파일을 업로드 한 후 ENCODE 버튼을 클릭합니다.

---

![image.png](4%EC%9E%A5%20Postman%20%E2%86%94%20Spring%20%EC%9D%B4%EB%AF%B8%EC%A7%80%20%EC%97%85%EB%A1%9C%EB%93%9C%20(Base64)/image%203.png)

1. 텍스트 파일의 문자들을 전체 복사하여 Postman에 사용합니다.

---

### **2)** upload 하기

요청 주소는 `POST /api/images/upload` 입니다. Body는 JSON 형식으로 `fileName`과 `fileData`를 포함합니다.

```json
{
  "fileName": "cat.png",
  "fileData": "iVBORw0KGgoAAAANSUhEUgAA..."
}

```

![image.png](4%EC%9E%A5%20Postman%20%E2%86%94%20Spring%20%EC%9D%B4%EB%AF%B8%EC%A7%80%20%EC%97%85%EB%A1%9C%EB%93%9C%20(Base64)/image%204.png)

---

![image.png](4%EC%9E%A5%20Postman%20%E2%86%94%20Spring%20%EC%9D%B4%EB%AF%B8%EC%A7%80%20%EC%97%85%EB%A1%9C%EB%93%9C%20(Base64)/image%205.png)

정상 응답에서는 저장된 정보가 JSON으로 반환됩니다. 

![image.png](4%EC%9E%A5%20Postman%20%E2%86%94%20Spring%20%EC%9D%B4%EB%AF%B8%EC%A7%80%20%EC%97%85%EB%A1%9C%EB%93%9C%20(Base64)/image%206.png)

`url` 값을 브라우저에 입력하면 실제 이미지가 보이는지 확인할 수 있습니다.

![image.png](4%EC%9E%A5%20Postman%20%E2%86%94%20Spring%20%EC%9D%B4%EB%AF%B8%EC%A7%80%20%EC%97%85%EB%A1%9C%EB%93%9C%20(Base64)/image%207.png)

[http://localhost:8080/h2-console](http://localhost:8080/h2-console) 로 접속하여 DB도 정상으로 저장되었는지 확인합니다.

---

### 4) id 조회

업로드 응답에서 받은 `id`로 상세 조회를 확인합니다. 아래 `GET http://localhost:8080/1` 주소로 요청한 결과입니다.

![image.png](4%EC%9E%A5%20Postman%20%E2%86%94%20Spring%20%EC%9D%B4%EB%AF%B8%EC%A7%80%20%EC%97%85%EB%A1%9C%EB%93%9C%20(Base64)/image%208.png)

---

### **5) list 조회 테스트**

저장된 전체 이미지 목록을 조회합니다. 아래 `GET http://localhost:8080/list` 주소로 요청한 결과입니다.

![image.png](4%EC%9E%A5%20Postman%20%E2%86%94%20Spring%20%EC%9D%B4%EB%AF%B8%EC%A7%80%20%EC%97%85%EB%A1%9C%EB%93%9C%20(Base64)/image%209.png)

### 6) 웹브라우저 확인

![image.png](4%EC%9E%A5%20Postman%20%E2%86%94%20Spring%20%EC%9D%B4%EB%AF%B8%EC%A7%80%20%EC%97%85%EB%A1%9C%EB%93%9C%20(Base64)/image%2010.png)

url을 브라우저에서 요청하여 확인할 수 있습니다.

---

## **4.2 한눈에 보는 전체 흐름**

Postman에서 base64로 전송한 이미지가 서버에서 파일로 저장되고, URL로 노출되는 과정을 아래 요청흐름으로 확인해봅니다.

### **요청흐름**

![image.png](4%EC%9E%A5%20Postman%20%E2%86%94%20Spring%20%EC%9D%B4%EB%AF%B8%EC%A7%80%20%EC%97%85%EB%A1%9C%EB%93%9C%20(Base64)/image%2011.png)

1. 포스트맨에서 Spring API로 base64 포함 JSON이 들어옵니다.
2. Spring 서버는 base64를 디코딩해 바이트로 만든 뒤 파일로 저장합니다.
3. 저장된 파일의 경로 또는 저장 파일명을 DB에 기록합니다.
4. Spring 서버는 브라우저에서 바로 열 수 있는 URL을 반환합니다.
5. 브라우저에서 응답 URL을 열면 이미지가 바로 보입니다.

---

## 4.3 환경설정

### **1) 업로드 저장 경로 설계**

이 프로젝트는 `uploads` 폴더에 파일을 저장합니다. 프로젝트 폴더에 `uploads` 있는지 확인합니다.

![image.png](4%EC%9E%A5%20Postman%20%E2%86%94%20Spring%20%EC%9D%B4%EB%AF%B8%EC%A7%80%20%EC%97%85%EB%A1%9C%EB%93%9C%20(Base64)/image%2012.png)

**(확인) 경로: src/main/resources/application.properties**

```java
spring.web.resources.static-locations=file:uploads/
```

application.properties 파일에 정적 리소스 경로 설정을 함께 확인합니다.

---

### **2) 테이블/엔티티 설계**

엔티티는 DB 테이블과 매핑되는 자바 클래스입니다. 파일 경로와 생성 시각을 저장할 수 있도록 필드를 구성합니다.

![image.png](4%EC%9E%A5%20Postman%20%E2%86%94%20Spring%20%EC%9D%B4%EB%AF%B8%EC%A7%80%20%EC%97%85%EB%A1%9C%EB%93%9C%20(Base64)/image%2013.png)

**(확인) 경로: src/main/java/com/metacoding/spring_base64/image/ImageEntity.java**

```java
@Entity
@Table(name = "image_tb")
public class ImageEntity {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String uuid;
    private String fileName;
    private String url;
    private LocalDateTime createdAt;
}
```

URL 규칙은 다음과 같이 고정됩니다.

- 저장 파일명: UUID + 확장자
- URL: `/uploads/{savedFileName}`

이렇게 설계하는 이유는 아래와 같습니다.

- URL을 그대로 저장하면 응답에서 바로 사용할 수 있어 서비스 로직이 단순해집니다.
- 파일명 충돌을 피하기 위해 UUID를 사용하고, 원본 이름은 필요 시 별도 컬럼으로 확장할 수 있습니다.
- 정적 리소스 매핑 경로와 일치하므로 브라우저에서 즉시 확인할 수 있습니다.

---

## **4.4 요청/응답 설계**

![image.png](4%EC%9E%A5%20Postman%20%E2%86%94%20Spring%20%EC%9D%B4%EB%AF%B8%EC%A7%80%20%EC%97%85%EB%A1%9C%EB%93%9C%20(Base64)/image%2014.png)

### **1) 요청 DTO**

**(확인) 경로: src/main/java/com/metacoding/spring_base64/image/ImageRequest.java**

```java
public record UploadDTO(
    String fileName,
    String fileData
){}

```

**ImageRequest**는 **fileName, fileData(Base64)** 문자열을 한 묶음으로 전달하기 위한 구조입니다.

### **2) 응답 DTO**

**(확인) 경로: src/main/java/com/metacoding/spring_base64/image/ImageResponse.java**

```java
public record DTO(
        Long id,
        String uuid,
        String fileName,
        String url,
        LocalDateTime createdAt) {
    public static DTO fromEntity(ImageEntity imageEntity) {
        return new DTO(
                imageEntity.getId(),
                imageEntity.getUuid(),
                imageEntity.getFileName(),
                imageEntity.getUrl(),
                imageEntity.getCreatedAt());
    }
}
```

**ImageResponse**는 **id, uuid, fileName, url, createdAt**으로 구성되어 있으며, 엔티티를 DTO로 변환해 응답 형식을 일정하게 유지합니다.

---

## **4.5 업로드 API 구현 (Base64 → 파일)**

업로드 요청을 받아 Base64를 디코딩하고 파일로 저장하는 핵심 로직을 다룹니다. 

![image.png](4%EC%9E%A5%20Postman%20%E2%86%94%20Spring%20%EC%9D%B4%EB%AF%B8%EC%A7%80%20%EC%97%85%EB%A1%9C%EB%93%9C%20(Base64)/image%2015.png)

---

### **1) Base64 디코딩 로직**

디코딩은 인코딩된 문자열을 원본 바이트로 되돌리는 과정입니다.

**(확인) 경로: src/main/java/com/metacoding/spring_base64/image/ImageService.java**

```java
byte[] fileBytes = Base64.getDecoder().decode(uploadDTO.fileData());

```

---

### **2) 파일명/확장자 처리**

파일명은 중복을 피하기 위해 UUID를 붙여 고유하게 만들고, 확장자를 함께 저장합니다.

**(확인) 경로: src/main/java/com/metacoding/spring_base64/image/ImageService.java**

```java
String uuid = UUID.randomUUID().toString();
int dotIndex = uploadDTO.fileName().lastIndexOf('.');
String fileExtension = uploadDTO.fileName().substring(dotIndex + 1).trim().toLowerCase();
String savedFileName = uuid + "." + fileExtension;

```

---

### **3) 로컬 디스크 저장**

디코딩된 바이트 배열을 로컬 `uploads` 폴더에 파일로 저장합니다.

**(확인) 경로: src/main/java/com/metacoding/spring_base64/image/ImageService.java**

```java
Path uploadDir = Paths.get("uploads");
Path filePath = uploadDir.resolve(savedFileName);
Files.write(filePath, fileBytes);

```

---

### **3) DB 저장 로직**

저장된 파일의 URL을 만들고 엔티티에 담아 DB에 기록합니다.

**(확인) 경로: src/main/java/com/metacoding/spring_base64/image/ImageService.java**

```java
String publicUrl = "/uploads/" + savedFileName;
ImageEntity entity = ImageEntity.builder()
        .uuid(uuid)
        .fileName(savedFileName)
        .url(publicUrl)
        .createdAt(LocalDateTime.now())
        .build();
imageRepository.save(entity);
```

---

## **4.6 정적 리소스 매핑 & 조회 API**

저장된 파일을 URL로 바로 볼 수 있게 하는 방법을 다룹니다. 

![image.png](4%EC%9E%A5%20Postman%20%E2%86%94%20Spring%20%EC%9D%B4%EB%AF%B8%EC%A7%80%20%EC%97%85%EB%A1%9C%EB%93%9C%20(Base64)/image%2016.png)

### **1) 정적 리소스 경로 매핑 (/uploads/**)**

정적 리소스는 서버에서 그대로 반환되는 파일을 의미합니다. `/uploads/**` 요청을 로컬 `uploads` 폴더로 연결하면 브라우저에서 바로 확인할 수 있습니다.

**(확인) 경로: src/main/java/com/metacoding/spring_base64/_core/config/WebConfig.java**

```java
@Configuration
public class WebConfig implements WebMvcConfigurer {

    @Override
    public void addResourceHandlers(ResourceHandlerRegistry registry) {
        registry.addResourceHandler("/uploads/**")
                .addResourceLocations("file:uploads/");
    }
}
```

---

### **2) 조회 API 설계**

정적 URL 대신 조회 API로 접근할 수 있습니다. 이 프로젝트는 목록 조회와 단건 조회 엔드포인트를 제공하고 있습니다.

**(확인) 경로: src/main/java/com/metacoding/spring_base64/image/ImageController.java**

```java
@GetMapping("/list")
public List<ImageResponse.DTO> getAllImages() {
    return imageService.listAll();
}

@GetMapping("/{id}")
public ImageResponse.DTO getImageDetail(@PathVariable Long id) {
    return imageService.findById(id);
}

```

---

### **3) URL로 이미지 바로 보기**

브라우저에서 `GET /uploads/{fileName}`을 호출하면 저장된 이미지가 응답됩니다. 업로드 응답의 `url` 값을 그대로 사용하면 됩니다.

![image.png](4%EC%9E%A5%20Postman%20%E2%86%94%20Spring%20%EC%9D%B4%EB%AF%B8%EC%A7%80%20%EC%97%85%EB%A1%9C%EB%93%9C%20(Base64)/image%2017.png)

**http://localhost:8080/uploads/c5b8f37c-e767-46b1-97fd-e2d67bd79dff.png**

---

## **4.7 마무리 & 운영 팁**

운영 단계에서 주의해야 할 내용을 정리합니다. 성능, 보안, 확장 방향을 차근차근 점검하면 안정적인 서비스 운영에 도움이 됩니다.

### **1) 성능/용량 관리**

대용량 파일은 업로드 시간을 늘리고 서버 부하를 높입니다. 파일 크기 제한과 업로드 용량 정책을 미리 정해 두는 것이 안전합니다.

---

### **2) 보안 주의사항 (파일 확장자, 크기 제한)**

확장자 검증과 접근 권한 설정은 기본 보안입니다. 특히 허용 도메인을 제한하는 CORS 설정은 운영 환경에서 더 엄격하게 관리해야 합니다.

**(확인) 경로: src/main/java/com/metacoding/spring_base64/_core/config/CorsConfig.java**

```java
config.addAllowedOrigin("http://localhost:5173");
config.addAllowedMethod("*");
config.addAllowedHeader("*");
config.setAllowCredentials(true);

```

---

### **3) 클라우드 스토리지 연동 방향**

로컬 저장은 학습용으로 충분하지만, 운영에서는 S3 같은 클라우드 스토리지를 검토하는 것이 일반적입니다. 파일 관리와 백업을 자동화할 수 있기 때문입니다.

---

## 4.8 React 연동하기

아래 리액트 깃헙을 준비하였습니다.

```java
https://github.com/metacoding-11-spring-reference/react-base64
```

포스트맨은 웹브라우저 요청이 아니라서 CORS 설정이 false로 되어있습니다. 해당 설정을 위 **4.7 챕터의** ‘**2) 보안 주의사항**’ 설정에 맞춰 변경 후 리액트로 실행된 브라우저에서 이미지를 업로드 하고 조회해보세요.

---

### 1) 이미지 업로드

![image.png](4%EC%9E%A5%20Postman%20%E2%86%94%20Spring%20%EC%9D%B4%EB%AF%B8%EC%A7%80%20%EC%97%85%EB%A1%9C%EB%93%9C%20(Base64)/image%2018.png)

### 2) 이미지 목록

![image.png](4%EC%9E%A5%20Postman%20%E2%86%94%20Spring%20%EC%9D%B4%EB%AF%B8%EC%A7%80%20%EC%97%85%EB%A1%9C%EB%93%9C%20(Base64)/image%2019.png)

### 3) 이미지 상세보기

![image.png](4%EC%9E%A5%20Postman%20%E2%86%94%20Spring%20%EC%9D%B4%EB%AF%B8%EC%A7%80%20%EC%97%85%EB%A1%9C%EB%93%9C%20(Base64)/image%2020.png)

---

여기까지  **4장. Postman → Spring Base64**을 마무리하도록 하겠습니다.