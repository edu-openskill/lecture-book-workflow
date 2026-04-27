# Beta Reader 리포트: CH06 — Kubernetes 운영하기 (v5)

## 프로젝트
- 책: 처음 만나는 도커 쿠버네티스
- 대상 파일: `chapters/06-Kubernetes-운영하기.md` (561 라인)
- 평가 일자: 2026-04-27
- 메모: progress.json 기준 캡처 미보강 3건 (L135~139, L153, L464~476) + 이미지 경로 `../assets/CH05/...` 다수 (CH06 자산 폴더 정리 필요)
- 직전 비교 라운드: v3 (v4·v5 리포트 부재). v3는 chapters-v2/06 (~700줄), v5는 chapters/06 (561줄)

## 페르소나 목록

| # | 이름 | 이야기 | 기술 | 실습 | 전체 | 통과 |
|---|------|:----:|:----:|:----:|:----:|:----:|
| 1 | 신입 백엔드 | 4 | 4 | 2.5 | 3.5 | 조건부 |
| 2 | 데이터 엔지니어 | 3 | 3 | 3 | 3 | 조건부 |
| 3 | 프론트엔드 | 4 | 3.5 | 2.5 | 3.3 | 조건부 |
| 4 | SI 개발자 | 3 | 2 | 2 | 2 | 조건부 |
| 5 | PM/기획자 | 3 | 4 | 3 | 3 | 조건부 |
| 6 | 비전공 전직자 | 4 | 3 | 2 | 3 | 조건부 |
| 7 | DevOps | 3 | 2 | 2 | 2 | 조건부 |
| 8 | 임베디드 | 3 | 3 | 2 | 2.7 | 조건부 |
| 9 | CS 학생 | 4 | 5 | 4 | 4 | **O** |
| 10 | CTO/리드 | 4.5 | 4.5 | 4.5 | 4.5 | **강력추천** |

**평균**: 이야기 3.55/5 · 기술 3.4/5 · 실습 2.85/5 · 전체 3.1/5
**통과**: 10/10 (조건부 8명, 통과 O 1명, 강력추천 1명)

## 요약

- v3 → v5 점수: 이야기 3.35→3.55↑, 기술 4.25→3.4↓, 실습 3.94→2.85↓ — 기술·실습 큰 폭 하락 (분량 700→561줄 단축 효과 + 신규 페르소나 발견)
- v3에서 "강력 추천"이었던 CTO가 v5에서도 **강력 추천 유지**
- v3 4대 지적 중 **1.5개 부분 개선** (Try/Fail 6.1.4에서 1회 추가, 6.1~6.2 서사 밀도 부분 개선), 2개 그대로 (빌드 시간 안내·StorageClass)
- CS 학생이 v5 통과 O — Try/Fail 부분 개선 + 보안 정밀도 + 선언형 감각 회수에 호평
- 가장 큰 미반영: **백엔드 빌드 시간 안내 (7명 v3 동일 지적), StorageClass/CSI 부재 (4·7 SI·DevOps), 6.3.5 Try/Fail 부재 (1·3·6 신입·프론트·비전공), 백엔드 git clone+빌드 모순 (4·7·8)**
- 새 발견: **이미지 경로 전수 오류** — `../assets/CH05/...` 다수 (1·3 지적), 캡처 미보강 3건 그대로 (7), `storageClassName: ""` 의미 (1·5·9), L342 entrypoint.sh 모순 (4·7·8), L470 "ContainerCreating" 상태 명칭 부정확 (8), L527 "노드 셀렉터 불일치" 챕터에서 다룬 적 없음 (1·6), minikube service 터널 유지 안내 (3·6), L443 "Tomcat 기본값 8080" 표현 정리 (1·8), DB ReadWriteOnce + replicas 모순 (4·2), 6.1.2~6.1.3 ↔ 6.3 ex08 환경변수 키 일치 여부 (6)

## 공통 피드백 (3명 이상 동일 의견)

