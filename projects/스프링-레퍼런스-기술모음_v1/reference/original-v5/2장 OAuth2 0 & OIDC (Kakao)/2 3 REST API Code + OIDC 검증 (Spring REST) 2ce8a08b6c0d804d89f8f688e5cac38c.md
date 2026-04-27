# 2.3 REST API: Code + OIDC 검증 (Spring REST)

이번 실습에서는 Authorization code 방식과 OIDC(OpenID connect)를 결합하여 사용하는 구조에 대해서 알아보겠습니다.

**start 코드(기본 환경**)에서 시작해 **end 코드(단계별 커밋 포함)**를 따라가며 완성하는 방식으로 진행합니다. 각 단계에서는 안내된 커밋을 기준으로 변경된 파일(diff)을 확인하면서 그대로 적용하면 됩니다.

---

## 실습코드

1. start 코드

```java
https://github.com/metacoding-11-spring-reference/kakao-oauth-code-oidc-start
```

1. end 코드 

```java
https://github.com/metacoding-11-spring-reference/kakao-oauth-code-oidc-end
```

---

## **1) 대칭키 vs 공개키 (Symmetric vs Public Key)**

```java
그림?
사용자  -> 서버 : 같은 비밀번호로 잠금/암호화
서버    -> 사용자 : 같은 비밀번호로 열기/복호화
```

1. **대칭키란**
    
    대칭키는 **같은 비밀번호로 잠그고 여는 방식**입니다. 문에 비밀번호를 설정해 두고, 그 비밀번호를 아는 사람만 들어오는 것과 같습니다. 빠르다는 장점이 있지만, 그 비밀번호를 **어떻게 안전하게 전달하는냐에 따라 구조가 정해집니다.**
    

```java
그림?
사용자  -> 서버 : 공개키(자물쇠)로 잠금/암호화
서버    -> 사용자 : 개인키(열쇠)로 열기/복호화
```

1. **공개키란**
    
    공개키는 **자물쇠와 열쇠 방식**입니다. 자물쇠는 누구에게나 공개할 수 있고, 열쇠는 나만 가지고 있습니다.
    
    상대방은 자물쇠로 잠그기만 하고, 열쇠를 가진 사람만 열 수 있습니다. 따라서 **비밀번호를 직접 주고받지 않아도 안전합니다**.
    

---

## **2) OIDC란?**

> **OIDC(OpenID Connect)는 로그인(인증)을 표준화한 프로토콜입니다.**
> 

OIDC는 권한을 빌려 쓰는 방식이 아니라, 카카오나 구글이 확인해 준 ‘완전한 신분증(ID Token)’을 받아 로그인하는 규칙입니다.

OIDC에서는 우리 서비스가 사용자의 권한을 받아서 뭔가를 하는 것이 아닙니다. 대신 카카오나 구글이 사용자의 로그인을 직접 확인한 뒤,“이 사용자는 누구이며, 언제 로그인했고, 지금도 유효하다”라는 정보가 담긴신분증(ID Token)을 발급해 줍니다.

즉, 사용자에 대한 신분을 카카오, 구글이 증명해주는 규칙이라고 생각하면 됩니다.

---

## 3) **Code + OIDC 방식 프로세스 이해**

![image.png](2%203%20REST%20API%20Code%20+%20OIDC%20%EA%B2%80%EC%A6%9D%20(Spring%20REST)/image.png)

기존 **Code 방식**에서는 우리 서버가 **code로 Access Token**을 발급받은 뒤, 그 Access Token을 사용해 **카카오 서버에 사용자 조회 요청**을 했습니다.

반면 **Code + OIDC 방식**에서는 우리 서버가 **Access Token 대신 사용자 정보가 포함된 ID Token**을 받아

**추가 사용자 조회 없이 로그인 처리를 완료**할 수 있습니다. 필요하면 조회를 붙일 수도 있습니다.

---

## 4) Spring boot 실습

이제는 우리 서버에 어떻게 적용하는지 흐름과 구조를 살펴보겠습니다. 해당 실습은 포스트맨을 사용합니다. 또한, 입력해야하는 코드와 설명이 필요한 코드는 확인 및 입력으로 표시하겠습니다.

**실습코드 - start git**

```java
https://github.com/metacoding-11-spring-reference/kakao-oauth-code-oidc-start
```

