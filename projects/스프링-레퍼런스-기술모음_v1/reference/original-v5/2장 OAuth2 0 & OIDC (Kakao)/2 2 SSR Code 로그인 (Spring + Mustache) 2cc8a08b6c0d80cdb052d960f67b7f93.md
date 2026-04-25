# 2.2 SSR: Code 로그인 (Spring + Mustache)

이번 실습은 **start 코드(기본 환경**)에서 시작해 **end 코드(단계별 커밋 포함)**를 따라가며 완성하는 방식으로 진행합니다. 각 단계에서는 안내된 커밋을 기준으로 변경된 파일(diff)을 확인하면서 그대로 적용하면 됩니다.

## 실습코드

1. start 코드

```java
https://github.com/metacoding-11-spring-reference/kakao-oauth-code-ssr-start
```

1. end 코드

```java
https://github.com/metacoding-11-spring-reference/kakao-oauth-code-ssr-end
```

---

![image.png](2%202%20SSR%20Code%20%EB%A1%9C%EA%B7%B8%EC%9D%B8%20(Spring%20+%20Mustache)/image.png)

---

## **1. OAuth 2.0 구성 요소 정의**

### **Resource Owner (사용자)**

Resource Owner는 **카카오 계정의 주인인 사용자**를 의미합니다. 사용자는 자신의 계정 정보에 대한 접근 권한을 가지고 있으며, OAuth 흐름에서 동의 화면을 통해 **우리 서비스가 자신의 정보를 사용**

**할 수 있도록 허용할지 여부를 결정합니다**. OAuth에서 사용자는 단순히 로그인하는 대상이 아니라, **권한을 위임하는 주체**입니다.

---

### **Resource Server (카카오 API 서버)**

Resource Server는 **사용자의 실제 데이터가 저장되어 있는 서버**입니다. 카카오 사용자 정보 API와 같은 엔드포인트가 이에 해당합니다. Resource Server는 아무 요청이나 허용하지 않으며, **유효한 Access Token이 포함된 요청만 처리합니다**. 즉, Access Token은 Resource Server에 접근하기 위한 필수 조건입니다.

---

### **Authorization Server (카카오 인증 서버)**

Authorization Server는 **사용자의 로그인과 동의 절차를 처리하고, 토큰을 발급하는 서버**입니다. 사용자가 카카오 계정으로 로그인하고 권한 위임에 동의하면, Authorization Server는 인가 코드(code)를 발급하고 이후 Access Token을 생성합니다. OAuth 흐름에서 인증과 권한 부여의 중심 역할을 수행합니다.

---

### **Client (우리 서비스 = 스프링 서버)**

Client는 **사용자를 대신하여 카카오 API를 호출하는 우리 서비스**를 의미합니다. Client는 사용자의 아이디와 비밀번호를 직접 처리하지 않으며, Authorization Server로부터 발급받은 Access Token을 이용해 Resource Server에 접근합니다. 이를 통해 Client는 사용자 정보를 안전하게 조회하고, 우리 서비스의 로그인 및 회원 처리를 수행합니다.

> OAuth 구조를 
카카오서버 (Authorization Server + Resource Server),
우리 서버(Client),
사용자(Resource Owner)로 **3자 구조로 이해하는 것이 좋습니다.**
> 

---

## **2. Authorization Code 방식이란 무엇인가?**

Authorization Code 방식은 사용자가 카카오 인증 서버에서 로그인과 권한 위임에 동의하면, 카카오 서버가 인가 코드(code)를 우리 서버로 전달하고, 우리 서버가 이 인가 코드를 사용해 Access Token을 발급받은 뒤, 해당 토큰으로 사용자 정보를 조회하는 구조입니다. 이 방식은 토큰이 브라우저에 노출되지 않도록 설계되어 있으며, 서버 중심으로 권한을 관리하기 때문에 보안성이 높습니다.

### 1) **브라우저는 인증의 시작점일 뿐이며, 실제 권한을 가지지 않습니다.**

사용자는 브라우저를 통해 카카오 로그인과 동의를 수행하지만, 브라우저가 최종 권한(Access Token)을 직접 받지는 않습니다. 브라우저는 오직 인가 코드(code)를 전달하는 역할만 수행합니다.

### **2) 인가 코드(code)는 권한이 아니라 ‘교환권’입니다.**

