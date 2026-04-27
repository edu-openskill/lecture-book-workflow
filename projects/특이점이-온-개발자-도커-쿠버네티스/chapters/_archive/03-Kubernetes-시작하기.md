# 챕터 3. Kubernetes 시작하기 — v3.0

## 학습 목표
- 쿠버네티스의 구조와 동작 원리를 이해한다.
- Minikube로 로컬 환경에 쿠버네티스 클러스터를 구성한다.
- Deployment로 Pod을 관리하고, 롤링 업데이트와 롤백을 수행한다.
- Service로 Pod에 안정적으로 접근하는 네트워크를 구성한다.
- ConfigMap과 Secret으로 설정과 민감 정보를 외부에서 주입한다.
- Volume과 PV/PVC로 영구 저장소를 구성한다.
- 미니큐브 위에서 풀스택 웹사이트를 배포한다.


## 3.1 Kubernetes : 컨테이너 오케스트레이션

### 3.1.1 Kubernetes : 왜 필요한가

Docker Compose로 여러 컨테이너를 실행할 수 있게 되었지만 운영 환경에서는 새로운 문제가 생깁니다. 쇼핑몰을 예로 들어보겠습니다.

**상황 1 — 새벽 3시, 컨테이너가 죽었다**

백엔드 컨테이너가 메모리 부족으로 종료됐습니다. 사용자는 "서버 오류" 화면만 보게 됩니다. Docker Compose 환경이라면? 개발자가 알림을 확인하고 직접 `docker compose up`을 다시 실행해야 합니다. 그 사이 서비스는 멈춰 있습니다.

**상황 2 — 타임세일, 트래픽이 10배로 폭증**

평소에는 컨테이너 1대로 충분했는데, 이벤트가 시작되자 응답 시간이 급격히 느려졌습니다. 수동으로 컨테이너 수를 늘리려면 서버를 준비한 뒤 설정을 수정하고 다시 배포해야 합니다. 이벤트가 끝나면 또 줄여야 하는데, 이걸 매번 사람이 해야 합니다.

**상황 3 — 새 버전 배포, 서비스가 잠시 멈춘다**

결제 기능을 수정한 새 버전을 배포하는 상황입니다. 기존 컨테이너를 멈추고 새 컨테이너를 띄우는 그 짧은 순간, 결제 중이던 사용자는 오류를 만나게 됩니다.

컨테이너가 몇 개일 때는 수동 관리가 가능하지만, 수십~수백 개로 늘어나면 사람 손으로는 감당할 수 없습니다. 이걸 자동으로 해주는 게 바로 쿠버네티스입니다.

> **쿠버네티스(Kubernetes)** 는 구글에서 만든 대규모 컨테이너 관리 시스템입니다. 컨테이너를 자동으로 배포, 확장, 복구, 관리해주는 운영 플랫폼입니다.

### 3.1.2 Kubernetes : 핵심 리소스

쿠버네티스는 `Pod`, `Deployment`, `Service`라는 핵심 리소스로 컨테이너를 관리합니다. 각 리소스의 상세한 역할은 이후에 하나씩 학습합니다. 여기서는 전체적인 요청 흐름만 간략히 살펴보겠습니다.

<!-- image-prompt: Minimal black line drawing on white background, very few details, icon-like simplicity, 4:3 aspect ratio, 800x600px. with Korean labels: Concept diagram showing the flow of an external request (외부 요청) through Kubernetes resources: Ingress arrow to Service arrow to Deployment arrow to Pod, with ConfigMap (설정), Secret (비밀 정보), and PVC (저장소 요청) connected to the Pod, illustrating the overall K8s architecture (쿠버네티스 구조도). -->
![쿠버네티스 구조도](images/chap03-k8s-architecture.png)
*그림 3-1: 쿠버네티스 구조도*

이 그림은 외부 요청이 클러스터 내부의 각 리소스를 거쳐 처리되는 전체 흐름을 보여줍니다.

| 리소스 | 역할 | 이야기 속 비유 |
|--------|------|--------------|
| **Ingress** | 외부 요청을 클러스터 내부로 라우팅하는 진입점 | 항구의 입구 게이트 |
| **Service** | Pod의 IP가 바뀌어도 고정된 진입점을 제공하여 트래픽을 전달 | 대표 전화번호 |
| **Deployment** | Pod의 생성, 개수 유지, 업데이트를 자동 관리하는 지침서 | "이 앱을 3개 유지하라"는 지침서 |
| **Pod** | 컨테이너를 실행하는 가장 작은 단위 | 컨테이너를 담는 가장 작은 상자 |
| **ConfigMap** | 데이터베이스 주소 등 일반 설정값을 저장 | 환경 설정표 |
| **Secret** | 비밀번호, API 키 등 민감한 설정값을 암호화하여 저장 | 금고 |
| **PVC / PV** | 컨테이너가 삭제되어도 데이터를 유지하는 영구 저장소 | 창고 신청서 / 창고 |

### 3.1.4 Kubernetes : 동작 원리

쿠버네티스는 크게 **컨트롤 플레인(Control Plane)** 과 **워커 노드(Worker Node)** 로 구성되어 있습니다. 이 둘을 하나의 시스템처럼 묶은 구조를 **클러스터(Cluster)** 라고 합니다.

![쿠버네티스 클러스터 구조](images/fig-3-2.png)
*그림 3-2: 쿠버네티스 클러스터 구조*

개발자가 `kubectl` 명령어를 입력하면 어떤 일이 벌어지는지 살펴봅시다. 다음과 같은 순서로 동작합니다.

**Step 1.** 명령이 컨트롤 플레인의 `Kube API Server`에 도달합니다.

![개발자의 명령이 Kube API Server로 전달되는 흐름](images/fig-3-3.png)
*그림 3-3: 개발자의 명령이 Kube API Server로 전달되는 흐름*

**Step 2.** `Kube API Server`는 컨트롤 플레인 내부의 구성 요소와 상호 작용합니다.

![컨트롤 플레인 내부 구성 요소의 상호 작용](images/fig-3-4.png)
*그림 3-4: 컨트롤 플레인 내부 구성 요소의 상호 작용*

| 구성 요소 | 역할 |
|-----------|------|
| **etcd** | 상태 정보를 저장하는 저장소 |
| **Controller** | 원하는 상태와 실제 상태를 비교하여 필요한 작업을 자동 생성 |
| **Scheduler** | 명령이 실행될 노드를 자동 선택 |

**Step 3.** 실행할 작업과 노드가 정해지면 워커 노드의 `kubelet`으로 전달됩니다.

![kubelet의 컨테이너 관리](images/fig-3-5.png)
*그림 3-5: kubelet의 컨테이너 관리*

> **kubelet** 은 컨트롤 플레인으로부터 명령을 받아 실제로 컨테이너를 관리하는 관리자입니다.

쿠버네티스가 무엇이고, 어떻게 동작하는지 알아보았습니다. 이제 직접 실행해 볼 차례입니다. 다만 실제 쿠버네티스 환경을 로컬 PC에서 구현하기는 어렵기 때문에, 로컬 PC 한 대에서도 쿠버네티스를 체험할 수 있는 **미니큐브(Minikube)** 를 먼저 설치해보겠습니다. 미니큐브는 말하자면 **미니 항구**, 학습용으로 딱 좋은 작은 항구입니다.

---

## 3.2 Minikube : 로컬 K8s 환경