---

![image.png](2%203%20REST%20API%20Code%20+%20OIDC%20%EA%B2%80%EC%A6%9D%20(Spring%20REST)/image%201.png)

---

### 1. JWT 발급 및 검증

이번 code + oidc 방식에서는 jwt를 생성하고 검증하는 로직이 추가 되었습니다. 아래 코드들은 이미 start 코드 깃헙주소에 준비되어있으니 확인만 해주시면 됩니다.

실습코드

```java
https://github.com/metacoding-11-spring-reference/kakao-oauth-code-oidc-end/tree/1.JWT-발급-및-검증
```

---

**(확인) 경로: build.gradle**

```java
// https://mvnrepository.com/artifact/com.nimbusds/nimbus-jose-jwt
implementation("com.nimbusds:nimbus-jose-jwt:10.5")
```

nimbusds(님부스) 라이브러리는 OIDC에서 받은 **ID Token(JWT)** 을 “검증”하기 위해 사용합니다. 단순히 공개키를 조회하는 용도만이 아니라 **JWT 파싱, JWKS 다운로드/파싱, RSA 공개키로 서명 검증, 클레임 추출 등** 작업을 한 번에 처리할 수 있게 해줍니다.

---

**(확인) 경로: src/main/java/com/metacoding/spring_oauth_oidc/_core/utils/JwtUtil.java**

```java
/**
 * JwtUtil
 * - OAuth/OIDC 로그인 성공 "이후" 우리 서비스에서 사용할 JWT를 만든다.
 * - 이후 요청에서 넘어온 JWT를 검증해서 "누가 요청했는지" 복원한다.
 */
public class JwtUtil {

    // HTTP 헤더 이름 (Authorization: Bearer {JWT})
    public static final String HEADER = "Authorization";

    // Authorization 헤더에서 JWT 앞에 붙는 접두어
    public static final String TOKEN_PREFIX = "Bearer ";

    // HS256 서명용 대칭키(최소 32바이트 이상 권장)
    // 운영에서는 .env / 환경변수로 빼서 관리해야 한다.
    private static final String SECRET = "metacoding-secret-key-should-be-long";

    // 만료 시간(7일) = 밀리초 단위
    private static final long EXPIRATION_TIME = 1000L * 60 * 60 * 24 * 7;

    /**
     * JWT 생성
     * - 로그인 성공 후 user 정보를 기반으로 "우리 서비스용 토큰"을 만든다.
     * - 토큰에는 username(sub), 발급시간(iat), 만료시간(exp), 사용자 id(claim)를 담는다.
     */
    public static String create(User user) {
        try {
            // 1) Payload(Claims) 구성: 토큰에 넣을 사용자 정보와 시간 정보
            JWTClaimsSet claims = new JWTClaimsSet.Builder()
                    .subject(user.getUsername()) // sub: 이 토큰의 주인(대표 식별자)
                    .issueTime(new Date()) // iat: 발급 시간
                    .expirationTime(new Date(System.currentTimeMillis() + EXPIRATION_TIME)) // exp: 만료 시간
                    .claim("id", user.getId()) // 우리 서비스에서 쓰는 사용자 PK
                    .build();

            // 2) Header + Claims 결합 (HS256 = 대칭키 서명)
            SignedJWT signedJWT = new SignedJWT(
                    new JWSHeader(JWSAlgorithm.HS256),
                    claims);

            // 3) SECRET으로 서명 → 위조 방지
            signedJWT.sign(new MACSigner(SECRET));

            // 4) Authorization 헤더에 바로 넣을 수 있게 "Bearer "를 붙여 반환
            return TOKEN_PREFIX + signedJWT.serialize();

        } catch (JOSEException e) {
            throw new RuntimeException("JWT 생성 실패", e);
        }
    }

    /**
     * JWT 검증
     * - 클라이언트가 보낸 JWT가 위조되지 않았는지(서명) 확인한다.
     * - 검증에 성공하면 토큰 안의 정보로 User(인증 주체)를 복원한다.
     */
    public static User verify(String jwt) {
        try {
            // 1) 문자열 JWT → SignedJWT 파싱
            SignedJWT signedJWT = SignedJWT.parse(jwt);

            // 2) 서명 검증: SECRET으로 검증 실패하면 위조/변조 토큰
            if (!signedJWT.verify(new MACVerifier(SECRET))) {
                throw new RuntimeException("JWT 서명 검증 실패");
            }

            // 3) Claims(Payload) 추출
            JWTClaimsSet claims = signedJWT.getJWTClaimsSet();

            // 4) 우리가 create()에서 넣어둔 값들 꺼내기
            Integer id = claims.getIntegerClaim("id");
            String username = claims.getSubject();

            // 5) 토큰 정보로 User 복원 (필요하면 여기서 DB 조회를 추가할 수도 있다)
            return User.builder()
                    .id(id)
                    .username(username)
                    .build();

        } catch (ParseException | JOSEException e) {
            throw new RuntimeException("JWT 검증 실패", e);
        }
    }
}
```

