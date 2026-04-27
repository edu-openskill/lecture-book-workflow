# Beta Reader 리포트: CH04 — Kubernetes 시작하기 (v4)

## 프로젝트
- 책: 특이점이 온 개발자 — 도커·쿠버네티스
- 대상 파일: `chapters/04-Kubernetes-시작하기.md` (550 라인)
- 독자 상수: 입사 3~6개월차 주니어
- 평가 일자: 2026-04-27

## 페르소나 목록

| # | 이름 | 이야기 | 기술 | 실습 | 통과 |
|---|------|:----:|:----:|:----:|:----:|
| 1 | 신입 백엔드 | 4 | 3 | 2 | O (조건부) |
| 2 | 데이터 엔지니어 | 4 | 4 | 3 | O |
| 3 | 프론트엔드 | 4 | 4 | 3 | O |
| 4 | SI 개발자 | 4 | 4 | 3 | O |
| 5 | PM/기획자 | 4 | 5 | 3 | O |
| 6 | 비전공 전직자 | 4 | 3 | 2 | O (조건부) |
| 7 | DevOps 엔지니어 | 4 | 3 | 3 | O (조건부) |
| 8 | 임베디드 개발자 | 4 | 3 | 4 | O |
| 9 | CS 학생 | 4 | 4 | 4 | O |
| 10 | CTO/리드 | 5 | 4 | 4 | **O (즉시 투입)** |

**평균**: 이야기 4.1/5 · 기술 3.7/5 · 실습 3.1/5
**통과**: 10/10 (조건부 3명)

## 요약

- **최대 강점**: 팀장의 "새벽 2시에 누가 살려?" 도입 + 본사·가맹점 프랜차이즈 비유 + 선언형 vs 명령형 — 거의 전 페르소나 강한 호평
- **결정적 장면**: §4.4.6 "바뀌는 번호" Pod IP 변동 발견 → CH05 Service 자연스러운 cliffhanger (PM·프론트·임베디드·CTO 호평)
- **분량 550라인 적절** — Service/Ingress를 CH05로 미룬 결정은 CTO 추천 (입문 챕터 부담 분산)
- **공통 약점**: YAML 친절도(apiVersion 차이)·Minikube 환경구축·Deployment→ReplicaSet→Pod 3단 위임 다이어그램

## 공통 피드백 (3명 이상 동일 의견)

| 영역 | 피드백 | 언급 페르소나 | 심각도 |
|------|--------|-------------|--------|
| YAML 친절도 | apiVersion `v1` vs `apps/v1` 변경 설명 없음. metadata/spec/template 의미 풀이 부족 | 1, 3, 5, 6 | **높음** |
| Deployment→RS→Pod 3단 위임 | ReplicaSet의 자동복구가 "마법"처럼 보임. 위임 다이어그램 1장 누락 | 2, 8, 9 | **높음** |
| Minikube 환경구축 | Chocolatey 사전설치, `minikube start --driver=docker` 옵션, Docker Desktop 실행 확인 부족 | 1, 6 | **높음** |
| 컬럼·옵션 풀이 | `READY 1/1`, `STATUS`, `-w`, `-o wide` 의미 본문 풀이 부족 | 1, 4, 5, 6 | 중간 |
| 4.1.4 컨트롤플레인 한꺼번에 | etcd/Scheduler/Controller Manager/kubelet/kube-proxy 5개가 한 박스에 쏟아짐 | 1, 5 | 중간 |
| ReplicaSet 자동복구 메커니즘 | livenessProbe/readinessProbe → kubelet → ReplicaSet 계층 누락 | 7 | 중간 |

## 강점 (다수 또는 전원 언급)

- 팀장 "새벽 2시" 도입(L1) — **9명 호평**, CH01 "두 시간 헤매다"의 회수
- 프랜차이즈 본사·가맹점 비유 — **전 페르소나** 일관 호평 (PM은 회의 인용 가능 수준)
- 선언형 vs 명령형 비유(§4.1.1) — CS 학생·SI·데이터 엔지니어 호평 (각자의 맥락에서 매핑됨)
- §4.4.6 IP 변동 cliffhanger — **6명 강한 호평**, CH05 Service 동기 형성
- §4.4.4 `maxSurge:4, maxUnavailable:0` 무중단 시연 — SI는 "토요일 새벽 점검 공지"의 해방으로 충격
- §4.4.5 `kubectl rollout undo` 두 줄 롤백 — SI는 "Oracle DBLink 백업 SQL" 공포 해방으로 호평