### 3.2.1 Minikube : 로컬에서 K8s를 실행하다

> **미니큐브(Minikube)** 는 Mini + Kubernetes라는 의미로, 로컬 PC에서 쿠버네티스 환경을 손쉽게 구성할 수 있도록 해주는 개발용 프로그램입니다. Docker 컨테이너, VirtualBox 가상 머신 등을 사용해 미니큐브 환경을 구성할 수 있습니다.

기본 구조는 쿠버네티스와 동일하지만, 개발 환경용이기 때문에 하나의 노드에 컨트롤 플레인과 워커 노드의 기능이 모여 있습니다.

![미니큐브의 단일 노드 구조](images/fig-3-6.png)
*그림 3-6: 미니큐브의 단일 노드 구조*

단일 노드로 구성되기 때문에 구조가 단순하고, 필요한 리소스도 적어 로컬 PC에서 손쉽게 활용할 수 있습니다. 다만 로드 밸런싱이나 오토 스케일링 같은 기능은 쓸 수 없습니다.

미니큐브를 쓰는 이유가 있습니다. 미니큐브에서 애플리케이션이 정상적으로 동작한다면, 동일한 설정과 구조를 그대로 실제 쿠버네티스 환경에도 적용할 수 있기 때문입니다.

> 3.2부터 3.7까지 작성하는 `YAML(yml)` 파일은 https://github.com/metacoding-10-linux-docker/docker/tree/master/yaml 에서 확인할 수 있습니다.

### 3.2.2 Minikube : 기본 명령어

#### 미니큐브 설치

**[실습]** OS에 맞는 패키지 관리자를 사용하여 미니큐브를 설치합니다.
```bash
# Windows (터미널을 관리자 권한으로 실행)
choco install minikube

# Mac (터미널에서 실행)
brew install minikube
```

Windows는 `Chocolatey`, Mac은 `Homebrew` 패키지 관리자가 설치되어 있어야 동작하니 참고합니다.

#### 미니큐브 실행

**[실습]** 미니큐브를 실행합니다.
```bash
minikube start                    # Minikube 클러스터 시작
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

### 3.2.3 kubectl : 기본 명령어

> **kubectl** 은 쿠버네티스 내부의 클러스터 리소스를 관리하는 명령어입니다.

#### Pod을 명령어로 생성하는 방법

> **Pod** 는 쿠버네티스에서 컨테이너를 실행하는 가장 작은 단위입니다. Pod는 하나 이상의 컨테이너로 구성되어 있습니다.

`kubectl run` 명령어를 사용하면 `Pod`를 손쉽게 생성할 수 있습니다. `kubectl run <pod명> --image=<이미지명>` 형태로 작성합니다.

**[참고]** `hello-pod1` Pod를 생성하는 명령어입니다.
```bash
kubectl run hello-pod1 --image=nginx    # nginx 이미지로 Pod 생성
```

#### Pod을 yml 파일로 생성하는 방법

yml 파일에 스크립트를 작성해서 `Pod`를 생성할 수도 있습니다. hello-pod2.yml은 nginx:1.20 이미지를 사용하는 단일 `Pod`를 정의합니다.

**[참고]** Github 프로젝트의 `yaml/hello-pod2.yml`을 참고합니다.

**yaml/hello-pod2.yml**
```yaml
apiVersion: v1
kind: Pod                 # 리소스 종류
metadata:
  name: hello-pod2        # 리소스명
spec:
  containers:
    - name: hello-container
      image: nginx:1.20        # 이미지
```

![실행 결과](images/chap03-20.png)
*그림 3-8: hello-pod2.yml 작성*

**[실습]** 터미널 창을 **yml 파일이 위치한 폴더**로 이동 후 아래 명령어를 실행하면 `Pod`가 생성됩니다.
```bash
kubectl apply -f hello-pod2.yml         # YAML 파일로 Pod 생성
```

![실행 결과](images/chap03-21.png)
*그림 3-9: kubectl apply로 Pod 생성*

#### Pod 조회

**[실습]** 생성된 `Pod` 목록을 조회합니다.
```bash
kubectl get pod                         # Pod 목록 조회
```

![실행 결과](images/chap03-22.png)
*그림 3-10: Pod 목록 조회*

`kubectl describe pod <Pod이름>` 명령어로 Pod의 상세 정보도 조회할 수 있습니다.

![실행 결과](images/chap03-25.png)
*그림 3-11: Pod 상세 조회*

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

미니큐브를 설치하고 기본적인 kubectl 명령어로 Pod을 생성해봤습니다. 그런데 Pod을 직접 만들면 한 가지 걱정이 생깁니다. "이 Pod이 죽으면 누가 살려주지?" 다음에는 이 문제를 해결하는 Deployment를 알아보겠습니다.

## 3.3 Pod, Deployment, ReplicaSet : 컨테이너 실행 단위

### 3.3.1 Pod와 Deployment : 컨테이너를 띄우다

이전에 `kubectl run` 명령어로 `Pod`를 생성하는 방법을 배웠습니다. 그런데 `Pod`를 직접 생성하면 한 가지 문제가 있습니다. `Pod`가 오류로 종료되었을 때 아무도 다시 살려주지 않습니다.

이 문제를 해결해주는 게 `Deployment`입니다. `Deployment`는 **"이 앱을 3개 유지하고, 문제 생기면 자동 교체하라"** 는 지침서와 같습니다.

> **Deployment** 는 Pod을 자동으로 생성, 업데이트, 복구하는 관리 리소스입니다. Pod의 개수, 버전, 장애 여부를 지정된 상태에 맞게 자동으로 관리합니다.

**[실습]** `kubectl run`으로 직접 생성한 `Pod`와 `Deployment`를 통해 생성한 `Pod`의 차이를 확인합니다. 먼저 비교를 위해 `Pod`를 하나 직접 생성합니다.
```bash
kubectl run nginx-pod --image=nginx     # nginx Pod 생성
```

deploy-ex01.yml은 nginx:1.20 이미지를 사용하는 `Deployment`를 정의하며, replicas: 1로 `Pod` 1개를 생성합니다.

**[참고]** Github 프로젝트의 `yaml/deploy-ex01.yml`을 참고합니다.

**yaml/deploy-ex01.yml**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deploy
spec:                    # pod에 대한 상태 지정
  replicas: 1            # 생성할 pod 수 지정
  selector:
    matchLabels:
      app: nginx         # 라벨이 app : nginx인 pod를 관리
  template:
    metadata:
      labels:
        app: nginx       # pod에 붙일 라벨
    spec:
      containers:
        - name: nginx-container
          image: nginx:1.20
```

> **Selector** 는 특정 label을 가진 리소스를 선택하기 위한 조건입니다. Deployment나 Service와 같은 리소스의 Selector와 Pod의 labels가 일치하는 Pod를 찾아 관리합니다.

<!-- image-prompt: Minimal black line drawing on white background, very few details, icon-like simplicity, 4:3 aspect ratio, 800x600px. with Korean labels: Diagram showing Kubernetes Deployment 셀렉터 (selector) matching with Pod 라벨 (labels), connected by a dotted arrow labeled 매칭 (match), illustrating how 셀렉터 find their target Pods. -->
![Selector와 Labels의 매칭 관계](images/fig-3-8.png)
*그림 3-12: Selector와 Labels의 매칭 관계*

**[실습]** `Deployment`를 생성하고 `Pod`를 확인합니다.
```bash
kubectl apply -f deploy-ex01.yml        # 디플로이먼트 생성
kubectl get pod                         # Pod 목록 조회
```

