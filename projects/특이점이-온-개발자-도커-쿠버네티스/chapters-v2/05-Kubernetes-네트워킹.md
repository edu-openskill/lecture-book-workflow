# Ch.5 Kubernetes 네트워킹

> 한 줄 요약: Service로 Pod에 고정 주소를 부여하고, Ingress로 외부 요청을 라우팅한다
> 핵심 개념: Service, kube-proxy, Ingress, L4/L7, Label-Selector

Pod를 띄우고 Deployment로 자동 복구까지 할 수 있게 되었습니다. 그런데 한 가지 문제가 있습니다. Pod IP가 죽을 때마다 바뀌는데, 이것을 어떻게 찾아갈 수 있을까요? 3장에서 Docker 네트워크가 어떻게 진화했는지 기억하시죠. 기본 bridge에서 이름 통신이 안 되던 것을 사용자 정의 네트워크로 해결했고, Compose가 자동화까지 해줬습니다. 쿠버네티스에서도 같은 이야기가 더 큰 스케일로 벌어집니다.

## 5.1 Service : Pod의 대표 전화번호

### 5.1.1 왜 Service가 필요한가

Pod IP는 Pod가 죽으면 바뀝니다. 직접 확인해 보겠습니다.

**[실습]** `Pod`의 IP는 재시작 시 변경됩니다. IP를 확인한 후 `Pod`를 삭제하고 다시 조회하면 IP가 달라진 것을 볼 수 있습니다.
```bash
kubectl get pod -o wide           # IP 확인 (예: 10.244.0.7)
kubectl delete pod --all          # Pod 삭제
kubectl get pod -o wide           # IP 변경됨 (예: 10.244.0.8)
```

![](../assets/CH04/08_pod-ip-change.png)
*Pod 재시작 시 IP 변경 확인*

이러면 고정 주소가 필요합니다. 그것이 **Service** 입니다. 콜센터 대표 번호를 생각하면 됩니다. 상담사 개인 번호를 몰라도 대표 번호로 걸면 연결되는 것처럼, Service는 Pod 앞에 고정 주소를 하나 만들어줍니다.

![](../assets/CH05/k8s-step3.png)
*Service는 고정 주소를 제공합니다. Pod IP가 바뀌어도 Service 주소는 그대로입니다*

> **Service** 는 Pod에 접근할 때 고정 IP를 제공해 안정적으로 접근할 수 있게 하는 리소스입니다.

### 5.1.2 Service 생성

`Service`는 `Deployment`처럼 selector의 라벨이 일치하는 `Pod`를 관리합니다. service-ex01.yml은 `NodePort` 타입의 `Service`를 정의하며, 외부에서 접근할 수 있게 합니다.

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

Service의 포트는 외부 요청이 Pod까지 도달하는 경로를 정의합니다. 트래픽은 외부 -> `nodePort` -> `port` -> `targetPort` -> Pod 순서로 전달됩니다.

| 포트 종류 | 역할 | 생략 시 |
|----------|------|--------|
| `port` | 클러스터 내부에서 Service에 접근하는 포트 | 필수 |
| `targetPort` | Service가 트래픽을 전달할 Pod의 포트 | `port` 값과 동일하게 설정 |
| `nodePort` | 외부에서 노드 IP로 접근할 때 사용하는 포트 (30000~32767) | 범위 내 자동 할당 |

**[실습]** `Service`를 생성합니다.
```bash
kubectl apply -f service-ex01.yml     # Service 생성
```

![](../assets/CH04/10_kubectl-apply-service.png)
*Service 생성*

### 5.1.3 Label-Selector 매칭

4장에서 Deployment의 selector를 배웠습니다. Service도 같은 방식을 씁니다.

Service가 Pod를 찾는 유일한 방법은 **label** 입니다. selector에 `app: nginx`라고 적으면, 그 라벨을 가진 Pod만 연결됩니다.

