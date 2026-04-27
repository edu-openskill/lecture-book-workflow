# Beta Reader 리포트: CH06 — Kubernetes 운영하기 (v4)

## 프로젝트
- 책: 특이점이 온 개발자 — 도커·쿠버네티스
- 대상 파일: `chapters/06-Kubernetes-운영하기.md` (563 라인) — 마지막 챕터
- 독자 상수: 입사 3~6개월차 주니어
- 평가 일자: 2026-04-27

## 페르소나 목록

| # | 이름 | 이야기 | 기술 | 실습 | 통과 |
|---|------|:----:|:----:|:----:|:----:|
| 1 | 신입 백엔드 | 4 | 3 | 2 | O (조건부) |
| 2 | 데이터 엔지니어 | 4 | 3 | 3 | O |
| 3 | 프론트엔드 | 4 | 4 | 3 | O |
| 4 | SI 개발자 | 4 | 3 | 3 | O (조건부) |
| 5 | PM/기획자 | 4 | 4 | 4 | O |
| 6 | 비전공 전직자 | 4 | 3 | 4 | O |
| 7 | DevOps 엔지니어 | 4 | 3 | 2 | **X (운영 함정 7종)** |
| 8 | 임베디드 개발자 | 3 | 4 | 3 | O |
| 9 | CS 학생 | 3 | 3 | 4 | O |
| 10 | CTO/리드 | 4.5 | 4 | 4.5 | **O (강력 추천)** |

**평균**: 이야기 3.85/5 · 기술 3.4/5 · 실습 3.25/5
**통과**: 9/10 (조건부 2명, 비통과 1명 — DevOps 운영 정확성)

## 요약

- **최대 강점**: §6.4 디버깅 4단계 (`get → describe → logs → endpoints`) + 종합 실습이 CH02~CH05 회수 — 4명 강한 호평. CTO 강력 추천
- **결정타 차단 이슈**: **이미지 경로가 `assets/CH05/`로 박혀 있음** — CH06 챕터 22·72·99·120·145·187·273·293·322·383·417·482·489 라인 일괄 정정 필요
- **MySQL을 Deployment로 띄우는 위험** — SI·DevOps·데이터 엔지니어 3명 동일 지적 (StatefulSet+volumeClaimTemplates 경고 필수)
- **6.3 종합실습 ConfigMap→Spring 매핑 부재** — 신입·프론트가 "ConfigMap의 conn_url이 Spring 어디로 가는지" 못 잡음
- 디버깅 4단계는 SI 1차 진단·임베디드 GDB와 동형 — 운영 입문 자산으로 작동

## 공통 피드백 (3명 이상 동일 의견)

| 영역 | 피드백 | 언급 페르소나 | 심각도 |
|------|--------|-------------|--------|
| 이미지 경로 오기 | `assets/CH05/` → `assets/CH06/` 일괄 정정 (라인 22·72·99·120·145·187·273·293·322·383·417·482·489) | 2, 3, 10 | **높음 (차단)** |
| MySQL Deployment 운영 위험 | StatefulSet+headless Service+volumeClaimTemplates 경고 박스 필수. Pod 재스케줄·RWO 락 충돌·데이터 손상 위험 | 2, 4, 7 | **높음** |
| ConfigMap → Spring 매핑 부재 | docker-compose env ↔ ConfigMap/Secret 키 ↔ Spring 프로퍼티 3열 매핑표, nginx.conf `proxy_pass` 발췌 | 1, 3 | **높음** |
| PV/PVC 클래스 vs 인스턴스 + 동적/정적 바인딩 | "정적 바인딩" 용어 갑자기 등장. PV(인스턴스) vs PVC(요구) vs StorageClass(클래스) 3단 추상화 표 | 1, 6, 8, 9 | 중간 |
| 6.3 후반 캐릭터 부재 | 종합실습 후반 + 6.4 디버깅에 캐릭터 부재. 팀장 한 줄 등장 권장 | 5, 9, 10 | 중간 |

## 강점 (다수 또는 전원 언급)

