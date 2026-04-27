# 아웃라인 v2 — 처음 만나는 도커 쿠버네티스

> **변경 사유**: 네트워킹을 돋보기 사이드바에서 각 챕터 본문으로 전환. K8s 네트워킹 전용 챕터(CH05) 신설. 기존 5챕터 → 6챕터.
> **핵심 원칙**: "부품을 먼저 배우고, 조립한 뒤에 전체 그림을 본다"
> **네트워킹 전략**: 무거운 개념은 CH02~CH04에서 미리 나눠 싣고, CH05는 연결만 한다.

---

## 전체 구조

| 챕터 | 제목 | 핵심 | 네트워킹 부담 |
|------|------|------|-------------|
| CH01 | 왜 컨테이너인가 | 컨테이너 개념, Docker/K8s 소개, 학습 흐름 | 없음 |
| CH02 | Docker 이해하기 | 가상화, 이미지/컨테이너, CLI, 리눅스, 생명주기, 마운트 | ■■■ (Namespace, iptables, Docker DNS) |
| CH03 | Docker 다루기 | Dockerfile, NGINX, Redis, MySQL, Compose | ■■ (bridge 한계→사용자정의→Compose 자동) |
| CH04 | Kubernetes 시작하기 | 클러스터 구조, Minikube, Pod, Deployment, ReplicaSet | ■ (kube-proxy 배치, Pod 네트워크, label 복선) |
| CH05 | Kubernetes 네트워킹 | Service, kube-proxy, Ingress, L4/L7, 전체 흐름 | ■■■ (조립 — 새로운 건 적고 연결이 대부분) |
| CH06 | Kubernetes 운영하기 | ConfigMap, Secret, Volume, 종합실습, 디버깅 | ■ (CoreDNS 연결) |

---

## CH01. 왜 컨테이너인가

> 변경: 최소. 학습 흐름(1.3) 업데이트 — 6챕터 반영.

### 1.1 말콤 맥린 : 컨테이너의 아버지
- 1.1.1 해상 운송의 초기
- 1.1.2 컨테이너의 도입
- 1.1.3 IT에서의 컨테이너

### 1.2 Docker와 Kubernetes
- Docker = 컨테이너를 만들고 실행
- Kubernetes = 컨테이너를 운영하는 플랫폼
- 비교 표

### 1.3 이 책의 학습 흐름
- **변경**: 5챕터 → 6챕터 구조 반영
- CH02 Docker 이해하기 → CH03 Docker 다루기 → CH04 K8s 시작하기 → CH05 K8s 네트워킹 → CH06 K8s 운영하기
- 로드맵 이미지 업데이트 필요

### 이것만은 기억하자

---

## CH02. Docker 이해하기

> 변경: 2.2절(docker run의 비밀)을 CLI 실습(2.4) 뒤로 이동. 나머지 유지.
> 네트워킹: 이미 본문 — Namespace, veth, docker0, iptables DNAT, Docker DNS. 유지.

### 2.1 Docker 작동 원리
- 2.1.1 가상화 : 하나의 컴퓨터를 여러 개로 사용하는 법
- 2.1.2 컨테이너 가상화 : OS 없이 격리하다
- 2.1.3 Docker : 이미지에서 컨테이너까지
- 2.1.4 Docker 이미지

### 2.2 Docker Desktop : 설치

### 2.3 Docker CLI : 기본 명령어
- 2.3.1 docker pull
- 2.3.2 docker run
- 2.3.3 docker run -d
- 2.3.4 docker ps
- 2.3.5 자주 사용하는 Docker 명령어 (표)

### 2.4 전체 그림 : docker run의 비밀 ← 기존 2.2를 여기로 이동
- Step 1. 컨테이너 ↔ 호스트 연결 (Namespace + veth + docker0)
- Step 2. 외부 → 컨테이너 접근 (iptables DNAT 포트포워딩)
- Step 3. 컨테이너 간 통신 (Docker DNS)
- 전체 요약 표

> **이동 이유**: docker run을 직접 쳐본 뒤 "뒤에서 뭐가 벌어지는지" 보여주면 훨씬 와닿음

### 2.5 Linux : 컨테이너 안에서 쓰는 명령어
- 2.5.1 ~ 2.5.7 (기존 유지)