```
Service (Selector: app=web)
        ↓ 매칭
Pod A (Label: app=web)  ← 연결됨
Pod B (Label: app=api)  ← 연결 안 됨
```

[GEMINI PROMPT: Selector가 app=web인 Service가 app=web 라벨의 Pod만 연결하고, app=api 라벨의 Pod는 연결하지 않는 매칭 다이어그램. 왼쪽에 Service 박스, 오른쪽에 Pod 3개. 매칭되는 것은 실선, 안 되는 것은 점선+X 표시]

![](../assets/CH05/label-selector-matching.png)
*Service는 selector와 일치하는 label을 가진 Pod만 연결합니다*

### 5.1.4 Service 타입

아까 작성한 YAML에 `type: NodePort`가 있었습니다. **NodePort** 는 노드의 실제 IP에 실제 포트(30000~32767)를 열어서 외부에서 접근할 수 있게 해주는 Service 타입입니다.

![](../assets/CH04/ch4-service-2-nodeport.png)
*NodePort --- 노드의 실제 IP + 실제 포트로 외부 접근 가능합니다*

타입을 명시하지 않으면 기본 타입인 **ClusterIP** 가 적용됩니다. 내선 번호와 같아서 클러스터 안에서만 통합니다.

![](../assets/CH04/ch4-service-1-clusterip.png)
*ClusterIP --- 클러스터 내부에서만 접근 가능합니다*

그렇다면 외부에서 접근해야 할 때 항상 NodePort를 쓰면 될까요? NodePort는 노드 IP를 직접 알아야 합니다. 클라우드에서는 **LoadBalancer** 타입을 사용하면 공인 IP를 자동으로 만들어주고, 여러 노드에 트래픽도 알아서 나눠줍니다.

![](../assets/CH04/ch4-service-3-loadbalancer.png)
*LoadBalancer --- 클라우드 LB가 공인 IP로 여러 노드에 트래픽을 분산합니다*

| 타입 | 접근 범위 | 사용 사례 |
|------|----------|----------|
| **ClusterIP** | 클러스터 내부만 | 백엔드, DB 등 외부 노출 불필요한 서비스 |
| **NodePort** | 노드IP:포트로 외부 접근 가능 | 테스트, 개발 환경 |
| **LoadBalancer** | 공인 IP로 외부 접근 가능 | 클라우드 운영 환경 |

### 5.1.5 kube-proxy : 보이지 않는 경비원

Service를 만들면 고정 IP(ClusterIP)가 부여됩니다. 그런데 이 IP는 어떤 네트워크 장비에도 할당되지 않은 **가상 IP** 입니다.

진짜 IP가 아닌데 어떻게 요청이 도달할까요? 2장에서 Docker가 포트포워딩에 iptables를 사용한 것을 기억하시죠. kube-proxy가 같은 일을 합니다. 'ClusterIP로 오는 요청은 이 Pod로 보내라'고 iptables 규칙을 세워두는 것입니다.

4장에서 kube-proxy가 모든 워커 노드에 존재한다고 배웠습니다. kube-proxy는 두 곳에서 일합니다.

- **NodePort 처리**: 외부에서 노드 포트로 들어온 요청을 올바른 Pod로 전달
- **ClusterIP 처리**: 클러스터 내부에서 Service의 가상 IP로 온 요청을 실제 Pod IP로 변환

[GEMINI PROMPT: kube-proxy의 이중 역할을 보여주는 다이어그램. 왼쪽에서 두 갈래 화살표가 kube-proxy로 들어옴 — 하나는 "외부 요청 (NodePort:30080)"이고 다른 하나는 "내부 요청 (ClusterIP:80)". kube-proxy 안에 "iptables 규칙"이 있고, 오른쪽으로 "실제 Pod IP (10.244.0.5:80)"로 나감]

![](../assets/CH05/kube-proxy-dual-role.png)
*kube-proxy는 NodePort 처리와 ClusterIP 처리를 모두 담당합니다*


