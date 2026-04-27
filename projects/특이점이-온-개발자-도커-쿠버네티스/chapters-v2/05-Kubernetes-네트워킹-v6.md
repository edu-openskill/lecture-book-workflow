# Ch.5 Kubernetes 네트워킹

챕터 4의 끝에서 오픈이는 한 가지 벽 앞에 멈춰 섰습니다. Deployment로 Pod 개수는 맞춰졌지만, 되살아난 Pod의 IP가 매번 달라졌습니다. 프론트엔드 Pod가 백엔드 Pod를 부르려면 주소가 있어야 하는데, 그 주소가 계속 바뀌면 어떻게 연결을 이어가라는 걸까요. 자동 복구까지는 해결됐지만, 브라우저에서 내 앱에 안정적으로 들어가는 길은 아직 남아 있습니다.

오늘 목표는 한 줄로 정리됩니다.

**Pod IP가 바뀌어도 끊기지 않는 주소를 만들고, 외부 브라우저에서 URL로 내 앱에 접근하는 전체 경로를 완성한다.**

이 챕터에서 쌓는 부품은 어제 갑자기 튀어나온 개념이 아닙니다. 챕터 2에서 만난 Docker 네트워크(iptables DNAT, Docker DNS, docker0)가 이름만 바꿔 더 큰 규모로 다시 등장합니다.

## 5.1 Service — Pod의 대표 전화번호

### 5.1.1 Pod IP가 매번 바뀐다

자리에 앉자마자 옆자리 동료가 모니터 쪽으로 고개를 내밀었습니다.

**동료**: "방금 되던 주소가 또 안 돼."

오픈이는 어제 끝낸 작업 화면을 열어 같은 상황을 직접 재현해 봤습니다.

```bash
kubectl get pod -o wide           # 현재 IP 확인
kubectl delete pod --all          # Pod 삭제
kubectl get pod -o wide           # 다시 조회하면 IP가 달라져 있음
```

![](../assets/CH04/08_pod-ip-change.png)

*그림 5-1 Pod 재시작 시 IP 변경 확인*

같은 nginx 이미지인데 주소 뒷자리가 `7`에서 `8`로 바뀌어 있었습니다. 숫자 한 자리 차이지만, 이걸 프론트엔드 코드에 박아두면 하루도 못 버팁니다. 오픈이가 오늘 풀어야 할 첫 과제가 여기 있었습니다.

필요한 건 "**Pod IP가 어떻게 바뀌든 항상 같은 주소**"입니다. **가맹점 대표 전화번호**처럼요. 매장 안 직원 내선 번호는 교대 때마다 바뀌어도, 손님은 늘 가맹점 대표 번호로 걸면 됩니다. 한 매장에 직원이 여럿이면 대표 번호가 요청을 돌려가며 한 명씩 연결해 줍니다.

그 대표 번호 역할을 하는 리소스의 이름이 **Service**입니다.

![](../assets/CH04/k8s-step3.png)

*그림 5-2 Service는 고정 주소를 제공. Pod IP가 바뀌어도 Service 주소는 그대로*

> **참고: Service**
> Pod에 접근할 때 고정 IP를 제공해 안정적으로 접근할 수 있게 하는 리소스입니다. Pod가 죽고 다시 태어나 IP가 바뀌어도 Service 주소는 바뀌지 않습니다. 뒤에 여러 Pod가 붙어 있으면 요청을 돌려가며 나눠줍니다(로드밸런싱).

### 5.1.2 Service의 3가지 포트

Service를 YAML로 만들기 전에 포트 이름 세 개를 정리해 두는 편이 좋습니다. 외부 요청이 Pod에 도달하기까지 포트를 세 번 거치는데, 이름이 비슷해서 처음엔 꼭 헷갈립니다. 각 포트가 **누구 입장에서 붙인 번호인지**로 구분하면 실마리가 잡힙니다.

