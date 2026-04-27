# 챕터 3. Kubernetes 시작하기


## 학습 목표

- 쿠버네티스의 구조와 동작 원리를 이해한다.
- Minikube로 로컬 환경에 쿠버네티스 클러스터를 구성한다.
- Deployment로 Pod를 관리하고, 자동 복구와 롤링 업데이트를 수행한다.
- Service로 Pod에 안정적으로 접근하는 네트워크를 구성한다.
- ConfigMap과 Secret으로 설정과 민감 정보를 외부에서 주입한다.
- Volume으로 영구 저장소를 구성하고, Ingress로 외부 요청을 라우팅한다.
- 미니큐브 위에서 풀스택 웹사이트를 배포한다.

## 3.1 쿠버네티스(Kubernetes)

### 3.1.1 쿠버네티스가 필요한 이유

Docker Compose로 여러 컨테이너를 실행할 수 있게 되었지만, 운영 환경에서는 다른 문제가 생깁니다. 예를 들어보겠습니다.

**상황 1 — 새벽 3시, 컨테이너가 죽었다**

백엔드 컨테이너가 메모리 부족으로 종료됐습니다. 사용자는 "서버 오류" 화면만 보게 됩니다. Docker Compose 환경이라면, 개발자가 알림을 확인하고 직접 `docker compose up`을 다시 실행해야 합니다. 그 사이 서비스는 멈춰 있습니다.

**상황 2 — 타임세일, 트래픽이 10배로 폭증**

평소에는 컨테이너 1대로 충분했는데, 이벤트가 시작되자 응답 시간이 급격히 느려졌습니다. 수동으로 컨테이너 수를 늘리려면 서버를 준비하고 설정을 수정한 뒤 다시 배포해야 합니다. 이벤트가 끝나면 또 줄여야 하는데, 매번 사람이 손으로 해야 합니다.

**상황 3 — 새 버전 배포, 서비스가 잠시 멈춘다**

결제 기능을 수정한 새 버전을 배포하는 상황입니다. 기존 컨테이너를 멈추고 새 컨테이너를 띄우는 그 짧은 순간, 결제 중이던 사용자는 오류를 만나게 됩니다.

컨테이너가 몇 개일 때는 수동 관리가 가능하지만, 수십~수백 개로 늘어나면 사실상 불가능합니다. 이를 자동으로 처리하는 것이 쿠버네티스입니다.

> **쿠버네티스(Kubernetes)** 는 구글에서 만든 대규모 컨테이너 관리 시스템입니다. 컨테이너를 자동으로 배포, 확장, 복구, 관리하는 운영 플랫폼입니다.

**"원하는 상태가 무엇인지"** 만 선언하면, "어떻게 복구할지"는 쿠버네티스가 알아서 맞춰 갑니다. 이것이 쿠버네티스의 핵심 철학인 **선언적 관리(Desired State)** 입니다. "백엔드 서버 3대를 유지해라"라고 선언해 두면, 1대가 죽었을 때 개발자가 개입하지 않아도 쿠버네티스가 자동으로 새 컨테이너를 띄워 3대를 맞춥니다. 이 장의 실습에서 이 동작을 직접 확인해 봅니다.

### 3.1.2 쿠버네티스의 핵심 리소스

외부에서 요청이 들어오면 아래 그림처럼 쿠버네티스의 각 리소스를 거쳐 컨테이너(Pod)에 도달합니다. 지금은 전체 흐름만 가볍게 살펴보겠습니다.

<!-- image-prompt: Minimal black line drawing on white background, very few details, icon-like simplicity, 4:3 aspect ratio, 800x600px. with Korean labels: Concept diagram showing the flow of an external request (외부 요청) through Kubernetes resources: Ingress arrow to Service arrow to Deployment arrow to Pod, with ConfigMap (설정), Secret (비밀 정보), and PVC (저장소 요청) connected to the Pod, illustrating the overall K8s architecture (쿠버네티스 구조도). -->
![쿠버네티스 구조도](images/chap03-k8s-architecture.png)
*그림 3-1: 쿠버네티스 핵심 리소스 구조도*

각 리소스의 역할은 아래 표와 같습니다. 상세 내용은 실습에서 하나씩 다룹니다.

| 리소스 | 역할 | 이야기 속 비유 |
|--------|------|--------------|
| **Ingress** | 외부 요청을 클러스터 내부로 라우팅하는 진입점 | 항구의 입구 게이트 |
| **Service** | Pod의 IP가 바뀌어도 고정된 진입점을 제공하여 트래픽을 전달 | 대표 전화번호 |
| **Deployment** | Pod의 생성, 개수 유지, 업데이트를 자동 관리하는 지침서 | "이 앱을 3개 유지하라"는 지침서 |
| **Pod** | 컨테이너를 실행하는 가장 작은 단위 | 컨테이너를 담는 가장 작은 상자 |
| **ConfigMap** | 데이터베이스 주소 등 일반 설정값을 저장 | 환경 설정표 |
| **Secret** | 비밀번호, API 키 등 민감한 설정값을 암호화하여 저장 | 금고 |
| **PVC / PV** | 컨테이너가 삭제되어도 데이터를 유지하는 영구 저장소 | 창고 신청서 / 창고 |


### 3.1.3 쿠버네티스의 동작 원리

쿠버네티스는 크게 **컨트롤 플레인(Control Plane)** 과 **워커 노드(Worker Node)** 로 구성되어 있습니다. 이 둘을 하나의 시스템처럼 묶은 구조를 **클러스터(Cluster)** 라고 합니다.

회사에 비유하면 다음과 같습니다.

- **컨트롤 플레인** — 본사 관리팀. "서버 3대를 유지해라", "이 서버가 죽으면 새로 띄워라" 같은 판단과 지시를 내립니다.
- **워커 노드** — 현장 작업자. 관리팀의 지시를 받아 실제로 컨테이너를 실행하고 관리합니다.

![쿠버네티스 클러스터 구조](images/fig-3-1.png)
*그림 3-2: 쿠버네티스 클러스터 구조*

개발자가 명령어를 입력하면 어떤 일이 벌어지는지 살펴봅시다.

**Step 1.** 명령이 컨트롤 플레인의 `Kube API Server`에 도달합니다.

![개발자의 명령이 Kube API Server로 전달되는 흐름](images/fig-3-2.png)
*그림 3-3: 개발자의 명령이 Kube API Server로 전달되는 흐름*

**Step 2.** `Kube API Server`는 컨트롤 플레인 내부의 구성 요소와 상호 작용합니다.

![컨트롤 플레인 내부 구성 요소의 상호 작용](images/fig-3-3.png)
*그림 3-4: 컨트롤 플레인 내부 구성 요소의 상호 작용*

| 구성 요소 | 역할 |
|-----------|------|
| **etcd** | 상태 정보를 저장하는 저장소 |
| **Controller** | 원하는 상태와 실제 상태를 비교하여 필요한 작업을 자동 생성 |
| **Scheduler** | 명령이 실행될 노드를 자동 선택 |

**Step 3.** 실행할 작업과 노드가 정해지면 워커 노드의 `kubelet`으로 전달됩니다.

![kubelet의 컨테이너 관리](images/fig-3-4.png)
*그림 3-5: kubelet의 컨테이너 관리*

> **kubelet** 은 컨트롤 플레인으로부터 명령을 받아 실제로 컨테이너를 관리하는 관리자입니다.

쿠버네티스가 무엇이고 어떻게 동작하는지 알아보았습니다. 이제 직접 실행해 볼 차례입니다. 실제 운영용 쿠버네티스 환경을 로컬 PC에서 그대로 구현하기는 어렵습니다. 로컬 PC 한 대로도 쿠버네티스를 체험할 수 있는 **미니큐브(Minikube)** 를 먼저 설치해보겠습니다.

## 3.2 미니큐브(Minikube)

> 3.2부터 3.7까지 작성하는 **YAML(yml)** 파일은 https://github.com/metacoding-10-linux-docker/docker/tree/master/yaml 에서 확인할 수 있습니다.

### 3.2.1 미니큐브(Minikube)란?

> **미니큐브(Minikube)** 는 Mini + Kubernetes라는 의미로, 로컬 PC에서 쿠버네티스 환경을 구성할 수 있는 개발용 프로그램입니다. Docker 컨테이너, VirtualBox 가상 머신 등을 사용해 미니큐브 환경을 구성할 수 있습니다.

미니큐브와 쿠버네티스의 기본 구조는 동일하지만, 미니큐브는 개발 환경용으로 설계된 만큼 하나의 노드에 컨트롤 플레인과 워커 노드 기능이 함께 들어 있습니다.

![미니큐브의 단일 노드 구조](images/fig-3-5.png)
*그림 3-6: 미니큐브의 단일 노드 구조*

미니큐브는 단일 노드로 구성되어 구조가 단순하고 필요한 리소스도 적습니다. 로컬 PC에서 간편하게 쓸 수 있는 대신, 로드 밸런싱이나 오토 스케일링 같은 기능은 지원하지 않습니다. 그래도 미니큐브를 쓰는 이유가 있습니다. 미니큐브에서 애플리케이션이 정상적으로 동작한다면, 동일한 설정과 구조를 실제 쿠버네티스 환경에도 그대로 적용할 수 있습니다.

