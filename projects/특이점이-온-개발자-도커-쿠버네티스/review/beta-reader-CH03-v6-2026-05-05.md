# Beta Reader 리포트: CH03 — Docker 다루기 (v6)

**대상 파일**: `chapters/03-Docker-다루기-v6.md` (1682줄)
**검수 일자**: 2026-05-05
**라운드**: 적극 리라이트(v6) 후 첫 베타 리딩

## 페르소나 10명

| # | 이름 | 이야기 | 기술 | 실습 | 전체 |
|---|------|:----:|:----:|:----:|:----:|
| 1 | 신입 백엔드 | 4 | 3 | 3 | 3 |
| 2 | 클라우드 입문 엔지니어 | 4 | 3 | 3 | 3 |
| 3 | iOS 개발자 | 4 | 3 | 3 | 3.5 |
| 4 | ML 엔지니어 | 4 | 4 | 3 | 3.5 |
| 5 | PM/서비스 기획자 | 4 | 3 | 1 | 3 |
| 6 | 테크 PM | 4 | 3.5 | 3 | 3.5 |
| 7 | DevOps 시니어 | 4.5 | 3.5 | 4 | 4 |
| 8 | 풀스택 CTO | 2.5 | 2.5 | 2 | 2.5 |
| 9 | 부트캠프 수료생 | 4 | 3 | 3 | 3.3 |
| 10 | CS 학생 | 4 | 2.5 | 3 | 3 |

**평균**: 이야기 3.9 / 기술 3.05 / 실습 2.8 / 전체 3.23

## 요약
- 도입(회의실 의뢰) → 시연(빔프로젝터)으로 닫히는 원형 서사·동료 캐릭터 3.3 등판은 광범위하게 호평
- **3.4 MySQL 볼륨 부재 + 3.6 entrypoint.sh 안티패턴 + depends_on 누락** 세 가지가 챕터의 구조적 결함으로 동시 지적됨
- 1682줄 분량이 한 챕터로 과하다는 의견 지속

## 공통 피드백 (3명 이상 동일 의견)

| # | 피드백 | 페르소나 | 심각도 |
|---|--------|--------|:----:|
| 1 | **3.4 MySQL 볼륨 마운트 부재** (절 제목 "영구 데이터" + 종합 실습 db에도 volumes 없음) | P1,P2,P4,P10 | 높음 |
| 2 | **3.6.2 entrypoint.sh의 git clone+Gradle build 안티패턴** — 시연 장면이 학습용임을 명시하지 않음 | P1,P2,P4,P8,P9 | 높음 |
| 3 | **3.6 docker-compose.yml에 depends_on 누락** (3.5.2 골격 표엔 있는데 ex07엔 빠짐) | P2,P6,P7,P8,P10 | 높음 |
| 4 | **3.2 NGINX 분량 비대** (챕터의 35%, 캐싱 분리 또는 챕터 분할 권장) | P3,P6,P8 | 높음 |
| 5 | **컨테이너 ID 앞자리 약식 표기(`1fc2`·`5fcd`) 안내 부재** | P1,P3,P5,P9,P10 | 중간 |
| 6 | **`SPRING_DATASOURCE_URL` 백슬래시 줄바꿈 YAML 함정** | P1,P7,P9 | 중간 |
| 7 | **3.3 동료 시나리오와 실습 어긋남** (라운드 로빈 세션 깨짐 시나리오인데 실습은 5001/5002 직접 호출) | P1,P6,P8 | 중간 |
| 8 | **3.3 Redis 절 인지 부담** (세션+Redis+사용자정의 네트워크+라운드 로빈이 한 절) | P3,P8,P9,P10 | 중간 |
| 9 | **선배 캐릭터 부재** (3.5 Compose 도입에 한마디 비어 있음) | P1,P6,P8 | 낮음 |

## 단독 페르소나 핵심 지적

### P7 DevOps 시니어 (정확성 6건)
- **`proxy_cache_path` 위치 위험** — `http {}` 컨텍스트 전용. ex03 nginx Dockerfile이 `conf.d/default.conf`로 덮어쓴다면 NGINX 기동 실패 (`directive is not allowed here`). 검증 필요
- **`host.docker.internal` Linux 한정** — Docker Desktop(Mac/Win) 기본. Linux Engine은 `--add-host` 옵션 필요. 레포명이 `linux-docker`라 직접 모순
- **`proxy_pass http://app1/;` 끝 슬래시 prefix 제거 동작 미설명** — 실무에서 가장 흔히 깨지는 함정
- **MySQL `MYSQL_USER=root` 함정** — 학습 본문엔 영향 없지만 보강 한 줄 필요
- **`X-Forwarded-For` 부재** — 두 컨테이너 클라이언트 IP가 lb IP로 동일하게 찍힘
- **CMD shell vs exec form 용어 부재** — exec form만 다루면서 용어 자체 안 씀