| 포트 종류 | 누구의 포트인가 | 역할 | 생략 시 |
|----------|----------------|------|--------|
| `nodePort` | **노드(서버) 입장**의 포트 | 외부에서 노드 IP로 접근할 때 열리는 30000~32767 포트 | 범위 내 자동 할당 |
| `port` | **Service 입장**의 포트 | 클러스터 내부에서 Service를 부를 때 쓰는 포트 | 필수 |
| `targetPort` | **Pod(컨테이너) 입장**의 포트 | 실제 컨테이너 안 애플리케이션이 귀를 대고 있는 포트 | `port` 값과 동일하게 설정 |

nginx 컨테이너는 기본 80 포트로 떠 있습니다. 잠시 뒤 만들 YAML에서는 `port: 80`만 적고 `targetPort`는 생략하는데, 생략하면 자동으로 `port` 값과 같아져서 Pod의 80 포트로 그대로 전달됩니다. `nodePort`도 적지 않으면 30000~32767 범위에서 K8s가 알아서 하나를 골라줍니다. 바깥 사람은 `nodePort`로 들어오고, 클러스터 안 이웃은 `port`로 부르고, 결국 도착해서 말을 거는 대상이 `targetPort`입니다. 세 이름은 같은 흐름을 서로 다른 입장에서 부르는 번호일 뿐입니다.

### 5.1.3 Service 생성

Service가 연결할 Pod부터 다시 띄워 둡니다. 챕터 4 마지막에 `nginx-replica` Deployment를 지워 둔 상태라 지금은 붙일 Pod가 한 개도 없습니다. 챕터 4에서 썼던 `deploy-ex02.yml`을 다시 적용합니다.

```bash
kubectl apply -f deploy-ex02.yml   # app=nginx 라벨의 Pod 4개 생성
kubectl get pod -l app=nginx       # 라벨로 Pod 확인
```

Pod가 준비됐으니 Service YAML을 적어 봅니다.

**yaml/service-ex01.yml**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  type: NodePort        # 노드 IP+포트로 외부 접근 가능한 타입
  selector:
    app: nginx
  ports:
  - port: 80            # 서비스가 클러스터 내부에서 열어둔 포트
