# ex13 — ConfigMap + Secret

CH06 §6.1에서 사용. 일반 설정값(ConfigMap)과 민감 정보(Secret)를 이미지 바깥으로 빼서 Deployment에 주입.

`deploy-ex03.yml`은 ConfigMap만 연결한 상태로 시작합니다 (`secretRef` 두 줄은 주석 처리). Secret 단계에서 그 주석을 풀고 다시 apply합니다.

## 1단계 — ConfigMap만 연결

```bash
kubectl apply -f ex13/configmap-conn.yml
kubectl apply -f ex13/deploy-ex03.yml
kubectl get pod                          # Pod 이름 확인
kubectl exec -it <Pod명> -- env          # Pod 환경 변수 조회
```

## 2단계 — Secret 추가 연결

`deploy-ex03.yml` 의 `secretRef` 두 줄(`#` 주석)을 풀어 줍니다.

```bash
kubectl apply -f ex13/secret-password.yml
kubectl apply -f ex13/deploy-ex03.yml       # Secret까지 연결한 변경판 적용
kubectl get pod                             # 새 Pod 이름 확인
kubectl exec -it <Pod명> -- env             # Pod 환경 변수 조회
```

## 3단계 — ConfigMap 값 변경 후 rollout 확인

`configmap-conn.yml` 의 `conn_info` 포트를 80에서 90으로 바꾸고 다시 apply하면 `configured` 메시지는 뜨지만 Pod 안 환경 변수는 그대로입니다. Pod를 재시작해야 새 값이 반영됩니다.

```bash
kubectl apply -f ex13/configmap-conn.yml
kubectl rollout restart deployment nginx-config-secret
```

## 정리

```bash
kubectl delete -f ex13/
```
