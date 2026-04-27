# 코드 설명 패턴 (기술 파트용)

> 공통 코드 규칙(언어 태그, 구조, 파트별 규칙)은 `.claude/rules/code.md` 참조.
> 이 파일은 code 스킬에서만 사용하는 고유 기능을 정의한다.
> 주의: 이야기 파트에는 코드가 등장하지 않는다. 이 규칙은 기술 파트에서만 적용.

---

## 핵심 라인 강조 (3~6개 권장)

모든 라인이 아닌 **독자가 이해해야 할 핵심 라인만** 표시한다.

```java
@PostMapping("/login")
public String login(@RequestParam String id,      // 사용자가 입력한 ID
                    @RequestParam String pw,      // 사용자가 입력한 비밀번호
                    HttpSession session) {        // 여기가 핵심! 세션 객체
    if (memberService.authenticate(id, pw)) {
        session.setAttribute("loginUser", id);    // 세션에 로그인 정보 저장
        return "redirect:/";
    }
    return "login";
}
```

---

## 코드 아래 흐름 설명

블록 인용문(`>`)으로 자연스럽게 설명한다.

```markdown
> 사용자가 ID와 비밀번호를 보내면, 서버가 확인한 뒤
> 세션에 "이 사람 로그인했음"을 기록합니다.
> 다음부터는 세션만 보면 누구인지 알 수 있죠.
```

---

## 실행 결과 조건

코드 실행 시 터미널에 출력되는 결과를 보여준다.
실행 결과가 없는 코드(클래스 정의, 설정 등)는 생략 가능.

---

## 상세 설명이 필요 없는 경우

| 코드 유형 | 예시 | 사유 |
|----------|------|------|
| 쉘 명령어 | `pip install`, `./gradlew bootRun` | 실행 명령어, 로직 없음 |
| 환경 설정 | `.env` 파일 내용 | 설정 단계 |
| Git 명령어 | `git clone`, `git pull` | 버전 관리 |

> 코드 블록의 언어 태그가 `bash`, `sh`, `shell`이면 상세 설명 불필요.

---

## 스토리텔링 코드 설명

- 코드 설명을 딱딱한 나열이 아니라 대화체로 쓴다
- "이 부분이 핵심이에요" 같은 자연스러운 강조