```

`selector.app: nginx`는 방금 띄운 Pod의 라벨과 같은 이름표입니다. `targetPort`와 `nodePort`는 일부러 비웠습니다. `targetPort`를 적지 않으면 `port` 값(80)이 그대로 쓰이고, `nodePort`를 적지 않으면 30000~32767 중 하나가 자동 할당됩니다.

```bash
kubectl apply -f service-ex01.yml
```

![](../assets/CH04/10_kubectl-apply-service.png)

*그림 5-3 Service 생성*

### 5.1.4 Label-Selector — 연결 고리는 또 label

Service가 Pod를 찾는 방법은 Deployment와 똑같이 **label 매칭**입니다. selector에 `app: nginx`라고 적으면, 그 라벨을 가진 Pod만 이 Service에 연결됩니다.

*'앞 챕터 Deployment랑 같은 원리네.'*

챕터 4에서 Deployment가 Pod를 관리할 때 쓴 그 매칭과 같은 방식입니다.

![](../assets/CH04/selector-labels.png)

*그림 5-4 Service는 selector와 일치하는 label을 가진 Pod만 연결*

IP가 아니라 **이름표**로 연결되기 때문에, Pod가 새로 태어나 IP가 바뀌어도 이름표만 같으면 Service는 요청을 그대로 넘겨줍니다. Pod IP 변동 문제의 실마리가 여기서 풀립니다.

### 5.1.5 Service 타입 — 어디서 접근할 수 있는가

방금 만든 YAML에 `type: NodePort`라고 적은 이유가 따로 있습니다. Service는 타입에 따라 접근 범위가 달라집니다.

아무것도 적지 않으면 기본은 **ClusterIP**. 회사 내선 번호와 비슷합니다. 같은 클러스터 안에서만 걸리고, 외부에서는 아예 닿지 않습니다.

![](../assets/CH04/ch4-service-1-clusterip.png)

*그림 5-5 ClusterIP — 클러스터 내부에서만 접근 가능*

**NodePort**는 노드의 실제 IP에 포트(30000~32767) 하나를 뚫어서 외부 접근을 열어줍니다. 개발/테스트용으로 쓰기 편합니다.

![](../assets/CH04/ch4-service-2-nodeport.png)

*그림 5-6 NodePort — 노드 IP + 포트로 외부 접근 가능*

클라우드 환경에서 쓰는 **LoadBalancer**는 공인 IP를 자동으로 발급받고, 여러 노드에 트래픽을 나눠줍니다.

![](../assets/CH04/ch4-service-3-loadbalancer.png)

*그림 5-7 LoadBalancer — 공인 IP로 여러 노드에 트래픽 분산*

| 타입 | 접근 범위 | 사용 사례 |
|------|----------|----------|
| **ClusterIP** | 클러스터 내부만 | 백엔드·DB 등 외부 노출 불필요한 서비스 |
| **NodePort** | 노드IP:포트로 외부 접근 가능 | 테스트, 개발 환경 |
| **LoadBalancer** | 공인 IP로 외부 접근 가능 | 클라우드 운영 환경 |

### 5.1.6 보이지 않는 손 — kube-proxy

오픈이는 Service의 ClusterIP가 어느 장비에 붙어 있는 건지 궁금해졌습니다. 노드 IP도 아니고 Pod IP도 아닌 낯선 주소였습니다.

실제로 어디에도 붙어 있지 않았습니다. ClusterIP는 **어느 장비에도 할당되지 않은 가상 주소**입니다. 그럼 이 주소로 오는 요청은 누가 처리할까요. 보통이라면 받아줄 장비가 없으니 허공에 떠돌다 버려질 텐데, K8s에서는 사정이 다릅니다. 노드의 커널에 심어둔 규칙이 목적지 주소를 실제 Pod IP로 바꿔줍니다.

여기서 오픈이는 챕터 2에서 본 장면이 겹쳐 올라왔습니다. Docker가 포트포워딩을 구현한 방식이 같은 원리였습니다. 호스트 포트로 들어온 패킷의 목적지를 컨테이너 포트로 바꿔치기. 그 기술의 이름이 **iptables DNAT**입니다. K8s에서도 기본 모드에서는 같은 iptables를 쓰고, 그걸 관리하는 주체가 **kube-proxy**입니다.

> **참고: kube-proxy와 iptables**
> kube-proxy는 모든 워커 노드에서 동작하며, 노드의 리눅스 커널에 네트워크 규칙을 심는 역할을 합니다. ClusterIP로 오는 요청의 목적지를 실제 Pod IP로 바꿔치기. 챕터 2에서 본 Docker의 DNAT과 같은 메커니즘입니다. kube-proxy는 iptables 외에 IPVS/nftables 모드로도 동작할 수 있지만, 기본값은 iptables입니다.

![](../assets/CH05/kube-proxy-dnat.png)

*그림 5-8 kube-proxy는 NodePort 처리와 ClusterIP 처리를 모두 담당*

kube-proxy는 두 곳에서 이 일을 합니다.

- **NodePort 처리**: 외부에서 노드의 30000~32767 대역 포트로 들어온 요청을 실제 Pod IP로 변환
- **ClusterIP 처리**: 클러스터 내부에서 가상 IP로 온 요청을 실제 Pod IP로 변환

여기서 자연스럽게 따라오는 질문 하나. Pod IP가 바뀌면 그 iptables 규칙은 누가 다시 적을까요. 답은 **Endpoint Controller**입니다.

> **참고: Endpoint / Endpoint Controller**
> - **Endpoint**: "이 Service 뒤에 실제로 어떤 Pod IP들이 연결돼 있는지"를 담은 K8s 리소스입니다. 한 줄짜리 주소록이라고 생각하면 됩니다.
> - **Endpoint Controller**: Pod IP 변화를 감시하면서 그 주소록(Endpoint 리소스)을 갱신하는 주체입니다.
> - 최신 K8s(v1.21+)에서는 **EndpointSlice**가 기본 메커니즘이고, Endpoints는 하위호환용으로 유지됩니다.

![](../assets/CH05/endpoint-controller.png)

*그림 5-9 Endpoint Controller가 Pod IP 변화를 감시하고, kube-proxy가 규칙을 갱신*

세 요소가 이어지는 흐름을 따라가 봅니다. Service가 고정 주소(가상 IP)를 선언하고, Endpoint Controller가 Pod IP 변화를 감시해 주소록을 갱신하고, kube-proxy가 그 주소록을 각 노드의 iptables 규칙으로 집행합니다. 오픈이가 풀어야 했던 IP 변동 문제는 이 세 요소가 손을 맞춰 해결합니다.

### 5.1.7 외부에서 Service 접속해 보기

`kubectl get service`로 방금 만든 Service의 상세를 봅니다. `PORT(S)` 열에 `80:3xxxx/TCP` 형태로 찍히는데, 콜론 뒤 다섯 자리 숫자가 자동 할당된 `nodePort`입니다. Minikube는 내부적으로 VM이나 컨테이너로 한 겹 싸여 있어서 호스트 PC에서 NodePort로 바로 찌르기가 까다롭습니다. Minikube에는 이 상황을 위해 임시 터널을 뚫어주는 명령이 있습니다.

```bash
minikube service nginx-service --url   # Service 접근 URL 생성
```

![](../assets/CH04/chap03-43.png)

*그림 5-10 minikube service URL 생성*

명령을 치면 터미널이 URL 한 줄을 뱉은 뒤 커서가 그대로 멈춰 섭니다. 프롬프트가 돌아오지 않아 잠깐 당황스럽지만, 이 명령은 원래 실행 중 터미널을 계속 잡고 있는 종류입니다. 생성된 URL로 접속하면 Minikube 내부 Service를 거쳐 Pod로 요청이 전달됩니다.

![](../assets/CH04/chap03-44.png)

*그림 5-11 브라우저에서 nginx 접속 확인*

`minikube service --url`은 실행 중 터미널을 계속 잡아 두기 때문에, 확인이 끝나면 `CTRL + C`로 빠져나와야 다음 명령을 이어서 칠 수 있습니다.

이제 오늘 첫 과제를 다시 꺼내볼 차례입니다. Pod를 전부 지워 보고, 같은 URL로 다시 접속해 봅니다.

```bash
kubectl delete pod --all
minikube service nginx-service --url
```

![](../assets/CH04/11_delete-pod-minikube-service.png)

*그림 5-12 Pod 삭제 후 Service 접속*

새 URL로 접속해 봤더니 nginx 페이지가 그대로 떴습니다. 뒤에서 Pod는 새로 태어나 IP가 바뀌었을 텐데, 화면에는 그 흔적이 남아 있지 않았습니다. Endpoint Controller가 Pod IP 변화를 감시하고, kube-proxy가 iptables 규칙을 다시 쓰고, Service가 대표 번호를 끝까지 유지해 준 덕분입니다.

대목표 중 "Pod IP가 바뀌어도 끊기지 않는 주소"가 이 절에서 달성됐습니다. 남은 과제는 "외부 브라우저에서 **URL**로 접속하는 상태"입니다.

실습이 끝나면 리소스를 정리합니다.

```bash
kubectl delete deployment nginx-replica
kubectl delete service nginx-service
```

## 5.2 Ingress — 건물 안내 데스크

### 5.2.1 왜 Service만으로는 부족한가

Service 덕분에 Pod를 안정적으로 찾아가는 길은 뚫렸습니다. 그런데 서비스가 여러 개가 되면 새 문제가 기다리고 있습니다.

점심 먹고 자리에 돌아오자 동료가 다시 고개를 내밀었습니다.

**동료**: "포트 번호 외우고 다녀야 돼? 주소만 주면 안 돼?"
**팀장**: "실제 서비스는 도메인으로 들어오잖아. 같은 도메인 안에서 경로로 나눠 줘야지."

맞는 말이었습니다. `minikube service`는 터미널 하나를 붙잡는 임시 경로였고, NodePort는 `노드IP:3xxxx` 식이라 사용자가 포트 번호를 외우고 입력해야 했습니다. 실제 서비스는 도메인 기반 URL로 접속되고, 서비스마다 포트를 따로 외우는 게 아니라 같은 도메인 안에서 경로로 나누어 씁니다. Service 혼자서는 이걸 감당하지 못합니다.

*'챕터 3에서 NGINX가 URL 경로 보고 요청 나눠줬던 그 역할 아닌가.'*

K8s 안에서 그 역할을 맡는 리소스가 **Ingress**입니다.

### 5.2.2 L4와 L7 — 고속도로 분기점과 안내 데스크

Ingress를 이해하려면 네트워크 계층을 한 번 훑어두는 편이 좋습니다. L4와 L7이라는 용어가 자주 나오는데, 처음엔 경계가 흐릿하게 느껴집니다.

차가 고속도로 분기점에 들어섭니다. 분기점은 단순해요. "수도권 방향입니까, 호남선 방향입니까." 방향과 차선만 확인하고, 차 안에 누가 탔는지, 무슨 짐이 실렸는지는 보지 않죠. 빠르지만 판단은 단순합니다.

건물 1층 안내 데스크는 다릅니다. "어느 부서 찾으세요?" 방문자의 목적지를 듣고, 약속이 있는지 확인한 뒤, 적절한 층과 방 번호를 알려주죠. 이름과 목적을 읽어야 안내할 수 있어요. 느리지만 판단은 정확합니다.

![](../assets/CH05/l4-vs-l7.png)

*그림 5-13 L4는 빠른 분배, L7은 정확한 라우팅*

K8s 네트워크도 이 둘로 나뉩니다. **kube-proxy**가 고속도로 분기점 역할을 맡아 IP와 포트만 보고 Pod에 넘깁니다. **Ingress Controller**가 건물 안내 데스크 역할을 맡아 URL 경로와 Host 헤더를 읽고 해당 Service로 안내합니다.

> **참고: L4와 L7**
> 네트워크 OSI 7계층에서 가져온 숫자입니다. **L4(4계층, 전송 계층)** 는 TCP/IP 포트 번호까지만 봅니다. **L7(7계층, 애플리케이션 계층)** 은 HTTP의 URL 경로, Host 헤더, 쿠키처럼 사람이 읽는 수준의 내용을 봅니다. kube-proxy가 L4, Ingress Controller가 L7에서 동작한다는 뜻입니다.

| 구분 | L4 (kube-proxy) | L7 (Ingress Controller) |
|------|-----------------|------------------------|
| 확인하는 것 | IP, Port | URL 경로, Host 헤더 |
| 비유 | 고속도로 분기점 | 건물 안내 데스크 |
| JSON 파싱 | 안 함 | 안 함 |

JSON을 해석하고 비즈니스 로직을 태우는 건 최종 목적지인 **Pod 안의 애플리케이션**이 하는 일입니다. 네트워크 계층은 어디까지나 **전달**만 합니다.

### 5.2.3 Ingress 리소스와 Ingress Controller

Ingress 쪽에는 용어가 두 개 있어서 처음엔 헷갈립니다. **Ingress 리소스**와 **Ingress Controller**. 비슷해 보이지만 역할이 다릅니다.

> **참고: Ingress 리소스 vs Ingress Controller**
> - **Ingress 리소스**: 클러스터 외부의 HTTP/HTTPS 요청을 내부 어느 Service로 보낼지 **라우팅 규칙을 YAML로 선언**하는 K8s 오브젝트입니다. 규칙만 담고 있을 뿐, 스스로 요청을 받지는 않습니다.
> - **Ingress Controller**: 위의 Ingress 리소스(규칙)를 읽어 **실제로 외부 요청을 받아 처리하는 소프트웨어**입니다. Nginx Ingress Controller가 대표적입니다.

![](../assets/CH04/k8s-step4c.png)

*그림 5-14 외부 요청은 Ingress를 통해 Service로 전달*

| 구성 요소 | 역할 | 비유 |
|-----------|------|------|
| **Ingress 리소스** | 어떤 요청을 어떤 Service로 보낼지 정의한 규칙 (YAML) | 안내 데스크의 부서 안내판 |
| **Ingress Controller** | 실제로 외부 요청을 받아 처리하는 소프트웨어 | 안내 데스크에 앉은 직원 |

리소스(YAML)는 "규칙을 적어둔 안내판"이고 Controller는 "그 안내판을 읽고 실제로 손님을 안내하는 직원"입니다. 둘 다 있어야 Ingress가 동작합니다. 규칙만 있고 직원이 없으면 안내판은 벽에 붙은 종이고, 직원만 있고 규칙이 없으면 어디로 안내할지 모릅니다.

Minikube에서는 `minikube addons enable ingress` 한 줄로 Ingress Controller가 활성화됩니다. Ingress 리소스 YAML과 실제 배포는 다음 챕터 종합실습에서 Service 여러 개와 묶어 써 보게 됩니다.

## 5.3 브라우저에서 Pod까지 — 전체 경로 조립

### 5.3.1 요청의 여정

오픈이는 지금까지 쌓아둔 부품을 하나의 흐름으로 이어 봤습니다. 사용자가 브라우저에 URL을 치는 순간부터 Pod에 도달하기까지, 요청은 여러 손을 차례로 거칩니다.

![](../assets/CH05/net-10a-full-path.png)

*그림 5-15 외부 요청이 Pod에 도달하기까지의 전체 흐름*

| 단계 | 컴포넌트 | 하는 일 | 확인하는 것 |
|------|---------|--------|-----------|
| 1 | **브라우저** | 요청 전송 | - |
| 2 | **Ingress Controller** | URL 경로 확인 → 적절한 Service로 라우팅 | URL, Host |
| 3 | **Service** | Label-Selector로 매칭된 Pod 그룹에 요청 전달 | Label |
| 4 | **kube-proxy** | 네트워크 규칙으로 실제 Pod IP로 변환 | IP, Port |
| 5 | **Pod** | 애플리케이션이 요청을 처리 | 비즈니스 로직 |

각 단계마다 "확인하는 것"이 딱 하나씩입니다. Ingress는 URL만, Service는 Label만, kube-proxy는 IP/Port만, Pod만 마지막에 비즈니스 로직을 태웁니다. 겹치는 일 없이 역할이 깔끔하게 나뉘어 있습니다. 네트워크 계층은 전달만 하고, 비즈니스 로직은 Pod 안에서 본다는 원칙이 이 표 다섯 줄에 담겨 있습니다.

오늘 대목표였던 "외부 브라우저에서 URL로 내 앱에 접근하는 전체 경로"가 이 표 하나에 담겨 있습니다. 다음 챕터 종합실습에서는 이 경로가 실제로 동작하는 모습을 확인해 봅니다.

### 5.3.2 Docker에서 Kubernetes로 — 같은 원리, 다른 이름

오픈이는 펜을 내려놓고 노트를 앞쪽으로 넘겼습니다. 챕터 2 마지막에 적어둔 작은 표, "컨테이너 통신 지도"가 거기 있었습니다. 그때 "나중에 챕터 5에서 Kubernetes 버전으로 다시 옵니다"라고 적어 뒀던 표.

이번엔 그 옆자리에 오늘 배운 이름들을 한 줄씩 옮겨 적어 봅니다. 왼쪽에 Docker 이름, 오른쪽에 Kubernetes 이름. 한 줄씩 적어 내려가다 보니 양쪽이 놀랄 만큼 같은 그림이라는 게 눈에 들어옵니다. **같은 원리, 다른 규모**. Docker는 호스트 한 대에서, 쿠버네티스는 클러스터 전체에서, 동일한 역할을 맡는 친구들이 이름만 바꿔 서 있을 뿐이었습니다.

*'CH02 푸드코트랑 진짜 같네.'*

| Docker | CH 섹션 | Kubernetes | CH 섹션 |
|--------|---------|-----------|---------|
| docker0 (bridge) | 2.5.2 | Pod 네트워크 | 4.3 |
| iptables DNAT | 2.5.3 | kube-proxy iptables | 5.1.6 |
| Docker DNS | 2.5.4 | CoreDNS + Service | 6.1 |
| 사용자 정의 네트워크 | 3.3 | Service (ClusterIP) | 5.1 |
| docker-compose 컨테이너명 DNS | 3.5 | Service 이름 기반 통신 | 6.1 |
| NGINX 경로 라우팅 | 3.2, 3.6 | Ingress Controller | 5.2 |

표를 관통하는 원리는 하나입니다. 포트 변환은 `iptables DNAT`이 그대로 하고, 이름으로 서로를 찾는 일은 DNS가 맡고, 경로에 따라 요청을 나누는 일은 NGINX 류가 합니다. Docker에서는 Docker 엔진·Docker DNS·`nginx.conf`가, 쿠버네티스에서는 kube-proxy·CoreDNS·Ingress Controller가 그 자리를 차지합니다. 설정 언어와 규모만 달라졌을 뿐입니다.

> **참고: CoreDNS (미리보기)**
> Kubernetes 안에서 **Service 이름을 ClusterIP로 바꿔주는 내장 DNS 서버**입니다. Service가 생성되는 순간 이름이 자동 등록되어, Pod는 IP 대신 `backend-service` 같은 이름으로 상대를 부릅니다. 챕터 2의 Docker DNS가 클러스터 규모로 확장된 것이며, 자세한 동작과 실습은 챕터 6에서 다룹니다.

오픈이는 노트에 한 줄 메모해 뒀습니다. **"Docker 네트워크는 혼자 사는 집. 쿠버네티스 네트워크는 같은 원리로 지은 대단지."**

## 이것만은 기억하자

- **Service는 Pod의 대표 전화번호.** Pod가 생겼다 사라지며 IP가 바뀌지만, Service는 고정된 접근점을 제공하고 여러 Pod 사이에 요청을 돌려가며 나눠줍니다. 세 포트(`nodePort`/`port`/`targetPort`)는 각각 노드·Service·Pod 입장의 번호입니다.
- **kube-proxy는 챕터 2 iptables가 클러스터로 확장된 것.** ClusterIP는 어디에도 할당되지 않은 가상 주소로, 커널이 iptables DNAT로 실제 Pod IP로 바꿔 보냅니다. Endpoint Controller가 Pod IP 변화를 감시해 주소록을 최신으로 유지합니다.
- **Ingress는 건물 안내 데스크.** L4 고속도로 분기점(kube-proxy)은 IP/Port만 보고, L7 안내 데스크(Ingress Controller)는 URL과 Host를 읽습니다. 규칙을 적는 **Ingress 리소스**와 규칙을 집행하는 **Ingress Controller**는 서로 다릅니다.
- **Docker 네트워크가 이름만 바꿔 Kubernetes에서 반복됩니다.** iptables DNAT → kube-proxy, 컨테이너명 DNS → CoreDNS + Service 이름, NGINX 경로 라우팅 → Ingress Controller. 같은 원리, 다른 규모입니다.

오늘 대목표였던 "Pod IP 변동에도 끊기지 않는 주소"와 "브라우저에서 URL로 접근하는 경로"가 이 챕터에서 완성됐습니다. 다음 챕터에서는 이 경로 위에 **설정·비밀번호·데이터 영속성**을 얹고, 챕터 3에서 만든 풀스택 구성을 Kubernetes 위에 실제로 배포해 봅니다.
