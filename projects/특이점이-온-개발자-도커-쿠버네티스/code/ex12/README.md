# ex12 — Ingress 경로 기반 라우팅 실습

Ingress Controller와 Ingress 리소스를 분리해서 써 보고, 같은 호스트 아래 두 경로를 서로 다른 Service로 보내 보는 실습입니다.

- `localhost/order`  → `order-service`   ("주문 접수 완료")
- `localhost/stores` → `stores-service`  ("매장 선택")

## 파일 구조

```
ex12/
├── order-deploy.yml      # 주문 서비스 Deployment (http-echo)
├── order-service.yml     # 주문 서비스 ClusterIP Service
├── stores-deploy.yml     # 매장 서비스 Deployment (http-echo)
├── stores-service.yml    # 매장 서비스 ClusterIP Service
└── ingress-ex01.yml      # /order, /stores 라우팅 규칙
```

## 실행 순서

### 1. Ingress Controller 활성화

```bash
minikube addons enable ingress
kubectl get pods -n ingress-nginx
```

### 2. 전체 리소스 한 번에 배포

```bash
kubectl apply -f ex12/
kubectl get ingress
```

### 3. 터널 열기

Docker 드라이버 환경에서는 클러스터가 컨테이너 안에 있어 호스트에서 직접 닿지 않으므로, 별도 터미널에서 터널을 띄워 둡니다. 이 터널이 호스트의 `localhost`로 들어온 요청을 Ingress Controller까지 이어 줍니다.

```bash
minikube tunnel
```

### 4. 브라우저 또는 curl로 검증

```bash
curl http://localhost/order
# 주문 접수 완료

curl http://localhost/stores
# 매장 선택

curl -i http://localhost/
# 404 Not Found  (규칙에 없는 경로는 보내지 않음)
```

## 도메인 기반 라우팅

실제 운영 환경에서는 `rules` 아래에 `host: shop.example.com` 처럼 도메인을 적어 같은 클러스터 안에서도 도메인별로 다른 서비스를 받게 합니다. 실제 DNS가 이미 그 도메인을 클러스터로 연결해 두기 때문에 hosts 파일을 수동으로 매핑할 필요가 없습니다.

이 실습은 경로 분기만 눈으로 확인하려고 `host` 를 생략했습니다.

## 정리

```bash
kubectl delete -f ex12/
```
