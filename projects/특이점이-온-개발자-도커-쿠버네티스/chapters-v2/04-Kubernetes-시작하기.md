# Ch.4 Kubernetes 시작하기

> 한 줄 요약: 쿠버네티스가 컨테이너를 자동으로 관리하고 복구한다
> 핵심 개념: Kubernetes, Minikube, Deployment, ReplicaSet, Service

## 4.1 쿠버네티스가 필요한 이유

### 4.1.1 왜 쿠버네티스인가

도커 컴포즈는 여러 컨테이너를 한꺼번에 실행하기에는 아주 편리한 도구입니다. 하지만 실제 서비스를 운영하다 보면 도커 컴포즈만으로는 해결하기 어려운 문제들이 발생합니다. 다음의 세 가지 상황을 가정해 보겠습니다.

#### 상황 1: 모두가 잠든 새벽 3시, 서버가 다운된다면?
갑작스러운 메모리 부족으로 백엔드 컨테이너가 종료되었습니다. 사용자는 "서버 오류" 화면만 보게 되고, 서비스는 중단됩니다. 도커 컴포즈 환경이라면 개발자가 새벽에 깨어나 알림을 확인하고, 직접 서버에 접속해 명령어를 입력해서 다시 살려내야 합니다. 개발자가 대응하기 전까지 서비스는 계속 멈춰 있게 됩니다.

#### 상황 2: 갑작스러운 이벤트로 트래픽이 10배 폭증한다면?
평소에는 컨테이너 1대로 충분했지만, 타임세일이나 이벤트가 시작되자 접속자가 몰려 응답이 느려집니다. 이때 컨테이너 수를 늘리려면 개발자가 수동으로 설정을 바꾸고 다시 배포해야 합니다. 이벤트가 끝나고 접속자가 줄어들면 다시 수동으로 컨테이너를 줄여야 하는 번거로움도 생깁니다.

#### 상황 3: 서비스 중단 없는 업데이트가 필요하다면?
새로운 기능을 배포하려면 기존 컨테이너를 멈추고 새 컨테이너를 띄워야 합니다. 이 교체 과정에서 아주 짧은 시간 동안 서비스가 중단됩니다. 운 나쁘게 그 순간 결제 중이던 사용자는 오류를 경험하게 됩니다.

수십, 수백 개의 컨테이너를 사람이 일일이 감시하고 관리하는 것은 불가능에 가깝습니다. 이 과정을 자동으로 처리해 주는 시스템이 바로 **쿠버네티스(Kubernetes, K8s)**입니다. 쿠버네티스는 구글에서 만든 컨테이너 관리 플랫폼으로, 운영의 핵심적인 부분을 자동화합니다.

#### 쿠버네티스의 핵심: 선언적 관리 (Desired State)
쿠버네티스의 가장 큰 특징은 **원하는 상태** 만 알려주면 된다는 점입니다.

예를 들어, 개발자가 "백엔드 컨테이너 3대를 항상 유지해줘"라고 선언해 둡니다. 만약 새벽에 컨테이너 1대가 죽으면, 쿠버네티스는 즉시 이를 감지하고 스스로 새 컨테이너를 띄워 다시 3대를 맞춥니다. 개발자가 직접 개입하지 않아도 시스템이 알아서 복구하는 '자기 회복(Self-healing)' 기능입니다.

요약하자면
 - 도커: 한 대의 컴퓨터 안에서 컨테이너를 만들고 실행하는 도구입니다.
 - 쿠버네티스: 수많은 컴퓨터(Node)를 하나로 묶어, 수백 개의 컨테이너를 자동으로 관리하고 배치하는 거대한 운영 시스템입니다.

### 4.1.2 쿠버네티스의 핵심 리소스

쿠버네티스에는 **리소스** 라는 개념이 있습니다. 외부에서 요청이 들어오면 이 리소스들을 거쳐 컨테이너에 도달합니다. 전체 흐름을 먼저 보겠습니다.

![](../assets/CH04/chap03-k8s-architecture.png)
*쿠버네티스 핵심 리소스 구조도*

각 리소스의 역할은 아래 표와 같습니다. 상세 내용은 실습에서 하나씩 다룹니다.