인가 코드는 사용자가 동의했다는 사실을 증명하는 임시 값이며, 이 코드 자체로는 카카오 API를 호출할 수 없습니다. 오직 서버에서만 이 코드를 사용해 Access Token으로 교환할 수 있습니다.

### **3) 실제 권한은 클라이언트에서 관리됩니다.**

우리 스프링 서버(클라이언트)는 인가 코드를 받아 카카오 인증 서버에 직접 토큰 발급을 요청합니다. 이후 발급된 Access Token을 이용해 카카오 API 서버에 접근하며, 이 과정은 전부 서버 내부에서 이루어집니다.

---

## 3. **로그인 요청(인가 코드 받기)**

사용자가 우리 서비스에서 “카카오 로그인” 버튼을 클릭하면, 실제로는 **우리 서비스가 직접 로그인 처리를 하는 것이 아니라 카카오 인증 서버로 사용자를 이동시키는 과정**입니다.

<aside>
💡

로그인 요청이라고 표현하지만, 이 단계에서 우리 서비스가 수행하는 역할은 매우 제한적입니다. 우리 서비스는 사용자의 아이디나 비밀번호를 받지 않으며, 로그인 화면을 직접 제공하지도 않습니다. 단지 **카카오 인증 서버의 인가 엔드포인트(authorize endpoint)로 브라우저를 리다이렉트**시킵니다.

</aside>

---

### 1) 문서 확인하기

![image.png](2%202%20SSR%20Code%20%EB%A1%9C%EA%B7%B8%EC%9D%B8%20(Spring%20+%20Mustache)/image%201.png)

카카오 로그인 요청을 위한 문서 확인을 위하여 **카카오 디벨로퍼 → 로그인 → 문서탭 → 카카오 로그인 → REST API**으로 이동합니다. 바로 실습을 진행하기 위해 REST API로 이동하였지만 이해하기 부분을 읽고 진행해도 무방합니다. 

---

![image.png](2%202%20SSR%20Code%20%EB%A1%9C%EA%B7%B8%EC%9D%B8%20(Spring%20+%20Mustache)/image%202.png)

아래로 드래그하여 인가 코드 요청 부분을 확인합니다. http요청을 할 수 있는 메서드 URL을 확인할 수 있습니다.

---

![image.png](2%202%20SSR%20Code%20%EB%A1%9C%EA%B7%B8%EC%9D%B8%20(Spring%20+%20Mustache)/image%203.png)

다시 아래로 드래그하여 요청 > 쿼리 파라미터를 확인할 수 있습니다. 여기서는 필수로 보내야하는 client_id, redirect_uri, response_type 을 확인할 수 있으며 그외 파라미터들도 살펴볼 수 있습니다. 

---

![image.png](2%202%20SSR%20Code%20%EB%A1%9C%EA%B7%B8%EC%9D%B8%20(Spring%20+%20Mustache)/image%204.png)

인가 코드 요청에 의한 응답 중 code를 받을 수 있으며 예제를 통해 어떻게 url을 조합해서 http 요청을 보내야하는지 확인할 수 있습니다.

```python
https://kauth.kakao.com/oauth/authorize?
response_type=code
&client_id=${REST_API_KEY}
&redirect_uri=${REDIRECT_URI}

+ 추가
&scope=profile_nickname
```

![image.png](2%202%20SSR%20Code%20%EB%A1%9C%EA%B7%B8%EC%9D%B8%20(Spring%20+%20Mustache)/image%205.png)

요청 > 쿼리 파라미터에서 scope인 동의항목 필수동의로 설정한 닉네임도 추가로 받을 수 있는 인가 코드 요청 url를 생성해봅니다.

---

### 2) spring boot 실습

---

![image.png](2%202%20SSR%20Code%20%EB%A1%9C%EA%B7%B8%EC%9D%B8%20(Spring%20+%20Mustache)/image%206.png)

1. 사용자가 로그인 페이지에 접속하면, 우리 서버는 login.mustache를 렌더링하여 로그인 화면을 제공합니다.
2. 사용자가 “카카오로 로그인하기”를 클릭하면 브라우저는 /login/kakao 경로로 요청을 보냅니다.
3. 컨트롤러는 이 요청을 처리하면서 카카오로그인주소() 메서드를 호출하여 카카오 인가 요청 URL을 생성합니다.
4. 우리 서버는 redirect: 응답을 반환하여 브라우저를 카카오 인증 서버로 이동시킵니다.
5. 브라우저는 카카오 인증 서버의 인가 엔드포인트(/oauth/authorize)로 요청을 보내며, 이 과정에서 로그인 및 동의 화면이 표시됩니다.

