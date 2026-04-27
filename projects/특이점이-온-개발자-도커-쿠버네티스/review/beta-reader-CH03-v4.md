# Beta Reader 리포트: CH03 — Docker 다루기 (v4)

## 프로젝트
- 책: 특이점이 온 개발자 — 도커·쿠버네티스
- 대상 파일: `chapters/03-Docker-다루기.md` (951 라인)
- 독자 상수: 입사 3~6개월차 주니어
- 평가 일자: 2026-04-27

## 페르소나 목록

| # | 이름 | 이야기 | 기술 | 실습 | 통과 |
|---|------|:----:|:----:|:----:|:----:|
| 1 | 신입 백엔드 | 4 | 3 | 2 | O (조건부) |
| 2 | 데이터 엔지니어 | 4 | 4 | 5 | O |
| 3 | 프론트엔드 | 4 | 3 | 4 | O |
| 4 | SI 개발자 | 3.5 | 3.5 | 2.5 | O (조건부) |
| 5 | PM/기획자 | 4 | 5 | 4 | O |
| 6 | 비전공 전직자 | 4.5 | 4 | 3.5 | O |
| 7 | DevOps 엔지니어 | 4 | 3 | 3 | O (조건부) |
| 8 | 임베디드 개발자 | 4 | 3 | 4 | O |
| 9 | CS 학생 | 4 | 4 | 4 | O |
| 10 | CTO/리드 | 4 | 4 | 5 | **O (강추천)** |

**평균**: 이야기 4.0/5 · 기술 3.6/5 · 실습 3.7/5
**통과**: 10/10 (조건부 3명, 비통과 0명)

## 요약

- **최대 강점**: 네트워크 진화 정리표(L919~L923) — host.docker.internal → user-defined → Compose. 거의 전 페르소나가 백미로 호평
- **최대 약점**: ex07 entrypoint.sh의 `git clone + gradlew build` 패턴 — 첫 빌드 5~10분 + 컨테이너 immutability 위반
- **MySQL 데이터 보존(volumes) 부재** — SI·DevOps 두 페르소나가 강하게 지적. 3.4 실습·3.6 종합실습 모두 누락
- **3.2~3.5 캐릭터 부재** — 1인극 톤 (4명 지적)
- CTO는 **팀 온보딩 자료로 강추천** — 챕터 구조와 K8s 다리 역할 우수

## 공통 피드백 (3명 이상 동일 의견)

| 영역 | 피드백 | 언급 페르소나 | 심각도 |
|------|--------|-------------|--------|
| ex07 entrypoint.sh | `git clone + ./gradlew build at runtime` 함정. 첫 빌드 5~10분, 멈춘 줄 알고 Ctrl+C 위험. 컨테이너 immutability 위반 | 1, 2, 3, 4, 6, 9 | **높음** |
| 캐릭터 부재 | 3.2~3.5 거의 1인극. 동료/팀장 등장 거의 없음 | 3, 5, 9, 10 | **높음** |
| MySQL 데이터 보존 | 3.4·3.6에 `volumes:` 한 줄 없음. 컨테이너 삭제 시 데이터 증발 | 4, 7 | **높음** |
| MySQL 비밀번호 평문 | `MYSQL_ROOT_PASSWORD=root1234` 하드코딩 + Compose 평문. K8s로 미루지 말고 .env+env_file 즉시 시연 권장 | 4, 7 | 중간 |
| -dit/-p 옵션 회상 | 신입·비전공자에게 CH02에서 다뤘다고 가정하지 말고 한 번 더 미니박스 | 1, 6 | 중간 |
| nginx.conf/lb Dockerfile 본문 노출 | 폴더 트리 주석으로만 처리. 본문에 `COPY nginx.conf` 라인 직접 노출 필요 | 2, 6 | 중간 |
| Spring/gradlew 안전망 | 비전공·임베디드·프론트는 Spring 처음 봄. "내용은 몰라도 됨" 한 줄 | 6, 8 | 중간 |

## 강점 (전원 또는 다수 언급)