### 3.2.2 미니큐브 기본 명령어

#### 미니큐브 설치

**[실습]** OS에 맞는 패키지 관리자로 미니큐브를 설치합니다.
```bash
# Windows (터미널을 관리자 권한으로 실행)
choco install minikube

# Mac (터미널에서 실행)
brew install minikube
```

> Windows는 **Chocolatey**, Mac은 **Homebrew** 패키지 관리자가 설치되어 있어야 동작하는 점 참고합니다.

#### 미니큐브 실행

**[실습]** 터미널에서 미니큐브를 실행합니다.
```bash
minikube start         # 미니큐브 클러스터 시작
```

![실행 결과](images/chap03-15.png)
*그림 3-7: minikube start 실행*

#### 미니큐브 명령어 요약

| 명령어 | 설명 |
|--------|------|
| `minikube start` | 미니큐브 실행 |
| `minikube stop` | 미니큐브 종료 |
| `minikube ip` | 미니큐브 IP 확인 |
| `minikube version` | 미니큐브 버전 확인 |
| `minikube dashboard` | 대시보드 실행 |
| `minikube service <서비스명> --url` | 서비스 접근 URL 생성 |
| `minikube addons enable ingress` | Ingress Controller 활성화 |
| `minikube tunnel` | 클러스터 외부에서 내부로 접근할 수 있도록 터널 생성 |

### 3.2.3 kubectl 명령어 — Pod 생성 및 관리

> **kubectl** 은 쿠버네티스 내부의 클러스터 리소스를 관리하는 명령어입니다.

쿠버네티스를 다루려면 kubectl 명령어를 익혀야 합니다. 먼저 쿠버네티스의 핵심 리소스인 Pod로 명령어를 실습해 보겠습니다.

#### Pod

Docker에서는 컨테이너를 직접 실행했지만, 쿠버네티스에서는 컨테이너를 Pod라는 껍데기에 담아 실행합니다. 쿠버네티스가 관리하는 단위는 컨테이너가 아니라 Pod입니다.

> **Pod** 는 쿠버네티스에서 컨테이너를 실행하는 가장 작은 단위입니다. Pod는 하나 이상의 컨테이너로 구성되어 있습니다.

![Pod — 최소 실행 단위](../assets/k8s-step1.png)
*그림 3-8: Pod — 컨테이너를 감싸는 최소 실행 단위*


#### Pod를 명령어로 생성하는 방법

`kubectl run` 명령어로 `Pod`를 생성할 수 있습니다. `kubectl run <pod명> --image=<이미지명>` 형태로 작성합니다.

**[실습]** nginx 이미지를 사용해 Pod를 생성하는 명령어입니다.
```bash
kubectl run hello-pod1 --image=nginx  # Dockerhub의 nginx 이미지로 Pod 생성
```

![kubectl run hello-pod1 실행 결과](../assets/01_kubectl-run-hello-pod1.png)
*그림 3-9: kubectl run hello-pod1 실행 결과*

#### Pod를 YAML 파일로 생성하는 방법

YAML 파일로 `Pod`를 생성할 수도 있습니다. hello-pod2.yml은 nginx 이미지를 사용하는 `Pod`를 정의합니다.

**[참고]** Github 프로젝트의 `yaml/hello-pod2.yml`을 참고합니다.

**yaml/hello-pod2.yml**
```yaml
apiVersion: v1                # API 버전
kind: Pod                     # 리소스 종류
metadata:
  name: hello-pod2            # 리소스명
spec:                         # 상세 설정
  containers:                 # 컨테이너 설정
    - name: hello-container   # 컨테이너 이름
      image: nginx:1.20       # 사용할 이미지
```

**[실습]** 터미널 창을 **yaml 폴더** 로 이동 후 아래 명령어를 실행하면 `Pod`가 생성됩니다.
```bash
kubectl apply -f hello-pod2.yml       # YAML 파일로 Pod 생성
```

![실행 결과](images/chap03-21.png)
*그림 3-11: kubectl apply로 Pod 생성*

#### Pod 조회

**[실습]** 생성된 `Pod` 목록을 조회합니다.
```bash
kubectl get pod                       # Pod 목록 조회
```

![Pod 목록 조회](../assets/02_kubectl-get-pod.png)
*그림 3-12: Pod 목록 조회*

`kubectl describe pod <Pod이름>` 명령어로 Pod의 상세 정보도 조회할 수 있습니다.

**[실습]** 생성된 `Pod` 목록을 조회합니다.
```bash
kubectl describe pod hello-pod2       # Pod 상세 정보 조회
```

![실행 결과](images/chap03-25.png)
*그림 3-13: Pod 상세 조회*

#### kubectl 명령어 요약

| 명령어 | 설명 |
|--------|------|
| `kubectl apply -f <파일>` | YAML 파일로 리소스 생성/업데이트 |
| `kubectl get <리소스>` | 리소스 목록 조회 |
| `kubectl describe <리소스> <이름>` | 리소스 상세 정보 확인 |
| `kubectl delete <리소스> <이름>` | 리소스 삭제 |
| `kubectl exec -it <Pod명> -- bash` | Pod 내부 접속 |
| `kubectl logs <Pod명>` | Pod 로그 확인 |
| `kubectl set image` | 리소스 이미지 변경 |

## 3.3 Deployment, ReplicaSet

앞에서 명령어로 `Pod`를 생성하는 방법을 배웠습니다. 그런데 `Pod`를 직접 생성하면 한 가지 문제가 있습니다. `Pod`가 오류로 종료되면 개발자가 직접 다시 실행해야 합니다. 이 문제를 해결하는 것이 `Deployment`입니다. **"이 Pod를 3개 유지하고, 문제 생기면 자동 교체하라"** 는 Pod 관리지침서와 같습니다.

![Deployment → ReplicaSet → Pod](../assets/k8s-step2.png)
*그림 3-14: Deployment가 ReplicaSet을 생성하고, ReplicaSet이 Pod 수를 유지한다*

### 3.3.1 Deployment

> **Deployment** 는 Pod를 자동으로 생성, 업데이트, 복구하는 관리 리소스입니다. Pod의 개수, 버전, 장애 여부를 지정된 상태에 맞게 자동으로 관리합니다.

`Deployment`로 Pod를 생성해 보겠습니다. nginx 이미지를 사용하는 deploy-ex01.yml입니다.

**[참고]** Github 프로젝트의 `yaml/deploy-ex01.yml`을 참고합니다.

**yaml/deploy-ex01.yml**
```yaml
apiVersion: apps/v1            # API 버전
kind: Deployment               # 리소스 종류
metadata:
  name: nginx-deploy           # 리소스 이름
spec:                          # pod에 대한 상태 지정
  replicas: 1                  # 생성할 pod 수 지정(명시하지 않으면 기본이 1)
  selector:                    # 관리할 Pod 선택 조건
    matchLabels:               
      app: nginx               # 라벨이 app : nginx인 pod를 관리
  template:                    # Pod 템플릿
    metadata:
      labels:                  
        app: nginx             # pod에 붙일 라벨
    spec:                      # 컨테이너 상세 설정
      containers:              
        - name: nginx-container  # 컨테이너 이름
          image: nginx:1.20    # 사용할 이미지
```

**Selector** 는 특정 label을 가진 리소스를 선택하는 조건입니다. Deployment나 Service의 Selector와 Pod의 labels가 일치하면 그 Pod를 관리 대상으로 삼습니다.

<!-- image-prompt: Minimal black line drawing on white background, very few details, icon-like simplicity, 4:3 aspect ratio, 800x600px. with Korean labels: Top: a box labeled "Deployment" containing only a funnel icon with text "셀렉터 (selector): { app: web }". No server icons, no terminal icons around the Deployment box. Below: three Pod boxes labeled Pod 1, Pod 2, Pod 3, each containing "Labels (라벨)" with values { app: web }, { app: web }, { app: db } respectively. Dotted arrows labeled "매칭" connect from the selector down to Pod 1 and Pod 2 (matching app: web). Pod 3 (app: db) has no arrow, showing it does not match. -->
![Selector와 Labels의 매칭 관계](images/selector-labels.png)
*그림 3-15: Selector가 app: web인 Pod만 매칭하고, app: db인 Pod는 매칭하지 않음*

아래 명령어로 `Deployment`를 생성합니다.

**[실습]** `Deployment`를 생성하고 `Pod`를 확인합니다.
```bash
kubectl apply -f deploy-ex01.yml      # Deployment 생성
kubectl get pod                       # Pod 목록 조회
```

![Deployment와 Pod 생성 확인](../assets/03_kubectl-get-pod-deploy.png)
*그림 3-16: Deployment와 Pod 생성 확인*

아래 명령어로 현재 생성된 Pod를 모두 제거합니다. 3.2에서 만든 hello-pod1, hello-pod2도 포함됩니다.

**[실습]** 전체 `Pod`를 삭제한 뒤 다시 조회합니다.
```bash
kubectl delete pod --all              # 전체 Pod 삭제
kubectl get pod                       # Pod 목록 조회
```