JwtUtil 클래스에서는 카카오 인증 서버에게 ID Token을 받아 포함되어 있는 사용자 정보를 우리 서비스의 jwt로 생성하여 사용하는 create() 메서드와  클라이언트에서 요청받은 jwt를 검증하기 위한 verify() 메서드가 있습니다.

---

**(확인) 경로 : src/main/java/com/metacoding/spring_oauth_oidc/_core/utils/JwtProvider.java**

```java
@Slf4j
@Component
public class JwtProvider {

    /**
     * 요청 헤더에서 JWT를 꺼내 바로 검증하고 User 복원
     */
    public User verifyFromHeader(HttpServletRequest request) {
        String token = resolveToken(request);
        if (token == null || token.isBlank()) {
            throw new RuntimeException("Authorization 헤더에 Bearer 토큰이 없습니다.");
        }
        return JwtUtil.verify(token);
    }

    /**
     * 요청 헤더에서 JWT 토큰 추출
     */
    public String resolveToken(HttpServletRequest request) {
        String bearerToken = request.getHeader(JwtUtil.HEADER);
        if (bearerToken != null && bearerToken.startsWith(JwtUtil.TOKEN_PREFIX)) {
            return bearerToken.substring(JwtUtil.TOKEN_PREFIX.length());
        }
        return null;
    }
   
}
```

JwtProvider 클래스에서는 클라이언트에게 요청받은 헤더에서 jwt를 추출하는 resolveToken() 메서드와 추출한 jwt의 유효성을 체크하고 JwtUtil 클래스의 verify() 메서드로  jwt를 검증하는 validateToken()메서드가 있습니다.

---

**(확인) 경로: src/main/java/com/metacoding/spring_oauth_oidc/_core/utils/Resp.java**

```java
@Data
public class Resp<T> {

    // 응답 상태 코드(보통 200, 400, 401, 500 등)
    private Integer status;

    // 사용자에게 보여줄 메시지(성공/실패 이유 등)
    private String msg;

    // 실제 응답 데이터(제네릭 타입으로 어떤 DTO든 담을 수 있음)
    private T body;

    public Resp(Integer status, String msg, T body) {
        this.status = status;
        this.msg = msg;
        this.body = body;
    }

    /**
     * 성공 응답(기본 메시지 = "성공")
     * - 컨트롤러에서 return Resp.ok(dto); 처럼 쓰기 좋습니다.
     */
    public static <B> ResponseEntity<Resp<B>> ok(B body) {
        return ok("성공", body);
    }

    /**
     * 성공 응답(메시지 커스텀 가능)
     * - HTTP 상태 코드는 200(OK)로 내려줍니다.
     * - Resp 내부 status도 200으로 맞춰둡니다.
     */
    public static <B> ResponseEntity<Resp<B>> ok(String msg, B body) {
        // 공통 응답 포맷 생성
        Resp<B> resp = new Resp<>(200, msg, body);

        // HTTP 응답까지 200 OK로 감싸서 반환
        return new ResponseEntity<>(resp, HttpStatus.OK);
    }
}
```

Resp<T> 클래스는 클라이언트 요청에 대한 응답을 공통된 형식으로 전달하기 위한 응답 포맷 클래스입니다.

---

### 2. ID Token 발행 및 검증

![image.png](2%203%20REST%20API%20Code%20+%20OIDC%20%EA%B2%80%EC%A6%9D%20(Spring%20REST)/image%202.png)