![실행 결과](images/chap03-28.png)
*그림 3-13: Deployment와 Pod 생성 확인*

**[실습]** 전체 `Pod`를 삭제한 뒤 다시 조회합니다.
```bash
kubectl delete pod --all                # 모든 Pod 삭제
kubectl get pod                         # Pod 재생성 확인
```

![실행 결과](images/chap03-30.png)
*그림 3-14: Pod 삭제 후 자동 재생성 확인*

결과가 보입니까? `kubectl run`으로 직접 생성한 `Pod`는 종료되었지만, `Deployment`를 통해 생성된 `Pod`는 자동으로 재시작되었습니다.

`Deployment`로 `Pod`를 생성하면 `Pod` 생성뿐만 아니라, `Pod`의 개수 유지와 장애 복구까지 자동으로 이루어집니다. 그래서 `Pod`는 직접 생성하기보다 `Deployment`를 통해 생성하는 것이 일반적입니다.

### 3.3.2 ReplicaSet : Pod 개수를 유지하다

만약 서비스에 트래픽이 몰려서 `Pod` 하나로는 감당이 안 된다면 어떻게 해야 할까요? 이번에는 `Pod`의 개수를 원하는 만큼 유지하고, 업데이트할 때도 서비스 중단 없이 교체하는 방법을 알아보겠습니다.

일반적으로 `ReplicaSet`은 `Deployment`가 자동으로 관리합니다. 에어컨을 24도로 설정하면 온도가 올라갈 때 냉방을 켜고, 내려가면 멈추는 것처럼, `ReplicaSet`도 현재 `Pod` 수가 설정과 다르면 자동으로 맞추는 역할을 합니다.

> **ReplicaSet** 은 지정한 개수만큼 Pod이 항상 살아있도록 관리하는 컨트롤러입니다. Pod이 죽거나 예상보다 많아지는 상황이 발생하면 원래 설정된 수에 맞게 Pod을 자동으로 생성하거나 제거하여 상태를 일정하게 유지합니다.

<!-- image-prompt: Minimal black line drawing on white background, very few details, icon-like simplicity, 4:3 aspect ratio, 800x600px. with Korean labels: Diagram showing a ReplicaSet maintaining three Pods (Pod 3개 유지), with one Pod 종료 (terminating) and a new Pod 자동 생성 (automatically being created) to maintain the 설정된 개수 (desired count), illustrating 자동 복구 (self-healing) behavior. -->
![실행 결과](images/chap03-31.png)
*그림 3-15: ReplicaSet의 Pod 개수 유지*

deploy-ex02.yml은 replicas를 4개로 설정하고 RollingUpdate 전략을 적용한 `Deployment`입니다.

**[참고]** Github 프로젝트의 `yaml/deploy-ex02.yml`을 참고합니다.

**yaml/deploy-ex02.yml**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-replica
spec:
  replicas: 4            # pod 수 지정

  strategy:              # Pod 교체 방식 설정
    type: RollingUpdate  # 롤링 업데이트 전략
    rollingUpdate:
      maxSurge: 4        # 업데이트 중 최대 4개까지 추가 생성
      maxUnavailable: 4  # 업데이트 중 최대 4개까지 종료 허용

  selector:              # 라벨이 app: nginx 인 pod를 관리
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx       # pod에 붙일 라벨
    spec:
      containers:
        - name: nginx-container
          image: nginx:1.20
```

**[실습]** `Deployment`를 생성하고 `Pod` 개수를 확인합니다.
```bash
kubectl apply -f deploy-ex02.yml        # 레플리카 디플로이먼트 생성
kubectl get pod                         # Pod 목록 조회
```

![실행 결과](images/chap03-32.png)
*그림 3-16: replicas 설정으로 Pod 4개 생성*

`Deployment`에 설정한 `replicas`의 수에 따라 `Pod`가 4개 생성된 걸 확인할 수 있습니다.

### 3.3.3 RollingUpdate : 무중단 배포

deploy-ex02.yml을 보면 `strategy`라는 설정이 포함되어 있습니다. `strategy`는 새 버전을 배포할 때 기존 `Pod`을 어떤 방식으로 교체할지 정의하는 설정입니다.

> **롤링 업데이트(RollingUpdate)** 는 기존 Pod을 한 번에 교체하지 않고, Pod을 점진적으로 교체하는 무중단 배포 방식입니다.

**[실습]** nginx 이미지를 1.21 버전으로 업데이트합니다.
```bash
kubectl set image deployment/nginx-replica nginx-container=nginx:1.21    # 이미지 버전 변경 (롤링 업데이트)
```

![실행 결과](images/chap03-33.png)
*그림 3-17: 이미지 버전 업데이트 실행*

**[실습]** 업데이트 진행 상황을 실시간으로 확인합니다.
```bash
kubectl get pods -w                     # Pod 상태 실시간 감시
```

![실행 결과](images/chap03-34.png)
*그림 3-18: 롤링 업데이트 진행 상황*

새 Pod는 `ContainerCreating(생성 중)` -> `Running(실행)` 순으로 올라오고, 기존 Pod는 `Terminating(종료 중)` 상태를 거쳐 삭제됩니다.

deploy-ex02.yml에 설정한 maxSurge와 maxUnavailable 값에 따라, 업데이트 과정에서 새로운 `Pod` 4개가 한 번에 생성되고 기존 `Pod` 또한 동시에 종료되었습니다. 이 설정을 조절하면 원하는 방식으로 업데이트를 진행할 수 있습니다.

**[실습]** `Deployment`의 상세 정보를 확인하면 1.21 버전으로 변경된 것을 확인할 수 있습니다.
```bash
kubectl describe deployment nginx-replica    # 디플로이먼트 상세 정보 조회
```

### 3.3.4 Rollback : 이전 버전으로 되돌리다

**[실습]** `Deployment`를 이전 상태로 롤백합니다.
```bash
kubectl rollout undo deployment/nginx-replica    # 이전 버전으로 롤백
```

![실행 결과](images/chap03-36.png)
*그림 3-19: Rollback 실행 결과*

`kubectl describe` 명령어로 원복된 이미지 버전을 확인할 수 있습니다.

Pod을 생성하고, 개수를 유지하고, 업데이트까지 자동으로 처리하는 방법을 배웠습니다. 그런데 한 가지 문제가 남았습니다. Pod이 재시작될 때마다 IP가 바뀌면, 외부에서 어떻게 접근할 수 있을까요? 다음에는 이 문제를 해결하는 Service를 알아보겠습니다.

## 3.4 Service : Pod에 고정 주소를 부여하다

### 3.4.1 Service : 왜 필요한가

이전에 `Deployment`를 통해 `Pod`를 생성하면 자동으로 관리된다는 것을 배웠습니다. 하지만 재시작될 때마다 IP가 바뀌기 때문에 외부에서 직접 접근하기가 어렵습니다. 이 문제를 해결해주는 게 `Service`입니다. 대표 전화번호처럼, 직원이 바뀌어도 같은 번호로 항상 연결할 수 있습니다.

> **Service** 는 외부에서 Pod에 접근할 때, 고정 IP를 만들어 안정적으로 접근할 수 있게 만들어주는 리소스입니다.

#### Pod IP 변경

**[실습]** `Pod`의 IP는 재시작 시 변경됩니다. IP를 확인한 후 `Pod`를 삭제하고 다시 조회하면 IP가 달라진 것을 확인할 수 있습니다.
```bash
kubectl get pod -o wide           # IP 확인 (예: 10.244.0.7)
kubectl delete pod --all              # 모든 Pod 삭제
kubectl get pod -o wide           # IP 변경됨 (예: 10.244.0.8)
```

이 문제를 해결하기 위해 `Service`를 생성해보겠습니다. `Service`는 `Deployment`와 마찬가지로 selector의 라벨이 일치하는 `Pod`를 관리합니다.

#### Service 생성

service-ex01.yml은 `NodePort` 타입의 `Service`를 정의하며, 외부에서 30080 포트로 접속할 수 있도록 설정합니다.

**[참고]** Github 프로젝트의 `yaml/service-ex01.yml`을 참고합니다.

**yaml/service-ex01.yml**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  type: NodePort        # 클러스터가 외부에서 접근할 수 있도록 노드를 열어줌
  selector:
    app: nginx
  ports:
  - protocol: TCP
    port: 80            # 서비스가 클러스터 내부에서 열어둔 포트
    targetPort: 80      # pod가 열어둔 포트
    nodePort: 30080     # 외부에서 접속할 포트 지정
```