![Pod 제거 후 자동 재생성 확인](../assets/04_kubectl-delete-pod-all.png)
*그림 3-17: Pod 제거 후 자동 재생성 확인*

`kubectl run`으로 직접 생성한 `Pod`는 종료되었지만, `Deployment`로 생성된 `Pod`는 자동으로 재시작되었습니다.

>**Deployment** 로 Pod를 생성하면 Pod 생성뿐만 아니라, 개수 유지와 장애 복구까지 자동으로 처리됩니다. 그래서 Pod는 직접 생성하기보다 **Deployment** 로 생성하는 것이 일반적입니다.

**[실습]** 다음 실습을 위해 생성한 `Deployment`를 제거합니다.

```bash
kubectl delete deployment nginx-deploy # Deployment 삭제
```

### 3.3.2 ReplicaSet

이번에는 `Pod` 개수를 원하는 만큼 유지하는 `ReplicaSet`을 알아보겠습니다.

에어컨의 자동 온도 조절을 떠올려 봅시다. 24도로 설정해두면 온도가 올라갈 때 냉방을 틀고 내려가면 멈추며 알아서 맞춰줍니다. `ReplicaSet`은 `Pod` 개수를 설정해두면, 현재 상태가 설정과 다를 때 자동으로 개수를 맞춰주는 컨트롤러입니다.

> **ReplicaSet** 은 지정한 개수만큼 Pod가 항상 살아있도록 관리하는 컨트롤러입니다. Pod가 죽거나 예상보다 많아지는 상황이 발생하면 원래 설정된 수에 맞게 Pod를 자동으로 생성하거나 제거하여 상태를 일정하게 유지합니다.

<!-- image-prompt: Minimal black line drawing on white background, very few details, icon-like simplicity, 4:3 aspect ratio, 800x600px. with Korean labels: Diagram showing a ReplicaSet maintaining three Pods (Pod 3개 유지), with one Pod 종료  and a new Pod 자동 생성 (automatically being created) to maintain the 설정된 개수 -->
![ReplicaSet의 Pod 개수 유지](images/replicaset.png)
*그림 3-18: Pod 3이 종료되면 ReplicaSet이 설정 개수를 맞추기 위해 Pod 4를 자동 생성*

`ReplicaSet`은 `Deployment`에 설정합니다. Pod를 4개 생성하는 Deployment를 작성합니다.

**[참고]** Github 프로젝트의 `yaml/deploy-ex02.yml`을 참고합니다.

**yaml/deploy-ex02.yml**
```yaml
apiVersion: apps/v1      # API 버전
kind: Deployment         # 리소스 종류
metadata:
  name: nginx-replica    # 리소스 이름
spec:                    # 상세 설정
  replicas: 4            # pod 수 지정

  strategy:              # Pod 교체 방식 설정
    type: RollingUpdate  # 롤링 업데이트 전략
    rollingUpdate:
      maxSurge: 4        # 업데이트 중 최대 4개까지 추가 생성
      maxUnavailable: 4  # 업데이트 중 최대 4개까지 종료 허용

  selector:              # 라벨이 app: nginx 인 pod를 관리
    matchLabels:         # 라벨이 일치하는 Pod 선택
      app: nginx         # app이 nginx인 Pod 선택
  template:              # Pod 템플릿
    metadata:
      labels:            # 라벨 지정
        app: nginx       # pod에 붙일 라벨
    spec:                # 컨테이너 상세 설정
      containers:        # 컨테이너 설정
        - name: nginx-container  # 컨테이너 이름
          image: nginx:1.20      # 사용할 이미지
```

Deployment를 생성합니다.

**[실습]** `Deployment`를 생성하고 `Pod` 개수를 확인합니다.
```bash
kubectl apply -f deploy-ex02.yml      # Deployment 생성
kubectl get pod                       # Pod 목록 조회
```

![replicas 설정으로 Pod 4개 생성](../assets/07_kubectl-get-pods-replicas.png)
*그림 3-19: replicas 설정으로 Pod 4개 생성*

`replicas`에 설정한 수에 따라 `Pod`가 4개 생성됩니다.

### 3.3.3 롤링 업데이트(RollingUpdate)

deploy-ex02.yml을 보면 `strategy`의 `type`이 `RollingUpdate`로 되어 있습니다. 새 버전을 배포할 때 `Pod`를 한꺼번에 바꾸지 않고 순차적으로 교체합니다.

> **롤링 업데이트(RollingUpdate)** 는 기존 Pod를 한꺼번에 내리지 않고, 하나씩 새 버전으로 바꿔가는 무중단 배포 방식입니다. `maxSurge`는 업데이트 중 추가로 띄울 수 있는 Pod 수, `maxUnavailable`은 동시에 내릴 수 있는 Pod 수를 뜻합니다.

**[실습]** nginx 이미지를 1.21 버전으로 업데이트합니다.
```bash
kubectl set image deployment/nginx-replica nginx-container=nginx:1.21  # nginx 이미지를 1.21로 업데이트
```

![실행 결과](images/chap03-33.png)
*그림 3-20: 이미지 버전 업데이트 실행*

**[실습]** 업데이트 진행 상황을 실시간으로 확인합니다.
```bash
kubectl get pod -w                    # Pod 상태 실시간 감시
```

![롤링 업데이트 진행 상황](../assets/06_kubectl-get-pods-w-rolling.png)
*그림 3-21: 롤링 업데이트 진행 상황*

기존 Pod가 `Terminating` 상태로 종료되는 동안 새 Pod가 `ContainerCreating` → `Running` 상태로 전환됩니다.

> deploy-ex02.yml에 설정한 maxSurge와 maxUnavailable 값에 따라, 새 `Pod` 4개가 한 번에 생성되고 기존 `Pod`도 동시에 종료되었습니다. 이 값을 조절하면 원하는 방식으로 업데이트할 수 있습니다.

**[실습]** `Deployment`의 상세 정보를 확인하면 이미지가 1.21 버전으로 변경된 것을 볼 수 있습니다.
```bash
kubectl describe deployment nginx-replica  # Deployment 상세 정보 조회
```

### 3.3.4 Rollback

롤백은 Deployment를 이전 상태로 되돌리는 기능입니다. 새 버전 배포 후 문제가 발생하면 이전 이미지 버전으로 즉시 복구할 수 있습니다.

**[실습]** 먼저 배포 이력을 확인한 뒤 롤백합니다.
```bash
kubectl rollout history deployment/nginx-replica  # 배포 이력 조회
kubectl rollout undo deployment/nginx-replica      # 이전 버전으로 롤백
```

![실행 결과](images/chap03-36.png)
*그림 3-22: Rollback 실행 결과*

`kubectl describe` 명령어로 롤백된 이미지 버전을 확인합니다.

**[실습]** 다음 실습을 위해 생성한 `Deployment`를 제거합니다.

```bash
kubectl delete deployment nginx-replica  # Deployment 삭제 (Pod도 함께 제거됨)
```

## 3.4 Service

### 3.4.1 Service란?

`Deployment`로 `Pod`를 생성하면 자동으로 관리된다는 것을 배웠습니다. 그런데 `Pod`가 재시작될 때마다 IP가 바뀌어 외부에서 직접 접근하기 어렵습니다. 이 문제를 해결하는 것이 `Service`입니다.

콜센터의 대표 번호를 떠올려 봅시다. 고객은 상담사 개인 번호를 몰라도 대표 번호만 알면 연결됩니다. `Service`는 이 대표 번호처럼 `Pod` 앞에 고정 접근 주소를 하나 만들어줍니다.

![Service → Pod](../assets/k8s-step3.png)
*그림 3-23: Service는 고정 주소를 제공한다. Pod IP가 바뀌어도 Service 주소는 그대로다*

> **Service** 는 외부에서 Pod에 접근할 때 고정 IP를 제공해 안정적으로 접근할 수 있게 하는 리소스입니다.

#### Pod IP 변경

**[실습]** `Pod`의 IP는 재시작 시 변경됩니다. IP를 확인한 후 `Pod`를 삭제하고 다시 조회하면 IP가 달라진 것을 볼 수 있습니다.
```bash
kubectl get pod -o wide           # IP 확인 (예: 10.244.0.7)
kubectl delete pod --all          # Pod 삭제
kubectl get pod -o wide           # IP 변경됨 (예: 10.244.0.8)
```

![Pod IP 변경 확인](../assets/08_pod-ip-change.png)
*그림 3-24: Pod 재시작 시 IP 변경 확인*

#### Service 생성

`Service`는 `Deployment`처럼 selector의 라벨이 일치하는 `Pod`를 관리합니다. service-ex01.yml은 `NodePort` 타입의 `Service`를 정의하며, 외부에서 30080 포트로 접속할 수 있게 합니다.

**[참고]** Github 프로젝트의 `yaml/service-ex01.yml`을 참고합니다.

**yaml/service-ex01.yml**
```yaml
apiVersion: v1           # API 버전
kind: Service            # 리소스 종류
metadata:
  name: nginx-service    # 서비스 이름
spec:                    # 상세 설정
  type: NodePort         # 클러스터가 외부에서 접근할 수 있도록 노드를 열어줌
  selector:              # 연결할 Pod 선택 조건
    app: nginx           # app이 nginx인 Pod에 연결
  ports:                 # 포트 설정
  - port: 80             # 서비스가 클러스터 내부에서 열어둔 포트
```