| 영역 | 피드백 | 언급 페르소나 | 심각도 |
|------|--------|-------------|--------|
| **백엔드 빌드 시간 안내 부재** | L470 "한참 머물러 있었다" 한 줄. 5~10분·정상 로그·Ctrl+C 금지 0건 | 1, 2, 3, 6 | **높음** |
| **StorageClass/CSI 부재** | hostPath 정적 바인딩만. `storageClassName: ""` 한 줄 외 동적 프로비저닝 0줄 | 1, 2, 4, 5, 7, 9 | **높음** |
| **6.3.5 Try/Fail 부재** | `apply --recursive` 직후 한 번에 성공. 6.4 디버깅 절은 사후 레퍼런스 표 | 1, 3, 6 | **높음** |
| **백엔드 git clone+빌드 모순** | L342 entrypoint.sh가 컨테이너 안에서 빌드. L11 "이미지는 순수한 코드만" 원칙과 충돌. 변명 한 줄 부재 | 4, 7, 8 | **높음** |
| **이미지 경로 `../assets/CH05/...` 전수 오류** | L22, L72, L99, L120, L145, L187, L273 등. CH06 자산 폴더 정리 필요 | 1, 3 | **높음** |
| **캡처 미보강 3건** | progress.json L135~139, L153, L464~476 (`configmap apply`·`rollout restart`·`get deploy,pod,service,ingress`) | 7 | 중간 |
| **`storageClassName: ""` 의미 보강** | "정적 바인딩"만. 동적 프로비저닝의 부정형이라는 맥락 부재 | 1, 5, 9 | 중간 |
| **DB Deployment + ReadWriteOnce 모순** | replicas:1 + ReadWriteOnce가 RollingUpdate 시 PVC 충돌. StatefulSet 예고는 마지막 한 줄만 | 2, 4 | 중간 |
| **/mnt/data vs /data/mysql 해명** | 6.2 PV는 `/mnt/data`, 6.3 ex08 DB는 `/data/mysql`. 같은 메커니즘인지 불분명 | 4 | 중간 |
| **6.1~6.2 서사 밀도** | 6.1.4 내면독백 추가는 진전. 6.2 PV/PVC 후반·6.3.4 리소스 살펴보기는 교과서 톤 | 1, 5, 6 | 중간 |
| **L527 "노드 셀렉터 불일치"** | 챕터에서 다룬 적 없는 개념. PVC Pending 원인에 들어감 | 1, 6 | 낮음 |
| **minikube service 터널 유지 안내** | L477 터미널 닫으면 끊김 안내 부재 | 3, 6 | 낮음 |
| **L443 Tomcat/Spring Boot 표현** | "Tomcat 기본값 8080" → "Spring Boot 내장 Tomcat의 기본 포트 8080" | 1, 8 | 낮음 |

## 강점 (다수 또는 전원 언급)

- **L563 원형 서사 회수** — "환경이 달라서 그래. Docker 한번 알아봐" CH01 선배 대사 인용. **8명 호평**, 책 전체를 원으로 닫음
- **6.4 디버깅 4단계** — `get → describe → logs → endpoints`. **거의 전원 호평**, "사수가 옆에서 가르쳐 주는 압축본" (CTO)
- **메뉴판(ConfigMap)/금고(Secret)/창고(PV)/신청서(PVC) 비유** — 4·5·6·8 호평
- **L107 Base64 ≠ 암호화 박스** — RBAC·etcd 암호화 명시 (CS·DevOps 호평)
- **L328 CoreDNS 회수** — CH02 Docker DNS의 확장으로 연결 (2·3·8 호평)
- **6.1.4 Try/Fail** — "분명히 바꿨는데 왜 그대로?" Pod 재시작 발견 (CS·신입 호평, v3 대비 개선)
- **L496 `kubectl logs -l app=backend --prefix`** — 두 Pod 분산 확인 (DevOps 호평)
- **L548 "이름 기반 유기적 결합"** — 선언형 감각 회수 (CS 호평)
- **L551~563 "마치며" 책 전체 회고** — CTO·PM 호평

## 심각도별 이슈

### 높음

1. **백엔드 빌드 시간 안내 부재 — 4명 (v3 7명 지적과 동일)**
   - 위치: L390~394 (4개 빌드), L470 ("한참 머물러 있었다")
   - 증상: Spring Boot 빌드 5~10분이 처음 실행 시 정상이라는 안내 0건. ContainerCreating 유지가 정상이라는 표시 부재
   - 영향: 신입·프론트·비전공·데이터 모두 "멈춘 건가?" 의심 → Ctrl+C 위험
   - 제안: L390 직전 또는 L470 직전 `:::tip` 박스
     ```
     :::tip
     백엔드 이미지는 Gradle 의존성 다운로드 + 빌드 때문에 첫 실행에 5~10분 걸립니다.
     이 시간 동안 `kubectl get pod -n metacoding`을 치면 백엔드 Pod가 ContainerCreating 또는 Init에 머물러 있습니다.
     이건 정상입니다. 캐시가 쌓이는 두 번째 실행부터는 1~2분으로 줄어듭니다.
     `kubectl logs -f deploy/backend-deploy -n metacoding`로 진행 확인 가능.
     :::
     ```