우리 서버에서 code로 카카오 인증 서버에게 토큰을 요청하여 ID Token을 발행해봅니다. OIDC를 사용하기 전 카카오 디벨로퍼 앱 → 카카오 로그인 → 일반 → OepnID Connect 사용을 활성화 합니다. 자세한 부분은 2.1 준비 챕터를 확인해주세요.

**실습코드**

```java
https://github.com/metacoding-11-spring-reference/kakao-oauth-code-oidc-end/tree/2.ID-Token-발행-및-검증
```

---

ID Token을 요청하기 위해서는 기존 카카오 로그인 인가 코드 요청을 할때와는 요청하는 URL 주소가 다릅니다. 요청하는 주소 조합은 아래와 같습니다.

```java
https://kauth.kakao.com/oauth/authorize?
response_type=code
&client_id=${REST_API_KEY}
&redirect_uri=${REDIRECT_URI}

+ 추가
&scope=openid profile_nickname
```

ID Token은 scope에 openid을 붙여 요청을 해야 카카오 오어스 서버에서 OIDC를 사용하는 code 발급요청이란 걸 알 수 있습니다. 그렇지 않으면 Access Token만 발행하는 code를 발급해줍니다. 아래 메서드를 입력합니다.

---

**(입력) 경로: src/main/java/com/metacoding/spring_oauth_oidc/user/UserService.java**

```java
public String 카카오로그인주소() {

    String encodedRedirect = URLEncoder.encode(kakaoRedirectUri, StandardCharsets.UTF_8);
    String scope = URLEncoder.encode("openid profile_nickname", StandardCharsets.UTF_8);
    return kakaoAuthorizeUri
            + "?response_type=code"
            + "&client_id=" + kakaoClientId
            + "&redirect_uri=" + encodedRedirect
            + "&scope=" + scope;
}
```

**UserService.java** 파일에 ****카카오로그인주소() 메서드를 입력합니다.

---

**(확인) 경로: src/main/java/com/metacoding/spring_oauth_oidc/user/UserController.java**

```java
// 카카오 로그인 콜백
@GetMapping("/oauth/callback")
@ResponseBody
public ResponseEntity<?> kakaoCallback(@RequestParam("code") String code) {
    UserResponse.DTO resDTO = userService.카카오로그인(code);
    return Resp.ok("카카오 로그인 성공", resDTO);
}
```

**UserController.java의** kakaoCallback() 메서드에서는 code를 수신받아 카카오로그인() 메서드로 주입합니다. 최종적으로 유저 정보와 우리 서버 jwt 토큰을 Resp 포멧으로 응답합니다.

---

**(확인) 경로:** src/main/java/com/metacoding/spring_oauth_oidc/user/KakaoOidcResponse.java

```java
public record KakaoOidcResponse(
                String subject,
                String nickname,
                Instant expiresAt) {
}
```

ID Token을 파싱하여 응답 데이터를 담을 KakaoOidcResponse를 확인합니다. 

---

**(입력) 경로:** src/main/java/com/metacoding/spring_oauth_oidc/_core/utils/KakaoOidcUtil.java

```java
@Component
public class KakaoOidcUtil {

    @Value("${kakao.client-id}")
    private String kakaoClientId;

    @Value("${kakao.oidc-jwks-uri}")
    private String kakaoOidcJwksUri;

    /**
     * 🔒 카카오 OIDC 토큰 검증 전체 처리
     */
    public KakaoOidcResponse verify(String idToken) {
        if (idToken == null || idToken.isBlank()) {
            throw new RuntimeException("id_token 값이 비어 있습니다.");
        }

        try {
            // 토큰 파싱
            SignedJWT signedJWT = SignedJWT.parse(idToken);
        
            // JWKS에서 공개키 가져오기
            RSAKey rsaKey = getKeyFromJwks(signedJWT.getHeader().getKeyID());

            // 서명 검증
            if (!signedJWT.verify(new RSASSAVerifier(rsaKey))) {
                throw new RuntimeException("카카오 id_token 서명 검증 실패");
            }

            // 클레임 추출
            JWTClaimsSet claims = signedJWT.getJWTClaimsSet();

            // 검증 완료 후 응답 생성
            return new KakaoOidcResponse(
                    claims.getSubject(),
                    claims.getStringClaim("nickname"),
                    claims.getExpirationTime().toInstant());

        } catch (ParseException | JOSEException e) {
            throw new RuntimeException("카카오 id_token 검증 중 오류 발생", e);
        }
    }

    /**
     * 🔑 JWKS에서 RSA 공개키 조회
     */
    private RSAKey getKeyFromJwks(String keyId) {
        if (keyId == null || keyId.isBlank()) {
            throw new RuntimeException("id_token 헤더에 kid 값이 없습니다.");
        }

        try {
            // JWKS JSON 가져오기
            JWKSet jwkSet = JWKSet.load(URI.create(kakaoOidcJwksUri).toURL());
            JWK jwk = jwkSet.getKeyByKeyId(keyId);

            if (jwk == null) {
                throw new RuntimeException("kid에 해당하는 공개키를 찾을 수 없습니다: " + keyId);
            }

            if (!(jwk instanceof RSAKey rsaKey)) {
                throw new RuntimeException("kid에 대한 키 타입이 RSA가 아닙니다: " + keyId);
            }

            return rsaKey;

        } catch (Exception e) {
            throw new RuntimeException("JWKS 불러오기 또는 파싱 실패", e);
        }
    }

}

```