### P8 풀스택 CTO (구조 결함)
- **`chap02-XX.png` 파일명 잔재 19곳** — CH03 본문에 chap02-* 박혀 있음. structure.md 이미지 경로 규칙 위반
- **그림 3-24 누락** — 3-23 → 3-25 점프, 번호 재정렬 필요
- **MySQL `0.0.0.0:3306` 호스트 모든 인터페이스 노출 위험** — `127.0.0.1:3306:3306` 권장
- **Try/Fail 실종** — 모든 실습이 한 번에 성공. 80포트 충돌·502·depends_on 타이밍 같은 막힘 장면 부재

### P10 CS 학생
- **stateless backend / sticky session 정식 용어 0회** — 인턴 면접 어휘로 옮길 수 없음
- **Redis 영속성(RDB·AOF) 한 줄 부재** — "Redis = 휘발성"으로 잘못 외울 위험
- **`proxy_ignore_headers Cache-Control Expires` 무시 이유 미설명**
- **로드밸런싱 알고리즘이 라운드 로빈 한 종류** — `least_conn`·`ip_hash`·`weight` 한 줄 언급 필요
- **`depends_on` 한계(컨테이너 시작 순서만 보장, healthcheck 아님) 미고지**

### P2 클라우드 입문
- **AWS 매니지드 매핑 한 줄 박스 부재** — NGINX↔ALB / Redis↔ElastiCache / MySQL↔RDS / Compose↔ECS Task Definition
- **AWS 매핑 :::tip 박스 4~5개**만 추가해도 페르소나 점수 회복

### P4 ML 엔지니어
- **GPU/CUDA·NVIDIA Container Toolkit·`--gpus all` 0회 등장**
- **베이스 이미지 선택 함의 부재** — `pytorch/pytorch:2.x-cuda12.x` 같은 공식 이미지 한 줄
- **conda·requirements·uv 흔적 없음** — ML 의존성 지옥 매핑 부재

## 페르소나별 핵심 한 줄

| # | 한 줄 |
|---|------|
| 1 신입 백엔드 | "도입·회의실 비유 좋음. 3.3 동료 시나리오↔실습 어긋남, 3.4 영구 데이터인데 볼륨 마운트 없음" |
| 2 클라우드 입문 | "AWS 매니지드(ALB·ECR·EBS·RDS) 매핑 0건. 3.4 볼륨 누락이 가장 큰 구멍" |
| 3 iOS 개발자 | "1682줄 부담. 3.2 NGINX 분량 누적, Redis 정의에 휘발성 한 줄 부재" |
| 4 ML 엔지니어 | "ex07 entrypoint.sh가 안티패턴인데 데모 명시 없음. 볼륨·GPU·비밀 주입 세 곳 공백" |
| 5 PM 비개발 | "비유는 좋음. 따라갈 수 있는 비율 35~40%. 동료 등장은 PM 컴플레인 형태 그대로" |
| 6 테크 PM | "`:::goal`·`:::prep` 도입 블록 누락. Redis가 종합 실습에 회수 안 됨이 가장 큰 결함" |
| 7 DevOps 시니어 | "정확성 6건 보강 필요. YAML jdbc URL·host.docker.internal·proxy_cache_path 셋이 시급" |
| 8 풀스택 CTO | "1챕터 욕심 과다. entrypoint git clone은 안티패턴, depends_on 누락. 챕터 분할 권장" |
| 9 부트캠프 수료생 | "동료 등장 절대 사족 아님. 3.6.2 git clone에서 '내 코드는?' 의문" |
| 10 CS 학생 | "각 절이 비유에서 멈춤. stateless·휘발성·TTL·depends_on 한계 정식 용어 부재" |

## 심각도별 이슈

### 높음 (구조적·다수 페르소나 일치)
1. **3.4 MySQL 볼륨 마운트 실습 부재** + 종합 실습 db에도 `volumes:` 없음 — CH06 PV/PVC 다리 약화
2. **3.6.2 entrypoint.sh의 git clone+Gradle build 안티패턴** — `:::note` "학습용임을 명시" 또는 multi-stage build로 재구성
3. **3.6 docker-compose.yml `depends_on` 누락** — 3.5.2 표와 ex07 일관성 깨짐. backend가 db보다 먼저 떠서 첫 부팅 실패 위험
4. **3.2 NGINX 분량 비대(35%)** — 캐싱(3.2.6) 분리 또는 챕터 분할 검토
5. **3.3 동료 시나리오 vs 실습 어긋남** — 라운드 로빈 세션 깨짐 도입 → 실습은 5001/5002 직접 호출. NGINX lb 앞단 두는 흐름으로 정합 필요