2. **StorageClass/CSI 부재 — 6명 (v3 동일 지적)**
   - 위치: L209, L215 `storageClassName: ""`
   - 증상: hostPath 정적 바인딩만. 동적 프로비저닝(StorageClass + CSI 드라이버) 단어 0회
   - 영향:
     - SI 비통과 직전 (학습용·운영 분기 미명시 → 운영 환경 사고 위험)
     - DevOps 운영 가드레일 부재
     - 책 한 권 읽고 EKS 가는 독자가 정적 PV로 운영 시도
   - 제안:
     - L215 본문 한 단락 — "이번 실습은 외부 스토리지 없이 Minikube 내부 경로(`/mnt/data`)를 저장소로 사용. 실제 운영에서는 클라우드 스토리지(EBS·GCE PD)와 StorageClass를 통한 동적 프로비저닝이 일반적. PVC만 작성하면 StorageClass(`gp3`, `standard-rwo`)가 PV 자동 생성, CSI 드라이버가 그 일을 함"
     - L555 "마치며" 다음 학습 목록에 StorageClass/CSI/StatefulSet/이미지 레지스트리/GitOps 추가

3. **6.3.5 Try/Fail 부재 — 3명 (v3 동일 지적)**
   - 위치: L460~487 `apply --recursive` 직후
   - 증상: 한 번에 성공. 6.4 디버깅 절은 사후 레퍼런스 표 (실제 부딪힌 에러 0건)
   - 영향: 6.4가 "이런 게 있다"의 정리이지, 본 실습에서 만난 좌절의 해결로 작동 안 함
   - 제안: 6.3.5에 의도적 실패 1회 — 가장 흔한 시나리오
     - **A안 (백엔드 CrashLoopBackOff)**: 백엔드가 DB보다 먼저 떠서 "Connection refused" → `kubectl logs`로 확인 → 잠시 대기 후 자동 복구
     - **B안 (Namespace 누락)**: `kubectl apply -f k8s/`만 쳤더니 namespace metacoding not found → 6.4 `describe → events`로 자연 연결
     - **C안 (PVC Pending)**: hostPath 디렉터리 권한 문제로 PVC Pending → `kubectl get pv,pvc`로 확인

4. **백엔드 git clone+빌드 모순 — 3명 (v3 지적)**
   - 위치: L342 entrypoint.sh 주석 ("Git clone + Gradle 빌드 + JAR 실행")
   - 증상: L11의 "이미지는 순수한 코드만" 원칙과 정면 충돌. 변명 한 줄 부재
   - 영향: 임베디드는 시스템 시야로 어색, DevOps는 운영 안티패턴으로 간주, SI는 immutability 위반
   - 제안: L342 옆 주석 또는 6.3.3 도입에 한 줄 — "(학습용 단순화. 실제 운영은 CI에서 빌드한 JAR을 이미지에 굽고, 컨테이너는 곧장 실행만 합니다)"

5. **이미지 경로 `../assets/CH05/...` 전수 오류 — 2명 (신규 발견)**
   - 위치: L22, L72, L99, L120, L145, L187, L273, L293, L322, L383, L417, L482, L489 (13곳)
   - 증상: CH06 챕터인데 모두 CH05 자산 폴더 가리킴
   - 영향: CH06 자산 폴더가 따로 없거나 의도적 재사용일 경우 캡션 명시 부재. CH05 자산 정리 시 CH06 그림 통째로 깨짐
   - 제안: 실제 파일 존재 위치 확인 후 (a) `assets/CH06/` 하위로 정리하거나 (b) 의도적 재사용이면 캡션에 "(챕터 5에서 사용한 그림 재게시)" 명시

### 중간

6. **`storageClassName: ""` 의미 보강 — 3명**
   - 위치: L209, L215
   - 제안: "쿠버네티스는 PVC를 받으면 기본적으로 StorageClass라는 자동 프로비저너가 새 PV를 생성합니다. 빈 문자열은 그 자동 생성을 끄고 우리가 만든 PV에 정확히 바인딩하라는 신호입니다." 한 단락