**[실습]** `Service`를 생성합니다.
```bash
kubectl apply -f service-ex01.yml       # 서비스 생성
```

**[실습]** `Pod`를 재시작하고 `Service` IP가 유지되는지 확인합니다.
```bash
kubectl delete pod --all                # 모든 Pod 삭제
kubectl get pod,service -o wide         # Pod과 서비스 상세 조회
```

![실행 결과](images/chap03-41.png)
*그림 3-20: Pod 재시작 후 Service IP 유지 확인*

`Pod`의 IP는 재시작마다 바뀌지만, `Service`의 IP는 변하지 않고 동일하게 유지됩니다.

#### Service 타입 비교

| 타입 | 설명 | 접근 범위 |
|------|------|----------|
| ClusterIP | 클러스터 내부에서만 접근 가능한 기본 타입 | 내부 전용 |
| NodePort | 노드의 특정 포트(30000~32767)를 통해 외부에서 접근 가능 | 외부 접근 가능 |
| LoadBalancer | 클라우드 환경에서 외부 로드밸런서를 자동 생성 | 외부 접근 가능 (클라우드) |

이번 실습에서는 외부에서 접근해야 하므로 NodePort를 사용했습니다. 만약 ClusterIP로 설정하면 클러스터 내부의 다른 Pod에서만 접근할 수 있고, 브라우저에서는 접근할 수 없습니다.

### 3.4.2 Networking : 서비스 간 통신

로컬 PC와 미니큐브는 서로 다른 네트워크에 있기 때문에, Service의 IP로 직접 접근할 수 없습니다. `minikube service` 명령어를 사용하면 임시 접근 경로가 생성됩니다.

> **minikube service** 명령어는 특정 Service에 대해 임시 접근 경로를 생성하여, 로컬 PC에서 해당 Service에 바로 접속할 수 있도록 해줍니다.

**[실습]** 로컬 PC에서 `Service`에 접속할 수 있는 URL을 생성합니다.
```bash
minikube service nginx-service --url    # 서비스 외부 접근 URL 확인
```

![실행 결과](images/chap03-43.png)
*그림 3-21: minikube service URL 생성*

생성된 URL로 접속하면, 미니큐브 내부의 `Service`를 통해 해당 `Pod` 서버로 요청이 전달됩니다.

![실행 결과](images/chap03-44.png)
*그림 3-22: 브라우저에서 nginx 접속 확인*

확인 후 `CTRL + C`를 입력해 터미널을 빠져나옵니다.

**[실습]** 실습이 끝난 후 `Deployment`를 삭제합니다.
```bash
kubectl delete deployment nginx-deploy  # 디플로이먼트 삭제
```

Service 덕분에 Pod의 IP가 바뀌어도 안정적으로 접근할 수 있게 되었습니다. 다만 실제 서비스를 운영하려면 데이터베이스 주소, API 키, 비밀번호 같은 설정 값이 필요합니다. 이런 값을 코드에 직접 넣으면 변경할 때마다 이미지를 다시 빌드해야 합니다. 다음에는 이 문제를 해결하는 ConfigMap과 Secret을 알아보겠습니다.

## 3.5 ConfigMap, Secret : 설정과 비밀 정보 관리

### 3.5.1 ConfigMap : 일반 환경변수 주입

이전에 언급한 것처럼 설정 값을 코드에 직접 넣으면 변경할 때마다 이미지를 다시 빌드해야 합니다. 쿠버네티스는 이 문제를 ConfigMap과 Secret으로 해결합니다.

ConfigMap은 환경 설정표와 같습니다. 코드와 설정을 분리해서, 설정이 바뀌어도 코드를 건드릴 필요가 없게 만드는 것입니다.

> **ConfigMap** 은 일반적인 설정 값을 외부에서 관리하는 리소스입니다. 환경 변수, 설정 파일 등 민감하지 않은 설정 정보를 저장하며, Pod는 이를 환경변수로 전달받아 사용합니다.

**[참고]** Github 프로젝트의 `yaml/configmap-conn.yml`을 참고합니다.

**yaml/configmap-conn.yml**
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: configmap-conn               # ConfigMap 이름 지정
data:                                # 설정값 넣는 영역
  conn_info: "localhost:80"
  conn_url: "config.test"
```

deploy-ex03.yml에서는 `envFrom.configMapRef`를 사용하여 `ConfigMap`에 정의된 모든 설정 값을 환경 변수 형태로 `Pod`에서 사용할 수 있습니다.

**[참고]** Github 프로젝트의 `yaml/deploy-ex03.yml`을 참고합니다.

**yaml/deploy-ex03.yml**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-config-secret
spec:
  replicas: 1                              # pod 수 지정
  selector:
    matchLabels:
      app: nginx                           # 라벨이 app : nginx인 pod를 관리
  template:
    metadata:
      labels:
        app: nginx                          # pod에 붙일 라벨
    spec:
      containers:
        - name: nginx-container
          image: nginx:1.20
          envFrom:
            - configMapRef:
                name: configmap-conn         # ConfigMap 연결
```

**[실습]** `ConfigMap`과 `Deployment`를 생성합니다.
```bash
kubectl apply -f configmap-conn.yml     # ConfigMap 생성
kubectl apply -f deploy-ex03.yml        # 디플로이먼트 생성
```

**[실습]** `Pod`의 환경 변수를 조회하여 `ConfigMap` 설정이 적용되었는지 확인합니다.
```bash
kubectl get pod                         # Pod 목록 조회
kubectl exec -it nginx-config-secret-5898f5c7f-nn2rh -- env    # Pod 내부 환경변수 확인
```

![실행 결과](images/chap03-46.png)
*그림 3-23: Pod 환경 변수 조회*

여러 개의 환경 변수 중 `ConfigMap`에 설정한 `conn_info`와 `conn_url`이 잘 들어가 있습니다.

### 3.5.2 Secret : 민감한 정보 관리

ConfigMap이 환경 설정표라면, Secret은 **금고**입니다. 비밀번호나 API 키처럼 민감한 정보는 설정표에 적어두면 안 됩니다. 금고에 따로 보관해야 합니다.