Service의 포트는 외부 요청이 Pod까지 도달하는 경로를 정의합니다. 트래픽은 외부 → `nodePort` → `port` → `targetPort` → Pod 순으로 전달됩니다.

| 포트 종류 | 역할 | 생략 시 |
|----------|------|--------|
| `port` | 클러스터 내부에서 Service에 접근하는 포트 | 필수 |
| `targetPort` | Service가 트래픽을 전달할 Pod의 포트 | `port` 값과 동일하게 설정 |
| `nodePort` | 외부에서 노드 IP로 접근할 때 사용하는 포트 (30000~32767) | 범위 내 자동 할당 |

**[실습]** `Service`를 생성합니다.
```bash
kubectl apply -f service-ex01.yml     # Service 생성
```

![Service 생성](../assets/10_kubectl-apply-service.png)
*그림 3-25: Service 생성*

#### Service 타입 비교

Service 타입에 따라 외부 접근 가능 여부가 달라집니다. 백엔드나 DB처럼 외부에 노출할 필요가 없는 서비스는 `ClusterIP`로, 사용자가 직접 접속해야 하는 서비스는 `NodePort`나 `LoadBalancer`로 설정합니다.

| 타입 | 설명 | 접근 범위 |
|------|------|----------|
| ClusterIP | 클러스터 내부에서만 접근 가능한 기본 타입 | 내부 전용 |
| NodePort | 노드의 특정 포트(30000~32767)를 통해 외부에서 접근 가능 | 외부 접근 가능 |
| LoadBalancer | 클라우드 환경에서 외부 로드밸런서를 자동 생성 | 외부 접근 가능 (클라우드) |

### 3.4.2 Networking

`Service`를 생성했지만, 로컬 PC와 미니큐브는 서로 다른 네트워크에 있어 Service의 IP로 직접 접근할 수 없습니다. 두 네트워크를 잇는 다리가 필요한데, `minikube service` 명령어가 그 역할을 합니다. 실행하면 로컬 PC에서 접근할 수 있는 임시 경로가 생성됩니다.

> **minikube service** 명령어는 특정 Service에 대해 임시 접근 경로를 생성해, 로컬 PC에서 그 Service에 바로 접속할 수 있도록 합니다.

**[실습]** 로컬 PC에서 `Service`에 접속할 수 있는 URL을 생성합니다.
```bash
minikube service nginx-service --url  # Service 접근 URL 생성
```

![실행 결과](images/chap03-43.png)
*그림 3-26: minikube service URL 생성*

생성된 URL로 접속하면 미니큐브 내부 `Service`를 거쳐 `Pod` 서버로 요청이 전달됩니다.

![실행 결과](images/chap03-44.png)
*그림 3-27: 브라우저에서 nginx 접속 확인*

확인 후 CTRL + C를 입력해 터미널을 빠져나옵니다.

이번에는 `Pod`를 전부 삭제한 뒤 다시 접속해 보겠습니다.

**[실습]** `Pod`를 삭제하고, `minikube service` 명령어로 다시 접근합니다.
```bash
kubectl delete pod --all              # 전체 Pod 삭제
minikube service nginx-service --url  # Service 접근 URL 생성
```

![Pod 삭제 후 Service 접속](../assets/11_delete-pod-minikube-service.png)
*그림 3-28: Pod 삭제 후 Service 접속*

새 URL로 접속하면 nginx 페이지가 정상적으로 표시됩니다. `Service`가 고정 접근 경로를 유지하므로 Pod가 재실행되어도 연결이 끊기지 않습니다.

**[실습]** 실습이 끝난 후 `Deployment`와 `Service`를 삭제합니다.
```bash
kubectl delete deployment nginx-replica   # Deployment 삭제
kubectl delete service nginx-service     # Service 삭제
```

### 3.4.3 Ingress

`minikube service` 명령어는 테스트용 임시 경로입니다. 실제 운영 환경에서는 `http://my-service.com` 같은 도메인으로 접속합니다. 외부 요청을 클러스터 내부 `Service`로 연결하는 역할을 맡은 것이 `Ingress`입니다.

건물에 비유하면, `Service`가 각 부서의 내선 번호라면 `Ingress`는 건물 1층의 **안내 데스크**입니다. 방문자(외부 요청)가 들어오면 안내 데스크가 "어느 부서를 찾으세요?"라고 확인한 뒤 적절한 내선 번호(`Service`)로 연결합니다.

![Ingress → Service → Pod](../assets/k8s-step4c.png)
*그림 3-29: 외부 요청은 Ingress를 통해 Service로 전달된다*

> **Ingress** 는 클러스터 외부의 HTTP/HTTPS 요청을 내부 Service로 라우팅하는 규칙을 정의하는 리소스입니다.

`Ingress`가 동작하려면 두 가지가 갖춰져야 합니다.

| 구성 요소 | 역할 | 비유 |
|-----------|------|------|
| **Ingress Controller** | 실제로 외부 요청을 받아 처리하는 소프트웨어 | 안내 데스크에 앉아있는 직원 |
| **Ingress 리소스** | 어떤 요청을 어떤 Service로 보낼지 정의한 규칙 | 안내 데스크에 놓인 부서 안내판 |

`Ingress Controller`는 Nginx를 주로 사용하며, 미니큐브에서는 `minikube addons enable ingress` 명령어 한 줄로 활성화합니다.

`Ingress` 실습은 3.7절에서 진행합니다.

## 3.5 ConfigMap, Secret

Service 덕분에 Pod의 IP가 바뀌어도 안정적으로 접근할 수 있게 되었습니다. 그런데 실제 서비스를 운영하려면 데이터베이스 주소, API 키, 비밀번호 같은 설정 값이 필요합니다. 이런 값을 코드에 직접 넣으면 값이 바뀔 때마다 이미지를 다시 빌드해야 합니다. ConfigMap과 Secret이 이 문제를 해결합니다.

![ConfigMap / Secret → Pod](../assets/k8s-step4a.png)
*그림 3-30: ConfigMap과 Secret은 Pod에 설정과 민감 정보를 주입한다*

### 3.5.1 ConfigMap

데이터베이스 주소나 접속 URL 같은 설정 값을 코드에 직접 넣으면, 값이 바뀔 때마다 이미지를 다시 빌드해야 합니다. `ConfigMap`은 이런 설정 값을 코드 밖에서 관리합니다.

> **ConfigMap** 은 일반적인 설정 값을 외부에서 관리하는 리소스입니다. 환경 변수, 설정 파일 등 민감하지 않은 설정 정보를 저장하며, Pod는 이를 환경 변수로 전달받아 사용합니다.

**[참고]** Github 프로젝트의 `yaml/configmap-conn.yml`을 참고합니다.

**yaml/configmap-conn.yml**
```yaml
apiVersion: v1                       # API 버전
kind: ConfigMap                      # 리소스 종류
metadata:
  name: configmap-conn               # ConfigMap 이름 지정
data:                                # 설정값 넣는 영역
  conn_info: "localhost:80"          # 접속 정보
  conn_url: "config.test"            # 접속 URL
```

deploy-ex03.yml에서는 `envFrom.configMapRef`로 `ConfigMap`에 정의된 설정 값을 환경 변수로 `Pod`에 넣습니다.

**[참고]** Github 프로젝트의 `yaml/deploy-ex03.yml`을 참고합니다.

**yaml/deploy-ex03.yml**
```yaml
apiVersion: apps/v1                        # API 버전
kind: Deployment                           # 리소스 종류
metadata:
  name: nginx-config-secret                # 리소스 이름
spec:                                      # 상세 설정
  replicas: 1                              # pod 수 지정
  selector:                                # 관리할 Pod 선택 조건
    matchLabels:                           # 라벨이 일치하는 Pod 선택
      app: nginx                           # 라벨이 app : nginx인 pod를 관리
  template:                                # Pod 템플릿
    metadata:
      labels:                              # 라벨 지정
        app: nginx                          # pod에 붙일 라벨
    spec:                                  # 컨테이너 상세 설정
      containers:                          # 컨테이너 설정
        - name: nginx-container            # 컨테이너 이름
          image: nginx:1.20                # 사용할 이미지
          envFrom:                         # 환경 변수 일괄 주입
            - configMapRef:                # ConfigMap 참조
                name: configmap-conn         # ConfigMap 연결
```

**[실습]** `ConfigMap`과 `Deployment`를 생성합니다.
```bash
kubectl apply -f configmap-conn.yml   # ConfigMap 생성
kubectl apply -f deploy-ex03.yml     # Deployment 생성
```

**[실습]** `Pod`의 환경 변수를 조회하여 `ConfigMap` 설정이 적용되었는지 확인합니다. `kubectl get pod`로 먼저 Pod명을 확인한 뒤, 자신의 Pod명으로 바꿔서 실행합니다. Pod명의 해시값은 실행할 때마다 달라집니다.
```bash
kubectl get pod                       # Pod 목록 조회
kubectl exec -it <Pod명> -- env       # Pod 환경 변수 조회
```