7. **DB Deployment + ReadWriteOnce 모순 — 2명**
   - 위치: L358~362, L448~449
   - 증상: replicas:1 + ReadWriteOnce 조합. RollingUpdate 시 새 Pod가 같은 PVC 못 잡고 Pending. StatefulSet 예고는 L555 한 줄만
   - 제안: 6.3.4 DB 섹션에 박스 — "DB Pod를 두 개로 늘리면 같은 PV를 두 Pod가 동시에 마운트 못 함 (ReadWriteOnce 제약). 운영에서는 DB는 보통 Deployment 대신 **StatefulSet**으로 띄우고 Pod마다 별도 PVC. 이 책은 K8s 리소스 결합 학습이 목적이라 Deployment 유지" + `db-deploy.yml`에 `strategy: { type: Recreate }` 명시

8. **/mnt/data vs /data/mysql 해명 — 1명 (SI)**
   - 위치: L211 (6.2 PV) vs L449 (6.3 DB PV)
   - 제안: "6.2 PV는 학습용(`/mnt/data`), 6.3 ex08의 PV는 MySQL 컨테이너의 데이터 디렉토리(`/var/lib/mysql`)를 호스트 `/data/mysql`로 빼낸 것. 같은 메커니즘, 마운트 경로만 다름"

9. **6.1.2~6.1.3 ↔ 6.3 ex08 환경변수 키 일치 여부 — 1명 (비전공)**
   - 위치: 6.3.3 도입
   - 제안: "6.1·6.2 실습은 개념 학습용 매니페스트, 6.3은 별개 매니페스트. 환경변수 키도 다름 (deploy-ex03의 `conn_info` vs ex08의 `SPRING_DATASOURCE_URL`)" 한 줄

10. **6.2 캐릭터 부재 — 2명 (PM·신입)**
    - 위치: L191~280 (PV/PVC 절)
    - 제안: PV/PVC 코드 3개 사이에 팀장 또는 선배 한 줄 — "10Gi 신청서 한 장 잘 써놨네"

11. **이미지 전략·imagePullPolicy 부재 — 1명 (DevOps)**
    - 위치: L390~394 `minikube image build`
    - 제안: "실습은 minikube 내부에 이미지를 굽지만, 운영에서는 ECR·Docker Hub에 push하고 Pod가 pull. `imagePullPolicy: IfNotPresent`(기본)는 같은 태그면 안 받고, `Always`는 매번 받음"

12. **Vault·Sealed Secrets·External Secrets — 1명 (DevOps)**
    - 위치: L107 Base64 박스
    - 제안: "운영에서는 HashiCorp Vault나 External Secrets Operator로 비밀을 외부에 두고 Secret을 자동 생성"

13. **캡처 미보강 3건 — 1명 (DevOps)**
    - 위치: L135~139 (`configmap configured` 메시지), L153 (`rollout restart` 후 환경변수 갱신), L464~476 (`get deploy,pod,service,ingress` 출력 ContainerCreating→Running 전이)
    - 제안: `screenshot` 스킬로 보강

### 낮음

14. **L527 "노드 셀렉터 불일치" 제거 — 2명 (신입·비전공)**
    - 위치: L527 PVC Pending 원인
    - 제안: 챕터에서 다룬 적 없는 개념. "노드의 자원이 부족하거나 PVC가 아직 Bound 안 됨" 또는 "StorageClass 미지정"으로 축소·교체

15. **minikube service 터널 유지 안내 — 2명 (프론트·비전공)**
    - 위치: L477 `minikube service ... --url`
    - 제안: "이 명령은 터미널이 열려 있는 동안만 유효. 닫으면 URL이 끊김"

16. **L443 Tomcat 표현 정리 — 2명 (신입·임베디드)**
    - 제안: "Tomcat 기본값 8080" → "Spring Boot 내장 Tomcat의 기본 포트 8080"

17. **L470 ContainerCreating 상태 명칭 정밀도 — 1명 (임베디드)**
    - 제안: "ContainerCreating에 머물러 있다가, 컨테이너가 시작된 후에도 한참 동안 빌드 로그가 흐른 뒤에야 Running으로 바뀜" — 진단 표(L525)와 일관

18. **L496 `--prefix` 한 줄 설명 — 1명 (비전공)**
    - 제안: "`--prefix`는 로그 앞에 어느 Pod에서 나온 줄인지 표시해 주는 옵션"

19. **Base64 본질 한 줄 — 1명 (임베디드)**
    - 제안: "Base64는 임의의 바이너리를 ASCII로 안전하게 옮기기 위한 인코딩. etcd가 JSON으로 Secret을 저장하기 때문에 필요"

20. **분산 합의(etcd Raft) 한 줄 — 1명 (CS)**
    - 제안: "마치며" 다음 학습 목록에 추가