- §6.4 디버깅 4단계 — **6명 호평**. SI는 1차 진단 절차(`ps→tail→netstat`)와 동형, 임베디드는 GDB(`info threads→bt→print`)와 동형, CTO는 입문 운영에 충분
- §6.3 종합실습이 CH02~CH05 회수 — **CTO·데이터·프론트 강한 호평**. 표 6-3.4가 백미 ("어떤 자리가 어떤 문제를 푸는가")
- ConfigMap=메뉴판 / Secret=금고 / Volume=창고+신청서 비유 — PM·비전공 즉각 이해
- §6.1.4 "apply만으론 환경변수 안 바뀜" Try/Fail 장면 — 5명 호평
- §6.4 STATUS 3종(ImagePullBackOff·CrashLoopBackOff·Pending)을 "어디까지 진행됐는지"로 묶은 표 — 비전공·임베디드 호평
- "챕터 1 선배 'Docker 한번 알아봐'" 회수 — CTO 원형 서사 마무리로 호평

## 심각도별 이슈

### 높음

1. **이미지 경로 오기 — 3명, 차단 이슈**
   - 위치: 라인 22, 72, 99, 120, 145, 187, 273, 293, 322, 383, 417, 482, 489 (총 13개 이미지 경로)
   - 증상: CH06 챕터인데 `assets/CH05/` 폴더 참조 (또는 `chap03-*.png` 파일명 그대로)
   - 영향: HTML/PDF 빌드 시 404 또는 의도한 이미지와 다른 이미지 표시 가능
   - 제안: `assets/CH06/`로 일괄 정정. 파일도 함께 이동 or symlink

2. **MySQL Deployment vs StatefulSet — 3명**
   - 위치: §6.3.4 DB 절
   - 증상: MySQL을 Deployment로 띄우는 학습용 구성에 운영 경고 약함. 553라인 마치며에서 StatefulSet "DB 클러스터 등"으로만 처리
   - 영향: 입문자가 실무에 그대로 적용 시 Pod 재스케줄·RWO 락 충돌·데이터 정합성 사고 위험
   - 제안:
     - §6.3.4 DB 절 끝에 경고 박스 1단락 — "단일 Pod 한정. 운영은 StatefulSet + headless Service + volumeClaimTemplates"
     - 553라인 StatefulSet 설명 구체화 — "Pod 정체성과 저장소가 1:1로 묶여야 하는 DB·Kafka·Elasticsearch"

3. **ConfigMap → Spring 매핑 부재 — 2명**
   - 위치: §6.3.4 Backend 절 (L443~)
   - 증상: "ConfigMap에는 DB 접속 URL, JDBC 드라이버, Redis 호스트와 포트"라고 글로만 풀어놓음. 실제 키↔Spring 프로퍼티 매핑 없음
   - 영향: 신입은 `application.yml`의 `spring.datasource.url`이 ConfigMap의 `conn_url`과 어떻게 연결되는지 못 잡음, 프론트는 `nginx.conf`의 `proxy_pass http://backend-service:8080`이 어디 있는지 모름
   - 제안:
     - 환경변수 매핑 표 1개 — docker-compose env ↔ ConfigMap/Secret 키 ↔ Spring Boot 프로퍼티 3열
     - frontend 절(L439~)에 `nginx.conf`의 `proxy_pass http://backend-service:8080;` 한 줄 발췌
     - 방문 카운터 시퀀스 한 줄 — `브라우저 → Ingress → frontend → /api/visit → backend → redis-service`

### 중간

4. **DevOps 운영 함정 7종 (P7 단독 지적이지만 신뢰도 결정타)**
   - **Secret Base64 본문 강화** — 참고박스만으론 약함. 본문에 명시 + SealedSecrets·External Secrets·etcd encryption 1줄
   - **hostPath 운영 금지** — 노드 파일시스템 직접 접근 권한 상승 공격 벡터, PSA 차단 대상. CSI 동적 프로비저닝(EBS·EFS·Ceph) 한 줄
   - **envFrom 함정** — `envFrom`로 모든 키 일괄 주입 시 키 충돌·앱이 모르는 환경변수 오염. 명시 주입 패턴 권장
   - **RBAC 디버깅 단계** — 4단계에 "5. ServiceAccount/RBAC 권한 확인" 추가
   - **Git 평문 저장 우려** — `stringData` 평문이 Git에 들어가는 흐름. SOPS·git-crypt·ESO 1단락 경고
   - 위치: §6.1.3, §6.2.1, §6.4

