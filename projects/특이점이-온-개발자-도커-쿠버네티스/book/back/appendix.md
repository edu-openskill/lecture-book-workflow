# 부록: 더 깊이 공부하기

이 책에서 전체 그림을 잡았다면, 이제 각 기술을 더 깊이 파고들 차례입니다. 아래 자료들은 다음 단계로 나아가는 데 도움이 됩니다.

---

## Docker

| 자료 | 설명 |
|------|------|
| Docker 공식 문서 | docs.docker.com — 명령어 레퍼런스, Dockerfile 작성법, 네트워크 설정 등 가장 정확한 자료 |
| Docker Hub | hub.docker.com — 공식 이미지 검색 및 사용법 확인 |
| Docker Compose 공식 문서 | docs.docker.com/compose — Compose 파일 문법, 멀티 컨테이너 구성 심화 |

**이 책에서 다루지 않은 Docker 심화 주제**:
- Docker 네트워크 종류 (bridge, host, overlay)
- 멀티 스테이지 빌드 (이미지 크기 최적화)
- Docker 보안 (rootless 모드, 이미지 스캐닝)
- .dockerignore 활용

---

## Kubernetes

| 자료 | 설명 |
|------|------|
| Kubernetes 공식 문서 | kubernetes.io/docs — 개념 설명, 튜토리얼, API 레퍼런스 |
| Kubernetes 공식 튜토리얼 | kubernetes.io/docs/tutorials — 단계별 실습 가이드 |
| kubectl 치트시트 | kubernetes.io/docs/reference/kubectl/cheatsheet — 자주 쓰는 명령어 모음 |

**이 책에서 다루지 않은 K8s 심화 주제**:
- Ingress (외부 트래픽 라우팅)
- HPA (수평 자동 확장)
- Helm (패키지 매니저)
- RBAC (역할 기반 접근 제어)
- 클라우드 배포 (AWS EKS, Google GKE, Azure AKS)

---

## 이 책의 예제 코드

이 책에서 사용한 모든 예제 코드는 아래 저장소에서 확인할 수 있습니다.

- **GitHub**: 저장소 URL (추후 추가)

각 장별 예제 폴더 구조:

```
ex01~ex03/  →  2장 NGINX 실습
ex04/       →  2장 Redis 실습
ex05/       →  2장 DB Server 실습
ex06/       →  2장 Docker Compose 실습
ex07/       →  2장 풀스택 웹사이트
ex08/       →  3장 K8s 풀스택 웹사이트
yaml/       →  3장 K8s 리소스 실습
```

---

## 주요 명령어 모음

### Docker 명령어

| 명령어 | 설명 |
|--------|------|
| `docker pull [이미지]` | 이미지 다운로드 |
| `docker run [옵션] [이미지]` | 컨테이너 실행 |
| `docker ps` | 실행 중인 컨테이너 목록 |
| `docker ps -a` | 모든 컨테이너 목록 |
| `docker stop [컨테이너]` | 컨테이너 중지 |
| `docker rm [컨테이너]` | 컨테이너 삭제 |
| `docker images` | 이미지 목록 |
| `docker rmi [이미지]` | 이미지 삭제 |
| `docker build -t [태그] .` | Dockerfile로 이미지 빌드 |
| `docker commit [컨테이너] [이미지명]` | 컨테이너를 이미지로 저장 |
| `docker push [이미지]` | 이미지를 레지스트리에 업로드 |
| `docker exec -it [컨테이너] bash` | 실행 중인 컨테이너에 접속 |
| `docker compose up -d` | Compose로 서비스 실행 |
| `docker compose down` | Compose 서비스 중지 및 삭제 |

### kubectl 명령어

| 명령어 | 설명 |
|--------|------|
| `kubectl get pods` | Pod 목록 조회 |
| `kubectl get deployments` | Deployment 목록 조회 |
| `kubectl get services` | Service 목록 조회 |
| `kubectl apply -f [파일]` | YAML 파일로 리소스 생성/수정 |
| `kubectl delete -f [파일]` | YAML 파일의 리소스 삭제 |
| `kubectl describe [리소스] [이름]` | 리소스 상세 정보 |
| `kubectl logs [Pod명]` | Pod 로그 확인 |
| `kubectl exec -it [Pod명] -- bash` | Pod 내부 접속 |
| `kubectl set image deployment/[이름] [컨테이너]=[이미지]` | 이미지 업데이트 |
| `kubectl rollout undo deployment/[이름]` | 이전 버전으로 롤백 |
| `kubectl rollout restart deployment/[이름]` | Deployment 재시작 |
| `minikube start` | 미니큐브 클러스터 시작 |
| `minikube service [서비스명] --url` | 서비스 접근 URL 확인 |