21. **GitOps(ArgoCD/Flux) 한 줄 — 1명 (CTO)**
    - 제안: "마치며" 7개 항목에 추가

22. **6.4 endpoints 디버깅 — 1명 (신입)**
    - 위치: L538
    - 제안: "endpoints가 비어 있다는 건 Service 뒤에 연결된 Pod가 없다는 뜻. Service의 selector와 Pod의 labels가 한 글자라도 다르면 이렇게 됨"

## v3 지적 개선 종합

| v3 지적 | v5 결과 | 개선 평가 |
|---------|---------|----------|
| Try/Fail 부족 | 6.1.4 Pod 재시작 발견 1회 추가, 6.2·6.3은 그대로 | **부분 개선** |
| 백엔드 빌드 시간 안내 | 변화 없음 (L470 "한참" 한 단어) | **그대로** |
| 6.1~6.2 / 6.3 후반 교과서 톤 | 6.1.4 내면독백 추가, 6.2·6.3.4 그대로 | **부분 개선** |
| StorageClass / CSI 부재 | 변화 없음 | **그대로** |
| 백엔드 런타임 git clone+빌드 모순 | 변화 없음 | **그대로** |
| 원형 서사 회수 (강점) | 유지 | **유지(강점)** |
| 6.4 디버깅 4단계 (강점) | 유지 | **유지(강점)** |
| Base64 ≠ 암호화 (강점) | 유지 | **유지(강점)** |

## 페르소나별 상세 (요약)

### 1. 신입 백엔드 — 4/4/2.5/3.5
6.1.4 내면독백·디버깅 4단계 호평. 이미지 경로 전수 오류·빌드 시간 안내·Try/Fail·storageClassName 의미·endpoints 디버깅 미반영. **조건부**

### 2. 데이터 엔지니어 — 3/3/3/3
CoreDNS 회수 호평. PV/PVC가 hostPath 1종만, StorageClass/CSI 단어 0회, StatefulSet 예고 마지막 한 줄, git clone+빌드 모순 미해명. **조건부**

### 3. 프론트엔드 — 4/3.5/2.5/3.3
Vercel 비교 + 창고/신청서 비유 호평. ex08 통합이 너무 빠르게 성공, 빌드 시간 안내 부재, nginx.conf `/api → backend-service` 본문 노출 부재. **조건부**

### 4. SI 개발자 — 3/2/2/2
DB 운영 시야 절반 비어있음. StorageClass·StatefulSet·ReadWriteOnce 모순·`/mnt/data` vs `/data/mysql` 해명 4가지 모두 미반영. **조건부**

### 5. PM/기획자 — 3/4/3/3
6.1 ConfigMap·Secret 비유 강력. "책 전체를 돌아보며" 6챕터 한 줄 정리표 부재. ex08 풀스택 통합 카타르시스 짧음. **조건부**

### 6. 비전공 전직자 — 4/3/2/3
이야기 안정. 빌드 시간 안내·6.1~6.3 매니페스트 매핑·`--prefix` 설명·minikube service 터널 5가지 미반영. **조건부**

### 7. DevOps — 3/2/2/2
StorageClass·이미지 레지스트리·imagePullPolicy·Vault 4가지 운영 가드레일 미반영. 캡처 3건 미보강. **조건부**

### 8. 임베디드 — 3/3/2/2.7
Pod 휘발성 → PV/PVC 분리 = RTOS RAM/Flash 매핑. git clone+빌드 모순·hostPath 단일 노드·Base64 본질 미반영. **조건부**

### 9. CS 학생 — 4/5/4/4 → **통과 O**
v3 5/5 기술 점수 유지. Try/Fail 부분 개선 평가. CS 1:1 매핑(환경 변수 프로세스 모델·PV/PVC·CoreDNS·Namespace) 강력. 보안 정밀도(Base64·RBAC·etcd) 호평.

### 10. CTO/리드 — 4.5/4.5/4.5/4.5 → **강력추천**
v3 강력 추천 v5 유지. L563 원형 서사 회수·"마치며" 6챕터 회고·6.4 디버깅 압축본 모두 호평. StorageClass 한 줄·이미지 레지스트리·GitOps 한 줄 보강 권고만 남음.

## 수정 제안 (우선순위순)