KakaoOidcUtil 클래스에서 verify() 메서드는 ID Token을 받아 서명을 파싱하고 파싱한 데이터의 keyId를  getKeyFromJwks() 메서드로 주입하고  JWKS에서 RSA 공개키를 조회 후 매칭하여 맞는 reaKey를 받아 카카오 유저를 생성할때 필요한 클레임을 추출하여 KakaoOidcResponse를 응답하는 클래스입니다.

<aside>
💡

JWKS란?

카카오·구글 같은 인증 서버는 **ID Token을 비밀키로 서명**해서 발급합니다. 우리 서버는 그 비밀키를 알 수 없기 때문에, 대신 **공개키**로 검증해야 합니다.

이 공개키들을 모아둔 곳이 바로 **JWKS**입니다.

**(확인) 경로: src/main/resources/application.properties** 

```
# --------------------------------------
# 카카오 OIDC 공개키(JWKS) 조회 주소
# --------------------------------------
# ID Token(JWT)의 서명을 검증하기 위한 공개키 목록(JWKS)을 제공하는 엔드포인트
# 서버는 이 주소에서 공개키를 조회해
# ID Token의 위변조 여부를 검증함
kakao.oidc-jwks-uri=https://kauth.kakao.com/.well-known/jwks.json
```

</aside>

---

**(확인) 경로: src/main/java/com/metacoding/spring_oauth_oidc/user/KakaoResponse.java**

```java
public class KakaoResponse {

        // 토큰 응답 DTO (/oauth/token)
        public record TokenDTO(
                        @JsonProperty("token_type") String tokenType,
                        @JsonProperty("access_token") String accessToken,
                        @JsonProperty("expires_in") Long expiresIn,
                        @JsonProperty("refresh_token") String refreshToken,
                        @JsonProperty("refresh_token_expires_in") Long refreshTokenExpiresIn,

                        @JsonProperty("id_token") String idToken, // OIDC용 ID 토큰
                        String scope) {
        }

}
```

ID Token을 발행하게 되면 카카오 인증서버의 응답 바디에는 idToken라는 파라미터가 추가 되어있습니다.

---

**(입력) 경로:** src/main/java/com/metacoding/spring_oauth_oidc/user/UserService.java

```java
@Transactional
public UserResponse.DTO 카카오로그인(String code) {
    // 인가 코드로 토큰 요청 (access_token + id_token 포함)
    KakaoResponse.TokenDTO tokenDTO = kakaoApiClient.getKakaoToken(code);

    // OIDC 검증
    KakaoOidcResponse resDTO = kakaoOidcUtil.verify(tokenDTO.idToken());
    System.out.println("resDTO = " + resDTO);
    return null;
}
```

카카오로그인() 메서드는 code를 kakaoApiClient.getKakaoToken() 메서드에 주입하여 ID Token을 전달받고 kakaoOidcUtil.verify() 메서드로 tokenDTO.idToken()를 주입하여 OIDC 검증을 진행합니다. 이후 KakaoOidcResponse로 응답을 받습니다.

---

서버를 실행하기 전 .env파일을 설정하세요. 