5. **PV/PVC/StorageClass 추상화 정밀도 — 4명**
   - 위치: §6.2.2 L191~L215
   - 증상:
     - PV "공간"과 PVC "신청서"가 모두 "공간/신청서"로만 표현 → 인스턴스 vs 명세 대비 흐림 (CS 학생)
     - "정적 바인딩" 용어가 갑자기 등장 (비전공)
     - StorageClass가 "저장소 종류 이름"인지 "동적 프로비저너 클래스"인지 모호 (CS 학생)
     - hostPath의 노드 이동 시 한계 명시 부족 (SI)
   - 제안:
     - L191~192: "PV는 클러스터 관리자가 미리 만들어 둔 **실제 창고 한 칸**, PVC는 사용자의 **창고 요구 명세**" 인스턴스 vs 명세 대비
     - L215 `storageClassName: ""` 뒤: "동적 바인딩(StorageClass가 PV 자동 생성) vs 정적 바인딩(미리 만든 PV에 수동 연결)" 1줄
     - StorageClass 절 신설 (3단 추상화 표 — PV/PVC/StorageClass)

6. **6.3 캐릭터 부재 — 3명**
   - 위치: §6.3 후반 + §6.4
   - 제안:
     - §6.3.5 결과 확인 직후 동료 검증 한 줄 ("비밀번호도 안 보이고 데이터도 살아있네요?")
     - §6.4 도입에 팀장 "장애 났을 때 제일 먼저 어디 봐요?" 한 줄 (4단계 도출 동기)

7. **AccessMode ReadWriteOnce — 1명 (SI)**
   - 위치: §6.2.2
   - 제안: "한 노드에서만 마운트 가능 → DB 클러스터링 제약" 1줄 보강

8. **stringData vs data — 1명 (비전공)**
   - 위치: §6.1.3 L88~L89
   - 제안: "data(Base64 직접) vs stringData(평문→자동변환)" 1줄 비교

9. **envFrom 하이픈 list 설명 — 1명 (비전공)**
   - 위치: L55~58, L113~118
   - 제안: `- configMapRef:`의 하이픈이 list 항목임을 1줄 주석

10. **volume mount 자동 갱신 대안 — 1명 (CS)**
    - 위치: §6.1.4 환경 변수 갱신 한계 설명
    - 제안: "volume mount로 ConfigMap을 파일로 주입하면 갱신 자동 반영. 이 책은 envFrom만 다룸" 1줄

11. **`exec -it` 디버깅 5단계 — 1명 (SI)**
    - 위치: §6.4.3
    - 제안: 4단계 후 "5. `kubectl exec -it <pod> -- /bin/sh` 컨테이너 내부 진단" 추가 (WAS 서버 SSH 감각)

### 낮음

12. **ContainerCreating 시간 구체화 — 2명 (P1, P6)**
    - 위치: §6.3.5 L470
    - 제안: "한참" → "약 1~3분 (Gradle 빌드 시간)"

13. **PV `hostPath` 학습용 명시 — 1명 (P1)**
    - 위치: §6.2.2 L209~215
    - 제안: "Minikube 학습용이라 동적 프로비저닝 대신 정적 바인딩" 1줄

14. **Redis 방문 카운터 코드 — 1명 (P1)**
    - 위치: §6.3.4 Redis 절 L450~453
    - 제안: 백엔드의 어느 코드가 Redis INCR을 호출하는지 1줄

15. **추상화별 트러블슈팅 — 1명 (P1)**
    - 위치: §6.4.2 에러 표 L519~529
    - 제안: ConfigMap·Secret·PV·PVC 각각의 실패 사례 1줄 — "Secret 키 오타로 CrashLoopBackOff", "PVC Pending 시 PV 용량·storageClassName 확인"

16. **펌웨어/일반 디버깅 매핑 — 1명 (P8)**
    - 위치: §6.4.2 표
    - 제안: ImagePullBackOff=binary fetch, CrashLoopBackOff=init/main crash, Pending=리소스 할당 실패 매핑 칼럼

17. **PM 시점 회수 — 1명 (P5)**
    - 위치: §6.3.5 결과 확인 직후
    - 제안: "비밀번호는 YAML에 평문으로 없고, DB Pod 지워도 데이터 살아있다" 두 줄 검증 — 챕터 도입의 세 문제 회수

18. **6.4 → 마치며 연결문 — 1명 (CTO)**
    - 제안: "이제 막힌 곳을 좁히는 법까지 익혔다" 1줄 회고