| # | 위치 | 제안 | 심각도 | 관련 페르소나 |
|---|------|------|--------|-------------|
| 1 | L390 직전 또는 L470 | 빌드 시간 `:::tip` 박스 (5~10분, ContainerCreating 정상, `logs -f` 진행 확인) | **높음** | 1, 2, 3, 6 |
| 2 | L215 + L555 | StorageClass/CSI 한 단락 (운영 분기 명시) + 다음 학습 목록 추가 | **높음** | 1, 2, 4, 5, 7, 9 |
| 3 | 6.3.5 (L460~487) | Try/Fail 1회 삽입 (CrashLoopBackOff 또는 Namespace 누락) → 6.4 자연 연결 | **높음** | 1, 3, 6 |
| 4 | L342 또는 6.3.3 도입 | git clone+빌드 모순 변명 한 줄 ("학습용 단순화, 운영은 JAR 굽기") | **높음** | 4, 7, 8 |
| 5 | L22, L72, L99, L120, ... 13곳 | 이미지 경로 `../assets/CH05/...` 전수 점검·정리 | **높음** | 1, 3 |
| 6 | L209·L215 | `storageClassName: ""` 의미 한 단락 (자동 프로비저닝 부정형) | 중간 | 1, 5, 9 |
| 7 | 6.3.4 DB 섹션 | DB Deployment + ReadWriteOnce 박스 ("StatefulSet 정석, 이 책은 학습용 Deployment 유지") + `strategy: Recreate` 명시 | 중간 | 2, 4 |
| 8 | L211·L449 | `/mnt/data` vs `/data/mysql` 같은 메커니즘 한 줄 | 중간 | 4 |
| 9 | 6.3.3 도입 | "6.1·6.2는 학습용 매니페스트, 6.3은 별개" 한 줄 + 환경변수 키 차이 | 중간 | 6 |
| 10 | 6.2 PV/PVC 절 | 캐릭터 한 줄 (팀장 또는 선배) — 6.1.4 내면독백 균형 | 중간 | 1, 5, 6 |
| 11 | L390~394 | 이미지 레지스트리·imagePullPolicy 한 단락 | 중간 | 7 |
| 12 | L107 Base64 박스 | Vault·External Secrets Operator 한 줄 | 중간 | 7 |
| 13 | L135~139, L153, L464~476 | 캡처 미보강 3건 보강 (`screenshot` 스킬) | 중간 | 7 |
| 14 | L527 | "노드 셀렉터 불일치" 제거·교체 | 낮음 | 1, 6 |
| 15 | L477 | minikube service 터널 유지 한 줄 | 낮음 | 3, 6 |
| 16 | L443 | "Spring Boot 내장 Tomcat의 기본 포트 8080" | 낮음 | 1, 8 |
| 17 | L470 | ContainerCreating 상태 명칭 정밀도 | 낮음 | 8 |
| 18 | L496 | `--prefix` 한 줄 설명 | 낮음 | 6 |
| 19 | L20 또는 L92 | Base64 본질 한 줄 (바이너리 ASCII 안전 전송) | 낮음 | 8 |
| 20 | L555 "마치며" | 분산 합의(Raft)·GitOps(ArgoCD/Flux) 추가 | 낮음 | 9, 10 |
| 21 | L538 | endpoints 디버깅 의미 한 줄 (selector·labels 매칭) | 낮음 | 1 |

## 결론

**CH06는 책 마무리 챕터로서 원형 서사 회수와 디버깅 4단계가 결정적 강점.** CTO 강력 추천 + CS 학생 통과 O로 마무리 챕터의 완결성은 확보됨. 다만 v3 4대 지적 중 빌드 시간 안내·StorageClass·git clone+빌드 모순 3가지가 미반영되었고, 신규로 이미지 경로 전수 오류 + Try/Fail 부재 + DB 운영 가드레일 부재가 발견되어 SI·DevOps·신입·비전공 페르소나는 조건부에 머묾.

**우선순위 권고**: 위 표 1~5번(빌드 시간 박스·StorageClass 한 단락·Try/Fail 1회·git clone 변명·이미지 경로 정리)만 적용해도 SI·DevOps 점수 +0.5~1.0 상승, 입문 페르소나 좌초 위험 해소, 평균 +0.5점 상승 예상. 모두 단일 박스·한 단락 보강으로 가능.

**핵심 진단**: CH06는 v3 강점(원형 서사 회수·디버깅 4단계·Base64 보안)이 그대로 유지된 안정 라운드이지만, v3에서 지적된 운영 가드레일 부재가 v5에서도 그대로 + 신규 이미지 경로 오류가 발견되어 출간 전 위 1~5번 즉시 처리 권고. 강력 추천(CTO) 평가는 유지될 것으로 예상.