![실행 결과](images/chap03-46.png)
*그림 3-31: Pod 환경 변수 조회*

출력된 환경 변수 중 `ConfigMap`에 설정한 `conn_info`와 `conn_url`이 보입니다.

### 3.5.2 Secret

ConfigMap이 일반적인 환경 설정이라면, Secret은 **금고**입니다. 비밀번호나 API 키처럼 민감한 정보는 설정표에 적어두면 안 됩니다. 금고에 따로 보관해야 합니다.

> **Secret** 은 비밀번호, 토큰, 인증 키처럼 민감한 정보를 안전하게 저장하고 관리하기 위한 리소스입니다. ConfigMap과 구조는 비슷하지만 Secret의 값은 Base64로 인코딩되어 저장됩니다. 단, Base64는 암호화가 아닌 단순 인코딩이므로 보안을 보장하지는 않습니다. Secret은 평문이 설정 파일에 직접 노출되는 것을 방지하는 수준이며, 실제 운영 환경에서는 별도의 암호화 솔루션을 사용해야 합니다.

**[참고]** Github 프로젝트의 `yaml/secret-password.yml`을 참고합니다.

**yaml/secret-password.yml**
```yaml
apiVersion: v1              # API 버전
kind: Secret                # 리소스 종류
metadata:
  name: secret-password     # Secret 이름
stringData:                 # 평문을 자동으로 Base64 변환
  password: metacoding1234  # 비밀번호 설정
```

**[실습]** `Secret`을 생성합니다. stringData 속성을 쓰면 평문이 자동으로 Base64로 변환됩니다.
```bash
kubectl apply -f secret-password.yml  # Secret 생성
```

**[실습]** `Secret`의 내부를 YAML 형태로 출력합니다.
```bash
kubectl get secret secret-password -o yaml  # Secret 내용을 YAML 형태로 출력
```

![실행 결과](images/chap03-48.png)
*그림 3-32: Secret의 Base64 인코딩 확인*

`Secret`을 YAML 형태로 출력해보면 비밀번호가 Base64로 인코딩되어 있습니다.

### 3.5.3 환경 변수 추가

deploy-ex03.yml에 `Secret`을 추가해보겠습니다. `secretRef`를 쓰면 `Secret`에 정의된 값을 환경 변수로 `Pod`에 넣을 수 있습니다.

3.5.1에서 작성한 deploy-ex03.yml의 `envFrom` 항목에 `secretRef`를 추가합니다. 추가된 부분만 표시합니다.

**[참고]** Github 프로젝트의 `yaml/deploy-ex03.yml`에서 `envFrom` 항목을 참고합니다.

**yaml/deploy-ex03.yml**
```yaml
          # ... 생략

          envFrom:
            - configMapRef:
                name: configmap-conn         # ConfigMap 연결
            - secretRef:
                name: secret-password        # Secret 연결 (추가)
```

**[실습]** 변경된 `Deployment`를 적용합니다. YAML 파일 내부의 `template` 속성이 변경되면 `kubectl apply -f`로 반영합니다.
```bash
kubectl apply -f deploy-ex03.yml     # 변경된 Deployment 적용
```

**[실습]** `Pod`의 환경 변수를 조회하면 `Secret`에 저장된 비밀번호가 주입되어 출력됩니다.
```bash
kubectl get pod                       # Pod 목록 조회
kubectl exec -it <Pod명> -- env       # Pod 환경 변수 조회
```

![Pod 환경 변수에 Secret 값 확인](../assets/13_secret-env.png)
*그림 3-33: Pod 환경 변수에 Secret 값 확인*

`Secret`에 Base64로 인코딩된 비밀번호는 `Pod`에서 사용될 때 자동으로 평문으로 변환됩니다.

### 3.5.4 환경 변수 수정

`ConfigMap`이나 `Secret`에서 환경 변수 값을 변경한 후 `kubectl apply -f 파일명`을 실행하면 변경 내용이 `Kube API Server`에 저장됩니다. 그런데 저장된 환경 변수가 실행 중인 `Pod`에 즉시 반영될까요? 그렇지 않습니다.

`Pod`나 `Deployment`는 설정 변경을 스스로 감지하지 않습니다. `Kube API Server`도 변경된 설정을 기존 `Pod`에 강제로 밀어 넣지 않습니다.

![ConfigMap 변경 후 Pod 재시작으로 반영되는 흐름](images/fig-3-6.png)
*그림 3-34: ConfigMap 변경 후 Pod 재시작으로 반영되는 흐름*

환경 변수 같은 실행 환경 설정은 프로세스가 시작될 때 한 번만 적용됩니다. 변경된 설정을 반영하려면 **Pod를 재시작**해야 합니다.

실습을 위해 configmap-conn.yml의 `conn_info` 포트를 90으로 수정해보겠습니다.

**[참고]** Github 프로젝트의 `yaml/configmap-conn.yml`에서 포트 수정 내용을 참고합니다.

**yaml/configmap-conn.yml**
```yaml
# ... 생략

  conn_info: "localhost:90"          # 환경변수 수정
```

**[실습]** 변경된 `ConfigMap`을 적용하고 `Pod`를 재시작합니다.
```bash
kubectl apply -f configmap-conn.yml   # 변경된 ConfigMap 적용
kubectl rollout restart deployment nginx-config-secret  # 재시작
```

![실행 결과](images/chap03-52.png)
*그림 3-35: ConfigMap 수정 후 Pod 재시작*

**[실습]** 재시작된 `Pod`의 환경 변수를 확인합니다.
```bash
kubectl exec -it <Pod명> -- env       # Pod 환경 변수 조회
```

![실행 결과](images/chap03-53.png)
*그림 3-36: 변경된 환경 변수 확인*

`conn_info` 변수의 포트가 90으로 변경되었습니다.

**[실습]** 다음 실습을 위해 생성한 리소스를 제거합니다.

```bash
kubectl delete deployment nginx-config-secret  # Deployment 삭제
kubectl delete configmap configmap-conn        # ConfigMap 삭제
kubectl delete secret secret-password          # Secret 삭제
```

## 3.6 Volume

`Pod` 안에서 생성한 파일은 `Pod`이 재시작되면 모두 사라집니다. 로그 파일이나 데이터베이스처럼 데이터를 보존해야 한다면 `Volume`이 필요합니다.

> **볼륨(Volume)** 은 Pod 내부 컨테이너가 사용할 수 있는 외부 저장 공간을 의미합니다.

Volume에는 여러 종류가 있습니다.

| 종류 | 설명 | 데이터 유지 |
|------|------|------------|
| **emptyDir** | Pod 생성 시 만들어지는 임시 저장 공간. 같은 Pod 안의 컨테이너끼리 데이터를 공유할 때 사용 | Pod 삭제 시 함께 삭제 |
| **hostPath** | 워커 노드(호스트)의 특정 경로를 Pod에 마운트 | 노드에 남아 있지만, Pod가 다른 노드로 이동하면 접근 불가 |
| **PV / PVC** | 클러스터 외부에 영구 저장소를 만들고, 요청서(PVC)를 통해 Pod에 연결 | Pod가 삭제되어도 유지 |

실무에서 가장 많이 사용하는 `PV / PVC`를 실습해 보겠습니다.

### 3.6.1 Persistent storage

**Persistent storage** 는 Pod가 종료되어도 데이터가 사라지지 않는 영구 저장소입니다. 실제 저장 공간인 `PV`(PersistentVolume)와 그 공간을 요청하는 `PVC`(PersistentVolumeClaim)로 구성됩니다.

![PV / PVC → Pod](../assets/k8s-step4b.png)
*그림 3-37: PV는 실제 저장 공간, PVC는 요청서. PVC를 통해 Pod에 저장소를 연결한다*

`PV`는 **창고** 공간이고, `PVC`는 **"10평짜리 창고가 필요합니다"라는 신청서**입니다. Pod은 PVC로 조건에 맞는 PV를 찾아 연결합니다. 실습 순서는 PV 생성 → PVC 생성 → Pod 연결입니다.

#### PV(PersistentVolume)

> **PV(PersistentVolume)** 는 실제 데이터가 저장되는 저장소입니다.

이번 실습에서는 로컬 PC의 폴더를 저장소로 사용합니다.

**[참고]** Github 프로젝트의 `yaml/volume-pv.yml`을 참고합니다.

**yaml/volume-pv.yml**
```yaml
apiVersion: v1             # API 버전
kind: PersistentVolume     # 리소스 종류
metadata:
  name: volume-pv          # PV 이름
spec:                      # 상세 설정
  capacity:
    storage: 1Gi           # 1Gi 용량 할당
  accessModes:
    - ReadWriteOnce        # 읽기/쓰기 권한
  storageClassName: ""     # PVC가 볼륨을 자동으로 생성 못하게 방지
  hostPath:
    path: /mnt/data        # 볼륨 경로 지정
```

`hostPath`의 `/mnt/data`는 미니큐브 내부 경로입니다. 로컬 PC의 폴더와 연결하려면 `minikube mount` 명령이 필요합니다. 먼저 데이터를 저장할 경로에 폴더를 생성합니다.