### 중간 (정확성·실습 막힘)
6. **컨테이너 ID 앞자리 약식 표기** — `1fc2`·`5fcd` 첫 등장 자리에 "본인 화면 ID 앞 4자리" 한 줄
7. **`SPRING_DATASOURCE_URL` 백슬래시 줄바꿈 YAML 함정** — "한 줄로 입력 / 책 표기 줄바꿈" 더 강한 안내 + GitHub 원본 참고
8. **`proxy_cache_path` http 컨텍스트 위치** — ex03 nginx Dockerfile 검증 + 주의 박스
9. **`host.docker.internal` Linux 한정** — term-box에 "Docker Desktop 기본 / Linux는 별도 옵션" 한 줄
10. **`proxy_pass` 끝 슬래시 prefix 제거** — 실무 함정 한 줄
11. **3.3 인지 부담** — 사용자 정의 네트워크는 :::tip 박스로, 라운드 로빈 시나리오와 실습 일치
12. **그림 3-24 결번** — 번호 재정렬

### 낮음 (개선)
13. **chap02-*.png 파일명 잔재 19곳** — `assets/CH03/`로 이동 + 리네임
14. **선배 캐릭터 부재** — 3.5 Compose 도입에 한마디
15. **`:::goal`·`:::prep` 도입 블록 누락** — chapter-format.md 표준 도입 추가
16. **AWS/GPU/OS 매핑 :::tip 박스** — 페르소나별 1~2개씩
17. **로드밸런싱 알고리즘 한 줄·Redis 영속성 한 줄·`depends_on` 한계 한 줄** — 정식 용어 보강
18. **MySQL 포트 노출 `0.0.0.0:3306` 위험 안내** — `127.0.0.1:3306:3306` 권장
19. **YAML 인덴트 안전망** — "공백 2칸·탭 금지·`services must be a mapping` 에러" 한 줄

## 수정 제안 (우선순위)

| # | 위치 | 제안 | 심각도 |
|---|------|------|:----:|
| 1 | 3.4 / 3.6 ex07 db 서비스 | `volumes: - mysql-data:/var/lib/mysql` 추가 + 컨테이너 재시작 후 데이터 잔존 검증 실습 1단계 | 높음 |
| 2 | 3.6.2 entrypoint.sh 위 | ":::note 학습용으로 git clone+빌드를 시작 시점에 두었음 / 실무는 multi-stage Dockerfile" 박스 | 높음 |
| 3 | 3.6 docker-compose.yml | `depends_on: db` 추가 + "컨테이너 시작 순서만 보장, healthcheck 아님" 한 줄 | 높음 |
| 4 | 3.2 구조 | 캐싱(3.2.6)을 별책/부록으로 분리 검토 또는 챕터 자체를 둘로 분할 | 높음 |
| 5 | 3.3 ex04 | NGINX lb를 앞단에 두고 라운드 로빈 → Redis 공유 → 새로고침해도 세션 유지 시나리오로 정합 | 중간 |
| 6 | 2.4 또는 3.4 첫 등장 | "컨테이너 ID 앞 4자리는 본인 화면 기준" 한 줄 | 중간 |
| 7 | 3.6.5 코드블록 위 | "한 줄로 입력하세요. 책 지면 때문에 줄을 나눴습니다" 굵게 + GitHub 원본 링크 강조 | 중간 |
| 8 | 3.2.6 ex03 nginx Dockerfile | `nginx.conf`(http 블록 포함)로 덮어쓰는 형태로 수정 | 중간 |
| 9 | 3.2.4 host.docker.internal term-box | "Docker Desktop 기본 / Linux 엔진은 `--add-host` 옵션" 한 줄 | 중간 |
| 10 | 3.2.3 proxy_pass | 끝 슬래시 prefix 제거 동작 한 줄 | 중간 |
| 11 | 그림 3-24 자리 | 번호 시프트 + 누락 그림 추가 또는 후속 번호 재정렬 | 중간 |
| 12 | 본문 전반 | `chap02-*.png` → `assets/CH03/03-*.png` 19곳 이동·리네임 | 낮음 |
| 13 | 3.5.1 도입 | 선배 한마디 추가 ("그거 일일이 칠 거예요?") | 낮음 |
| 14 | 챕터 도입 | `:::goal` + `:::prep` 블록 표준 도입 | 낮음 |
| 15 | 본문 전반 | AWS/GPU/OS 매핑 `:::tip` 박스 페르소나별 1~2개 | 낮음 |
| 16 | 3.3 / 3.5 | Redis 영속성·로드밸런싱 알고리즘·depends_on 한계 한 줄씩 | 낮음 |

## 결론
이야기 큰 틀(회의실 의뢰 → 시연 회수)은 단단함. 다음 라운드 핵심은 **3.4 볼륨 실습**, **3.6 entrypoint.sh 안티패턴 명시**, **3.6 depends_on 추가**, **3.2 NGINX 분량 분리** 네 가지가 가장 임팩트 큼. 정확성 보강(host.docker.internal Linux, proxy_cache_path 위치, YAML 줄바꿈) 세 건은 따라치는 독자 보호용으로 시급.