### 2.6 컨테이너 생명주기
- 2.6.1 ~ 2.6.5 (기존 유지)

### 2.7 이미지 만들기
- 2.7.1 ~ 2.7.4 (기존 유지)

### 2.8 마운트 : 데이터 보존
- 2.8.1 바인드 마운트
- 2.8.2 볼륨 마운트

### 이것만은 기억하자

---

## CH03. Docker 다루기

> 변경: 돋보기④⑤⑥ → 본문 대화로 전환. 이모지(🔍💡) 전면 제거.
> 3장 끝(이것만은 기억하자 앞)에 Docker 네트워크 진화 정리표 추가.

### 3.1 프로비저닝 : 환경을 자동으로 구성하다
- 3.1.1 ~ 3.1.5 (기존 유지)

### 3.2 NGINX : 웹 서버와 리버스 프록시
- 3.2.1 NGINX : 동작 원리
- 3.2.2 경로 기반 라우팅
  - 실습 후 **본문으로**: "왜 컨테이너끼리 직접 통신 못 하나" (기존 돋보기④)
  - 기본 bridge에서는 이름 통신 불가 → host.docker.internal 우회 필요
  - 선배: "이건 우회 경로야. 근본적으로 해결하는 방법은 나중에 나와."
- 3.2.3 라운드 로빈
- 3.2.4 캐싱

### 3.3 Redis : 세션 저장소
- 3.3.1 세션 : 왜 외부 저장소가 필요한가
- 3.3.2 Redis : 실습
  - docker network create 직후 **본문으로**: "사용자 정의 네트워크의 마법 — DNS가 열린다" (기존 돋보기⑤)
  - host='redis'가 동작하는 이유 = Docker DNS(127.0.0.11) 자동 활성화
  - "2장에서 배운 Docker DNS가 여기서 작동하는 거야"
  - 기본 bridge vs 사용자 정의 bridge 비교 표

### 3.4 MySQL : DB 서버 구축
- (기존 유지)

### 3.5 Docker Compose : 여러 컨테이너를 한 번에
- 3.5.1 왜 필요한가
- 3.5.2 실습
  - nginx.conf 비교 직후 **본문으로**: "Compose 네트워크 — 서비스 이름이 곧 주소" (기존 돋보기⑥)
  - docker compose up이 내부적으로 하는 일 (네트워크 생성 + DNS + 연결 자동)
  - EX01(host.docker.internal) → EX06(app1:80) 변화의 이유
- 3.5.3 주요 명령어

### 3.6 종합 실습 : 웹 사이트 만들기
- 3.6.1 ~ 3.6.6 (기존 유지)

### Docker 네트워크의 진화 ← 신규 정리절

> 3장을 마무리하며, 지금까지 겪은 Docker 네트워크의 변화를 한눈에 정리.

| 단계 | 방식 | 이름 통신 | 해결책 |
|------|------|---------|--------|
| docker run 개별 실행 | 기본 bridge | 불가 | host.docker.internal 우회 |
| docker network create | 사용자 정의 bridge | 가능 | Docker DNS 자동 활성화 |
| docker compose up | Compose 자동 네트워크 | 가능 | 전부 자동 |

- 선배: "이 흐름 기억해 둬. 쿠버네티스에서 똑같은 게 더 큰 스케일로 나와."

### 이것만은 기억하자

---

## CH04. Kubernetes 시작하기

> 변경:
> - 4.1.3에 kube-proxy 배치 추가 (파일03 기반)
> - 4.1.4 "전체 그림" 대폭 축소 → 한 문단 예고로 변경
> - Pod 돋보기(공유 Namespace) → 본문화
> - Deployment에서 label/selector 복선 심기
> - **Service, Ingress는 CH05로 이동** (기존 4.4 전체가 CH05로)

### 4.1 왜 Kubernetes인가 : 컨테이너 운영의 한계
- 4.1.1 쿠버네티스가 필요한 이유 (이야기 — 새벽 3시)
- 4.1.2 쿠버네티스의 핵심 리소스 (표)
- 4.1.3 쿠버네티스의 동작 원리
  - 컨트롤 플레인 vs 워커 노드
  - **추가**: kube-proxy가 모든 워커 노드에 존재
  - "2장에서 배운 iptables, 기억나? kube-proxy가 K8s에서 그걸 해"
  - 파일03의 물리 구조를 여기에 녹임