![실행 결과](images/chap03-58.png)
*그림 3-38: 로컬 PC에 볼륨 폴더 생성*

**[실습]** 로컬 PC의 `C:/volume` 경로와 미니큐브의 `/mnt/data` 경로를 마운트합니다.
```bash
minikube mount "C:/volume:/mnt/data"  # Windows
minikube mount "$HOME/volume:/mnt/data"  # Mac/Linux
```

![실행 결과](images/chap03-59.png)
*그림 3-39: minikube mount 실행*

`minikube mount` 명령어는 포그라운드로 실행됩니다. 터미널 창이 종료되면 마운트도 함께 끊기므로, 실습 중에는 **새 터미널 창을 열어야 합니다.** 이후 실습에서 `minikube tunnel`도 포그라운드로 실행되므로 터미널을 추가로 열게 됩니다. 현재 열린 터미널 상태를 정리하면 다음과 같습니다.

> **터미널 A**: `minikube mount` 실행 중 (종료하면 안 됨)
> **터미널 B**: `kubectl` 명령 전용 (이후 실습은 여기서 진행)

#### PVC(PersistentVolumeClaim)

저장 공간(PV)이 준비되었으니, 신청서(PVC)를 만듭니다.

> **PVC(PersistentVolumeClaim)** 는 Pod가 사용할 저장소의 조건(용량, 접근 모드 등)을 정의한 요청서입니다.

**[참고]** Github 프로젝트의 `yaml/volume-pvc.yml`을 참고합니다.

**yaml/volume-pvc.yml**
```yaml
apiVersion: v1                 # API 버전
kind: PersistentVolumeClaim    # 리소스 종류
metadata:
  name: volume-pvc             # pod가 참조하는 pvc명
spec:                          # 상세 설정
  accessModes:
    - ReadWriteOnce        # 읽기 쓰기 권한
  storageClassName: ""     # PVC가 자동으로 PV 생성하지 않도록 설정
  resources:
    requests:
      storage: 1Gi         # 용량
  volumeName: volume-pv    # 참조할 PV명
```

`PVC`가 `PV`와 바인딩되려면 `accessModes`와 `storageClassName` 설정이 서로 일치해야 하고, 요청 용량이 `PV` 용량 이하여야 합니다.

PV와 PVC가 준비되었으니 Pod에 연결해 보겠습니다.

**[참고]** Github 프로젝트의 `yaml/volume-pod.yml`을 참고합니다.

**yaml/volume-pod.yml**
```yaml
apiVersion: v1                   
kind: Pod                        
metadata:
  name: volume-pod               
spec:                            # 상세 설정
  containers:                    
  - name: nginx-volume           
    image: nginx                 
    volumeMounts:                # 사용할 볼륨 마운트
    - name: storage              # 볼륨 이름
      mountPath: /mnt/data       # 컨테이너에서 접근할 볼륨 위치
  volumes:                       # 볼륨 정의
  - name: storage                # 볼륨 이름
    persistentVolumeClaim:       # PVC 연결
      claimName: volume-pvc      # 참조할 PVC
```

**[실습]** 새로운 터미널 창에서 `PV`, `PVC`, `Pod`를 순서대로 생성합니다.
```bash
kubectl apply -f volume-pv.yml        # PV 생성
kubectl apply -f volume-pvc.yml       # PVC 생성
kubectl apply -f volume-pod.yml       # Pod 생성
```

**[실습]** `PV`와 `PVC`의 바인딩 상태를 확인합니다. `STATUS` 값이 **BOUND**이면 정상입니다.
```bash
kubectl get pv,pvc -o wide            # PV와 PVC 바인딩 상태 확인
```

![실행 결과](images/chap03-60.png)
*그림 3-40: PV와 PVC 바인딩 상태 확인*

**[실습]** 컨테이너 내부에 접속하여 `/mnt/data` 경로에 파일을 생성합니다.
```bash
kubectl exec -it volume-pod -- /bin/bash  # Pod 내부 접속
touch /mnt/data/c.txt                    # 볼륨 경로에 파일 생성
ls /mnt/data                             # 파일 목록 확인
```

![실행 결과](images/chap03-61.png)
*그림 3-41: 볼륨 경로에 파일 생성*

`/mnt/data` 경로에 파일이 정상적으로 생성되었습니다. 연결된 로컬 PC에도 같은 파일이 생성됩니다.

![실행 결과](images/chap03-62.png)
*그림 3-42: 로컬 PC에서 마운트된 파일 확인*

정리하면 다음과 같습니다.

- **인프라 운영자**는 PV(실제 스토리지 자원)를 생성하고 관리합니다.
- **개발자**는 PVC(스토리지 사용 요청)를 정의해 필요한 저장 공간을 요청합니다.
- **Pod**는 애플리케이션이 실행되는 최소 단위입니다.
- **PVC**는 Pod가 사용할 스토리지를 요청하는 신청서입니다.
- **PV**는 그 요청에 응답하는 실제 스토리지 자원입니다.

**[실습]** 다음 실습을 위해 생성한 리소스를 제거합니다.

```bash
kubectl delete pod volume-pod          # Pod 삭제
kubectl delete pvc volume-pvc          # PVC 삭제
kubectl delete pv volume-pv            # PV 삭제
```

쿠버네티스의 핵심 리소스를 하나씩 살펴보았습니다. 이제 이 개념들을 엮어 웹사이트 하나를 미니큐브 위에 배포해보겠습니다.

## 3.7 미니큐브를 활용한 웹 사이트 만들기

챕터 2에서는 프론트 서버 + 백엔드 서버 + DB 서버를 Docker Compose로 실행했습니다. 이번에는 Redis 서버를 추가해 미니큐브 환경에서 실행해보겠습니다.

> 실습 코드는 https://github.com/metacoding-10-linux-docker/docker/tree/master/ex08 에서 확인할 수 있습니다.

### 3.7.1 아키텍처

배포할 애플리케이션은 프론트엔드(Nginx), 백엔드(Spring Boot), DB(MySQL), Redis, 총 4개의 서비스로 구성됩니다.

![ex08 풀스택 Kubernetes 아키텍처](images/fig-3-7.png)
*그림 3-43: ex08 풀스택 Kubernetes 아키텍처*

챕터 2에서는 브라우저에서 `localhost`로 프론트엔드에 직접 접속했습니다. 쿠버네티스에서는 외부 요청이 클러스터 내부로 바로 들어갈 수 없어 `Ingress`가 앞단에 놓입니다. 브라우저 요청은 `Ingress`가 받아 `Frontend Service`로 넘기고, 이후 프론트엔드 → 백엔드 → DB/Redis 순으로 흐릅니다.

### 3.7.2 이미지 폴더

**[EX08 패키지 구조]**

```
ex08/
├── backend/
│   ├── Dockerfile
│   └── entrypoint.sh
├── db/
│   ├── Dockerfile
│   └── init.sql
├── frontend/
│   ├── Dockerfile
│   ├── index.html
│   └── nginx.conf
├── redis/
│   └── Dockerfile
└── k8s/
```

EX08 폴더에는 이미지 생성을 위한 backend, db, frontend, redis 폴더와 쿠버네티스 배포 설정을 담은 k8s 폴더가 있습니다.

> Backend, DB, Frontend, Redis 폴더는 EX07과 동일한 구조입니다. 설명이 필요한 부분만 코드로 표시합니다.

Redis를 추가하기 위해 Dockerfile을 작성합니다.

**[참고]** Github 프로젝트의 `ex08/redis/Dockerfile`을 참고합니다.

**ex08/redis/Dockerfile**
```dockerfile
FROM redis:7.4-alpine       # Redis 이미지 사용
CMD ["redis-server"]         # Redis 서버 실행
```

backend 폴더의 entrypoint.sh에서 `Git clone` 주소를 수정합니다.

**[참고]** Github 프로젝트의 `ex08/backend/entrypoint.sh`를 참고합니다.

**ex08/backend/entrypoint.sh**
```bash
#!/bin/bash
git clone https://github.com/metacoding-10-linux-docker/backend-redis-server  # 백엔드 서버 내려받기
cd backend-redis-server      # 내려받은 폴더로 이동
chmod +x gradlew             # 실행 권한 부여
./gradlew build              # 스프링 프로젝트 빌드
java -jar -Dspring.profiles.active=prod build/libs/*.jar  # 빌드된 파일 실행
```

수정된 백엔드 서버는 API 요청 시 회원 정보와 Redis에 저장된 방문 횟수를 함께 돌려줍니다.

**[참고]** `entrypoint.sh`에서 내려받는 백엔드 서버의 핵심 API 코드는 다음과 같습니다.

**UserController.java**
```java
@GetMapping("/api/users")
public ResponseEntity<?> findAll() {

    List<User> users = userRepository.findAll();       // DB에서 회원 목록 조회

    Long count = redisTemplate.opsForValue()
            .increment("cnt:/api/users:total");        // Redis 방문 횟수 증가

    Map<String, Object> response = new HashMap<>();
    response.put("users", users);                      // 회원 목록
    response.put("count", count);                      // 방문 횟수

    return Resp.ok(response);
}
```

