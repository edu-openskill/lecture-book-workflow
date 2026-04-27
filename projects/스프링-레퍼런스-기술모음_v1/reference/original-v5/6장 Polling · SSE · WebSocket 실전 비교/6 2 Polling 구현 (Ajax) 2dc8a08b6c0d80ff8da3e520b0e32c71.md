# 6.2 Polling 구현 (Ajax)

## Polling 시퀸스 다이어그램

```mermaid
sequenceDiagram
  participant 클 as 클라이언트
  participant 서 as 서버

  Note over 클,서: 일정 시간마다<br/>클라이언트가 상태를 물어봄

  loop 매 2초
    클->>서: 상태 확인
    서-->>클: 상태 응답
  end
```

폴링은 서버가 먼저 알려주는 방식이 아니라, 클라이언트가 일정 주기마다 서버에 “지금 상태가 뭐야”라고 반복해서 요청하는 방식입니다. 그래서 구현이 단순하지만 주기가 짧을수록 요청이 많아져 서버 부담이 커질 수 있어 화면 특성에 맞게 폴링 주기를 조절하는 것이 중요합니다.

---

Polling 구현은 아래 깃주소를 git clone 하고 직접 서버를 실행하여 실습합니다.

**실습 코드**

```java
https://github.com/metacoding-11-spring-reference/spring-polling
```

---

## **1) Polling 서버 구현**

---

**(확인) 경로: src/main/java/com/metacding/polling/chat/ChatService.java**

### **1. 저장 로직(save)**

요청 → 엔티티 생성 → DB 저장

```java
@Transactional
public Chat save(ChatRequest req) {
    Chat chat = Chat.builder()
            .message(req.message())
            .build();
    return chatRepository.save(chat);
}
```

/chats POST 요청이 들어오면 컨트롤러가 이 save()를 호출해 메시지를 저장하는 구조가 됩니다.

---

### **2. 전체 조회(findAll)**

최신순 정렬로 목록을 반환합니다.

```java
public List<Chat> findAll() {
    Sort desc = Sort.by(Sort.Direction.DESC, "id");
    return chatRepository.findAll(desc);
}
```

Sort.Direction.DESC, "id": id 기준 내림차순(최신 데이터가 먼저)으로 정렬합니다. findAll(desc): 정렬 조건을 적용한 전체 목록을 반환합니다.

프론트의 loadMessages()가 2초마다 /chats GET을 호출하면 이 findAll()이 실행되고, 최신순 목록을 받아 화면을 다시 그리게 됩니다.

---

**(확인) 경로: src/main/java/com/metacding/polling/chat/ChatController.java**

```java
@RequiredArgsConstructor
@Controller
public class ChatController {

    private final ChatService chatService;

    @GetMapping("/")
    public String index() {
        return "index";
    }

    @PostMapping("/chats")
    @ResponseBody
    public ResponseEntity<Chat> save(@RequestBody ChatRequest req) {
        Chat saved = chatService.save(req);
        return ResponseEntity.ok(saved);
    }

    @GetMapping("/chats")
    @ResponseBody
    public ResponseEntity<List<Chat>> list() {
        return ResponseEntity.ok(chatService.findAll());
    }
}
```

핵심은 `/chats` 저장/조회 API입니다. `/`는 화면 진입용으로 사용합니다.

---

## **2) Front 구현 (Vanilla JS)**

**(확인) 경로: src/main/resources/templates/index.mustache**

---

### **1. 목록 조회 함수(loadMessages)**

서버에서 전체 목록을 가져와 화면 갱신합니다.

```jsx
async function loadMessages() {
  const res = await fetch("/chats");
  const data = await res.json();
  const box = document.getElementById("chat-box");

  box.innerHTML = "";
  data.forEach(chat => {
    const li = document.createElement("li");
    li.innerText = chat.message;
    box.appendChild(li);
  });
}
```

- fetch("/chats"): 채팅 목록 API를 호출합니다.
- res.json(): 응답을 JSON 배열로 변환합니다.
- box.innerHTML = "": 기존 목록을 비우고, 최신 데이터로 다시 그립니다.
- data.forEach(...): 서버에서 받은 메시지들을 <li>로 만들어 #chat-box에 붙입니다.

---

### **2. 전송 함수(sendMessage): “POST로 메시지 저장 후 목록 다시 로드”**

```jsx
async function sendMessage() {
  const messageInput = document.getElementById("message");
  const message = messageInput.value.trim();

  await fetch("/chats", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message })
  });

  messageInput.value = "";
  messageInput.focus();
  loadMessages();
}
```

입력값을 trim()으로 정리하고, /chats에 POST로 전송합니다.

서버가 저장을 끝내면 입력창을 비우고, 바로 loadMessages()를 한 번 호출해 화면을 최신 상태로 맞춥니다.

---

### **4. 시작 구간: “초기 1회 로딩 + 2초마다 반복 조회”**

```jsx
loadMessages();
setInterval(loadMessages, 2000);
```

- loadMessages(): 페이지 처음 열 때 한 번 바로 조회해서 화면을 채웁니다.
- setInterval(loadMessages, 2000): 이후 2초마다 다시 요청하여 화면을 갱신합니다.

> Polling의 핵심은 “서버가 푸시하는 게 아니라, 클라이언트가 주기적으로 묻는다”가 포인트입니다.
> 

---

## 3) 실행

서버를 실행하여 결과를 확인합니다.

![image.png](6%202%20Polling%20%EA%B5%AC%ED%98%84%20(Ajax)/image.png)

F12로 DevTools를 실행하여 /Chats 요청이 2초마다 주기적으로 요청하는걸 확인할 수 있으며 메세지를 입력하면 목록 데이터를 갱신하는 것을 확인할 수 있습니다.

---