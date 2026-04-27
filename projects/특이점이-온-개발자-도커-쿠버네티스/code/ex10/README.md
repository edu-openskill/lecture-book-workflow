# ex10 — Deployment 롤링 업데이트

CH04 §4.4에서 사용. replicas 4개 + RollingUpdate 전략(maxSurge:4, maxUnavailable:0)으로 무중단 배포.

## 적용

```bash
kubectl apply -f ex10/deploy-ex02.yml
kubectl get pods -w
```

이미지 태그를 바꿔서 다시 apply하면 무중단 롤링 업데이트가 동작합니다.

## 정리

```bash
kubectl delete -f ex10/deploy-ex02.yml
```