| 리소스 | 역할 | 비유 |
|--------|------|--------------|
| **Ingress** | 외부 요청을 클러스터 내부로 라우팅하는 진입점 | 프랜차이즈 공식 주문 앱 |
| **Service** | Pod의 IP가 바뀌어도 고정된 진입점을 제공하여 트래픽을 전달 | 가맹점 전화번호 |
| **Deployment** | Pod의 생성, 개수 유지, 업데이트를 자동 관리하는 지침서 | 본사 운영 지침서 |
| **Pod** | 컨테이너를 실행하는 가장 작은 단위 | 가맹점 주방 |
| **ConfigMap** | 데이터베이스 주소 등 일반 설정값을 저장 | 일반 메뉴판/영업 안내 |
| **Secret** | 비밀번호, API 키 등 민감한 설정값을 별도로 분리하여 저장 | 레시피 |

### 4.1.3 쿠버네티스의 동작 원리

그렇다면 이것이 어떤 구조로 돌아가는 걸까요?

#### 노드: 독립된 가상 컴퓨터

쿠버네티스의 동작 원리를 알기 위해서 먼저 **노드(Node)** 에 대해 알아야 합니다.

쉽게 말해 노드는 거대한 물리 서버 한 대의 자원을 나누어 쓰는 **독립된 가상 컴퓨터** 입니다.

앞선 챕터 2에서 배운 컨테이너 가상화를 다시 한번 떠올려 볼까요? 이 시점에서 컨테이너와 노드의 역할을 명확히 구분하는 것은 매우 중요합니다.

먼저 컨테이너는 호스트 컴퓨터의 운영체제(OS)를 다른 컨테이너들과 함께 공유해서 사용하는 **격리된 프로세스** 입니다. 반면 노드는 이러한 컨테이너들을 품고 실제로 일하게 만드는 **하나의 컴퓨터** 입니다.

![](../assets/CH04/chap04-node.png)
*노드의 구조*

이 둘의 가장 결정적인 차이는 **운영체제의 독립성**에 있습니다. 컨테이너는 호스트 컴퓨터에 이미 깔려 있는 OS를 빌려서(공유해서) 사용합니다. 하지만 노드는 호스트 환경 위에 자신만의 독립된 운영체제(OS)를 별도로 설치하여 구동합니다.

우리가 방금 살펴본 이 독립적인 **노드들이** 수십, 수백 개씩 모여 하나의 거대한 팀을 이룬 것이 바로 **쿠버네티스** 입니다. 쿠버네티스는 이렇게 흩어져 있는 노드들을 하나로 묶어, 마치 한 대의 거대한 컴퓨터처럼 사용할 수 있게 관리하는 역할을 맡습니다.

#### 클러스터의 구조: 본사와 가맹점

쿠버네티스는 크게 **컨트롤 플레인(Control Plane)** 과 **워커 노드(Worker Node)** 로 구성되어 있습니다. 이 둘이 합쳐져 하나의 시스템처럼 유기적으로 돌아가는 구조를 **클러스터(Cluster)** 라고 합니다. 이를 프랜차이즈 기업 운영에 비유하면 다음과 같습니다.

- **클러스터 :** 프랜차이즈 기업입니다. 본사와 전국 가맹점들이 하나의 체계로 묶여 유기적으로 움직이는 전체 시스템을 의미합니다.
- **컨트롤 플레인 :** 본사 관리팀입니다. 브랜드 규모를 유지하기 위해 매장 수를 점검하고 조율합니다. 브랜드의 정책을 가맹점에게 전달하며 관리하는 컨트롤 타워입니다.
- **워커 노드 :** 각 지역 가맹점입니다. 본사의 지침을 받아 현장에서 실제로 음식을 만들고 손님을 맞이하며, 주방(Pod)을 직접 관리하는 실질적인 작업 공간입니다.

![](../assets/CH04/fig-3-1.png)
*쿠버네티스 클러스터 구조*

#### 쿠버네티스에 명령어를 실행했을 때

구성 요소를 알았으니, 이제 이것들이 실제로 어떻게 움직이는지 살펴보겠습니다. 개발자가 명령어를 입력하면 어떤 일이 벌어지는지, 프랜차이즈 본사에 새 매장 오픈을 요청하는 과정으로 따라가 보겠습니다.