![image.png](2%203%20REST%20API%20Code%20+%20OIDC%20%EA%B2%80%EC%A6%9D%20(Spring%20REST)/image%203.png)

![image.png](2%203%20REST%20API%20Code%20+%20OIDC%20%EA%B2%80%EC%A6%9D%20(Spring%20REST)/image%204.png)

서버와 포스트맨을 실행합니다. 포스트맨으로 GET  http://localhost:8080/login/kakao 요청합니다. 결과물 body 에서 continueUrl를 찾아 Crtl + 클릭하면 브라우저로 이동하며 카카오 로그인을 진행합니다.

<aside>
💡

직접 url을 생성하여 브라우저 주소창에 입력하여 요청해도 됩니다.

https://kauth.kakao.com/oauth/authorize

?response_type=code

&client_id={client_id}

&redirect_uri=http://localhost:8080/oauth/callback

&scope=openid profile_nickname

</aside>

---

![image.png](2%203%20REST%20API%20Code%20+%20OIDC%20%EA%B2%80%EC%A6%9D%20(Spring%20REST)/image%205.png)

![image.png](2%203%20REST%20API%20Code%20+%20OIDC%20%EA%B2%80%EC%A6%9D%20(Spring%20REST)/image%206.png)

![image.png](2%203%20REST%20API%20Code%20+%20OIDC%20%EA%B2%80%EC%A6%9D%20(Spring%20REST)/image%207.png)

![개인정보라서 가리는 부분을 캡쳐해놨습니다.](2%203%20REST%20API%20Code%20+%20OIDC%20%EA%B2%80%EC%A6%9D%20(Spring%20REST)/image%208.png)

개인정보라서 가리는 부분을 캡쳐해놨습니다.

동의화면을 완료하고 나면 **UserController 클래스** kakaoCallback()메서드의 메세지를 확인할 수 있으며, 우리 서버 터미널에서는 UserService 클래스 카카오로그인() 메서드의 KakaoOidcResponse resDTO의 출력값을 확인할 수 있습니다.

이제 “body”: null 부분에 유저정보와 토큰값을 넣어 클라이언트가 응답 받을 수 있도록 아래 DB 생성 및 jwt 발급을 진행합니다.

---

### 3. DB 생성 및 Jwt 발급

![image.png](2%203%20REST%20API%20Code%20+%20OIDC%20%EA%B2%80%EC%A6%9D%20(Spring%20REST)/image%209.png)

UserService 클래스 카카오로그인() 메서드에서 전달받은 KakaoOidcResponse resDTO의 정보를 우리 서버 DB에 생성하고 Jwt를 발급합니다.

**실습코드**

```java
https://github.com/metacoding-11-spring-reference/kakao-oauth-code-oidc-end/tree/3.-DB-생성-및-Jwt-발급
```

---

**(입력) 경로:** src/main/java/com/metacoding/spring_oauth_oidc/user/UserService.java

```java
@Transactional
public User 카카오유저생성및갱신(String providerId, String username) {
    String resolvedEmail = "kakao_" + providerId + "@kakao.com";
    String resolvedUsername = username;

    return userRepository.findByProviderAndProviderId("kakao", providerId)
            .map(user -> {
                user.updateEmail(resolvedEmail);
                user.updateUsername(resolvedUsername);
                return user;
            })
            .orElseGet(() -> userRepository.save(User.builder()
                    .username(resolvedUsername)
                    .password(UUID.randomUUID().toString())
                    .email(resolvedEmail)
                    .provider("kakao")
                    .providerId(providerId)
                    .build()));
}
```

UserService 클래스에 카카오유저생성및갱신() 메서드를 생성합니다.  String providerId, String username를 주입받아 해당 정보가 DB에 있는지 조회 후 저장 및 갱신을 합니다.

---

**(입력) 경로:** src/main/java/com/metacoding/spring_oauth_oidc/user/UserService.java

```java
@Transactional
public UserResponse.DTO 카카오로그인(String code) {
    // 인가 코드로 토큰 요청 (access_token + id_token 포함)
    KakaoResponse.TokenDTO tokenDTO = kakaoApiClient.getKakaoToken(code);

    // OIDC 검증
    KakaoOidcResponse resDTO = kakaoOidcUtil.verify(tokenDTO.idToken());

    User user = 카카오유저생성및갱신(resDTO.subject(), resDTO.nickname());

    String jwt = JwtUtil.create(user);
    return new UserResponse.DTO(user, jwt);
}
```