## 심각도별 이슈

### 높음

1. **YAML 친절도 — 4명**
   - 위치: §4.3.3 첫 YAML, §4.4.2 Deployment YAML
   - 증상: apiVersion이 `v1`(Pod) vs `apps/v1`(Deployment)로 갑자기 바뀌는데 설명 없음. metadata/spec/template/selector 들여쓰기 의미 풀이 부족
   - 영향: 비전공·신입은 YAML 들여쓰기 1칸 차이로 막힘
   - 제안:
     - apiVersion 표 1개 (Pod=v1, Deployment=apps/v1, Service=v1)
     - "두 칸 들여쓰기, 탭 금지, 콜론 뒤 공백 1개" 박스 1개
     - `kind`/`metadata.name`/`spec` 5초 가이드 박스

2. **Deployment → ReplicaSet → Pod 위임 다이어그램 — 3명**
   - 위치: §4.4.3 ReplicaSet
   - 증상: 그림 4-2 한 번 외 위임 구조 누적 안 됨
   - 영향: 데이터 엔지니어는 "Airflow Scheduler→Executor→Worker"와 비교하려는데 확신 안 섬, 임베디드는 평면 구조 익숙해서 위임 한 단계도 헷갈림, CS 학생은 사후 언급으로만 끝나 약함
   - 제안: §4.4.3 시작에 3단 위임 다이어그램 1장 + `kubectl get deploy,rs,pod` 한 번 실행해 세 리소스 동시 노출

3. **Minikube 환경구축 — 2명, 부트캠프생 필수**
   - 위치: §4.2.2 설치
   - 증상: "Chocolatey 미리 설치" 한 줄. 관리자 PowerShell, Docker Desktop 실행 상태, `--driver=docker` 옵션 부재
   - 영향: 비전공·신입은 `minikube start` 첫 시도에서 멈춤
   - 제안: 사전 준비 박스 1개 — Chocolatey 설치 한 줄, Docker Desktop 실행 확인, `--driver=docker`, 첫 실행 5~10분 안내, `minikube status` 정상 출력 예시

### 중간

4. **컬럼·옵션 풀이 — 4명**
   - 위치: §4.3.4 Pod 조회, §4.4.4 watch
   - 제안: `READY 1/1`·`STATUS Running`·`RESTARTS` 컬럼 1행 표, `-w`/`-o wide` 첫 등장 시 1줄 풀이

5. **§4.1.4 컨트롤플레인 한꺼번에 — 2명**
   - 위치: L99~L109
   - 제안: API Server + kubelet 2개만 본문에서 다루고, etcd/Scheduler/Controller Manager는 "나중에 설명" 또는 참고박스로 격하

6. **운영 함정 (DevOps 특유)**
   - 위치: §4.4.3, §4.4.4, §4.4.5
   - 제안:
     - §4.4.3: livenessProbe/readinessProbe 박스 1개 ("자동복구 1차 트리거")
     - §4.4.4 끝: "롤링업데이트 함정" 한 단락 — 노드 리소스 2배 확보, readinessProbe 미설정 시 트래픽 누락, PDB
     - §4.4.5: "rollback이 되돌리지 않는 것" 한 줄 — DB 마이그레이션, ConfigMap, Secret 회전

7. **rollback 메커니즘 보강 — 1명 (데이터)**
   - 위치: §4.4.5
   - 제안: "이전 ReplicaSet의 replicas를 0→4, 현재 ReplicaSet을 4→0" 한 줄 + `kubectl get rs` 두 RS 공존 캡처

8. **§4.3~§4.4 캐릭터 약화 — 1명 (PM)**
   - 제안: §4.4 시작에 팀장/동료 한 줄 (자동복구·스케일링이 운영비·SLA에 어떤 의미인지)

### 낮음

9. **kubectl run 경고 강화 — 1명 (CTO)**
   - 위치: §4.3.2 hello-pod1
   - 제안: "kubectl run은 학습용. 실무에서 쓰지 말라" 한 줄

10. **selector ↔ template.labels 일치 — 2명 (P1, P3)**
    - 제안: "selector가 template의 라벨을 못 찾으면 apply 실패" 한 줄