그런데 Pod IP는 Pod가 죽고 다시 태어날 때마다 바뀝니다. kube-proxy의 iptables 규칙은 누가 갱신할까요?

**Endpoint Controller** 가 이 역할을 합니다. Pod의 IP가 변하는 것을 감시하다가, 바뀌면 Service와 Pod 사이의 매핑 정보(Endpoints)를 자동으로 갱신합니다. kube-proxy는 이 갱신된 Endpoints를 보고 iptables 규칙을 업데이트합니다.

[GEMINI PROMPT: Endpoint Controller의 역할을 보여주는 흐름도. Pod가 죽고 새 Pod가 생기면(IP 변경), Endpoint Controller가 감지하여 Endpoints를 갱신하고, kube-proxy가 갱신된 Endpoints를 보고 iptables 규칙을 업데이트하는 순환 구조]

![](../assets/CH05/endpoint-controller.png)
*Endpoint Controller가 Pod IP 변화를 감시하고, kube-proxy가 규칙을 갱신합니다*

정리하면, Service가 고정 주소를 주고, kube-proxy가 실제 전달을 하고, Endpoint Controller가 매핑을 최신으로 유지합니다. 3장에서 Docker DNS가 컨테이너 이름을 IP로 바꿔준 것처럼, 쿠버네티스에서는 이 세 가지가 팀으로 같은 일을 합니다.

### 5.1.6 Networking

`Service`를 생성했지만, 로컬 PC와 미니큐브는 서로 다른 네트워크에 있어 Service의 IP로 직접 접근할 수 없습니다. `minikube service` 명령어로 임시 경로를 생성합니다.

> **minikube service** 명령어는 특정 Service에 대해 임시 접근 경로를 생성해, 로컬 PC에서 그 Service에 바로 접속할 수 있도록 합니다.

**[실습]** 로컬 PC에서 `Service`에 접속할 수 있는 URL을 생성합니다.
```bash
minikube service nginx-service --url  # Service 접근 URL 생성
```

![](../assets/CH04/chap03-43.png)
*minikube service URL 생성*

생성된 URL로 접속하면 미니큐브 내부 `Service`를 거쳐 `Pod` 서버로 요청이 전달됩니다.

![](../assets/CH04/chap03-44.png)
*브라우저에서 nginx 접속 확인*

확인 후 CTRL + C를 입력해 터미널을 빠져나옵니다.

이번에는 `Pod`를 전부 삭제한 뒤 다시 접속해 보겠습니다.

**[실습]** `Pod`를 삭제하고, `minikube service` 명령어로 다시 접근합니다.
```bash
kubectl delete pod --all              # 전체 Pod 삭제
minikube service nginx-service --url  # Service 접근 URL 생성
```

![](../assets/CH04/11_delete-pod-minikube-service.png)
*Pod 삭제 후 Service 접속*

새 URL로 접속하면 nginx 페이지가 정상적으로 표시됩니다. `Service`가 고정 접근 경로를 유지하므로 Pod가 재실행되어도 연결이 끊기지 않습니다.

**[실습]** 실습이 끝난 후 `Deployment`와 `Service`를 삭제합니다.
```bash
kubectl delete deployment nginx-replica   # Deployment 삭제
kubectl delete service nginx-service     # Service 삭제
```

## 5.2 Ingress : 건물 안내 데스크

Service로 접근은 가능해졌지만, `minikube service` 명령어는 테스트용 임시 경로입니다. 실제 운영 환경에서는 `http://my-service.com` 같은 도메인으로 접속합니다.

도메인으로 접속하려면 어떻게 해야 할까요? **Ingress** 를 사용해야 합니다. 3장에서 NGINX가 URL을 보고 요청을 나눠준 것을 기억하시죠. Ingress Controller가 쿠버네티스 안에서 같은 역할을 합니다.

### 5.2.1 L4 vs L7