19. **마치며 7개 항목 한 줄 설명 — 1명 (CTO)**
    - 위치: 553라인 StatefulSet/HPA/Helm 등
    - 제안: 제목만 던지지 말고 "왜 다음에 이걸 봐야 하는지" 한 줄씩

## 페르소나별 상세 (요약)

### 1. 신입 백엔드 — 4/3/2 (조건부)
ConfigMap→Secret→PV/PVC 비유는 "왜 필요한가" 자연스러움. 6.3 종합실습에서 ConfigMap의 conn_url이 Spring `application.yml`로 어떻게 매핑되는지 없어 막힘. PV 정적 바인딩 이유, Redis 카운터 코드 부재.

### 2. 데이터 엔지니어 — 4/3/3
Airflow Variable=ConfigMap, Connection=Secret 매핑 자연스러움. **MySQL Deployment 위험 + StatefulSet 단서 강화 + 이미지 경로 CH05 오기 발견** + SealedSecrets/External Secrets 1줄.

### 3. 프론트엔드 — 4/4/3
ConfigMap=메뉴판 / Secret=금고 비유 직관적. **환경변수 매핑 표 + nginx.conf proxy_pass 발췌 + 방문 카운터 시퀀스 + kubectl rollout restart 무중단 배포 연결 + 이미지 경로 CH05 확인**.

### 4. SI 개발자 — 4/3/3 (조건부)
"운영 DB 비번 Git 사고" 공감 강함. **DB Deployment는 위험한 가르침 — 경고 박스 필수**. AccessMode ReadWriteOnce 의미, hostPath 한계, exec -it 디버깅 5단계 추가.

### 5. PM/기획자 — 4/4/4
오프닝 보안 리스크가 PM 즉시 공감. PV/PVC 분리 이유를 "인프라팀=창고관리자, 개발팀=신청서작성자" 조직 분담으로. §6.3.5 두 줄 검증 장면 + Try/Fail 미니 에피소드.

### 6. 비전공 전직자 — 4/3/4
**§6.4 디버깅이 백미**. envFrom 하이픈 list 설명, stringData vs data 비교, "정적 바인딩" 풀어쓰기, ContainerCreating 시간 구체화 필요.

### 7. DevOps 엔지니어 — 4/3/2 — **비통과**
"운영 서적이라는 챕터 제목에 비해 실전 함정 경고가 결정적으로 빠짐". MySQL Deployment·hostPath·envFrom·RBAC·External Secrets·SealedSecrets 등 **운영 함정 7종** 보강 필수.

### 8. 임베디드 개발자 — 3/4/3
디버깅 4단계가 GDB와 동형. **StorageClass 절 신설 — PV/PVC/StorageClass 3단 추상화 표** + 디버깅 펌웨어 매핑(binary fetch/init crash/리소스 할당) + 단계별 검증 체크포인트.

### 9. CS 학생 — 3/3/4
**PV/PVC 클래스 vs 인스턴스 매핑 빠짐**. StorageClass가 클래스인지 태그인지 모호. volume mount 자동 갱신 대안 1줄. 6.3 후반 캐릭터 부재.

### 10. CTO/리드 — 4.5/4/4.5 — **강력 추천**
"챕터 1 선배 'Docker 한번 알아봐'" 원형 서사 마무리 압권. 팀 온보딩 자료 강력 추천. **이미지 경로 CH05 오류 라인 명시** + §6.4 캐릭터 1회 + 마치며 7개 항목 한 줄 설명 + 6.4→마치며 연결문.

## 수정 제안 (우선순위순)