> **Secret** 은 비밀번호, 토큰, 인증 키처럼 민감한 정보를 안전하게 저장하고 관리하기 위한 리소스입니다. ConfigMap과 구조는 비슷하지만, Secret의 값은 Base64로 인코딩되어 저장됩니다. 단, Base64는 암호화가 아닌 단순 인코딩이므로 보안을 보장하지는 않습니다. Secret은 평문이 설정 파일에 직접 노출되는 것을 방지하는 수준이며, 실제 운영 환경에서는 별도의 암호화 솔루션을 사용해야 합니다.

**[참고]** Github 프로젝트의 `yaml/secret-password.yml`을 참고합니다.

**yaml/secret-password.yml**
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: secret-password
type: Opaque                # key-value 형태의 secret 타입
stringData:                 # 평문을 자동으로 Base64 변환
  password: metacoding1234
```

**[실습]** `Secret`을 생성합니다. stringData 속성을 사용하면 평문을 자동으로 Base64로 변환해줍니다.
```bash
kubectl apply -f secret-password.yml    # Secret 생성
```

**[실습]** `Secret`의 내부를 YML 형태로 출력합니다.
```bash
kubectl get secret secret-password -o yaml    # Secret 상세 조회
```

![실행 결과](images/chap03-48.png)
*그림 3-24: Secret의 Base64 인코딩 확인*

`Secret`을 YML 형태로 출력해보면, 환경 변수로 설정한 비밀번호가 Base64로 인코딩되어 있는 걸 확인할 수 있습니다.

### 3.5.3 envFrom : 환경 변수 주입

deploy-ex03.yml에 `Secret`을 추가해보겠습니다. `secretRef`를 사용하면 `Secret`에 정의된 값을 환경 변수로 `Pod`에서 불러올 수 있습니다.

3.5.1에서 작성한 deploy-ex03.yml의 `envFrom` 항목에 `secretRef`를 추가합니다. 아래는 추가된 부분만 표시한 것입니다.

**[참고]** Github 프로젝트의 `yaml/deploy-ex03.yml`에서 `envFrom` 항목을 참고합니다.

**yaml/deploy-ex03.yml**
```yaml
          envFrom:
            - configMapRef:
                name: configmap-conn         # ConfigMap 연결
            - secretRef:
                name: secret-password        # Secret 연결 (추가)
```

**[실습]** 변경된 `Deployment`를 적용합니다. yml 파일 내부의 `template` 속성이 변경되면 `kubectl apply -f`를 통해 적용할 수 있습니다.
```bash
kubectl apply -f deploy-ex03.yml        # 디플로이먼트 재생성
```

**[실습]** `Pod`의 환경 변수를 조회하면 `Secret`에 저장된 비밀번호가 주입되어 출력됩니다.
```bash
kubectl exec -it nginx-config-secret-7fbccb65f5-z8c9r -- env    # Pod 내부 환경변수 확인
```

![실행 결과](images/chap03-50.png)
*그림 3-25: Pod 환경 변수에 Secret 값 확인*

여기서 주목할 점이 있습니다. `Secret`에 Base64로 인코딩되어 저장된 비밀번호가, `Pod`에서 사용할 때는 자동으로 평문 형태로 변경됩니다.

### 3.5.4 ConfigMap : 수정과 반영

`ConfigMap`이나 `Secret`에서 환경 변수 값을 변경한 후, `kubectl apply -f 파일명`을 실행해 변경 내용을 `Kube API Server`에 저장합니다. 그런데 저장된 환경 변수가 실행 중인 `Pod`에 즉시 반영될까요? 아닙니다, 반영되지 않습니다.

`Pod`나 `Deployment`는 설정이 바뀌었다고 알아서 감지하지 않고, `Kube API Server`도 변경된 설정을 기존 `Pod`에 강제로 주입하지 않기 때문입니다.

![ConfigMap 변경 후 Pod 재시작으로 반영되는 흐름](images/fig-3-26.png)
*그림 3-26: ConfigMap 변경 후 Pod 재시작으로 반영되는 흐름*

환경 변수 같은 실행 환경 설정은 프로세스가 시작될 때만 적용되고, 실행 중에는 변경할 수 없습니다. 따라서 변경된 설정을 반영하려면 **Pod를 재시작**해야 합니다.

실습을 위해 configmap-conn.yml의 `conn_info` 포트를 90으로 수정해보겠습니다.

**[참고]** Github 프로젝트의 `yaml/configmap-conn.yml`에서 포트 수정 내용을 참고합니다.

**yaml/configmap-conn.yml**
```yaml
# ... 생략
  conn_info: "localhost:90"          # 수정
```

**[실습]** 변경된 `ConfigMap`을 적용하고 `Pod`를 재시작합니다.
```bash
kubectl apply -f configmap-conn.yml     # ConfigMap 수정 적용
kubectl rollout restart deployment nginx-config-secret    # 디플로이먼트 재시작
```

![실행 결과](images/chap03-52.png)
*그림 3-27: ConfigMap 수정 후 Pod 재시작*

**[실습]** 재시작된 `Pod`의 환경 변수를 확인합니다.
```bash
kubectl exec -it nginx-config-secret-66df86b69d-bdzck -- env    # 변경된 환경변수 확인
```

![실행 결과](images/chap03-53.png)
*그림 3-28: 변경된 환경 변수 확인*

`conn_info` 변수의 포트가 90으로 잘 변경된 것을 확인할 수 있습니다.

ConfigMap과 Secret으로 설정과 민감 정보를 외부에서 관리하는 방법을 배웠습니다. 이제 한 가지 더 생각해볼 문제가 있습니다. Pod이 재시작되면 내부에 저장된 데이터는 모두 사라집니다. 데이터베이스처럼 데이터를 영구적으로 보존해야 하는 경우에는 어떻게 해야 할까요? 다음에는 Volume을 알아보겠습니다.

## 3.6 Volume : 데이터를 영속적으로 저장하다

### 3.6.1 emptyDir : Pod 내 임시 공유 저장소

이전에 예고한 대로 `Pod`가 재시작되면 내부 데이터는 모두 사라집니다. 이번에는 이 문제를 해결하는 외부 저장 공간인 `Volume`을 알아보겠습니다.

> **볼륨(Volume)** 은 Pod 내부 컨테이너가 사용할 수 있는 외부 저장 공간을 의미합니다.

이번에는 `Volume`의 몇 가지 종류를 알아보겠습니다.

> **emptyDir** 는 Pod가 생성될 때 함께 만들어지는 임시 저장 공간입니다. 컨테이너가 재실행되면 데이터가 유지되지만, Pod이 재실행되면 데이터가 삭제됩니다.

`Pod`가 삭제되면 `emptyDir`도 함께 제거되니까, 지속 보관이 필요 없는 임시 데이터나 컨테이너 간 공유해야 하는 휘발성 데이터를 저장하는 용도로 사용합니다.

**[참고]** Github 프로젝트의 `yaml/emptydir-pod.yml`을 참고합니다.

**yaml/emptydir-pod.yml**
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: emptydir-pod
spec:
  containers:
  - name: nginx-empty
    image: nginx
    volumeMounts:
    - name: cache         # 사용할 볼륨명
      mountPath: /cache   # 볼륨 저장 경로
  volumes:
  - name: cache           # 볼륨명
    emptyDir: {}          # emptyDir 타입
```