요청이 Pod에 도달하기까지 여러 계층을 지나갑니다. 각 계층은 확인하는 범위가 다릅니다.

고속도로 톨게이트를 생각해 보세요. 톨게이트는 차가 왔다는 사실과 어느 방향인지만 확인합니다. 차 안에 뭐가 실려 있는지, 운전자가 누구인지는 보지 않습니다. 빠르지만 판단이 단순합니다.

건물 1층 안내 데스크는 다릅니다. 방문자가 어느 부서를 찾는지, 약속이 있는지 확인한 뒤 적절한 층으로 안내합니다. 느리지만 판단이 정확합니다.

[GEMINI PROMPT: L4와 L7의 비교. 왼쪽은 "L4 톨게이트" — 차가 지나가는 톨게이트, "IP/Port만 확인, 빠름" 설명. 오른쪽은 "L7 안내 데스크" — 건물 로비에서 안내하는 직원, "URL/Host 확인, 정확함" 설명. 둘 다 아래에 "JSON 파싱: 안 함"으로 공통점 표시]

![](../assets/CH05/l4-vs-l7.png)
*L4는 빠른 분배, L7은 정확한 라우팅을 담당합니다*

| 구분 | L4 (kube-proxy) | L7 (Ingress Controller) |
|------|-----------------|------------------------|
| 확인하는 것 | IP, Port | URL 경로, Host 헤더 |
| 비유 | 고속도로 톨게이트 | 건물 안내 데스크 |
| JSON 파싱 | 안 함 | 안 함 |

그렇다면 JSON 파싱은 누가 할까요? 최종 목적지인 **Pod 안의 애플리케이션** 이 처리합니다. 네트워크 계층은 요청을 전달할 뿐, 내용을 해석하지 않습니다.

> **참고: 계층별 역할 분담**
>
> | 계층 | 컴포넌트 | 확인하는 것 | 안 하는 것 |
> |------|---------|-----------|-----------|
> | L4 | kube-proxy | IP, Port | URL, Host, JSON |
> | L7 | Ingress Controller | URL 경로, Host 헤더 | JSON 파싱 |
> | App | Pod (Spring 등) | JSON, 인증, 비즈니스 로직 | 라우팅, 포트 변환 |

### 5.2.2 Ingress 리소스

> **Ingress** 는 클러스터 외부의 HTTP/HTTPS 요청을 내부 Service로 라우팅하는 규칙을 정의하는 리소스입니다.

![](../assets/CH05/k8s-step4c.png)
*외부 요청은 Ingress를 통해 Service로 전달됩니다*

`Ingress`가 동작하려면 두 가지가 갖춰져야 합니다.

| 구성 요소 | 역할 | 비유 |
|-----------|------|------|
| **Ingress Controller** | 실제로 외부 요청을 받아 처리하는 소프트웨어 | 안내 데스크에 앉아있는 직원 |
| **Ingress 리소스** | 어떤 요청을 어떤 Service로 보낼지 정의한 규칙 | 안내 데스크에 놓인 부서 안내판 |

`Ingress Controller`는 Nginx를 주로 사용하며, 미니큐브에서는 `minikube addons enable ingress` 명령어 한 줄로 활성화합니다. Ingress 리소스의 실습은 6장 종합 실습에서 함께 다룹니다.

## 5.3 전체 흐름 : 브라우저에서 Pod까지

### 5.3.1 요청의 여정

지금까지 배운 부품들을 하나의 흐름으로 조립할 차례입니다.

브라우저에서 주소를 치는 순간부터 Pod까지 어떻게 도달하는지 따라가 보겠습니다.

[GEMINI PROMPT: 전체 트래픽 흐름 다이어그램. 왼쪽에서 오른쪽으로 흐름. 브라우저 → Ingress Controller(L7: URL 확인) → Service(Label-Selector 매칭) → kube-proxy(iptables: 실제 Pod IP로 변환) → Pod(JSON 파싱, 비즈니스 로직). 각 단계마다 "확인하는 것"과 "안 하는 것"을 작은 텍스트로 표시]