프론트엔드의 index.html도 수정합니다. EX07에서 방문 횟수를 표시하는 부분이 추가되었습니다.

**[참고]** Github 프로젝트의 `ex08/frontend/index.html`을 참고합니다. (핵심 부분 발췌)

**ex08/frontend/index.html**
```html
<h1>사용자 리스트</h1>
<h2>방문 횟수: <span id="visit-count">0</span></h2>

<script>
  fetch('/api/users')                    // nginx가 backend로 프록시
    .then(response => response.json())
    .then(data => {
      const users = data.body.users;     // 회원 목록
      const count = data.body.count;     // 방문 횟수

      users.forEach(user => {            // 응답 데이터를 테이블에 렌더링
        $("#user-list").append(render(user));
      });

      $("#visit-count").text(count);     // 방문 횟수 표시
    });
  // ... 생략
</script>
```

nginx.conf도 수정합니다. upstream의 서버 주소를 Kubernetes Service명(backend-service)으로 바꿉니다.

**[참고]** Github 프로젝트의 `ex08/frontend/nginx.conf`를 참고합니다.

**ex08/frontend/nginx.conf**
```nginx
events {}

http {
    # 백엔드 서버 주소 (K8s Service명으로 수정)
    upstream backend {
        server backend-service:8080;
    }

    server {
        listen 80;
        server_name _;

        # 정적 파일 제공
        location / {
            root   /usr/share/nginx/html;
            index  index.html;
        }

        # API 요청은 백엔드로 프록시
        location /api/ {
            proxy_pass http://backend;
        }
    }
}
```

### 3.7.3 k8s 폴더

ex08 폴더 내에 k8s 폴더가 있습니다.

> **k8s 폴더** 는 Kubernetes 배포 설정 파일을 모아둔 폴더입니다.

**[k8s 패키지 구조]**

```
k8s/
├── backend/
│   ├── backend-configmap.yml
│   ├── backend-deploy.yml
│   ├── backend-secret.yml
│   └── backend-service.yml
├── db/
│   ├── db-deploy.yml
│   ├── db-pv.yml
│   ├── db-pvc.yml
│   ├── db-secret.yml
│   └── db-service.yml
├── frontend/
│   ├── frontend-deploy.yml
│   ├── frontend-ingress.yml
│   └── frontend-service.yml
├── redis/
│   ├── redis-deploy.yml
│   └── redis-service.yml
└── namespace.yml
```

| 파일 | 설명 |
|------|------|
| namespace.yml | 리소스를 논리적으로 구분하는 `Namespace` 생성 |
| *-deploy.yml | 각 서버의 `Deployment` (Pod 생성 및 관리) |
| *-service.yml | 각 서버의 `Service` (고정 IP로 Pod 접근) |
| frontend-ingress.yml | 외부 요청을 프론트엔드 `Service`로 라우팅하는 `Ingress` |
| backend-configmap.yml | 백엔드 환경 변수 (DB 주소, Redis 주소) |
| backend-secret.yml | 백엔드 민감 정보 (DB 계정/비밀번호) |
| db-secret.yml | DB 민감 정보 (MySQL 계정/비밀번호) |
| db-pv.yml / db-pvc.yml | DB 데이터 영구 저장을 위한 `PV`/`PVC` |

#### Namespace

지금까지 실습에서 만든 Deployment, Service, ConfigMap 등은 모두 **default** 라는 기본 공간에 생성되었습니다. 리소스가 몇 개 안 될 때는 상관없지만, 여러 서비스의 리소스가 한 곳에 섞이면 관리하기 어렵습니다.

`Namespace`는 이 문제를 해결합니다. 회사 건물의 **층**과 같습니다. 1층은 프론트엔드 팀, 2층은 백엔드 팀, 3층은 데이터 팀처럼 층을 나누면 각 팀의 공간이 분리됩니다. Namespace로 나누면 리소스가 논리적으로 분리되어 이름이 겹칠 걱정 없이 독립 관리할 수 있습니다.

![Namespace](../assets/k8s-namespace.png)
*그림 3-44: 같은 Cluster 안에서 Namespace로 리소스를 분리한다*

> **Namespace** 는 쿠버네티스 리소스를 논리적으로 구분하는 가상의 공간입니다. 별도로 지정하지 않으면 모든 리소스는 **default** 네임스페이스에 생성됩니다.

이번 실습에서는 `metacoding`이라는 Namespace를 만들어 모든 리소스를 그 안에 생성합니다. 각 YAML 파일의 `metadata`에 `namespace: metacoding`이 들어가 있는 이유가 여기 있습니다.

**[참고]** Github 프로젝트의 `ex08/k8s/namespace.yml`을 참고합니다.

**ex08/k8s/namespace.yml**
```yaml
apiVersion: v1           # API 버전
kind: Namespace          # 리소스 종류
metadata:
  name: metacoding       # 네임스페이스 이름
```

Namespace를 지정한 리소스를 조회할 때는 `-n` 옵션으로 Namespace를 밝혀야 합니다.

**[예시]** Namespace를 지정하여 `Pod`를 조회합니다.
```bash
kubectl get pod -n metacoding        # metacoding 네임스페이스의 Pod 조회
```

#### backend-deploy.yml

backend-deploy.yml은 이번 실습에서 가장 많은 리소스를 조합한 설정입니다. `replicas: 2`로 `Pod`를 2개 생성하고, `envFrom`으로 `ConfigMap`과 `Secret`을 연결해 환경 변수를 주입합니다.

**[참고]** Github 프로젝트의 `ex08/k8s/backend/backend-deploy.yml`을 참고합니다.

**ex08/k8s/backend/backend-deploy.yml**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend-deploy
  namespace: metacoding                        # namespace 설정
spec:
  replicas: 2                                  # pod 2개 생성
  selector:
    matchLabels:
      app: backend                             # app: backend 라벨을 가진 pod 관리
  template:
    metadata:
      labels:
        app: backend                           # pod에 app: backend 라벨 붙임
    spec:
      containers:
        - name: backend-server
          image: metacoding/backend:1
          ports:
            - containerPort: 8080               # 8080 포트 사용
          envFrom:
            - configMapRef:
                name: backend-configmap         # configmap 연결
            - secretRef:
                name: backend-secret            # secret 연결
```

`ConfigMap`에는 DB 주소, Redis 주소 등 일반 설정을, `Secret`에는 DB 계정/비밀번호를 넣습니다. `Service`, `ConfigMap`, `Secret` 파일은 앞에서 배운 구조와 동일하므로 Github을 참고합니다.

#### db-deploy.yml

db-deploy.yml은 `volumeMounts`와 `PVC`를 연결해 DB 데이터를 영구적으로 저장합니다.

**[참고]** Github 프로젝트의 `ex08/k8s/db/db-deploy.yml`을 참고합니다.

**ex08/k8s/db/db-deploy.yml**
```yaml
apiVersion: apps/v1                    # API 버전
kind: Deployment                       
metadata:
  name: db-deploy                      
  namespace: metacoding                # namespace 설정
spec:                                  
  replicas: 1                          # Pod 1개 유지
  selector:                            # 관리할 Pod 선택 조건
    matchLabels:
      app: db                          # app: db 라벨을 가진 pod 관리
  template:
    metadata:
      labels:
        app: db                        # pod에 app: db 라벨 부여
    spec:
      containers:
        - name: db-server
          image: metacoding/db:1
          ports:
            - containerPort: 3306      # 3306 포트 사용
          envFrom:
            - secretRef:
                name: db-secret        # DB 접속을 위한 환경 변수 연결
          volumeMounts:
            - name: data
              mountPath: /var/lib/mysql  # volume 경로 설정
      volumes:
        - name: data
          persistentVolumeClaim:
            claimName: db-pvc            # PVC 연결
```

`Secret`, `PV`, `PVC`, `Service` 파일은 앞에서 본 구조와 동일하므로 Github을 참고합니다.

#### 나머지 설정

frontend, redis의 `Deployment`와 `Service`는 backend와 같은 구조입니다. 이미지명, 라벨, 포트만 다릅니다. 전체 코드는 Github을 참고합니다.

| 항목 | frontend | redis |
|------|----------|-------|
| image | metacoding/frontend:1 | metacoding/redis:1 |
| containerPort | 80 | 6379 |
| replicas | 1 | 1 |
| Service port | 80 | 6379 |

#### frontend-ingress.yml

`Ingress` 리소스를 작성합니다. 모든 외부 요청을 `frontend-service`의 80번 포트로 전달하는 규칙을 정의합니다.

**[참고]** Github 프로젝트의 `ex08/k8s/frontend/frontend-ingress.yml`을 참고합니다.

**ex08/k8s/frontend/frontend-ingress.yml**
```yaml
apiVersion: networking.k8s.io/v1         # API 버전
kind: Ingress                            # 리소스 종류
metadata:
  name: frontend-ingress                 # Ingress 이름
  namespace: metacoding                  # 네임스페이스 지정
