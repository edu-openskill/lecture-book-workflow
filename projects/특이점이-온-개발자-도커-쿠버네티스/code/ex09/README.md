# ex09 — Deployment 기본

CH04 §4.4에서 사용. nginx Pod 1개를 유지하는 Deployment.

## 적용

```bash
kubectl apply -f ex09/deploy-ex01.yml
kubectl get deploy,pod
```

## 정리

```bash
kubectl delete -f ex09/deploy-ex01.yml
```