- 4.1.4 ← **축소**: 한 문단 예고
  - "리소스들이 실제로 어떻게 연결되어 요청을 처리하는지는 Service와 Ingress를 배운 뒤 전체 그림으로 돌아올 것입니다."

### 4.2 Minikube : 로컬 클러스터
- 4.2.1 미니큐브란?
- 4.2.2 기본 명령어
- 4.2.3 kubectl로 첫 Pod 띄우기
  - Pod 개념
  - **본문화**: "Pod = 공유 Network Namespace" (기존 돋보기)
  - "Docker에서는 컨테이너가 네트워크 단위, K8s에서는 Pod가 네트워크 단위"
  - YAML 기본 문법
  - kubectl 명령어 요약

### 4.3 Deployment, ReplicaSet : 자동 복구와 스케일링
- 4.3.1 Deployment
  - **label/selector 설명 시 복선**: "selector는 Deployment만 쓰는 게 아닙니다. 다음 장에서 배울 Service도 이 라벨로 Pod를 찾습니다."
- 4.3.2 ReplicaSet
- 4.3.3 롤링 업데이트
- 4.3.4 Rollback

### 이것만은 기억하자
- **변경**: Ingress 언급 제거 (CH05에서 다루므로)
- Pod 네트워크 단위, Deployment의 label이 나중에 Service에서 쓰인다는 복선 회수 예고

---

## CH05. Kubernetes 네트워킹 ← 신규 챕터

> **핵심 원칙**: CH02~CH04에서 미리 배운 부품을 K8s 맥락에서 조립.
> 새로 외울 개념은 최소화하고, "Docker에서 배운 그게 여기서 이거"라는 연결이 중심.
> 참조: code/image-analysis-01, 02, 03

### 도입 (이야기 파트)

오픈이가 Deployment로 Pod를 띄울 수 있게 되었지만, Pod IP가 매번 바뀌고 외부에서 접속할 방법이 없습니다.

> **오픈이**: "Pod를 띄우는 건 됐는데, 이걸 어떻게 찾아가요? IP가 매번 바뀌잖아요."
> **선배**: "그래서 네트워크를 알아야 해. 3장에서 Docker 네트워크가 어떻게 진화했는지 봤잖아. K8s에서도 같은 이야기가 벌어져."

### 5.1 Service : Pod의 대표 전화번호

#### 5.1.1 왜 Service가 필요한가
- Pod IP 변경 실습 (기존 CH04 4.4.1 내용)
- 콜센터 대표번호 비유

#### 5.1.2 Service 생성
- ClusterIP, NodePort, LoadBalancer 타입 (기존 CH04 4.4.2 내용)
- YAML 작성 + 실습

#### 5.1.3 Label-Selector 매칭 ← 파일02 기반
- "4장에서 배운 selector가 여기서 쓰인다"
- Service가 Pod를 찾는 유일한 방법 = label 매칭
- Selector: app=web → Label: app=web인 Pod만 연결
- 매칭 다이어그램

#### 5.1.4 kube-proxy : 보이지 않는 경비원 ← 파일01 기반
- "2장의 iptables DNAT를 기억하시죠? kube-proxy가 클러스터 전체에서 같은 일을 합니다"
- ClusterIP의 정체: 진짜 IP가 아니라 iptables 규칙
- kube-proxy의 이중 역할: NodePort 처리 + ClusterIP 처리
- Endpoint Controller: Pod IP가 바뀌면 Service 매핑을 자동 갱신

#### 5.1.5 Networking
- minikube service 실습 (기존 CH04 4.4.3 내용)

### 5.2 Ingress : 건물 안내 데스크

#### 5.2.1 왜 Ingress가 필요한가
- "3장의 NGINX 경로 라우팅, 기억나시죠? Ingress Controller가 K8s 안에서 같은 역할을 합니다"
- Service만으로 부족한 이유

#### 5.2.2 L4 vs L7 ← 파일02 기반
- 톨게이트(L4: IP/Port만) vs 안내데스크(L7: URL/Host까지)
- JSON 파싱은 누가? → Pod의 애플리케이션만
- 비교 표

