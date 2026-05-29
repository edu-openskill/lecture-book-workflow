
#### 미니큐브 실행

- minikube start
- minikube addons enable ingress

#### 이미지 빌드

- minikube image build -t metacoding/db:1 ex15/db
- minikube image build -t metacoding/backend:1 ex15/backend
- minikube image build -t metacoding/frontend:1 ex15/frontend
- minikube image build -t metacoding/redis:1 ex15/redis

#### namespase 적용

- kubectl apply -f ex15/k8s/namespace.yml

#### pod 생성

- kubectl apply -f ex15/k8s/ --recursive

### 결과 확인

- kubectl get deploy,pod,service,ingress -n metacoding

### 로그 확인

 - kubectl logs -l app=backend -n metacoding --tail=100 --prefix

### 외부 진입 터널 (별도 터미널)

- minikube tunnel

### 접속

- http://127.0.0.1