아직 code는 발급되지 않았고, **사용자의 동의를 받기 위한 준비 단계**입니다. 아래 순서에 따라서 실습을 진행해봅니다.

---

![image.png](2%202%20SSR%20Code%20%EB%A1%9C%EA%B7%B8%EC%9D%B8%20(Spring%20+%20Mustache)/image%207.png)

start 깃헙주소를 클론합니다. 

---

코드는 커밋 주소를 통해 코드를 확인하며 실습을 진행합니다.

**실습코드**

```python
https://github.com/metacoding-11-spring-reference/kakao-oauth-code-ssr-end/tree/1.env
```

---

```python
KAKAO_CLIENT_ID= "REST API 키"
KAKAO_CLIENT_SECRET= "Client Secret"
```

.env 파일에 자신의 "REST API 키", "Client Secret"를 입력해줍니다.

---

> 카카오 로그인창 및 동의화면 띄우기
> 

**실습코드**

```python
https://github.com/metacoding-11-spring-reference/kakao-oauth-code-ssr-end/tree/2.Authorization-code
```

---

**경로: src/main/resources/templates/login.mustache**

```java
<!doctype html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>로그인 페이지</title>
</head>
<body>
<main>
    <h1>로그인 페이지</h1>
    <hr>

    <section>
        <h2>카카오 로그인</h2>
        <a href="/login/kakao">카카오로 로그인하기</a>
    </section>
</main>
</body>
</html>

```

사용자가 로그인 페이지에서 “카카오로 로그인하기” 버튼을 클릭하면, 브라우저는 /login/kakao 경로로 HTTP 요청을 보냅니다. 

---

**경로: src/main/java/com/metacoding/spring_oauth/user/UserController.java**

```java
@GetMapping("/login/kakao")
    public String redirectToKakao() {
        return "redirect:" + userService.카카오로그인주소();
}
```

/login/kakao 요청을 받은 컨트롤러는 서비스 계층의 카카오로그인주소() 메서드를 호출하여, 카카오 인증 서버로 이동할 인가 요청 URL을 생성합니다. 이후 redirect: 응답을 통해 브라우저를 해당 URL로 이동시킵니다.

---

**경로: src/main/java/com/metacoding/spring_oauth/user/UserService.java**

```java
    @Value("${kakao.authorize-uri}")
    private String kakaoAuthorizeUri;

    @Value("${kakao.client-id}")
    private String kakaoClientId;

    @Value("${kakao.redirect-uri}")
    private String kakaoRedirectUri;
```

카카오 OAuth 연동을 위해 application.yml(또는 application.properties)에 등록한 환경변수 값을 자바 코드에서 사용하기 위해, UserService.java에서 @Value 어노테이션을 사용해 해당 설정 값을 주입합니다.

---

```java
# --------------------------------------
# 카카오 OAuth 2.0 인가 요청 주소
# --------------------------------------
# 사용자가 "카카오 로그인" 버튼을 눌렀을 때
# 브라우저를 리다이렉트시키는 카카오 인증 페이지 주소
# → 여기서 사용자 로그인 + 권한 동의 화면이 표시됨
kakao.authorize-uri=https://kauth.kakao.com/oauth/authorize

# --------------------------------------
# 카카오 로그인 완료 후 콜백(리다이렉트) 주소
# --------------------------------------
# 사용자가 카카오 로그인 및 동의를 완료하면
# 카카오가 인가 코드(code)를 함께 전달해주는 우리 서버 주소
# → 이 주소에서 code를 받아 access token 교환을 시작함
kakao.redirect-uri=http://localhost:8080/oauth/callback

```