**Step 1.** 개발자가 쿠버네티스에 명령을 내리면, 그 요청은 가장 먼저 **Kube API Server** 라는 입구로 들어옵니다. 본사 대표 전화로 전화를 걸어 **"새 가맹점 하나 열고 싶어요"** 라고 공식적으로 요청을 접수하는 과정과 같습니다.

![](../assets/CH04/fig-3-2.png)
*개발자의 명령이 Kube API Server로 전달되는 흐름*

**Step 2.** 본사 창구(API Server)에 접수된 명령은 가장 먼저 **본사 데이터베이스(etcd)** 에 기록됩니다. 전산에 기록이 남으면 본사 관리팀 내의 담당자들이 각자의 분야를 처리합니다.

 - **스케줄러(Scheduler)** 가 새 매장이 들어서기에 가장 적당한 **상가 위치(노드)** 를 찾아 배정합니다. 어느 지점의 상권이 여유로운지, 새 매장을 들이기에 적합한 환경인지를 확인하여 최적의 장소를 결정합니다.
 - **컨트롤러 매니저(Controller Manager)** 가 새로운 매장이 **본사 규정(지침)** 대로 오픈될 것인지 확인하고 관리합니다. 인테리어와 메뉴 등 맞게 매장이 준비되고 있는지 전체적인 상태를 상시 점검합니다.

![](../assets/CH04/fig-3-3.png)
*컨트롤 플레인 내부 구성 요소의 상호 작용*

**Step 3.** 본사에서 확정된 입지 선정 결과와 운영 지침은 해당 가맹점의 **슈퍼바이저(Kubelet)** 에게 전달됩니다. 이제 서류상의 계획이 실제 현장에서 실물로 구현되는 단계입니다. Kubelet은 본사의 지시를 현장에서 수행하는 실무 책임자로, 매장이 주문서대로 잘 운영되고 있는지 끝까지 책임지고 본사에 보고합니다.

매장이 열리면 **kube-proxy** 가 외부에서 들어오는 주문을 올바른 주방(Pod)으로 연결합니다. 요청이 어떤 노드로 들어오든 올바른 Pod에게 도달할 수 있는 건 이 배달 담당자 덕분입니다.

![](../assets/CH04/fig-3-4.png)
*워커 노드에서 kubelet과 kube-proxy의 역할*

> **참고: kube-proxy와 iptables**
> kube-proxy는 모든 워커 노드에서 동작하며, 네트워크 규칙을 관리하는 구성 요소입니다. 2장에서 배운 iptables를 기억하시나요? Docker가 포트포워딩에 iptables를 사용했듯이, kube-proxy도 iptables 규칙을 세워 요청을 올바른 Pod로 전달합니다.

#### 구성 요소 정리

지금까지 등장한 클러스터 안의 구성 요소를 정리하면 다음과 같습니다.

**컨트롤 플레인 (본사 관리팀)**

| 구성 요소 | 역할 | 비유 |
|-----------|------|--------------|
| **Kube API Server** | 모든 요청이 가장 먼저 도달하는 클러스터의 입구 | 본사 대표 전화 |
| **etcd** | 클러스터의 모든 상태 정보를 저장하는 데이터베이스 | 본사 데이터베이스로 가맹점의 데이터를 기록 |
| **Controller Manager** | 원하는 상태와 실제 상태를 비교하며 시스템을 관리 | 매장이 본사 규정대로 운영되는지 상시 점검 |
| **Scheduler** | 명령이 실행될 노드를 자동 선택 | 새 매장을 열기에 가장 적합한 상가 위치를 선정 |

**워커 노드 (가맹점)**

| 구성 요소 | 역할 | 비유 |
|---------|------|--------------|
| **kubelet** | 컨테이너를 실제로 생성/관리하고 상태를 보고 | 본사의 지침을 받아 현장에서 수행하는 슈퍼바이저 |
| **kube-proxy** | 네트워크 규칙을 관리, 요청을 올바른 Pod로 전달 | 주문이 들어오면 어떤 주방으로 보내야 하는지 안내하는 배달 담당자 |

## 4.2 Minikube : 로컬 클러스터

> 4.2부터 작성하는 **YAML(yml)** 파일은 https://github.com/metacoding-10-linux-docker/docker/tree/master/yaml 에서 확인할 수 있습니다.