UserService 클래스의 카카오로그인() 메서드에 카카오유저생성및갱신() 메서드를 호출하여 파라미터를 주입합니다. 리턴된 user를 JwtUtil.create() 메서드에 주입하여 생성된 jwt 토큰을 리턴합니다.

---

다시 서버를 실행하여 포스트맨 에서 [http://localhost:8080/login/kakao](http://localhost:8080/login/kakao) 요청 또는 브라우저 주소창에 url을 입력하여 카카오 로그인을 진행합니다.

![image.png](2%203%20REST%20API%20Code%20+%20OIDC%20%EA%B2%80%EC%A6%9D%20(Spring%20REST)/image%2010.png)

로직이 성공하면 ‘카카오 로그인 성공’ 메세지를 확인할 수 있으며 username,  email, token이 body에 포함되어 있는 걸 확인할 수 있습니다.

<aside>
💡

**jwt를 사용하는 이유**

- **로그인한 사용자를 매 요청마다 쉽게 확인하기 위해서입니다.** JWT 안에는 사용자 정보가 들어 있어서, 서버는 요청이 올 때마다 “누가 요청했는지”를 바로 알 수 있습니다.
- **서버에 로그인 상태를 저장하지 않아도 되기 때문입니다.** JWT는 서버에 세션을 따로 저장하지 않아도 되어 구조가 단순해집니다.
- **카카오 인증과 우리 서비스 인증을 분리하기 위해서입니다.** 카카오의 ID Token은 “카카오가 이 사용자를 확인했다”는 증명이고, JWT는 “우리 서비스에서 이 사용자를 로그인 상태로 인정한다”는 토큰입니다.
</aside>

---

### 4. jwt 토큰 사용 및 인증필터

![image.png](2%203%20REST%20API%20Code%20+%20OIDC%20%EA%B2%80%EC%A6%9D%20(Spring%20REST)/image%2011.png)

발급받은 토큰으로 PostController클래스의 목록조회() 메서드를 실행해보겠습니다.

**실습코드**

```java
https://github.com/metacoding-11-spring-reference/kakao-oauth-code-oidc-end/tree/4.-jwt-토큰-사용-및-인증필터
```

---

**(확인) 경로:** src/main/java/com/metacoding/spring_oauth_oidc/post/PostController.java

```java
@GetMapping("/posts")
public ResponseEntity<?> 목록조회() {
    return Resp.ok("게시글 목록 조회", postService.게시글목록());
}
```

게시글목록()을 리턴하는 메서드입니다.

---

![image.png](2%203%20REST%20API%20Code%20+%20OIDC%20%EA%B2%80%EC%A6%9D%20(Spring%20REST)/image%2012.png)

포스트맨에서 전달받은 jwt 토큰중 Bearer를 제외한 token값을 Auth탭으로 이동하여

- Auth Type을  Bearer Token로 설정합니다.
- Token : token값을 입력합니다.

---

![image.png](2%203%20REST%20API%20Code%20+%20OIDC%20%EA%B2%80%EC%A6%9D%20(Spring%20REST)/image%2013.png)

성공 200과 게시글 목록 조회를 확인할 수 있습니다.

---

만약 유효하지 않은 토큰을 넣게 되며 어떻게 될까요? 아래 검증을 담당할 인증필터를 생성하여 잘못된 jwt token이 들어오게 되면 실패, 헤더에 jwt token이 없으면 없음을 검증해보겠습니다.

**(입력) 경로:**src/main/java/com/metacoding/spring_oauth_oidc/_core/filter/JwtAuthFilter.java

```java

@Component
@RequiredArgsConstructor
public class JwtAuthFilter extends OncePerRequestFilter {

    // 요청에서 JWT를 꺼내고 검증하는 역할을 하는 클래스
    private final JwtProvider jwtProvider;

    // 에러 응답(JSON)을 만들기 위한 ObjectMapper
    private final ObjectMapper objectMapper;

    /**
     * JWT 검증을 하지 않아도 되는 요청 경로를 지정
     * - OPTIONS: CORS preflight 요청
     * - /login/kakao: 카카오 로그인 시작
     * - /oauth/callback: 카카오 로그인 콜백
     */
    @Override
    protected boolean shouldNotFilter(HttpServletRequest request) {
        String path = request.getRequestURI();
        return "OPTIONS".equalsIgnoreCase(request.getMethod())
                || "/login/kakao".equals(path)
                || "/oauth/callback".equals(path);
    }

    /**
     * 모든 요청에 대해 한 번만 실행되는 JWT 인증 필터
     */
    @Override
    protected void doFilterInternal(HttpServletRequest request,
            HttpServletResponse response,
            FilterChain filterChain)
            throws ServletException, IOException {
        try {
            // Authorization 헤더에서 JWT 추출 (없거나 잘못되면 예외 발생)
            jwtProvider.verifyFromHeader(request);

            // JWT가 정상이라면 다음 필터 또는 컨트롤러로 요청 전달
            filterChain.doFilter(request, response);

        } catch (Exception e) {
            // JWT가 없거나 유효하지 않은 경우 → 인증 실패
            response.setStatus(HttpServletResponse.SC_UNAUTHORIZED);
            response.setContentType("application/json;charset=UTF-8");

            // 공통 응답 포맷으로 401 에러 반환
            response.getWriter().write(
                    objectMapper.writeValueAsString(
                            new Resp<>(401, e.getMessage(), null)));
        }
    }
}
```

JwtAuthFilter 클래스는 OncePerRequestFilter을 상속받아 스프링 가장 앞에서 한번만 검증을 하는 필터입니다. 검증이 필요없는 /login/kakao, /oauth/callback 요청은 제외하고 모든 요청의 HttpServletRequest request를 가로채 jwtProvider.verifyFromHeader(request)메서드에 주입하여 검증합니다.

---

![image.png](2%203%20REST%20API%20Code%20+%20OIDC%20%EA%B2%80%EC%A6%9D%20(Spring%20REST)/image%2014.png)

잘못된 Jwt token을 요청했을때 응답입니다.

---

![image.png](2%203%20REST%20API%20Code%20+%20OIDC%20%EA%B2%80%EC%A6%9D%20(Spring%20REST)/image%2015.png)

Jwt token이 header에 없을때 응답입니다.

---

### 5. JWT 보안

JWT Token의 만료, 저장위치, 재발급에 대한 내용을 알아보겠습니다.

---

**1. 우리 서비스 JWT는 “짧게 쓰고, 오래 쓰는 건 따로”가 기본입니다**

실습에서는 JwtUtil로 우리 서비스 JWT를 발급하고, JwtAuthFilter로 요청마다 검증합니다. JWT는 운영에서 두가지의 Token을 사용합니다.

**Access Token(짧게)**: API 호출용 토큰은 짧게 가져가야 합니다. 만약 탈취되더라도 피해 시간이 짧아집니다.

**Refresh Token(길게)**: Access Token이 만료됐을 때 다시 발급받기 위한 용도로 따로 둡니다.

---

**2. 저장 위치가 보안의 절반입니다**

토큰은 발급보다 “어디에 저장하느냐”가 더 위험할 수 있습니다.

- **브라우저 localStorage 저장**: 편하지만 XSS에 취약해서 토큰 탈취 위험이 있습니다.
- **HttpOnly Cookie 저장**: JS로 접근이 불가능해서 XSS에 강합니다. 대신 쿠키 기반이면 CSRF 방어 전략이 필요합니다.
- **최소 원칙**: 토큰을 오래 저장할수록 위험이 커지므로, 필요한 범위에서만 저장하는 정책을 선택합니다.

---

**3. 재발급과 로그아웃을 어떻게 처리할지 정해야 합니다**

보안은 “로그인 성공”에서 끝나지 않고, 만료 이후의 동작이 포함됩니다.

- Access 만료 시: Refresh로 재발급할지, 다시 로그인 시킬지 정책 필요
- 로그아웃 시: Refresh를 서버에서 폐기할지(토큰 무효화) 정책 필요
- 탈취 의심 시: 특정 토큰을 강제로 막는 방법(블랙리스트 등) 정책 필요

---

여기까지 code + OIDC를 결합한 구조를 알아보았습니다. 다음 챕터에서는 정리를 하며 Oauth를 마무리 하도록 하겠습니다.