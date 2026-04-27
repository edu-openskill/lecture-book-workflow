# v12 이미지 스타일 통일 작업

> 작업 일자: 2026-04-27
> 대상: HTML/D2 소스가 있는 다이어그램만 → 현재 이미지 에이전트 스타일(`#1565c0`/`#c62828`/Malgun Gothic)
> 선행 산출물: `review/v12-수정내역.md`
> 후행 산출물: `.build/01~06.html` (재빌드 통과)

---

## 0. 한눈에 보기

| 항목 | 결과 |
|---|---|
| 전체 챕터 이미지 수 | 145개 (CH01:4 / CH02:46 / CH03:37 / CH04:20 / CH05:25 / CH06:13) |
| 변환 대상 (HTML/D2 소스 보유) | **12개** (D2 9개 + HTML 3개) |
| 그대로 유지 | 17개 (CH05 NEW HTML — 이미 표준 스타일) |
| 작업 외 (개념 일러스트·터미널 캡처·MOCK) | 116개 |
| 렌더 파이프라인 | Chrome headless (`render-png.sh`) |
| HTML 빌드 검증 | 6챕터 모두 통과 |

---

## 1. 사용한 표준 스타일 토큰

| 항목 | 값 | 용도 |
|---|---|---|
| 배경 | `#fff` | body / 박스 기본 |
| 강조 배경 (블루 톤) | `#f5faff` | 그룹 박스 안쪽 |
| 강조 배경 (주황 톤) | `#fff3e0` | Secret / 핫스팟 박스 안쪽 |
| Primary 보더·텍스트 | `#1565c0` | 메인 박스·화살표·라벨 |
| Accent (위험·민감·강조) | `#c62828` | Secret·PV·NodePort·dnat 같은 부각 요소 |
| 본문 글꼴 | `Malgun Gothic`, `Apple SD Gothic Neo`, sans-serif | 한글 본문 |
| 모노 글꼴 | `Consolas`, monospace | IP·코드 |
| 박스 보더 | `2~2.5px solid` | radius `6~14px` |
| 그림자 | `0 0 0 3~4px rgba(21,101,192,0.10)` | Primary 박스 강조 |
| 다이어그램 폭 | `940~1080px` | 본문 가로 폭 기준 |

---

## 2. 챕터별 변환 작업

### CH01 (왜 컨테이너인가)
변환 대상 0개. 4장 모두 Gemini 손그림 일러스트(항구·로드맵)라 유지.

### CH02 (Docker 이해하기) — 5장 변환

