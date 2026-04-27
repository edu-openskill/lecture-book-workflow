# 7.2 Spring REST API 프로젝트 생성

이번 실습은 **VOD 스트리밍 기술(HLS,ffmpeg)**을 다루며, 업로드된 영상을 스트리밍 재생용 파일로 바꾸고 재생하는 과정을 진행합니다.

---

아래 깃주소를 git clone 하고 직접 서버를 실행하여 실습합니다. 

**실습코드**

```java
https://github.com/metacoding-11-spring-reference/spring-hls
```

---

### **1. 의존성 설정(FFmpeg, Web, Mustache)**

**(확인) 경로: rtmp/build.gradle**

```java
// FFmpeg 명령을 자바 코드에서 다루기 쉽게 해주는 라이브러리
implementation("net.bramp.ffmpeg:ffmpeg:0.8.0")
```

웹 API, 템플릿(간단한 플레이어 페이지), 그리고 FFmpeg 자바 래퍼를 사용하도록 구성합니다.

<aside>
💡

ffmpeg란?
mp4 같은 영상을 스트리밍용으로 바꾸거나, 화질·용량·형식을 바꾸는 변환기

- mp4 → mp3(영상에서 소리만 추출)
- mp4 화질 낮추기/높이기(용량 조절)
- 영상을 잘게 쪼개서 스트리밍(HLS) 재생용 파일로 만들기(.m3u8, .ts 생성)

실습에서는 업로드된 영상을 FFmpeg로 **720p와 1080p 두 가지 화질**로 변환한 뒤, 각각의 HLS 파일(.m3u8, .ts)로 만들어 저장하는데 사용됩니다.

</aside>

---

### **2. 업로드 용량/서버 설정**

**(확인) 경로: rtmp/src/main/resources/application.propertie**

```java
#############################################
# 파일 업로드 설정
#############################################
spring.servlet.multipart.max-file-size=2GB
spring.servlet.multipart.max-request-size=2GB
```

- `max-file-size`: **파일 하나의 최대 크기** 제한입니다.
- `max-request-size`: **요청 전체 크기**(파일 + 기타 필드) 제한입니다.

업로드를 위해 multipart 제한을 2GB로 설정합니다.

---

### **3. 로컬 저장 경로 규칙**

**(확인) 경로: rtmp/src/main/java/com/metacoding/hls/service/HlsService.java**

```java
// 루트 디렉토리 경로
private final String ROOT_DIR = System.getProperty("user.dir") + "/upload/";

// 원본 비디오 파일이 저장되는 디렉토리 경로
private final String ORIGINAL_DIR = ROOT_DIR + "original/";

// 720p 해상도 변환 결과가 저장되는 디렉토리 경로
private final String CONVERT_DIR_720 = ROOT_DIR + "hls/720p/";

// 1080p 해상도 변환 결과가 저장되는 디렉토리 경로
private final String CONVERT_DIR_1080 = ROOT_DIR + "hls/1080p/";

```

1. **ROOT_DIR**는 그 아래 upload/ 폴더입니다.
2. **ORIGINAL_DIR**는 원본 파일이 저장되는 폴더입니다.
    1. 예: .../upload/original/video.mp4
3. **CONVERT_DIR_720, CONVERT_DIR_1080**는 변환된 HLS 결과가 저장되는 폴더입니다.
    1. 예: .../upload/hls/720p/video.m3u8

---

### **4. 접근 URL 규칙**

**(확인) 경로: rtmp/src/main/java/com/metacoding/hls/controller/HlsController.java**

```java
@PostMapping("/upload")
@GetMapping("/hls/{quality}/{fileName}.m3u8")
@GetMapping("/hls/{quality}/{tsSegment}.ts")
```

- HLS 재생 목록(m3u8):예: **http://localhost:8080/hls/720p/video.m3u8**
- HLS 세그먼트(ts):예: **http://localhost:8080/hls/720p/video0.ts**

quality는 720p/1080p처럼 해상도를 의미하고, fileName은 현재 프로젝트에서는 video로 고정됩니다.

---

### **5. 비동기 활성화(@EnableAsync)**

**(확인) 경로: rtmp/src/main/java/com/metacoding/hls/HlsApplication.java**

```java
@SpringBootApplication
@EnableAsync
public class HlsApplication {
    public static void main(String[] args) {
        SpringApplication.run(HlsApplication.class, args);
    }
}
```

`@EnableAsync`가 있어야 `@Async` 메서드가 **별도 스레드에서 동작**합니다.

이 설정이 없으면 비동기 메서드도 결국 동기처럼 실행됩니다.