- 네트워크 진화 정리표(L919) — **9명 전원 백미로 호평**
- 선배의 "K8s에서 똑같은 게 더 큰 스케일로" 다리 멘트(L927) — 6명 호평 (단, 톤 정정 필요)
- ex01→ex06 점진 빌드업(특히 ex06이 ex01을 다시 만들며 service명 가치 체감) — 7명 호평
- NGINX 비유 (배달앱 주문 흐름·옷걸이 캐싱) — PM·프론트·신입 강한 호평
- Redis 사물함 비유 — PM·신입·CS 학생·임베디드 호평
- Compose 추상화 동기 부여 — 8명 호평 (Makefile→CMake 비유와 매핑되는 임베디드도 호평)

## 심각도별 이슈

### 높음

1. **ex07 `entrypoint.sh` 빌드 함정 — 6명 공통**
   - 위치: L832~L838
   - 증상: `git clone + chmod +x gradlew + ./gradlew build` 실행 시간 5~10분. 멈춘 듯 보여 Ctrl+C 좌절
   - 영향: 신입·비전공·임베디드는 빌드 도중 좌절, CS 학생·DevOps는 immutability 원칙 위반 지적
   - 제안:
     - L900 즈음 `:::tip` 박스로 "첫 실행 5~10분, 빌드 로그가 멈춘 듯 보여도 정상" 강화
     - L841 참고 박스를 **멀티스테이지 빌드 짧은 예시**로 확장
     - "운영에선 immutable 이미지에 JAR 포함" 톤을 더 강하게

2. **MySQL 데이터 보존 부재 — 2명 (SI·DevOps), 핵심 누락**
   - 위치: §3.4 MySQL 실습, §3.6 종합실습 db 서비스
   - 증상: `volumes:` 한 줄 없음. `docker compose down` 시 metadb 증발
   - 영향: SI 통과 조건부 (DBA 입장에서 무모해 보임)
   - 제안:
     - §3.4에 `docker run -v mysql-data:/var/lib/mysql` 한 단락 시연 → 컨테이너 삭제 후 named volume 잔존 확인
     - `init.sql`은 빈 데이터 디렉토리일 때만 동작 함정 박스 추가
     - §3.6 yml에도 `volumes:` 적용

3. **3.2~3.5 캐릭터 부재 — 4명 공통**
   - 위치: §3.2 NGINX부터 §3.5 Compose까지
   - 증상: 오픈이 내면독백 위주, 동료/팀장 등장 거의 없음. 후반부가 "혼자 책상에 앉은 다큐" 톤
   - 제안:
     - §3.2.4 라운드 로빈 직후 또는 §3.3 Redis 도입에 팀장/동료 한 줄 (비유 촉발)
     - §3.6 종합 실습 직후 동료 검증 대사 ("이제 한 줄로 다 뜨네요?") 1줄

### 중간

4. **MySQL 보안 평문 — 2명**
   - 위치: §3.4 ENV, §3.6 SPRING_DATASOURCE_PASSWORD
   - 제안: `.env` + `env_file:` 시연을 K8s로 미루지 말고 Compose 절에서 즉시 1회

5. **`-dit`/`-p` 옵션 회상 — 2명**
   - 위치: §3.1.3 첫 빌드
   - 제안: `-d`/`-i`/`-t`/`-p HOST:CONTAINER` 미니 표 한 번 더

6. **lb/Dockerfile, nginx.conf 본문 노출 — 2명**
   - 위치: §3.2 ex02 폴더 트리
   - 제안: `COPY nginx.conf /etc/nginx/conf.d/default.conf` 라인을 본문 코드블록으로 명시

7. **Spring/gradlew 안전망 — 2명**
   - 위치: ex07 entrypoint.sh 위
   - 제안: "Spring Boot가 뭔지 몰라도 됩니다. JAR이 결과물, gradlew는 그 빌드 도구" 1단락

8. **Compose `depends_on` 함정 — 1명 (DevOps)**
   - 위치: §3.6 docker-compose.yml
   - 제안: `healthcheck` + `condition: service_healthy` 1줄 시연 (Spring이 MySQL 초기화 전 연결 시도하는 함정 회피)

9. **DB 3306 호스트 노출 — 1명 (DevOps)**
   - 위치: ex07 db 서비스 `ports: 3306:3306`
   - 제안: 컨테이너 간만 필요하면 `ports:` 제거, 디버그용임을 명시