11. **maxSurge:4 해설 — 2명 (CTO, 임베디드)**
    - 위치: §4.4.4
    - 제안: 일반 기본값(25%)과 비교 1줄, (4,0)/(1,1)/(0,1) 매트릭스 표

12. **reconciliation loop 용어 박기 — 1명 (CS)**
    - 위치: §4.1.1 끝
    - 제안: "이 루프를 조정 루프(Reconciliation Loop)라 부릅니다" 한 줄

13. **etcd Raft·CNI·kube-proxy 모드 — 1명 (DevOps)**
    - 위치: §4.1.4
    - 제안: 참고박스에 etcd Raft 합의·홀수 노드, CNI Pod IP 발급, kube-proxy iptables/IPVS/eBPF 1줄씩

14. **Pod Network Namespace 공유 — 1명 (임베디드)**
    - 위치: §4.3.1 참고박스
    - 제안: "Pod = 한 네트워크 네임스페이스 + 한 IP. localhost로 서로 호출. 한 보드 위 RTOS 태스크가 같은 NIC 공유" 비유

15. **selector를 CSS 비유 — 1명 (프론트)**
    - 위치: §4.4.2
    - 제안: "CSS의 `.nginx { }`가 해당 클래스 요소만 선택하는 것과 같다" 한 줄

16. **용어 정리 3열 표 누락 — 1명 (CTO)**
    - 위치: 챕터 끝 "이것만은 기억하자" 직전
    - 제안: 본사/상가/가맹점/지침서 ↔ 컨트롤플레인/노드/Pod/Deployment ↔ 정식 정의 3열 표

17. **kube-proxy 박스 위치 조정 — 1명 (CTO)**
    - 위치: §4.1.4 참고박스
    - 제안: iptables 포트포워딩 문장은 5장으로 이동, "자세한 동작은 5장에서" 한 줄만 남기기

## 페르소나별 상세 (요약)

### 1. 신입 백엔드 — 4/3/2 (조건부)
선언형 개념·프랜차이즈 비유 진입은 부드러움. 4.1.4 컨트롤플레인 5요소 한꺼번에 + Minikube 설치 부족 + YAML 첫 등장 친절도 부족이 결정적 막힘.

### 2. 데이터 엔지니어 — 4/4/3
Airflow DAG ↔ Deployment 매핑 자연스러움. ReplicaSet 2단 구조·rollback 메커니즘 보강 필요. `kubectl get rs` 누락 + watch 시간 흐름 텍스트 부족.

### 3. 프론트엔드 — 4/4/3
"왜 K8s가 필요한가" 동기 명확. 4.4.6 IP 변동이 `axios.baseURL` 직결되어 강력. selector를 CSS 비유로 풀어주면 즉시 흡수.

### 4. SI 개발자 — 4/4/3
"VM 시절 WAS 내리고 WAR 교체" 비교 단락 추가 시 동기 폭발. kubectl 학습 곡선 표 분리 권장. ReplicaSet "DBA 세션 풀 min=4" 비유 추가.

### 5. PM/기획자 — 4/5/3
프랜차이즈 비유가 환상적 (회의 인용 가능). YAML 5초 가이드, 4.1.3 리소스 표에 형광펜 효과("이번 챕터 범위") 권장.

### 6. 비전공 전직자 — 4/3/2 (조건부)
비유는 머리에 쏙 박힘. 부트캠프 6개월은 명령어 한 줄 빠지면 멈춤 — Chocolatey, --driver, YAML 들여쓰기 박스 필수.

### 7. DevOps 엔지니어 — 4/3/3 (조건부)
입문 비유는 잘 박힘. 4년차 시각의 정확성·운영 함정 6종(etcd Raft·CNI·kube-proxy 모드·livenessProbe·롤링 함정·rollback 한계) 누락. 참고박스 한 줄씩만 더해도 신뢰 회복.

### 8. 임베디드 개발자 — 4/3/4
선언형 vs 명령형이 RTOS 자가복구와 매핑. 추상화 사다리(Container⊂Pod⊂RS⊂Deploy) 다이어그램 1장 + Pod Network Namespace 임베디드 친화 비유 필요.

### 9. CS 학생 — 4/4/4
OS 수업 ↔ 챕터 매핑 우수. **reconciliation loop** 용어가 본문에 박혀야 강의 노트와 매핑. controller 패턴이 K8s 전체를 관통하는 핵심임 명시 권장.

