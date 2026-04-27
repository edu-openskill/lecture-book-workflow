# ex14 — Volume (PV / PVC / Pod)

CH06 §6.2에서 사용. PersistentVolume 만들고 PersistentVolumeClaim으로 요청, Pod에 마운트.

## 적용

```bash
kubectl apply -f ex14/volume-pv.yml
kubectl apply -f ex14/volume-pvc.yml
kubectl apply -f ex14/volume-pod.yml
kubectl get pv,pvc,pod
```

또는 한 번에:

```bash
kubectl apply -f ex14/
```

Pod 안에 파일을 만들고, Pod를 삭제한 뒤 다시 띄워도 PV에 데이터가 살아남는지 확인합니다.

## 정리

```bash
kubectl delete -f ex14/
```
