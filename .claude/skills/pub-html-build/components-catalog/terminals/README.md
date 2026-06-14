# Terminals

> 서버 로그·셸 출력을 종이 책에 재현하는 HTML 컴포넌트. 실제 스크린샷 png 대신 재현 가능한 코드 구조로 표현해 수정·다국어화·접근성에 강함.

## 속함

- `.terminal-log` (컨테이너) + `.tl-chrome` · `.tl-traffic` · `.tl-title` + `.tl-body`
- `.tl-body` 내부 하위 요소: `.tl-label` · `.tl-key` · `.tl-val` · `.tl-num` · `.tl-str` · `.tl-dim` · `.tl-hl`
- 구조 보조: `.tl-kv` · `.tl-kv-row` · `.tl-divider` · `.tl-section` · `.tl-cursor`

## 속하지 않음

- 터미널 **스크린샷 png 2장 나란히** → [`../comparisons/`](../comparisons/)의 `.dual-image`
- 단발 bash 커맨드 (```` ```bash [터미널] ... ``` ````) → 코드블록. 로그 구조 재현이 필요 없는 경우

## 컴포넌트 목록

### .terminal-log

**언제 쓰는가**: **서버가 찍어내는 실시간 로그**(질문 수신 → 파이프라인 스텝 → 토큰 트래커 → 처리 완료)를 한 창으로 재현할 때. 단순 bash 출력이 아니라 **구조화된 로그**(섹션 라벨 · key/value · 지연·비용 수치)가 있을 때 쓴다. macOS 스타일 창 크롬(3 원 + 창 타이틀) + 흰 배경 본문. Rich console 팔레트(magenta/blue/green/brown/navy/gray)에 대응하는 6개 색 유틸 클래스를 제공해 중요 신호를 구분.

**사용 챕터**: CH11 §11.3

**HTML 사용 예**:
```html
<div class="terminal-log">
  <div class="tl-chrome">
    <div class="tl-traffic"><span></span><span></span><span></span></div>
    <div class="tl-title">ex11 — python run.py · POST /api/chat</div>
    <div class="tl-spacer"></div>
  </div>
  <div class="tl-body">
    <div><span class="tl-label">질문 수신</span> <span class="tl-dim">|</span> <span class="tl-str">병가 신청 절차 알려줘</span></div>

    <div class="tl-section">
      <span class="tl-label">QueryExpander</span>&nbsp;&nbsp;<span class="tl-key">병가</span>→<span class="tl-val">병가(병가 유급휴가)</span>
    </div>
    <div class="tl-kv-row">원본: 병가 신청 절차 알려줘</div>
    <div class="tl-kv-row">확장: 병가(병가 유급휴가) 신청 절차 알려줘</div>

    <div class="tl-section"><span class="tl-label">TokenTracker 기록</span></div>
    <div class="tl-kv">모델&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="tl-str">llama3.1:8b</span></div>
    <div class="tl-kv">입력 토큰&nbsp;&nbsp;<span class="tl-num">6</span></div>
    <div class="tl-kv">출력 토큰&nbsp;&nbsp;<span class="tl-num">226</span></div>
    <div class="tl-kv">비용 (USD)&nbsp;<span class="tl-num">$0.000000</span></div>
    <div class="tl-kv">지연 시간&nbsp;&nbsp;<span class="tl-num">24993 ms</span></div>

    <div class="tl-divider">
      <span class="tl-val">처리 완료</span> | 유형=unstructured · 소요=<span class="tl-num">24993ms</span><span class="tl-cursor"></span>
    </div>
  </div>
</div>
```

**렌더 CSS**: `styles/diagrams.css` 끝부분 `/* Terminal Log (CH11~) */` 블록 (`.terminal-log`, `.tl-chrome`, `.tl-traffic`, `.tl-title`, `.tl-spacer`, `.tl-body`, `.tl-label/.tl-key/.tl-val/.tl-num/.tl-str/.tl-dim/.tl-hl`, `.tl-kv`, `.tl-kv-row`, `.tl-divider`, `.tl-section`, `.tl-cursor`)

**변형**: `.tl-title`은 창 제목이므로 "프로젝트 — 실행 명령 · 요청 경로" 포맷 권장 (예: `ex11 — python run.py · POST /api/chat`, `ex11 — python run.py`). `.tl-cursor`는 마지막 줄 끝에 선택적(대기 중 인상). 색 클래스는 의미로 쓸 것:
- `.tl-label` = 섹션 라벨 (질문 수신, QueryExpander, TokenTracker 등)
- `.tl-key` = 약어·키 (매핑 좌변)
- `.tl-val` = 확장 결과·성공 상태 (매핑 우변, "처리 완료")
- `.tl-num` = 수치 (토큰, 지연, 비용)
- `.tl-str` = 문자열·모델명
- `.tl-dim` = 보조 회색 텍스트 (구분자 `|`, 원본/확장 레이블)
- `.tl-hl` = 노랑 형광펜 배경 강조 (`#fff3b0`). 예제로 주입한 값 등 특정 줄을 시스템 값과 구분 (CH6 §6.1 env 출력에서 ConfigMap/Secret 값)

**피해야 할 것**
- 스크린샷으로 대체 가능한 **정적 캡처**에 과용 금지. `.terminal-log`는 **구조화된 로그 재현**(여러 key/value + 섹션) 용도. 단일 커맨드 출력은 코드블록으로 충분
- `.tl-chrome` 생략: 3원 트래픽 라이트와 창 타이틀이 "이건 터미널 창이다"를 시그널. 생략하면 그냥 회색 박스로 보임
- `.tl-title` 한글 문장으로 길게 쓰기 금지: `ex11 — command · route` 영문 mono 포맷이 창 크롬 크기와 맞음. 한글 설명은 본문 또는 캡션으로
- 색 클래스 난용: 한 창 안에 6 색을 다 쓰면 집중 포인트가 흐려짐. 핵심 3~4 색만 선택 (보통 `.tl-label + .tl-key/.tl-val + .tl-num`)
- `.tl-cursor`를 중간 줄에 넣기 금지: 마지막 줄 끝에만. 중간에 두면 "실행 중 블록"이 되어 의미 달라짐