[application.properties](http://application.properties) 파일에는 카카오 디벨로퍼의 앱에서 리다이렉트 uri를 등록할때 설정했던 “http://localhost:8080/oauth/callback”주소와 인가 요청 주소가 등록되어 있습니다.

---

```java
[카카오 로그인 인가 코드 요청]
예제)
https://kauth.kakao.com/oauth/authorize
?response_type=code
&client_id=${REST_API_KEY}
&redirect_uri=${REDIRECT_URI}
&scope=profile_nickname
```

scope로 동의항목인 닉네임도 추가로 설정한 인가 코드 요청 url입니다.

---

```java
public String 카카오로그인주소() {
        String encodedRedirect = URLEncoder.encode(kakaoRedirectUri, StandardCharsets.UTF_8);
        return kakaoAuthorizeUri
                + "?response_type=code"
                + "&client_id=" + kakaoClientId
                + "&redirect_uri=" + encodedRedirect
                + "&scope=profile_nickname";
}
```

이 메서드는 위에서 작성한 인가 코드 요청 url을 자바로 만든 카카오로그인주소() 매서드입니다. 이제 사용자가 카카카오로 로그인하기 버튼을 클릭하여 /login/kakao 요청을 하게 되면 카카오로그인주소() 메서드가 호출이 되면서  카카오 로그인창을 브라우저에서 확인할 수 있습니다.

아래 서버를 실행하여 브라우저를 통해 카카오 로그인 창 및 동의화면을 확인합니다.

---

![image.png](2%202%20SSR%20Code%20%EB%A1%9C%EA%B7%B8%EC%9D%B8%20(Spring%20+%20Mustache)/image%208.png)

서버를 실행하여 **카카오로 로그인하기**를 클릭합니다.

---

![image.png](2%202%20SSR%20Code%20%EB%A1%9C%EA%B7%B8%EC%9D%B8%20(Spring%20+%20Mustache)/image%209.png)

![image.png](2%202%20SSR%20Code%20%EB%A1%9C%EA%B7%B8%EC%9D%B8%20(Spring%20+%20Mustache)/image%2010.png)

카카오 로그인 창을 확인할 수 있으며 로그인을 완료하면 동의화면이 렌더링되고 동의하기 항목에 닉네임이 포함되어 있는걸 확인할 수 있습니다.

---

```java
https://kauth.kakao.com/oauth/authorize
?response_type=code
&client_id=4c9035da98c350e01a23cfeeab4a0f4a
&redirect_uri=http%3A%2F%2Flocalhost%3A8080%2Foauth%2Fcallback
&scope=profile_nickname
```

브라우저의 주소를 확인하게 되면 카카오로그인주소() 메서드로 만들었던 인가 코드 요청 url을 확인할 수 있습니다.

---

> 인가코드 확인하기
> 

![image.png](2%202%20SSR%20Code%20%EB%A1%9C%EA%B7%B8%EC%9D%B8%20(Spring%20+%20Mustache)/image%2011.png)

1. 사용자가 카카오 로그인과 권한 동의를 완료합니다.
2. 카카오 인증 서버는 인가 코드(code)를 포함해 브라우저를 redirect_uri로 이동시킵니다.
3. 브라우저는 우리 서버의 /oauth/callback으로 인가 코드를 전달합니다.
4. 우리 서버는 @RequestParam으로 인가 코드를 수신합니다.
5. 우리 서버는 redirect 응답을 반환해 브라우저를 다음 페이지로 이동시킵니다.

이 단계까지가 **“로그인 요청(인가 코드 받기)” 단계**이며, Access Token얻기 전까지의 단계입니다.

---

**경로: src/main/java/com/metacoding/spring_oauth/user/UserController.java**

```java
@GetMapping("/oauth/callback")
    public String kakaoCallback(@RequestParam("code") String code) {
        System.out.println("code : " + code);
        return "redirect:/";
}
```

카카오 로그인과 동의가 완료되면, 카카오 인증 서버는 인가 코드(code)를 포함하여 우리 서버의 콜백 주소로 브라우저를 리다이렉트합니다. 여기서 리다이렉트 uri는 카카오 디벨로퍼 앱에 등록되어있어야 합니다.

---

서버를 다시 실행 한 후 카카오 로그인을 진행합니다.

![image.png](2%202%20SSR%20Code%20%EB%A1%9C%EA%B7%B8%EC%9D%B8%20(Spring%20+%20Mustache)/image%2012.png)

@RequestParam 들어온 인가 코드 **code**를 확인할 수 있습니다. 

여기까지가 카카오의 권한을 얻기전 인가 코드를 얻는 과정이었습니다. 이제 인가 코드로 권한을 위임받아 사용자의 정보를 조회해보도록 하겠습니다.

---

## 4.  code로 Access Token 발행하기

로그인 인가 코드를 요청한 후 /oauth/callback 으로 수신받은 code로 token을 발행합니다.

**실습코드**

```python
https://github.com/metacoding-11-spring-reference/kakao-oauth-code-ssr-end/tree/3.Access-Token
```

---

![image.png](2%202%20SSR%20Code%20%EB%A1%9C%EA%B7%B8%EC%9D%B8%20(Spring%20+%20Mustache)/image%2013.png)

---

**경로: src/main/java/com/metacoding/spring_oauth/user/UserController.java**

```java
@GetMapping("/oauth/callback")
  public String kakaoCallback(@RequestParam("code") String code) {
			userService.카카오로그인(code);
      return "redirect:/post/list";
}
```

kakaoCallback 컨트롤러는 인가 코드 요청 후 code를 받아 userService의 카카오로그인() 메서드로 주입하여 
Access Token을 발급받습니다.

---

**경로: src/main/java/com/metacoding/spring_oauth/user/KakaoResponse.java**

```java
public class KakaoResponse {

    public static record TokenDTO(
                    @JsonProperty("token_type") String tokenType,
                    @JsonProperty("access_token") String accessToken,
                    @JsonProperty("expires_in") Long expiresIn,
                    @JsonProperty("refresh_token") String refreshToken,
                    @JsonProperty("refresh_token_expires_in") Long refreshTokenExpiresIn,
                    String scope) {
    }
}

```

토큰 요청에 대한 응답을 받기 위해 **KakaoResponse.java**에 **TokenDTO**를 생성합니다.

---

**경로: src/main/java/com/metacoding/spring_oauth/user/UserService.java**

```java
@Transactional
public UserResponse.DTO 카카오로그인(String code) {
    KakaoResponse.TokenDTO tokenDTO = kakaoApiClient.getKakaoToken(code);
    System.out.println("tokenDTO = " + tokenDTO);
    return null;
}
```

토큰 요청을 위해 카카오 로그인 메서드를 생성합니다.

---

**경로: src/main/java/com/metacoding/spring_oauth/_core/utils/KakaoApiClient.java**

```java
@Component
public class KakaoApiClient {

    private final RestTemplate restTemplate = new RestTemplate();

    @Value("${kakao.client-id}")
    private String kakaoClientId;

    @Value("${kakao.redirect-uri}")
    private String kakaoRedirectUri;

    @Value("${kakao.token-uri}")
    private String kakaoTokenUri;

    @Value("${kakao.client-secret:}")
    private String kakaoClientSecret;

    public KakaoResponse.TokenDTO getKakaoToken(String code) {
        HttpEntity<MultiValueMap<String, String>> request = createTokenRequest(code);
        ResponseEntity<KakaoResponse.TokenDTO> response = restTemplate.exchange(
                kakaoTokenUri,
                HttpMethod.POST,
                request,
                KakaoResponse.TokenDTO.class);
        return response.getBody();
    }

    private HttpEntity<MultiValueMap<String, String>> createTokenRequest(String code) {
        HttpHeaders headers = new HttpHeaders();
        headers.add("Content-Type", "application/x-www-form-urlencoded;charset=utf-8");

        MultiValueMap<String, String> body = new LinkedMultiValueMap<>();
        body.add("grant_type", "authorization_code");
        body.add("client_id", kakaoClientId);
        body.add("redirect_uri", kakaoRedirectUri);
        body.add("code", code);
        if (StringUtils.hasText(kakaoClientSecret)) {
            body.add("client_secret", kakaoClientSecret);
        }

        return new HttpEntity<>(body, headers);
    }

}
```

RestTemplate를 사용하여 getKakaoToken()메서드에서 https://kauth.kakao.com/oauth/token 주소로 POST 요청을 보내며 createTokenRequest()메서드는 repuest header와 body를 구성합니다.

---

서버를 실행하여 카카오로 로그인하기를 진행하여 출력값을 확인합니다.

![image.png](2%202%20SSR%20Code%20%EB%A1%9C%EA%B7%B8%EC%9D%B8%20(Spring%20+%20Mustache)/image%2014.png)

카카로 로그인을 진행하면 터미널에서 응답값을 확인할 수 있습니다.

![image.png](2%202%20SSR%20Code%20%EB%A1%9C%EA%B7%B8%EC%9D%B8%20(Spring%20+%20Mustache)/image%2015.png)

이동한 /post/list 페이지에서 ‘사용자 조회가 되지 않았습니다.’를 확인할 수 있습니다. 다음은 발급 받은 토큰으로 사용자 조회를 진행하여 유저정보를 확인해보겠습니다.

---

## 5. 사용자 조회 및 세션관리

토큰을 받았다는건 카카오에게 사용자를 조회할 수 있는 권한을 위임받은 단계입니다. 이제 이 토큰으로 사용자의 정보를 조회하고 조회된 정보를 우리 서버 세션에서 관리할 수 있도록 합니다.

**실습코드**

```python
https://github.com/metacoding-11-spring-reference/kakao-oauth-code-ssr-end/tree/4.user-session
```

---

![image.png](2%202%20SSR%20Code%20%EB%A1%9C%EA%B7%B8%EC%9D%B8%20(Spring%20+%20Mustache)/image%2016.png)

---

**경로: src/main/java/com/metacoding/spring_oauth/user/UserController.java**

```java
@GetMapping("/oauth/callback")
    public String kakaoCallback(@RequestParam("code") String code) {
        UserResponse.DTO sessionUser = userService.카카오로그인(code);
        session.setAttribute("sessionUser", sessionUser);
        return "redirect:/post/list";
    }
```

토큰으로 사용자를 조회가 완료되면 세션에서 관리하도록 합니다.

---

**경로:  src/main/java/com/metacoding/spring_oauth/user/KakaoResponse.java**

```java
public class KakaoResponse {

    public static record KakaoUserDTO(
                    Long id,
                    @JsonProperty("connected_at") Timestamp connectedAt,
                    Properties properties) {
    }

    public static record Properties(
                    String nickname) {
    }

}
```

**KakaoResponse**에 사용자 조회 요청에 대한 응답 DTO인 KakaoUserDTO,Properties를 생성합니다. 

---

**경로: src/main/java/com/metacoding/spring_oauth/user/UserService.java**

```java
@Transactional
public UserResponse.DTO 카카오로그인(String code) {
    KakaoResponse.TokenDTO token = kakaoApiClient.getKakaoToken(code);
    KakaoResponse.KakaoUserDTO kakaoUser = kakaoApiClient.getKakaoUser(token.accessToken());
   
    String username = kakaoUser.properties().nickname();

    User user = userRepository.findByUsername(username)
            .orElseGet(() -> userRepository.save(
                    User.builder()
                            .username(username)
                            .password(UUID.randomUUID().toString())
                            .email("kakao" + kakaoUser.id() + "@kakao.com")
                            .provider("kakao")
                            .build()));

    return new UserResponse.DTO(user);
}
```

카카오로그인()는 카카오에서 조회한 사용자 정보를 우리 서버 DB에 저장합니다.

---

**경로: src/main/java/com/metacoding/spring_oauth/_core/utils/KakaoApiClient.java**

```java
@Value("${kakao.user-info-uri}")
private String kakaoUserInfoUri;
```

환경 변수에 등록된  [https://kapi.kakao.com/v2/user/me](https://kapi.kakao.com/v2/user/me)를 주입받습니다.

---

```java
public KakaoResponse.KakaoUserDTO getKakaoUser(String accessToken, RestTemplate restTemplate) {
    HttpEntity<MultiValueMap<String, String>> request = createUserRequest(accessToken);

    ResponseEntity<KakaoResponse.KakaoUserDTO> response = restTemplate.exchange(
            kakaoUserInfoUri,
            HttpMethod.GET,
            request,
            KakaoResponse.KakaoUserDTO.class);
    return response.getBody();
}

private HttpEntity<MultiValueMap<String, String>> createUserRequest(String accessToken) {
    HttpHeaders headers = new HttpHeaders();
    headers.add("Content-Type", "application/x-www-form-urlencoded;charset=utf-8");
    headers.add("Authorization", "Bearer " + accessToken);

    return new HttpEntity<>(headers);
}
```

getKakaoUser()는 유저정보를 조회하기 위한 메서드 이며, createUserRequest()는 발급 받은 Access Token을 header에 넣어 요청할 수 있는 repuest를 만듭니다.

---

서버를 실행하여 카카오로그인하기를 진행합니다.

![image.png](2%202%20SSR%20Code%20%EB%A1%9C%EA%B7%B8%EC%9D%B8%20(Spring%20+%20Mustache)/image%2017.png)

게시글 목록 페이지에서 Access Token으로 사용자 조회된 페이지를 확인할 수 있습니다.

---

여기까지 Authorization Code 흐름을 실습으로 확인하였습니다.