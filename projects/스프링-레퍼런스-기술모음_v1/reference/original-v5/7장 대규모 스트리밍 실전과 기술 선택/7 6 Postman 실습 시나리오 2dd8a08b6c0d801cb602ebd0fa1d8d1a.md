# 7.6 Postman 실습 시나리오

git clone 한 spring 서버를 실행한 후 포스트맨을 실행합니다.

---

### **1. VOD 업로드 요청**

![image.png](7%206%20Postman%20%EC%8B%A4%EC%8A%B5%20%EC%8B%9C%EB%82%98%EB%A6%AC%EC%98%A4/image.png)

`POST http://localhost:8080/upload` 요청합니다.

- Body 탭에서 `form-data` 선택
- Key는 반드시 `file`
- Type은 `File`
- Value에서 업로드할 mp4 파일 선택

업로드가 완료되면 `HLS 변환 시작` 메시지가 반환됩니다.

![image.png](7%206%20Postman%20%EC%8B%A4%EC%8A%B5%20%EC%8B%9C%EB%82%98%EB%A6%AC%EC%98%A4/image%201.png)

서버에서 업로드 되는 m3u8과 .ts 파일을 확인합니다.

---

### **2. 작업 상태 조회(처리중/완료/실패)**

![image.png](7%206%20Postman%20%EC%8B%A4%EC%8A%B5%20%EC%8B%9C%EB%82%98%EB%A6%AC%EC%98%A4/image%202.png)

현재 구현은 별도 상태 API가 없으므로, 아래 방식으로 간접 확인합니다. `GET http://localhost:8080/hls/720p/video.m3u8`  요청합니다.

- 200 OK: 변환 완료
- 404/500: 변환 미완료 또는 오류

업로드 직후에는 변환이 아직 진행 중일 수 있으므로, 1~2회 정도 다시 요청해 보는 것이 좋습니다.

---

### **3. 재생 URL 확인**

브라우저에서 열면 m3u8이 내려오며, 플레이어(Hls.js)가 ts를 순차 요청합니다.

```jsx
http://localhost:8080/hls/720p/video.m3u8
```

![image.png](7%206%20Postman%20%EC%8B%A4%EC%8A%B5%20%EC%8B%9C%EB%82%98%EB%A6%AC%EC%98%A4/image%203.png)

```

http://localhost:8080/hls/1080p/video.m3u8
```

![image.png](7%206%20Postman%20%EC%8B%A4%EC%8A%B5%20%EC%8B%9C%EB%82%98%EB%A6%AC%EC%98%A4/image%204.png)

---

## 4. 웹 브라우저

크롬 브라우저에서 http://localhost:8080을 입력합니다.

![image.png](7%206%20Postman%20%EC%8B%A4%EC%8A%B5%20%EC%8B%9C%EB%82%98%EB%A6%AC%EC%98%A4/image%205.png)

F12로 DevTools를 열고 Network 탭에서 video.m3u8와 video0.ts, video1.ts 같은 요청이 순서대로 내려오는지 확인합니다.