**[실습]** `Pod`를 생성하고 내부에 접속하여 루트(`/`)와 `/cache` 경로에 파일을 각각 생성합니다.
```bash
kubectl apply -f emptydir-pod.yml       # EmptyDir Pod 생성
kubectl exec -it emptydir-pod -- /bin/bash    # Pod 내부 접속
touch a.txt           # 루트(/) 경로에 파일 생성
touch /cache/b.txt    # emptyDir 경로에 파일 생성
```

**[실습]** 컨테이너의 메인 프로세스를 종료합니다. 컨테이너가 종료되면 `Pod`이 자동으로 재실행합니다.
```bash
kill 1                                  # 메인 프로세스 종료 (컨테이너 재시작 유도)
```

**[실습]** 다시 접속하여 파일 유지 여부를 확인합니다.
```bash
kubectl exec -it emptydir-pod -- /bin/bash    # 재시작된 Pod 내부 접속
ls            # a.txt 사라짐
ls /cache     # b.txt 유지됨
```

![실행 결과](images/chap03-57.png)
*그림 3-29: 컨테이너 재시작 후 파일 유지 확인*

컨테이너 재실행 시 루트(`/`)의 a.txt는 사라졌지만, `emptyDir`로 지정된 `/cache`의 b.txt는 유지됩니다.

### 3.6.2 PV, PVC : 영구 저장소

Persistent storage는 `PV`(PersistentVolume)와 `PVC`(PersistentVolumeClaim)로 구성되어 있습니다.

> **Persistent storage** 는 클러스터 외부에 데이터를 저장해, Pod이 종료되어도 데이터가 유지되는 영구 저장소입니다.

#### PV(PersistentVolume)

`PV`는 **창고** 공간이고, `PVC`는 **"10평짜리 창고가 필요합니다"라는 창고 신청서**입니다. 먼저 창고 공간에 해당하는 `PV`를 만들어 보겠습니다.

> **PV(PersistentVolume)** 는 실제 데이터가 저장되는 저장소입니다.

**[참고]** Github 프로젝트의 `yaml/volume-pv.yml`을 참고합니다.

**yaml/volume-pv.yml**
```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: volume-pv
spec:
  capacity:
    storage: 1Gi           # 1Gi 용량 할당
  accessModes:
    - ReadWriteOnce        # 읽기/쓰기 권한
  storageClassName: ""     # PVC가 볼륨을 자동으로 생성 못하게 방지
  hostPath:
    path: /mnt/data        # 볼륨 경로 지정
```

`PV`는 클라우드, NAS 등 다양한 저장소에 데이터를 저장할 수 있습니다. 이번에는 로컬 PC의 폴더를 저장소로 사용해보겠습니다.

먼저 데이터를 저장할 경로에 폴더를 생성합니다.

![실행 결과](images/chap03-58.png)
*그림 3-30: 로컬 PC에 볼륨 폴더 생성*

**[실습]** 로컬 PC의 `C:\volume` 경로와 미니큐브의 `/mnt/data` 경로를 마운트합니다. 이 명령어는 포그라운드로 실행되어 터미널을 점유하므로, 이후 명령어는 **새로운 터미널 창**에서 실행해야 합니다.
```bash
minikube mount "C:\volume:/mnt/data"   # Mac의 경우: minikube mount "$HOME/volume:/mnt/data"
```

![실행 결과](images/chap03-59.png)
*그림 3-31: minikube mount 실행*

터미널 창이 종료되면 로컬 PC와의 마운트도 함께 종료되기 때문에, 마운트가 필요한 동안은 이 터미널 창을 닫지 않아야 합니다.

#### PVC(PersistentVolumeClaim)

> **PVC(PersistentVolumeClaim)** 는 Pod이 사용할 저장소에 대한 정보가 담겨있습니다. Pod은 PVC를 통해 조건에 맞는 PV를 연결합니다.

**[참고]** Github 프로젝트의 `yaml/volume-pvc.yml`을 참고합니다.

**yaml/volume-pvc.yml**
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: volume-pvc         # pod가 참조하는 pvc명
spec:
  accessModes:
    - ReadWriteOnce        # 읽기 쓰기 권한
  storageClassName: ""     # PVC가 자동으로 PV 생성하지 않도록 설정
  resources:
    requests:
      storage: 1Gi         # 용량
  volumeName: volume-pv    # 참조할 PV명
```

`PVC`가 `PV`와 정상적으로 바인딩되려면 `accessModes`와 `storageClassName` 설정이 서로 일치해야 하고, `PVC`에서 요청한 용량이 `PV`가 제공하는 용량보다 작거나 같아야 합니다.

**[참고]** Github 프로젝트의 `yaml/volume-pod.yml`을 참고합니다.

**yaml/volume-pod.yml**
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: volume-pod
spec:
  containers:
  - name: nginx-volume
    image: nginx
    volumeMounts:               # 사용할 볼륨 마운트
    - name: storage
      mountPath: /mnt/data      # 컨테이너에서 접근할 볼륨 위치
  volumes:
  - name: storage
    persistentVolumeClaim:
      claimName: volume-pvc      # 참조할 PVC
```

**[실습]** 새로운 터미널 창에서 `PV`, `PVC`, `Pod`를 순서대로 생성합니다.
```bash
kubectl apply -f volume-pv.yml          # PersistentVolume 생성
kubectl apply -f volume-pvc.yml         # PersistentVolumeClaim 생성
kubectl apply -f volume-pod.yml         # 볼륨 연결된 Pod 생성
```

**[실습]** `PV`와 `PVC`의 바인딩 상태를 확인합니다. `STATUS` 값이 **BOUND**이면 정상입니다.
```bash
kubectl get pv,pvc -o wide              # PV, PVC 상태 조회
```

![실행 결과](images/chap03-60.png)
*그림 3-32: PV와 PVC 바인딩 상태 확인*

**[실습]** 컨테이너 내부에 접속하여 `/mnt/data` 경로에 파일을 생성합니다.
```bash
kubectl exec -it volume-pod -- /bin/bash    # Pod 내부 접속
touch /mnt/data/c.txt
ls /mnt/data
```

![실행 결과](images/chap03-61.png)
*그림 3-33: 볼륨 경로에 파일 생성*

`/mnt/data` 경로에 파일이 정상적으로 생성되었습니다.

그리고 연결된 로컬 PC에도 파일이 생성된 걸 확인할 수 있습니다.

![실행 결과](images/chap03-62.png)
*그림 3-34: 로컬 PC에서 마운트된 파일 확인*

정리하면 다음과 같습니다.

- **인프라 운영자**는 PV(실제 스토리지 자원)를 생성하고 관리합니다.
- **개발자**는 PVC(스토리지 사용 요청)를 정의하여 필요한 저장 공간을 요청합니다.
- **Pod**는 애플리케이션이 실제로 실행되는 실행 단위입니다.
- **PVC**는 Pod가 사용할 스토리지를 요청하는 요청서입니다.
- **PV**는 그 요청에 의해 연결되는 실제 스토리지 자원입니다.

## 3.7 종합 실습 : Minikube로 웹 사이트 배포

여기까지 쿠버네티스의 핵심 리소스를 하나씩 배워왔습니다. 마지막으로 챕터 2의 예제를 종합해 미니큐브 위에서 실행해보겠습니다.

> 실습 코드는 https://github.com/metacoding-10-linux-docker/docker/tree/master/ex08 에서 확인할 수 있습니다.

### 3.7.1 아키텍처