#### 5.2.3 Ingress 리소스 (기존 CH04 4.4.4 내용)
- Ingress Controller + Ingress 리소스
- minikube addons enable ingress

### 5.3 전체 흐름 : 브라우저에서 Pod까지 ← 파일01+02+03 통합

#### 5.3.1 요청의 여정
- 한 장의 그림으로 전체 흐름 조립
- 외부 → (L4 LB →) Ingress Controller(L7) → Service → kube-proxy(iptables) → Pod
- 각 단계에서 "누가 뭘 보고, 뭘 안 보는가"

#### 5.3.2 Docker에서 Kubernetes로 ← 대응표

| Docker | Kubernetes | 배운 챕터 |
|--------|-----------|----------|
| docker0 (bridge) | Pod 네트워크 (CNI) | CH02 |
| iptables DNAT (-p 포트포워딩) | kube-proxy iptables | CH02→CH05 |
| Docker DNS (127.0.0.11) | CoreDNS | CH03→CH06 |
| NGINX 경로 라우팅 | Ingress Controller | CH03→CH05 |
| docker network create | Service (ClusterIP) | CH03→CH05 |
| Docker Compose 자동 네트워크 | Namespace + Service DNS | CH03→CH06 |

### 이것만은 기억하자

---

## CH06. Kubernetes 운영하기 ← 기존 CH05 이동

> 변경: 챕터 번호 5→6. CoreDNS를 CH05 대응표와 연결. 나머지 기존 유지.

### 6.1 ConfigMap, Secret : 설정 분리
- 6.1.1 ConfigMap
- 6.1.2 Secret
- 6.1.3 환경 변수 추가
- 6.1.4 환경 변수 수정
- **CoreDNS 연결**: "CH05에서 Service 이름으로 통신할 수 있다고 했죠? ConfigMap에 db-service:3306처럼 적을 수 있는 이유가 CoreDNS입니다"

### 6.2 Volume : 데이터 보존
- 6.2.1 Persistent storage (PV/PVC)
- (기존 유지)

### 6.3 웹사이트 : Kubernetes 배포 (종합 실습)
- 6.3.1 아키텍처
- 6.3.2 이미지 폴더
- 6.3.3 k8s 폴더
- 6.3.4 실행하기
- **네트워킹 회고**: 종합 실습 결과를 보며 CH05의 전체 흐름을 실전에서 확인
  - "브라우저 → Ingress → frontend-service → Frontend Pod → backend-service → Backend Pod → DB/Redis"
  - 모든 서비스 간 통신에서 Service 이름(CoreDNS) 사용 확인

### 6.4 문제가 생겼을 때 : 디버깅
- 6.4.1 기본 진단 명령어
- 6.4.2 자주 만나는 에러와 해결법
- 6.4.3 디버깅 순서

### 이것만은 기억하자

---

## 프롤로그 변경사항

- "세 개의 챕터" → 실제 6챕터 구조와 일치하도록 수정
- `---` 수평선 제거
- 챕터 안내 업데이트:
  - 1장 → 왜 컨테이너인가
  - 2장 → Docker 이해하기
  - 3장 → Docker 다루기
  - 4장 → Kubernetes 시작하기
  - 5장 → Kubernetes 네트워킹
  - 6장 → Kubernetes 운영하기

## 맺음말 변경사항

- 챕터 흐름 요약 업데이트 (5장 네트워킹 추가)

---

## 이미지 변경 계획

| 챕터 | 변경 | 상세 |
|------|------|------|
| CH01 | 수정 | 로드맵 이미지 (6챕터 반영) |
| CH02 | 없음 | 기존 이미지 유지, 절 번호만 변경 |
| CH03 | 삭제 | 돋보기 전용 이미지 제거 or 본문 흐름에 맞게 재배치 |
| CH04 | 수정 | 4.1.4의 다이어그램 일부 CH05로 이동 |
| CH05 | 신규 | Service, kube-proxy, Ingress, L4/L7, 전체흐름 다이어그램 |
| CH06 | 없음 | 기존 CH05 이미지 경로 유지 (CH05→CH06 번호만 변경) |