### 4.2.1 미니큐브(Minikube)란?

쿠버네티스가 서버 여러 대를 관리하는 거라면, 로컬 PC 한 대로도 실습할 수 있을까요? **미니큐브(Minikube)** 가 그것을 가능하게 합니다.

> **미니큐브(Minikube)** 는 Mini + Kubernetes라는 의미로, 로컬 PC에서 쿠버네티스 환경을 구성할 수 있는 개발용 프로그램입니다. Docker 컨테이너, VirtualBox 가상 머신 등을 사용해 미니큐브 환경을 구성할 수 있습니다.

미니큐브와 쿠버네티스의 기본 구조는 동일하지만, 미니큐브는 개발 환경용으로 설계된 만큼 하나의 노드에 컨트롤 플레인과 워커 노드 기능이 함께 들어 있습니다.

![](../assets/CH04/fig-3-5.png)
*미니큐브의 단일 노드 구조*

미니큐브는 단일 노드로 구성되어 구조가 단순하고 필요한 리소스도 적습니다. 로컬 PC에서 간편하게 쓸 수 있는 대신, 클라우드 로드밸런서 자동 생성이나 멀티 노드 확장 같은 운영 환경 기능은 지원하지 않습니다. 그래도 미니큐브에서 애플리케이션이 정상적으로 동작한다면, 동일한 설정과 구조를 실제 쿠버네티스 환경에도 그대로 적용할 수 있습니다.

### 4.2.2 미니큐브 기본 명령어

#### 미니큐브 설치

**[실습]** OS에 맞는 패키지 관리자로 미니큐브를 설치합니다.
```bash
# Windows (터미널을 관리자 권한으로 실행)
choco install minikube

# Mac (터미널에서 실행)
brew install minikube
```