spec:                                    # 상세 설정
  rules:                                 # 라우팅 규칙
    - http:                              # HTTP 규칙
        paths:                           # 경로 설정
          - path: /                       # 모든 경로
            pathType: Prefix             # 경로 매칭 방식
            backend:                     # 요청을 전달할 대상
              service:                   # 서비스 지정
                name: frontend-service    # 프론트엔드 Service로 연결
                port:                    # 포트 설정
                  number: 80             # 서비스 포트 번호
```

**path**는 어떤 경로의 요청을 받을지 정하는 설정입니다. `/`로 지정하면 모든 경로의 요청을 받아 `frontend-service`의 80번 포트로 넘깁니다.

> 전체 k8s 설정 파일은 https://github.com/metacoding-10-linux-docker/docker/tree/master/ex08/k8s 에서 확인할 수 있습니다.

### 3.7.4 실행하기

**[실습]** 미니큐브가 실행되어 있지 않다면 먼저 미니큐브를 실행합니다.
```bash
minikube start                        # 미니큐브 클러스터 시작
```

#### Ingress Controller 활성화

`Ingress` 리소스가 동작하려면 `Ingress Controller`가 먼저 설치되어 있어야 합니다. 미니큐브에서는 애드온(addon)으로 활성화합니다.

**[실습]** Nginx Ingress Controller를 활성화합니다.
```bash
minikube addons enable ingress        # Ingress Controller 활성화
```

![실행 결과](images/chap03-ingress-addon.png)
*그림 3-45: Ingress Controller 활성화*

**[실습]** Ingress Controller가 정상 실행 중인지 확인합니다. `ingress-nginx-controller` Pod의 STATUS가 `Running`이면 정상입니다.
```bash
kubectl get pod -n ingress-nginx      # Ingress Controller Pod 상태 확인
```

![실행 결과](images/chap03-ingress-controller-running.png)
*그림 3-46: Ingress Controller 실행 확인*

#### 이미지 빌드

> **minikube image build**: 미니큐브는 별도의 가상 환경(Docker 컨테이너 또는 VM) 안에서 동작합니다. 로컬 PC에서 `docker build`로 만든 이미지는 미니큐브 내부에서 접근할 수 없습니다. `minikube image build` 명령을 사용하면 미니큐브 내부에 직접 이미지를 빌드해 별도의 이미지 레지스트리 없이도 Pod에서 바로 사용할 수 있습니다.

**[실습]** EX08 폴더로 이동한 뒤 각 서버의 Docker 이미지를 미니큐브 내부에 빌드합니다.
```bash
minikube image build -t metacoding/db:1 ./db            # DB 이미지 빌드
minikube image build -t metacoding/backend:1 ./backend   # 백엔드 이미지 빌드
minikube image build -t metacoding/frontend:1 ./frontend # 프론트엔드 이미지 빌드
minikube image build -t metacoding/redis:1 ./redis       # Redis 이미지 빌드
```

![실행 결과](images/chap03-67.png)
*그림 3-47: 미니큐브 이미지 빌드*

#### 리소스 생성

**[실습]** `Namespace`를 생성합니다.
```bash
kubectl apply -f k8s/namespace.yml    # Namespace 생성
```

![실행 결과](images/chap03-68.png)
*그림 3-48: Namespace 생성*

**[실습]** k8s 폴더의 모든 리소스를 생성합니다. `--recursive` 옵션을 붙이면 하위 폴더의 YAML 파일도 모두 적용됩니다.
```bash
kubectl apply -f k8s/ --recursive     # k8s 폴더의 모든 리소스 일괄 생성
```

![실행 결과](images/chap03-69.png)
*그림 3-49: k8s 리소스 일괄 생성*

**[실습]** 생성된 리소스 정보를 확인합니다.
```bash
kubectl get deploy,pod,service -n metacoding  # Deployment, Pod, Service 조회
```

![실행 결과](images/chap03-70.png)
*그림 3-50: Deployment, Pod, Service 조회*

#### 컨테이너 실행 확인

**[실습]** 각 서버의 로그를 확인합니다.
```bash
kubectl logs deploy/db-deploy -n metacoding --tail=5       # DB 서버 로그 확인
kubectl logs deploy/frontend-deploy -n metacoding --tail=5 # 프론트엔드 서버 로그 확인
kubectl logs deploy/backend-deploy -n metacoding --tail=5  # 백엔드 서버 로그 확인
```

![실행 결과](images/chap03-71.png)
*그림 3-51: 서버 로그 확인*

> **Pod** 가 Running 상태라고 해서 서버가 바로 정상 동작하는 건 아닙니다. 실행에 시간이 필요할 수 있으니 **kubectl logs** 명령어를 활용해 각 서버의 로그를 확인하며 정상적으로 동작하는지 확인합니다.

#### Ingress로 서버 연결

리소스가 모두 생성되었으니 `Ingress`를 통해 프론트엔드에 접속해보겠습니다.

**[실습]** 생성된 `Ingress` 정보를 확인합니다. ADDRESS에 IP가 표시되면 정상입니다. 1~2분 정도 기다려야 할 수 있습니다.
```bash
kubectl get ingress -n metacoding     # Ingress 리소스 조회
```

![실행 결과](images/chap03-ingress-get.png)
*그림 3-52: Ingress 리소스 확인*

**[실습]** `minikube tunnel` 명령어를 실행합니다. Docker Desktop 드라이버를 쓰는 경우 로컬 PC에서 미니큐브 내부 IP로 직접 접근할 수 없어 터널이 필요합니다.
```bash
minikube tunnel                       # 로컬 PC에서 클러스터 접근을 위한 터널 생성
```

![실행 결과](images/chap03-ingress-tunnel.png)
*그림 3-53: minikube tunnel 실행*

> `minikube tunnel`은 포그라운드로 실행됩니다. 터미널 창을 종료하면 터널도 함께 종료되니, 접속 확인이 끝날 때까지 유지합니다.

**[실습]** 브라우저에서 `http://127.0.0.1:80`로 접속합니다.

![실행 결과](images/chap03-ingress-result.png)
*그림 3-54: Ingress를 통한 웹사이트 접속*

DB에서 조회된 데이터가 화면에 표시됩니다. 여러 번 요청을 보내면 방문 횟수가 늘어납니다.

![실행 결과](images/chap03-ingress-result2.png)
*그림 3-55: 방문 횟수 증가 확인*

`minikube service`로 임시 URL을 만들어 접속하던 것과 달리, `Ingress`는 도메인 기반 라우팅을 지원해 실제 운영 환경에 더 가까운 구조입니다.

`Pod` 내부를 확인해보겠습니다. `minikube tunnel`이 실행 중인 터미널은 그대로 두고, 새 터미널 창을 엽니다.

**[실습]** 전체 `Pod` 목록을 확인합니다.
```bash
kubectl get pod -n metacoding         # metacoding 네임스페이스의 Pod 목록 조회
```

![실행 결과](images/chap03-75.png)
*그림 3-56: 전체 Pod 목록 확인*

**[실습]** 각 백엔드 서버의 로그를 확인합니다.
```bash
kubectl logs backend-deploy-f7878cc5f-rbs74 -n metacoding --tail=10  # 백엔드 서버 1 로그 확인
kubectl logs backend-deploy-f7878cc5f-wt2cd -n metacoding --tail=10  # 백엔드 서버 2 로그 확인
```

**backend-deploy-f7878cc5f-rbs74**

![실행 결과](images/chap03-76.png)
*그림 3-57: 백엔드 서버 1 로그*

**backend-deploy-f7878cc5f-wt2cd**

![실행 결과](images/chap03-77.png)
*그림 3-58: 백엔드 서버 2 로그*

로그에서 회원 정보를 조회하는 `SELECT문`이 출력됩니다. `backend-service`가 로드밸런싱을 수행해 요청이 두 서버로 분산되었습니다.

## 이것만은 기억하자

- **컨테이너가 많아지면, 관제탑이 필요하다.** 컨테이너 몇 개는 수동으로 관리할 수 있지만 수십~수백 개가 되면 자동으로 배포, 복구, 확장하는 쿠버네티스가 필요합니다.
- **Deployment + Service + Ingress = 안정적인 서비스.** Deployment가 Pod의 개수와 상태를 자동으로 유지하고, Service가 고정된 접근점을 제공하며, Ingress가 외부 요청을 적절한 Service로 라우팅합니다.
- **설정은 밖에서, 데이터는 영구히.** ConfigMap과 Secret으로 코드와 설정을 분리하고, PV/PVC로 컨테이너가 사라져도 데이터를 보존합니다.

Docker와 Kubernetes를 향한 여정이 마무리되었습니다. 챕터 1에서 컨테이너 하나를 띄우는 것으로 시작해, 챕터 2에서 Docker Compose로 여러 컨테이너를 한 번에 관리했습니다. 챕터 3에서는 쿠버네티스로 자동화된 운영 환경까지 구성했습니다. Ingress로 외부 요청을 도메인 기반으로 연결하는 것까지 마쳤으니, 실무 환경과의 거리가 한층 좁혀졌습니다. 실무에는 Helm, CI/CD 파이프라인 같은 주제가 더 기다리고 있습니다. 여기까지 온 이상, 그 어떤 기술도 낯설지 않을 것입니다.

