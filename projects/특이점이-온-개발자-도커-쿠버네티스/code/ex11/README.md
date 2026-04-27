# ex11 — Service (NodePort)

CH05 §5.1에서 사용. 4개의 nginx Pod를 NodePort Service로 묶어 외부 접근 허용.

`deploy-ex02.yml`은 ex10와 동일한 파일을 자체 보관 (자기 폴더 안에서 완결되도록).

## 적용

```bash
kubectl apply -f ex11/deploy-ex02.yml      # Pod 4개 생성
kubectl apply -f ex11/service-ex01.yml     # NodePort Service 생성
kubectl get svc
```

또는 한 번에:

```bash
kubectl apply -f ex11/
```

`minikube service nginx-service --url`로 접속 URL 확인.

## 정리

```bash
kubectl delete -f ex11/
```