> Windows는 **Chocolatey**, Mac은 **Homebrew** 패키지 관리자가 설치되어 있어야 합니다. 미설치 시 [Chocolatey 설치 가이드](https://chocolatey.org/install) 또는 [Homebrew 설치 가이드](https://brew.sh/)를 참고합니다.

#### 미니큐브 실행

**[실습]** 터미널에서 미니큐브를 실행합니다.
```bash
minikube start         # 미니큐브 클러스터 시작
```

![](../assets/CH04/chap03-15.png)
*minikube start 실행*

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

### 4.2.3 kubectl로 첫 Pod 띄우기

미니큐브가 실행되었으니 이제 **kubectl** 을 익힐 차례입니다. 쿠버네티스를 다루는 기본 도구입니다.

> **kubectl** 은 쿠버네티스 내부의 클러스터 리소스를 관리하는 명령어입니다.

쿠버네티스를 다루려면 kubectl 명령어를 익혀야 합니다. 먼저 쿠버네티스의 핵심 리소스인 Pod로 명령어를 실습해 보겠습니다.

#### Pod

Docker에서는 컨테이너를 바로 실행했습니다. 쿠버네티스는 다릅니다. 컨테이너를 직접 다루지 않고 **Pod** 라는 단위에 담아서 관리합니다.

> **Pod** 는 쿠버네티스에서 컨테이너를 실행하는 가장 작은 단위입니다. Pod는 하나 이상의 컨테이너로 구성되어 있습니다.

![](../assets/CH04/k8s-step1.png)
*Pod --- 컨테이너를 감싸는 최소 실행 단위*

#### 명령어 한 줄로 Pod 생성하기

가장 빠른 방법부터 시작해 보겠습니다. `kubectl run` 명령어 한 줄이면 Pod가 만들어집니다.

**[실습]** nginx 이미지를 사용해 Pod를 생성합니다.
```bash
kubectl run hello-pod1 --image=nginx  # Dockerhub의 nginx 이미지로 Pod 생성
```

![](../assets/CH04/01_kubectl-run-hello-pod1.png)
*kubectl run hello-pod1 실행 결과*

명령어 한 줄로 Pod가 만들어졌습니다. 이 한 줄이 실제로 무엇을 했는지 YAML 파일로 풀어 볼 수 있습니다. **같은 결과를 파일로 저장해서 재사용할 수 있게 만든 것**이 YAML입니다.

#### Pod를 YAML 파일로 생성하는 방법

위에서 `kubectl run`으로 만든 Pod를, YAML 파일로 작성하면 이렇게 됩니다.

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

앞에서 `kubectl run`으로 한 것과 결과는 같습니다. Pod 이름과 이미지 같은 설정을 파일에 적어둔 것입니다. YAML로 써두면 파일로 남으니 반복해서 쓸 수 있습니다.

**[실습]** 터미널 창을 **yaml 폴더** 로 이동 후 아래 명령어를 실행하면 `Pod`가 생성됩니다.
```bash
kubectl apply -f hello-pod2.yml       # YAML 파일로 Pod 생성
```

![](../assets/CH04/chap03-21.png)
*kubectl apply로 Pod 생성*

#### Pod 조회

**[실습]** 생성된 `Pod` 목록을 조회합니다.
```bash
kubectl get pod                       # Pod 목록 조회
```

![](../assets/CH04/02_kubectl-get-pod.png)
*Pod 목록 조회*

`kubectl describe pod <Pod이름>` 명령어로 Pod의 상세 정보도 조회할 수 있습니다.

**[실습]** Pod의 상세 정보를 조회합니다.
```bash
kubectl describe pod hello-pod2       # Pod 상세 정보 조회
```

![](../assets/CH04/chap03-25.png)
*Pod 상세 조회*

#### Pod의 네트워크

도커(Docker) 환경에서는 기본적으로 컨테이너마다 독립적인 IP가 할당됩니다. 그래서 컨테이너 A와 컨테이너 B가 통신하려면 서로의 IP 주소를 알거나, 사용자 정의 네트워크에 함께 있어야 합니다.

하지만 쿠버네티스의 Pod는 다릅니다. 하나의 파드 안에 있는 컨테이너들은 모두 동일한 IP 주소를 공유합니다. 이것이 어떻게 가능한 걸까요?

Pod가 생성되면 kubelet은 가장 먼저 새로운 **Network Namespace** 를 만듭니다. Network Namespace란 IP, 포트 등 네트워크 자원을 독립적으로 갖는 격리된 공간입니다. 이 공간에 IP(예: 10.10.10.10)가 부여되고, 그 안에서 **pause** 라는 아주 가벼운 컨테이너가 실행됩니다.

그 뒤에 생성되는 앱 컨테이너(nginx, redis 등)는 새로운 네트워크 공간을 만들지 않고, pause가 만들어둔 공간에 들어갑니다. 같은 공간 안에 있으니 같은 IP를 쓰고, **localhost** 로 서로 직접 통신할 수 있습니다.

![](../assets/CH04/net-07-pod-namespace.png)
*Pod 안의 컨테이너들은 하나의 Network Namespace를 공유합니다*

pause는 아무 프로세스도 실행하지 않고 살아만 있습니다. 만약 nginx가 네트워크를 소유하고 있다가 크래시로 죽으면 네트워크 공간 자체가 사라지지만, pause는 아무 일도 안 하니까 죽을 일이 없고 네트워크가 안정적으로 유지됩니다.

Docker에서 컨테이너가 네트워크의 단위였다면, Kubernetes에서는 **Pod가 네트워크의 단위** 입니다.



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

## 4.3 Deployment, ReplicaSet : 자동 복구와 스케일링

Pod를 띄우는 데 성공했습니다. 그런데 이 Pod가 죽으면 어떻게 될까요? 실험해 보겠습니다.

**[실습]** Pod를 수동으로 삭제해봅니다.
```bash
kubectl delete pod hello-pod1         # Pod 삭제
kubectl get pod                       # Pod 목록 조회
```

hello-pod1은 삭제되면 그냥 사라졌습니다. 아무도 다시 살려주지 않았습니다.

Pod를 직접 만들면 죽어도 아무도 살려주지 않습니다. 그래서 Pod를 직접 만들지 않고 **Deployment** 를 사용합니다. 'Pod 몇 개 유지하고, 문제 생기면 알아서 갈아 끼워라'는 지침서와 같습니다.

![](../assets/CH04/k8s-step2.png)
*Deployment가 ReplicaSet을 생성하고, ReplicaSet이 Pod 수를 유지한다*

### 4.3.1 Deployment

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

**Selector** 는 특정 label을 가진 리소스를 선택하는 조건입니다. Deployment의 Selector와 Pod의 labels가 일치하면 그 Pod를 관리 대상으로 삼습니다.

![](../assets/CH04/selector-labels.png)
*Selector가 app: web인 Pod만 매칭하고, app: db인 Pod는 매칭하지 않습니다*

이 label-selector 구조는 Deployment만 쓰는 게 아닙니다. 다음 장에서 배울 **Service** 도 이 라벨로 Pod를 찾아 네트워크를 연결합니다. label은 쿠버네티스에서 리소스를 연결하는 유일한 방법입니다.

아래 명령어로 `Deployment`를 생성합니다.

**[실습]** `Deployment`를 생성하고 `Pod`를 확인합니다.
```bash
kubectl apply -f deploy-ex01.yml      # Deployment 생성
kubectl get pod                       # Pod 목록 조회
```

![](../assets/CH04/03_kubectl-get-pod-deploy.png)
*Deployment와 Pod 생성 확인*

이제 진짜 실험입니다. 모든 Pod를 삭제해 보겠습니다. Deployment가 관리하지 않는 Pod도 함께 삭제됩니다.

**[실습]** 전체 `Pod`를 삭제한 뒤 다시 조회합니다.
```bash
kubectl delete pod --all              # 전체 Pod 삭제
kubectl get pod                       # Pod 목록 조회
```

![](../assets/CH04/04_kubectl-delete-pod-all.png)
*Pod 제거 후 자동 재생성 확인*

hello-pod1, hello-pod2는 사라졌는데 Deployment로 만든 Pod는 알아서 살아났습니다. Deployment가 'Pod 1개 유지해라'고 선언해놨기 때문에, 죽으면 알아서 새로 만드는 것입니다.

`kubectl run`으로 직접 생성한 `Pod`는 종료되었지만, `Deployment`로 생성된 `Pod`는 자동으로 재시작되었습니다.

> **Deployment** 로 Pod를 생성하면 Pod 생성뿐만 아니라 개수 유지와 장애 복구까지 자동으로 처리됩니다. Pod는 직접 생성하기보다 **Deployment** 로 생성하는 것이 일반적입니다.

**[실습]** 다음 실습을 위해 생성한 `Deployment`를 제거합니다.

```bash
kubectl delete deployment nginx-deploy # Deployment 삭제
```

### 4.3.2 ReplicaSet

Pod를 1개가 아니라 여러 개 유지하고 싶다면 어떻게 할까요? **ReplicaSet** 이 그 역할을 합니다. 에어컨 자동 온도 조절과 같습니다. 24도로 맞춰놓으면 올라가면 냉방 틀고 내려가면 멈추듯이, ReplicaSet도 Pod 개수를 설정해두면 모자라든 넘치든 알아서 맞춰줍니다.

> **ReplicaSet** 은 지정한 개수만큼 Pod가 항상 살아있도록 관리하는 컨트롤러입니다. Pod가 죽거나 예상보다 많아지는 상황이 발생하면 원래 설정된 수에 맞게 Pod를 자동으로 생성하거나 제거하여 상태를 일정하게 유지합니다.

![](../assets/CH04/replicaset.png)
*Pod 3이 종료되면 ReplicaSet이 설정 개수를 맞추기 위해 Pod 4를 자동 생성*

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
      maxUnavailable: 0  # 기존 Pod를 먼저 종료하지 않음 (무중단 배포)

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

![](../assets/CH04/07_kubectl-get-pods-replicas.png)
*replicas 설정으로 Pod 4개 생성*

`replicas`에 설정한 수에 따라 `Pod`가 4개 생성되었습니다.

`replicas`를 4로 설정했더니 정확히 4개가 생성되었습니다.

### 4.3.3 롤링 업데이트(RollingUpdate)

이제 새 버전을 배포해야 하는 상황을 생각해 보겠습니다. 기존 서버를 전부 내리고 새 서버를 올리면? 그 사이에 서비스가 멈춥니다. deploy-ex02.yml의 `strategy`에 `RollingUpdate`가 설정되어 있는 이유가 여기 있습니다.

> **롤링 업데이트(RollingUpdate)** 는 기존 Pod를 한꺼번에 내리지 않고, 새 Pod를 먼저 띄운 뒤 기존 Pod를 순차적으로 교체하는 무중단 배포 방식입니다. **maxSurge** 는 업데이트 중 추가로 띄울 수 있는 Pod 수, **maxUnavailable** 은 동시에 내릴 수 있는 Pod 수를 뜻합니다. `maxUnavailable: 0`이면 기존 Pod를 먼저 종료하지 않으므로, 새 Pod가 완전히 준비된 뒤에야 기존 Pod가 제거됩니다.

**[실습]** nginx 이미지를 1.21 버전으로 업데이트합니다.
```bash
kubectl set image deployment/nginx-replica nginx-container=nginx:1.21  # nginx 이미지를 1.21로 업데이트
```

![](../assets/CH04/chap03-33.png)
*이미지 버전 업데이트 실행*

**[실습]** 업데이트 진행 상황을 실시간으로 확인합니다.
```bash
kubectl get pod -w                    # Pod 상태 실시간 감시
```

![](../assets/CH04/06_kubectl-get-pods-w-rolling.png)
*롤링 업데이트 진행 상황*

새 Pod가 `ContainerCreating` → `Running` 상태로 먼저 전환된 뒤, 기존 Pod가 `Terminating` 상태로 종료됩니다. `maxUnavailable: 0`이기 때문에 기존 Pod가 먼저 죽지 않고, 새 Pod가 준비될 때까지 기다립니다.

새 Pod가 먼저 뜨고, 기존 Pod가 나중에 종료됩니다. `maxUnavailable: 0`으로 설정했기 때문에 기존 Pod를 먼저 죽이지 않고, 새 Pod가 다 뜬 다음에 순서대로 내립니다. `maxSurge`와 `maxUnavailable` 설정으로 원하는 방식의 업데이트를 구성할 수 있습니다.

**[실습]** `Deployment`의 상세 정보를 확인하면 이미지가 1.21 버전으로 변경된 것을 볼 수 있습니다.
```bash
kubectl describe deployment nginx-replica  # Deployment 상세 정보 조회
```

### 4.3.4 Rollback

새 버전을 배포했는데 버그가 터졌습니다. 이전 버전으로 되돌려야 합니다.

**[실습]** 먼저 배포 이력을 확인한 뒤 롤백합니다.
```bash
kubectl rollout history deployment/nginx-replica  # 배포 이력 조회
kubectl rollout undo deployment/nginx-replica      # 이전 버전으로 롤백
```

![](../assets/CH04/chap03-36.png)
*Rollback 실행 결과*

`kubectl describe` 명령어로 롤백된 이미지 버전을 확인합니다.

**[실습]** 다음 실습을 위해 생성한 `Deployment`를 제거합니다.

```bash
kubectl delete deployment nginx-replica # Deployment 삭제
```

## 이것만은 기억하자

- **컨테이너가 많아지면, 관제탑이 필요합니다.** 컨테이너 몇 개는 수동으로 관리할 수 있지만 수십~수백 개가 되면 자동으로 배포, 복구, 확장하는 쿠버네티스가 필요합니다.

- **Pod를 직접 관리하지 마세요.** Pod를 직접 만들면 죽었을 때 아무도 살려주지 않습니다. Deployment가 원하는 상태를 선언하면 쿠버네티스가 알아서 유지합니다.

- **label은 쿠버네티스의 연결 고리입니다.** Deployment가 selector로 Pod를 관리하듯이, 다음 장에서 배울 Service도 label로 Pod를 찾아 네트워크를 연결합니다.

- **Docker의 네트워크가 쿠버네티스에서 확장됩니다.** 2장에서 배운 iptables는 kube-proxy로, Docker DNS는 CoreDNS로 확장됩니다. 다음 장에서 이 연결을 직접 확인합니다.

Pod와 Deployment로 컨테이너를 띄우고 관리할 수 있게 되었습니다. 하지만 아직 해결 못한 문제가 있습니다. Pod IP는 죽을 때마다 바뀌는데, 외부에서는 어떻게 접속하고 Pod끼리는 어떻게 찾을까요?

Pod를 띄우는 건 됐는데, 이것을 어떻게 찾아갈 수 있을까요?