| 파일 | 종류 | 변경 |
|---|---|---|
| `diagram/ch2-step1-namespace.{d2 → html}` | 구조도 | Namespace A·B + Host(docker0·veth) 3열 레이아웃. greyscale → 블루 보더 + docker0 빨강·주황 강조 |
| `diagram/ch2-step2-dnat.{d2 → html}` | 흐름 | 외부 클라이언트 → Host(iptables DNAT) → 컨테이너 가로 흐름. iptables 빨강 강조 + ":8080 으로 요청 / :80 으로 변환" 라벨 |
| `diagram/ch2-step3-dns.{d2 → html}` | 시퀀스 | app ↔ Docker DNS ↔ db 3노드 + 번호 뱃지(①②③). 응답은 빨강 점선 |
| `chap01-33.html` | 터미널 프레임 | `.claude/skills/screenshot` 템플릿과 100% 일치시킴 (프롬프트 #0066cc, output line-height 1.5, font Menlo 우선) |
| `chap01-68.html` | 터미널 프레임 | 위와 동일. 터미널 출력은 실제 실행 결과이므로 ID(`coderyu5523/tomcat`) 그대로 유지 |

### CH03 (Docker 다루기) — 1장 변환

| 파일 | 종류 | 변경 |
|---|---|---|
| `ex01-lb-to-host.html` | 구조도 (Docker 내부 통신 우회) | Docker brand `#2496ED` → `#1565c0`, `#e74c3c` → `#c62828`, `#f7fbff` → `#f5faff`, `Pretendard` → `Malgun Gothic`. body `min-height:100vh` flex 센터 → 명시적 padding (라벨 잘림 해결) |

### CH04 (Kubernetes 시작하기) — 2장 변환

| 파일 | 종류 | 변경 |
|---|---|---|
| `k8s-step1.{d2 → html}` | 구조도 | Pod 안 Container 단순 nested. greyscale → 블루 보더 + 라이트 블루 안쪽 + Pod 라벨 부각 |
| `k8s-step2.{d2 → html}` | 흐름 | Deployment("Pod 3개 유지하라") → 생성 → ReplicaSet("Pod 수 조절") → Pod ① ② ③ 분기 |

### CH05 (Kubernetes 네트워킹) — 1장 변환 + 17장 점검

| 파일 | 종류 | 변경 |
|---|---|---|
| `k8s-step3.{d2 → html}` (CH04/) | 분배 흐름 | Service "고정 접근 주소" → 3개 Pod (10.0.0.5/.9/.12)에 SVG 부채꼴 분배 |

기존 17개 HTML 점검 결과 모두 표준 스타일 부합:
- 13개: `#1565c0` + `#c62828` + Malgun Gothic 표준
- 2개 (`service-type-step2/3`): Service Type 색 코드 의도적 차별 (NodePort=빨강, LoadBalancer=초록)
- 3개 (`mock-*`): 브라우저·UI mock 스크린 카테고리 (다이어그램이 아님)

### CH06 (Kubernetes 운영하기) — 3장 변환

| 파일 | 종류 | 변경 |
|---|---|---|
| `k8s-step4a.{d2 → html}` (CH05/) | 주입 흐름 | ConfigMap(블루) + Secret(빨강·주황) → Pod 점선 주입. SVG 두 화살표 + 라벨 |
| `k8s-step4b.{d2 → html}` (CH05/) | 흐름 | Pod → PVC("10Gi 요청") → PV("실제 디스크"). PV는 빨강·주황 강조 |
| `k8s-namespace.{d2 → html}` (CH05/) | 그룹 구조 | Cluster 안 dev(블루 점선) + prod(빨강 점선·주황 톤) Namespace, 각 Pod/Service/Deployment 세트 |

---

## 3. 유지된 이미지 (유저 결정으로 변환 대상 아님)

- **개념 일러스트** (Gemini 손그림 흑백): `chap01-1`(항구), `chap01-5`(요리사), `chap01-roadmap` 등 약 68장
- **터미널 캡처** (`01_kubectl-*` ~ `13_secret-env`, `42_volume-*`): 11장
- **MOCK** (`mock-ingress-get`, `mock-order-page`, `mock-stores-page`): 3장 (`pending_work`에서 별도 트래킹)

---

## 4. 렌더 헬퍼

`projects/.../​.build/render-png.sh` 추가. Chrome headless로 HTML → PNG.

```bash
bash .build/render-png.sh <html> <png> [width] [height]
```

기본값 1120×800. 다이어그램 컨텐츠 높이에 맞춰 명시적 지정 권장.

**자동 트림 (2026-04-27 추가)**: `render-png.sh`가 Chrome 캡처 직후 `trim-png.py`(Pillow)를 호출하여 흰 여백을 자동 트림하고 균등 12px 외곽 마진을 적용한다. 윈도우 크기를 컨텐츠보다 크게 줘도 결과 PNG는 컨텐츠에 딱 맞춰진다. 사전 요구: `pip install pillow`.

---

## 5. 검증

| 검증 | 결과 |
|---|---|
| 6챕터 HTML 빌드 | ✅ 통과 (`.build/01~06.html` 재생성) |
| 변환된 PNG 파일 갱신 | ✅ 12개 모두 갱신 (mtime 2026-04-27) |
| 챕터 .md 참조 경로 변경 | ❌ 없음 (모든 PNG는 같은 경로에 덮어쓰기) |
| 기존 D2 파일 보존 | ✅ `.d2` 원본 그대로 (참고용) |

---

## 6. 2차 통일 작업 (2026-04-27 후속)

소스가 사라졌던 기하학 다이어그램 23장을 v12 스타일 HTML로 신규 작성.

| 챕터 | 신규 변환 | 핵심 강조 (빨강·주황) |
|---|---|---|
| CH02 | 5장 | `fig-1-bp-0`(이미지) · `chap01-9`(OS 커널) · `chap01-13`(이미지 틀) · `bind-mount`(연결선) · `volume-mount`(metacoding-volume) |
| CH03 | 8장 | `chap02-1`(컨테이너) · `cache-hit/miss`(캐시 상태) · `session-problem/redis`(공유 저장소) · `net-05/06-docker-dns`(Docker DNS) · `fig-1-v2`(Compose 영역) |
| CH04 | 8장 | `chap03-k8s-architecture`(Pod) · `fig-3-1/4`(Kube API Server) · `fig-3-5`(Minikube 컨트롤 플레인) · `selector-labels`(매칭 Pod) · `replicaset`(설정 개수) · `chap04-node`(노드 격리) · `pod-creation`(pause container) |
| CH06 | 2장 | `fig-3-6`(rollout restart 흐름) · `fig-3-7-v2`(Redis Pod) |

진행 방식
- CH02 잔여는 메인 세션 직접 처리
- CH03·CH04·CH06은 illustrator 에이전트 3종 병렬 디스패치 → 메인 세션이 잘림·색상 위반 보정

검증
- 6 챕터 HTML 재빌드 통과 (`.build/01~06.html`)
- 색상 표준화: 모든 강조는 `#c62828` + `#fff3e0` (CH06 에이전트가 잘못 쓴 `#d68910` 일괄 치환)
- 라벨 잘림 보정: cache-hit/miss · fig-1-v2 · CH04 다수 height 보강 재렌더

---

## 7. 다음 작업

- (보류) 캐릭터 보강 (CH02·CH05 선배 한 줄)
- (보류) MOCK 이미지 3건 실환경 재캡처 (CH05 L332/L351/L358)
- (보류) CH06 캡처 보강 3건 (L135~139 / L153 / L464~476)
- (보류) PDF 재빌드