### 10. CTO/리드 — 5/4/4 — **즉시 투입 가능**
팀 신입 온보딩 자료로 즉시 투입. Service/Ingress를 CH05로 미룬 결정 정확. label/selector 복선이 인계점으로 작동. kubectl run 경고·maxSurge:4 해설·용어 정리 3열 표만 보완.

## 수정 제안 (우선순위순)

| # | 위치 | 제안 | 심각도 | 관련 페르소나 |
|---|------|------|--------|-------------|
| 1 | §4.3.3 첫 YAML | apiVersion 표 + "들여쓰기 2칸/탭 금지" 박스 + `kind`/`metadata`/`spec` 5초 가이드 | 높음 | 1, 3, 5, 6 |
| 2 | §4.4.3 시작 | Deployment→ReplicaSet→Pod 3단 위임 다이어그램 1장 + `kubectl get deploy,rs,pod` 동시 노출 | 높음 | 2, 8, 9 |
| 3 | §4.2.2 사전 준비 박스 | Chocolatey 설치 1줄, Docker Desktop 실행 확인, `--driver=docker`, 5~10분 안내, `minikube status` 예시 | 높음 | 1, 6 |
| 4 | §4.3.4 직후 | `READY 1/1`/`STATUS`/`RESTARTS` 컬럼 1행 표, `-w`/`-o wide` 첫 등장 1줄 풀이 | 중간 | 1, 4, 5, 6 |
| 5 | §4.1.4 컨트롤플레인 박스 | API Server + kubelet 2개만 본문, etcd/Scheduler/Controller Manager는 참고박스로 격하 | 중간 | 1, 5 |
| 6 | §4.4.3 직후 | livenessProbe/readinessProbe 박스 1개 ("자동복구 1차 트리거") | 중간 | 7 |
| 7 | §4.4.4 끝 | "롤링업데이트 함정" 한 단락 — 노드 리소스 2배·readinessProbe·PDB | 중간 | 7 |
| 8 | §4.4.5 끝 | "rollback이 되돌리지 않는 것 — DB·ConfigMap·Secret" 1줄 | 중간 | 7 |
| 9 | §4.4.5 | rollback 메커니즘 — "이전 RS replicas를 0→4, 현재 4→0" 1줄 + 두 RS 공존 캡처 | 중간 | 2 |
| 10 | §4.4 시작 | 팀장/동료 한 줄 등장 (자동복구·SLA 의미) | 중간 | 5 |
| 11 | §4.3.2 kubectl run | "학습용, 실무에서 쓰지 말라" 1줄 | 낮음 | 10 |
| 12 | §4.4.2 selector | "selector가 template 라벨을 못 찾으면 apply 실패" 1줄, "CSS 클래스 선택자와 동일" 비유 | 낮음 | 1, 3 |
| 13 | §4.4.4 maxSurge:4 | 기본값 25%와 비교 1줄, (4,0)/(1,1)/(0,1) 매트릭스 표 | 낮음 | 8, 10 |
| 14 | §4.1.1 끝 | "이 루프를 조정 루프(Reconciliation Loop)라 부릅니다" 1줄 | 낮음 | 9 |
| 15 | §4.1.4 참고박스 | etcd Raft·CNI 발급·kube-proxy 모드 1줄씩 | 낮음 | 7 |
| 16 | §4.3.1 Pod 박스 | "Pod = 한 네트워크 네임스페이스. 한 보드 위 RTOS 태스크가 NIC 공유와 동치" | 낮음 | 8 |
| 17 | "이것만은 기억하자" 직전 | 본사/가맹점 ↔ 컨트롤플레인/Pod ↔ 정식 정의 3열 용어 정리 표 | 낮음 | 10 |
| 18 | §4.1.4 kube-proxy 박스 | iptables 포트포워딩 문장은 5장으로 이동 | 낮음 | 10 |

## 결론

- 입문 챕터로 분량·구조 적절. CTO 즉시 투입 가능 평가.
- v4 결정타 3개: **(1) YAML apiVersion 표·들여쓰기 박스 + (2) Deploy→RS→Pod 3단 다이어그램 + (3) Minikube 사전 준비 박스**. 이 셋이 입문~비전공 페르소나 막힘 해소
- DevOps 운영 함정 6종은 본문 흐름 유지하되 참고박스 1줄씩만 추가 권장
- "바뀌는 번호" cliffhanger는 CH05 진입의 강력한 훅 — 유지