이번 실습에서 배포할 애플리케이션의 전체 구조는 다음과 같습니다. 프론트엔드(Nginx), 백엔드(Spring Boot), DB(MySQL), Redis 총 4개의 서비스로 구성됩니다.

![ex08 풀스택 Kubernetes 아키텍처](images/fig-3-35.png)
*그림 3-35: ex08 풀스택 Kubernetes 아키텍처*

### 3.7.2 Docker : 이미지 빌드

**[EX08 패키지 구조]**

```
ex08/
├── backend/             # 백엔드 서버 (Spring Boot)
│   ├── Dockerfile
│   └── entrypoint.sh   # Git clone + 빌드 + 실행 스크립트
├── db/                  # MySQL 데이터베이스
│   ├── Dockerfile
│   └── init.sql         # 초기 테이블 및 데이터 생성 SQL
├── frontend/            # 프론트엔드 (NGINX)
│   ├── Dockerfile
│   ├── index.html       # 화면 페이지
│   └── nginx.conf       # 정적 파일 제공 + API 프록시 설정
├── redis/               # Redis 세션 저장소
│   └── Dockerfile
└── k8s/                 # Kubernetes 매니페스트 폴더
```

EX08 폴더 내에는 이미지 생성을 위한 backend, db, frontend, redis 폴더가 있고, 이를 쿠버네티스 환경에서 실행하기 위한 k8s 폴더가 있습니다.

> Backend, DB, Frontend, Redis 폴더는 EX07과 동일한 구조를 사용합니다. 설명이 필요한 부분만 코드로 표시하겠습니다.

우선 Redis를 추가하기 위해 Dockerfile을 작성해보겠습니다.

**[참고]** Github 프로젝트의 `ex08/redis/Dockerfile`을 참고합니다.

**ex08/redis/Dockerfile**
```dockerfile
FROM redis:7.4-alpine

CMD ["redis-server"]
```

그리고 backend 폴더의 entrypoint.sh에서 `Git clone` 되는 주소를 수정합니다.

**[참고]** Github 프로젝트의 `ex08/backend/entrypoint.sh`를 참고합니다.

**ex08/backend/entrypoint.sh**
```bash
#!/bin/bash
# 백엔드 서버 Github에서 내려받기 (Redis 버전으로 수정)
git clone https://github.com/metacoding-10-linux-docker/backend-redis-server
# 내려받은 폴더로 이동
cd backend-redis-server
# 실행 권한 부여
chmod +x gradlew
# 스프링 프로젝트 빌드
./gradlew build
# 빌드된 파일 실행
java -jar -Dspring.profiles.active=prod build/libs/*.jar
```

수정된 백엔드 서버는 API 요청 시 회원 정보와 함께 Redis에 저장된 방문 횟수를 함께 응답합니다.

<!-- image-prompt: Minimal black line drawing on white background, very few details, icon-like simplicity, 4:3 aspect ratio, 800x600px. with Korean labels: Diagram showing the 백엔드 서버 요청 흐름 (backend server request flow): an API 요청 (request) arrives, queries MySQL for 회원 데이터 (user data) and Redis for 방문 횟수 (visit count), then returns a combined JSON 응답 (response), illustrating the 데이터 조합 패턴 (data aggregation pattern). -->
![실행 결과](images/chap03-65.png)
*그림 3-36: 수정된 백엔드 서버의 응답 구조*

프론트엔드의 index.html도 수정합니다. EX07과 비교해 방문 횟수를 표시하는 부분이 추가되었습니다.

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
      const count = data.body.count;     // Redis 방문 횟수

      users.forEach(user => {            // 응답 데이터를 테이블에 렌더링
        $("#user-list").append(render(user));
      });

      $("#visit-count").text(count);     // 방문 횟수 표시
    });
  // ... 생략
</script>
```

nginx.conf도 아래와 같이 수정합니다. upstream의 서버 주소를 Kubernetes Service명(backend-service)으로 변경합니다.

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

### 3.7.3 K8s : 매니페스트 구조

ex08 폴더 내에 k8s 폴더가 있습니다.

> **k8s 폴더** 는 Kubernetes 배포 설정 파일을 모아둔 폴더입니다.

**[k8s 패키지 구조]**

```
k8s/
├── backend/                       # 백엔드 매니페스트
│   ├── backend-configmap.yml      # 환경 설정 (DB 주소 등)
│   ├── backend-deploy.yml         # 디플로이먼트 (Pod 생성)
│   ├── backend-secret.yml         # 민감 정보 (DB 비밀번호 등)
│   └── backend-service.yml        # 서비스 (네트워크 노출)
├── db/                            # DB 매니페스트
│   ├── db-deploy.yml              # 디플로이먼트 (Pod 생성)
│   ├── db-pv.yml                  # 퍼시스턴트 볼륨 (물리 저장소)
│   ├── db-pvc.yml                 # 볼륨 클레임 (저장소 요청)
│   ├── db-secret.yml              # 민감 정보 (비밀번호 등)
│   └── db-service.yml             # 서비스 (네트워크 노출)
├── frontend/                      # 프론트엔드 매니페스트
│   ├── frontend-deploy.yml        # 디플로이먼트 (Pod 생성)
│   └── frontend-service.yml       # 서비스 (외부 접근용)
├── redis/                         # Redis 매니페스트
│   ├── redis-deploy.yml           # 디플로이먼트 (Pod 생성)
│   └── redis-service.yml          # 서비스 (네트워크 노출)
└── namespace.yml                  # 네임스페이스 (리소스 격리)
```

| 파일 | 설명 |
|------|------|
| namespace.yml | 리소스를 논리적으로 구분하는 `Namespace` 생성 |
| *-deploy.yml | 각 서버의 `Deployment` (Pod 생성 및 관리) |
| *-service.yml | 각 서버의 `Service` (고정 IP로 Pod 접근) |
| backend-configmap.yml | 백엔드 환경 변수 (DB 주소, Redis 주소) |
| backend-secret.yml | 백엔드 민감 정보 (DB 계정/비밀번호) |
| db-secret.yml | DB 민감 정보 (MySQL 계정/비밀번호) |
| db-pv.yml / db-pvc.yml | DB 데이터 영구 저장을 위한 `PV`/`PVC` |

먼저 namespace.yml 파일을 작성해보겠습니다.

> **Namespace** 는 쿠버네티스 리소스를 논리적으로 구분하고 관리하기 위한 설정입니다. 별도로 지정하지 않으면 모든 리소스는 기본적으로 `default`라는 이름으로 생성됩니다.

**[참고]** Github 프로젝트의 `ex08/k8s/namespace.yml`을 참고합니다.

**ex08/k8s/namespace.yml**
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: metacoding
```

#### backend-deploy.yml

backend-deploy.yml은 이번 실습에서 가장 많은 리소스를 조합한 설정입니다. `replicas: 2`로 `Pod`를 2개 생성하고, `envFrom`으로 `ConfigMap`과 `Secret`을 동시에 연결합니다.

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

`ConfigMap`에는 DB 주소, Redis 주소 등 일반 설정을, `Secret`에는 DB 계정/비밀번호를 저장합니다. `Service`, `ConfigMap`, `Secret` 파일은 이전에 배운 구조와 동일하므로 Github을 참고합니다.

#### db-deploy.yml

db-deploy.yml은 `volumeMounts`와 `PVC`를 연결하여 DB 데이터를 영구 저장하는 설정입니다.

**[참고]** Github 프로젝트의 `ex08/k8s/db/db-deploy.yml`을 참고합니다.