10. **NGINX 캐시 옵션 — 1명 (DevOps)**
    - 위치: §3.2.5 `proxy_cache_path`
    - 제안: `levels=`·`max_size=`·`inactive=` 운영 필수 옵션 1줄 주석

### 낮음

11. **선배 반말 톤 — 1명 (CTO)**
    - 위치: L927 "기억해 둬"
    - 제안: "기억해 둬요. 쿠버네티스에서 똑같은 게 더 큰 스케일로 나와요" — storytelling.md 대화체 톤 위반

12. **NGINX 골격 한 번 노출 — 1명 (데이터)**
    - 위치: §3.2.5 캐싱
    - 제안: `events{} / http{ proxy_cache_path; server{}}` 골격 한 번 보여주고 "이번엔 server 블록만"

13. **Redis 비유 보강 — 1명 (데이터)**
    - 위치: §3.3.1
    - 제안: "세션" 외 "Celery 큐, 캐시 레이어" 한 줄

14. **embedded DNS 127.0.0.11 — 1명 (CS)**
    - 위치: §3.3.3
    - 제안: "기본 bridge vs user-defined bridge — embedded DNS(127.0.0.11)" 1문단

15. **weighted round-robin 정정 — 1명 (CS)**
    - 위치: L359
    - 제안: "기본 정책은 가중 라운드 로빈(weight 미지정 시 균등)"

16. **MySQL `show databases;` 친절도 — 1명 (임베디드)**
    - 제안: "DB는 폴더, 테이블은 파일" 1문장 비유

17. **HTTP 흐름 도식 — 1명 (임베디드)**
    - 위치: §3.2.1 도입
    - 제안: 브라우저 → NGINX:80 → Backend:8080 1줄 도식

18. **K8s 예고 1행 — 1명 (CTO)**
    - 위치: L920 네트워크 진화 표
    - 제안: 4번째 행 "Kubernetes Service / 자동 DNS / 클러스터 스케일" 추가

## 페르소나별 상세 (요약)

### 1. 신입 백엔드 — 4/3/2 (조건부)
NGINX/Redis/Compose 비유는 우수. 환경 구축 디테일(폴더 위치, Dockerfile 저장 함정, ID 단축형) 산발적 누락. ex07 빌드 시간이 결정적 막힘.

### 2. 데이터 엔지니어 — 4/4/5
네트워크 진화 표가 압권. Compose는 Airflow 경험과 매핑. ex07 빌드 시간 + nginx.conf 골격 1회 노출 보강 필요.

### 3. 프론트엔드 — 4/3/4
Compose 도입 흐름은 거의 완벽. 다만 NGINX 직접 작성과 세션 처리는 "왜 프론트가 알아야 하나" 동기 약함. Vercel/Netlify 비교 1줄 권장.

### 4. SI 개발자 — 3.5/3.5/2.5 (조건부)
DB 데이터 보존 부재가 결정타. Oracle DBA 시각에서 무모. init.sql 함정 미언급. Compose 운영 적합성 결론(L944 5가지 운영 과제)을 더 일찍 노출 권장.

### 5. PM/기획자 — 4/5/4
NGINX·Redis·Compose 큰 그림이 회의 인용 수준. 후반 1인극 톤이 흠. 동료 검증 대사 1줄 권장.

### 6. 비전공 전직자 — 4.5/4/3.5
ex01→ex06 점진 학습은 부트캠프생에 맞춤. -dit·-p 옵션 회상, lb/Dockerfile 본문 노출, `compose up -d` 첫 시도 실패 1회 보강.

### 7. DevOps 엔지니어 — 4/3/3 (조건부)
운영 함정 5종(Dockerfile 모범사례, MySQL 평문, depends_on, db 포트 노출, NGINX 캐시 옵션) 누락. 그대로 사내 PoC 적용 시 사고 위험.

### 8. 임베디드 개발자 — 4/3/4
Compose가 Makefile→CMake 추상화와 매핑되어 호평. NGINX의 HTTP 단면, MySQL 폴더 비유, Spring 안전망 보강 필요.