![](../assets/CH05/full-traffic-flow.png)
*외부 요청이 Pod에 도달하기까지의 전체 흐름입니다*

| 단계 | 컴포넌트 | 하는 일 | 확인하는 것 |
|------|---------|--------|-----------|
| 1 | **브라우저** | 요청 전송 | - |
| 2 | **Ingress Controller** | URL 경로 확인 → 적절한 Service로 라우팅 | URL, Host |
| 3 | **Service** | Label-Selector로 매칭된 Pod 그룹에 요청 전달 | Label |
| 4 | **kube-proxy** | iptables 규칙으로 실제 Pod IP로 변환 | IP, Port |
| 5 | **Pod** | 애플리케이션이 요청을 처리 | JSON, 비즈니스 로직 |

네트워크 쪽은 전달만 하고, 진짜 일은 Pod 안에서 합니다. 각자 역할이 명확한 것이 쿠버네티스 네트워킹의 핵심입니다.

### 5.3.2 Docker에서 Kubernetes로

2장과 3장에서 배운 Docker 네트워크 개념이 쿠버네티스에서 어떻게 확장되었는지 정리합니다.

| Docker | Kubernetes | 배운 챕터 |
|--------|-----------|----------|
| docker0 (bridge) | Pod 네트워크 | CH02 → CH04 |
| iptables DNAT (`-p` 포트포워딩) | kube-proxy iptables | CH02 → CH05 |
| Docker DNS (127.0.0.11) | CoreDNS | CH03 → CH06 |
| NGINX 경로 라우팅 | Ingress Controller | CH03 → CH05 |
| docker network create | Service (ClusterIP) | CH03 → CH05 |
| Docker Compose 자동 네트워크 | Namespace + Service DNS | CH03 → CH06 |

Docker에서 배운 것이 쿠버네티스에서도 그대로 쓰입니다. 이름만 달라졌을 뿐 원리는 같습니다.

3장의 Docker 네트워크 진화 표를 기억하시죠? 같은 패턴이 쿠버네티스에서 반복됩니다.

| Docker의 문제 | Docker의 해결 | K8s에서 같은 역할 |
|-------------|-------------|----------------|
| 기본 bridge에서 이름 통신 불가 | 사용자 정의 네트워크 + DNS | Service + CoreDNS |
| 포트포워딩 수동 설정 | docker-compose.yml에 정의 | Service YAML에 정의 |
| NGINX로 URL 기반 라우팅 | nginx.conf 작성 | Ingress 리소스 YAML |

## 이것만은 기억하자

- **Service는 Pod의 대표 전화번호입니다.** Pod는 생겼다 사라지며 IP가 바뀌지만, Service는 고정된 접근점을 제공합니다.

- **kube-proxy는 보이지 않는 경비원입니다.** 2장에서 배운 iptables가 클러스터 전체로 확장된 것입니다. NodePort 처리와 ClusterIP 처리를 모두 담당하고, Endpoint Controller가 Pod IP 변화를 감시하여 규칙을 최신으로 유지합니다.

- **Ingress는 건물 안내 데스크입니다.** 3장의 NGINX가 URL 보고 요청을 나눠준 것처럼, Ingress Controller가 쿠버네티스 안에서 L7 라우팅을 담당합니다.

- **Docker의 네트워크가 Kubernetes에서 확장되었을 뿐, 원리는 같습니다.** iptables → kube-proxy, Docker DNS → CoreDNS, NGINX → Ingress Controller.

네트워크까지 연결되었으니, 이제 실제 서비스를 운영하는 데 필요한 것들을 다룹니다. 다음 장에서는 설정을 외부에서 주입하고, 데이터를 영구 보존하며, 3장에서 만든 웹사이트를 쿠버네티스 위에 배포합니다.