| # | 위치 | 제안 | 심각도 | 관련 페르소나 |
|---|------|------|--------|-------------|
| 1 | 라인 22·72·99·120·145·187·273·293·322·383·417·482·489 | 이미지 경로 `assets/CH05/` → `assets/CH06/` 일괄 정정 (출간 차단) | **높음** | 2, 3, 10 |
| 2 | §6.3.4 DB 절 끝 + 553라인 마치며 | MySQL Deployment 경고 박스 + StatefulSet 설명 구체화 | **높음** | 2, 4, 7 |
| 3 | §6.3.4 Backend 절 (L443~) | docker-compose env ↔ ConfigMap/Secret ↔ Spring 프로퍼티 3열 매핑표 | **높음** | 1, 3 |
| 4 | §6.3.4 Frontend 절 (L439~) | `nginx.conf`의 `proxy_pass http://backend-service:8080;` 1줄 발췌 + 방문 카운터 시퀀스 | **높음** | 1, 3 |
| 5 | §6.1.3 Secret 본문 | Base64 ≠ 암호화 본문 강화 + SealedSecrets·External Secrets·etcd encryption 1줄 | 중간 | 7, 9 |
| 6 | §6.2.1 hostPath 박스 | "운영 절대 금지. CSI 드라이버(EBS·EFS·Ceph) 사용" 1줄 | 중간 | 4, 7 |
| 7 | §6.1 ConfigMap 끝 또는 §6.3.4 | `envFrom` 키 충돌 함정 + 명시 주입(`env.valueFrom.configMapKeyRef`) 권장 1줄 | 중간 | 6, 7 |
| 8 | §6.2.2 L191~L215 | PV(인스턴스) vs PVC(명세) 대비 + 동적/정적 바인딩 + StorageClass 3단 추상화 표 | 중간 | 1, 6, 8, 9 |
| 9 | §6.4.3 디버깅 5단계 | "5. `kubectl exec -it`" + "ServiceAccount/RBAC 권한 확인" 추가 | 중간 | 4, 7 |
| 10 | §6.3.5 결과 확인 직후 + §6.4 도입 | 동료/팀장 한 줄 등장 (검증 + 디버깅 동기) | 중간 | 5, 9, 10 |
| 11 | §6.2.2 AccessMode | "ReadWriteOnce = 한 노드에서만 마운트 가능 → DB 클러스터 제약" 1줄 | 중간 | 4 |
| 12 | §6.1.3 L88~L89 | "data(Base64 직접) vs stringData(평문→자동변환)" 1줄 | 낮음 | 6 |
| 13 | L55~58, L113~118 | `- configMapRef:` 하이픈이 list 항목임을 1줄 주석 | 낮음 | 6 |
| 14 | §6.1.4 환경변수 갱신 한계 | "volume mount로 ConfigMap 파일 주입 시 자동 갱신. 이 책은 envFrom만" 1줄 | 낮음 | 9 |
| 15 | §6.3.5 L470 | "한참" → "약 1~3분 (Gradle 빌드)" 구체화 | 낮음 | 1, 6 |
| 16 | §6.2.2 L209~215 | "Minikube 학습용 정적 바인딩" 이유 1줄 | 낮음 | 1 |
| 17 | §6.3.4 Redis 절 | 백엔드의 어느 코드가 INCR 호출하는지 1줄 | 낮음 | 1 |
| 18 | §6.4.2 에러 표 | 추상화별 트러블슈팅 (ConfigMap·Secret·PV·PVC) 1줄씩 | 낮음 | 1 |
| 19 | §6.4.2 표 | 펌웨어/일반 디버깅 매핑 칼럼 (binary fetch / init crash / 리소스 할당) | 낮음 | 8 |
| 20 | §6.3.5 결과 확인 직후 | "비번 평문 없음 + DB 데이터 살아있음" 두 줄 회수 (도입 3문제 닫기) | 낮음 | 5 |
| 21 | §6.4 끝 | "이제 막힌 곳을 좁히는 법까지 익혔다" 1줄 회고 | 낮음 | 10 |
| 22 | 553라인 마치며 7개 항목 | StatefulSet/HPA/Helm 한 줄씩 설명 | 낮음 | 10 |

## 결론

- §6.4 디버깅 4단계 + §6.3 종합실습은 책 전체 회수의 백미. CTO 강력 추천.
- v4 결정타 4개:
  1. **이미지 경로 `assets/CH05/` → `assets/CH06/` 13곳 일괄 정정 (출간 차단)**
  2. **MySQL Deployment 경고 박스 (StatefulSet 권장)**
  3. **6.3.4 ConfigMap→Spring 매핑 표 + nginx.conf proxy_pass 발췌**
  4. **PV/PVC/StorageClass 3단 추상화 + 동적/정적 바인딩 명시**
- DevOps 운영 함정 7종은 본문 흐름 유지하되 참고박스 한 줄씩 추가. 추가 시 4년차 신뢰도 회복
- 통과율 9/10 — 운영 정밀도 + 이미지 경로 정정 시 10/10 가능