### 9. CS 학생 — 4/4/4
네트워크 수업 키워드 매핑 우수. 정밀도 보강 — embedded DNS·weighted round-robin·immutability·캐릭터 보강.

### 10. CTO/리드 — 4/4/5 — **강추천**
팀 온보딩 자료로 매우 우수. 분량·구조·K8s 다리 역할 완벽. 선배 반말 톤·3.4 캐릭터 부재·utf8mb4 부연·K8s 행 추가만 다듬으면 완성.

## 수정 제안 (우선순위순)

| # | 위치 | 제안 | 심각도 | 관련 페르소나 |
|---|------|------|--------|-------------|
| 1 | ex07 entrypoint.sh + L900 + L841 | 첫 빌드 시간 경고 강화, 멀티스테이지 빌드 짧은 예시로 참고박스 확장 | 높음 | 1, 2, 3, 4, 6, 9 |
| 2 | §3.4 MySQL + §3.6 yml | named volume 마운트 시연 1단락 + init.sql 재실행 함정 박스 + yml에 `volumes:` | 높음 | 4, 7 |
| 3 | §3.2~§3.5 도입 1회씩 | 동료/팀장 한 줄 등장으로 1인극 해소 (비유 촉발 역할) | 높음 | 3, 5, 9, 10 |
| 4 | §3.4 ENV / §3.6 yml | `.env` + `env_file:` 시연 1회 (K8s까지 미루지 않기) | 중간 | 4, 7 |
| 5 | §3.1.3 첫 빌드 | `-d`/`-i`/`-t`/`-p` 미니 회상 표 | 중간 | 1, 6 |
| 6 | §3.2 ex02 폴더 트리 직후 | `COPY nginx.conf /etc/nginx/conf.d/default.conf` 본문 노출 | 중간 | 2, 6 |
| 7 | ex07 entrypoint.sh 위 | "Spring Boot 몰라도 됩니다. JAR 결과물, gradlew는 빌드 도구" 1단락 | 중간 | 6, 8 |
| 8 | §3.6 docker-compose.yml | `healthcheck` + `condition: service_healthy` 1줄 시연 | 중간 | 7 |
| 9 | ex07 db 서비스 | 호스트 3306 노출 제거 또는 디버그용 명시 | 중간 | 7 |
| 10 | §3.2.5 `proxy_cache_path` | `levels=`·`max_size=`·`inactive=` 운영 옵션 1줄 | 중간 | 7 |
| 11 | L927 선배 대사 | "기억해 둬" → "기억해 둬요" (캐주얼 존댓말) | 낮음 | 10 |
| 12 | §3.2.5 캐싱 | nginx.conf 골격 1회 노출 | 낮음 | 2 |
| 13 | §3.3.3 | embedded DNS(127.0.0.11) 1문단, default vs user-defined 차이 명시 | 낮음 | 9 |
| 14 | L359 라운드 로빈 | "기본 정책은 가중 라운드 로빈" 정정 | 낮음 | 9 |
| 15 | L920 네트워크 진화 표 | K8s Service 행 추가 | 낮음 | 10 |
| 16 | §3.4 `show databases;` 직전 | "DB는 폴더, 테이블은 파일" 1문장 | 낮음 | 8 |
| 17 | §3.2.1 도입 | HTTP 흐름 1줄 도식 (브라우저 → NGINX:80 → Backend:8080) | 낮음 | 8 |
| 18 | §3.4 진입 시점 | 캐릭터 등장 (오픈이 내면독백 1회) | 낮음 | 10 |

## 결론

- 네트워크 진화 표·Compose 추상화 동기·NGINX/Redis 비유는 거의 완성형. CTO 강추천.
- v4 결정타 3개: **(1) ex07 빌드 시간/immutability 경고 강화 + (2) MySQL volumes 추가 + (3) 3.2~3.5 캐릭터 1회씩 등장**
- DevOps 페르소나의 운영 함정 5종(평문 비밀번호·healthcheck·db 포트·NGINX 캐시·Dockerfile 모범사례)은 본문 흐름 유지하되 참고 박스로 처리 가능
- v3 대비 분량은 적절. 951라인이 입문 챕터로 적합. 이전 v3 지적 "이야기/캐릭터" 일부는 유지·일부는 후속 보강 필요