**ex08/k8s/db/db-deploy.yml**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: db-deploy
  namespace: metacoding                # namespace 설정
spec:
  replicas: 1
  selector:
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

`Secret`, `PV`, `PVC`, `Service` 파일은 이전에 배운 구조와 동일하므로 Github을 참고합니다.

#### 나머지 설정

frontend, redis의 `Deployment`와 `Service`는 backend와 동일한 구조입니다. 이미지명, 라벨, 포트만 다릅니다. 아래 표를 참고합니다. 전체 코드는 Github을 참고합니다.

| 항목 | frontend | redis |
|------|----------|-------|
| image | metacoding/frontend:1 | metacoding/redis:1 |
| containerPort | 80 | 6379 |
| replicas | 1 | 1 |
| Service port | 80 | 6379 |

> 전체 k8s 설정 파일은 https://github.com/metacoding-10-linux-docker/docker/tree/master/ex08/k8s 에서 확인할 수 있습니다.

### 3.7.4 kubectl apply : 배포 및 확인

**[실습]** 미니큐브가 실행되어 있지 않다면 먼저 미니큐브를 실행합니다.
```bash
minikube start                          # Minikube 클러스터 시작
```

#### 이미지 빌드

EX08 폴더로 이동한 뒤, 각 서버의 Docker 이미지를 빌드합니다. 여기서 주의할 점이 있습니다. 지금까지는 `docker build`로 이미지를 만들었지만, 미니큐브 환경에서는 `docker build`로 만든 이미지를 사용할 수 없습니다.

> **minikube image build**: 미니큐브는 별도의 가상 환경(Docker 컨테이너 또는 VM) 안에서 동작합니다. 따라서 로컬 PC에서 `docker build`로 만든 이미지는 미니큐브 내부에서 접근할 수 없습니다. `minikube image build` 명령을 사용하면 미니큐브 내부에 직접 이미지를 빌드하여, 별도의 이미지 레지스트리 없이도 Pod에서 바로 사용할 수 있습니다.

**[실습]** 각 서버의 Docker 이미지를 미니큐브 내부에 빌드합니다.
```bash
minikube image build -t metacoding/db:1 ./db              # DB 이미지 빌드
minikube image build -t metacoding/backend:1 ./backend    # 백엔드 이미지 빌드
minikube image build -t metacoding/frontend:1 ./frontend  # 프론트엔드 이미지 빌드
minikube image build -t metacoding/redis:1 ./redis        # Redis 이미지 빌드
```

![실행 결과](images/chap03-67.png)
*그림 3-37: 미니큐브 이미지 빌드*

#### 리소스 생성

**[실습]** `Namespace`를 생성합니다.
```bash
kubectl apply -f k8s/namespace.yml      # 네임스페이스 생성
```

![실행 결과](images/chap03-68.png)
*그림 3-38: Namespace 생성*

**[실습]** k8s 폴더의 모든 리소스를 생성합니다. `--recursive` 옵션은 하위 폴더의 YML 파일도 모두 적용합니다.
```bash
kubectl apply -f k8s/ --recursive       # 모든 매니페스트 한 번에 적용
```

![실행 결과](images/chap03-69.png)
*그림 3-39: k8s 리소스 일괄 생성*

**[실습]** 생성된 리소스 정보를 확인합니다.
```bash
kubectl get deploy,pod,service -n metacoding    # 전체 리소스 상태 조회
```

![실행 결과](images/chap03-70.png)
*그림 3-40: Deployment, Pod, Service 조회*

#### 컨테이너 실행 확인

**[실습]** 각 서버의 로그를 확인합니다.
```bash
kubectl logs deploy/db-deploy -n metacoding --tail=100          # DB 로그 확인
kubectl logs deploy/frontend-deploy -n metacoding --tail=100    # 프론트엔드 로그 확인
kubectl logs deploy/backend-deploy -n metacoding --tail=100     # 백엔드 로그 확인
```

![실행 결과](images/chap03-71.png)
*그림 3-41: 서버 로그 확인*

`Pod`가 Running 상태라고 해서 서버가 바로 정상 동작하는 건 아닙니다. 실행에 시간이 필요할 수 있으니, `kubectl logs` 명령어를 활용해 각 서버의 로그를 확인하며 정상적으로 동작되었는지 확인합니다.

#### 서버 연결

**[실습]** 프론트 서버에 접속할 수 있는 URL을 생성합니다.
```bash
minikube service frontend-service -n metacoding --url    # 프론트엔드 외부 접근 URL 확인
```

![실행 결과](images/chap03-72.png)
*그림 3-42: 프론트 서비스 URL 생성*

`minikube service` 명령어를 통해 생성된 URL로 접속하면 DB에서 조회된 데이터가 화면에 표시됩니다.

![실행 결과](images/chap03-73.png)
*그림 3-43: 사용자 리스트와 방문 횟수 표시*

여러 번 요청을 보내면 방문 횟수가 증가하는 걸 볼 수 있습니다.

![실행 결과](images/chap03-74.png)
*그림 3-44: 방문 횟수 증가 확인*

이제 `Pod` 내부를 확인해보겠습니다. 먼저 `minikube service` 명령어에 의해 실행 중인 포그라운드를 `CTRL + C`를 입력해 빠져나옵니다.

**[실습]** 백엔드 `Pod`명을 확인합니다.
```bash
kubectl get pod -n metacoding           # Pod 목록 조회
```

![실행 결과](images/chap03-75.png)
*그림 3-45: 백엔드 Pod 목록 확인*

**[실습]** 각 백엔드 서버의 로그를 확인합니다.
```bash
kubectl logs <pod명> -n metacoding --tail=100
```

**backend-deploy-f7878cc5f-ltzmx**

![실행 결과](images/chap03-76.png)
*그림 3-46: 백엔드 서버 1 로그*

**backend-deploy-f7878cc5f-tdvnw**

![실행 결과](images/chap03-77.png)
*그림 3-47: 백엔드 서버 2 로그*

로그에서 회원 정보를 조회하기 위해 실행된 `SELECT문`이 출력됩니다. `backend-service`가 로드밸런싱을 수행해서 요청이 두 서버로 분산 처리된 것을 확인할 수 있습니다.

---

## 이것만은 기억하자

- **컨테이너가 많아지면, 관제탑이 필요하다.** 컨테이너 몇 개는 수동으로 관리할 수 있지만, 수십~수백 개가 되면 자동으로 배포·복구·확장하는 쿠버네티스가 필수입니다.
- **Deployment + Service = 안정적인 서비스.** Deployment가 Pod의 개수와 상태를 자동으로 유지하고, Service가 고정된 접근점을 제공합니다. 이 둘의 조합이 쿠버네티스의 핵심입니다.
- **설정은 밖에서, 데이터는 영구히.** ConfigMap과 Secret으로 코드와 설정을 분리하고, PV/PVC로 컨테이너가 사라져도 데이터를 보존합니다.

이것으로 Docker와 Kubernetes를 향한 오픈이의 여정이 마무리되었습니다. 챕터 1에서 컨테이너 하나를 띄우는 것부터 시작했습니다. 챕터 2에서 Docker Compose로 여러 컨테이너를 관리하는 법을 배웠고, 챕터 3에서는 쿠버네티스로 자동화된 운영 환경까지 구성했습니다. 여기까지 온 여러분이라면, 그 어떤 기술도 두렵지 않을 것입니다.

