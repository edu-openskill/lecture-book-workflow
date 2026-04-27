# Ch.6 Kubernetes 운영하기

> 한 줄 요약: 설정 분리, 데이터 보존으로 실제 서비스를 운영하고 종합 실습으로 완성한다
> 핵심 개념: ConfigMap, Secret, PV/PVC, Namespace

## 6.1 ConfigMap, Secret : 설정 분리

실제 서비스를 구성하려고 코드를 열었을 때, DB 비밀번호가 코드에 하드코딩되어 있다면 문제가 됩니다. 값이 바뀔 때마다 이미지를 다시 빌드해야 하기 때문입니다. **ConfigMap** 과 **Secret** 이 이 문제를 해결합니다.

![](../assets/CH05/k8s-step4a.png)
*ConfigMap과 Secret은 Pod에 설정과 민감 정보를 주입한다*

### 6.1.1 ConfigMap

데이터베이스 주소나 접속 URL 같은 설정 값을 코드에 직접 넣으면, 값이 바뀔 때마다 이미지를 다시 빌드해야 합니다. `ConfigMap`은 이런 설정 값을 코드 밖에서 관리합니다.

> **ConfigMap** 은 일반적인 설정 값을 외부에서 관리하는 리소스입니다. 환경 변수, 설정 파일 등 민감하지 않은 설정 정보를 저장하며, Pod는 이를 환경 변수로 전달받아 사용합니다.

**[참고]** Github 프로젝트의 `yaml/configmap-conn.yml`을 참고합니다.

**yaml/configmap-conn.yml**
```yaml
apiVersion: v1                       # API 버전
kind: ConfigMap                      # 리소스 종류
metadata:
  name: configmap-conn               # ConfigMap 이름 지정
data:                                # 설정값 넣는 영역
  conn_info: "localhost:80"          # 접속 정보
  conn_url: "config.test"            # 접속 URL
```

deploy-ex03.yml에서는 `envFrom.configMapRef`로 `ConfigMap`에 정의된 설정 값을 환경 변수로 `Pod`에 넣습니다.

**[참고]** Github 프로젝트의 `yaml/deploy-ex03.yml`을 참고합니다.

**yaml/deploy-ex03.yml**
```yaml
apiVersion: apps/v1                        # API 버전
kind: Deployment                           # 리소스 종류
metadata:
  name: nginx-config-secret                # 리소스 이름
spec:                                      # 상세 설정
  replicas: 1                              # pod 수 지정
  selector:                                # 관리할 Pod 선택 조건
    matchLabels:                           # 라벨이 일치하는 Pod 선택
      app: nginx                           # 라벨이 app : nginx인 pod를 관리
  template:                                # Pod 템플릿
    metadata:
      labels:                              # 라벨 지정
        app: nginx                          # pod에 붙일 라벨
    spec:                                  # 컨테이너 상세 설정
      containers:                          # 컨테이너 설정
        - name: nginx-container            # 컨테이너 이름
          image: nginx:1.20                # 사용할 이미지
          envFrom:                         # 환경 변수 일괄 주입
            - configMapRef:                # ConfigMap 참조
                name: configmap-conn         # ConfigMap 연결
```

**[실습]** `ConfigMap`과 `Deployment`를 생성합니다.
```bash
kubectl apply -f configmap-conn.yml   # ConfigMap 생성
kubectl apply -f deploy-ex03.yml     # Deployment 생성
```

**[실습]** `Pod`의 환경 변수를 조회하여 `ConfigMap` 설정이 적용되었는지 확인합니다. `kubectl get pod`로 먼저 Pod명을 확인한 뒤, 자신의 Pod명으로 바꿔서 실행합니다. Pod명의 해시값은 실행할 때마다 달라집니다.
```bash
kubectl get pod                       # Pod 목록 조회
kubectl exec -it <Pod명> -- env       # Pod 환경 변수 조회
```

![](../assets/CH05/chap03-46.png)
*Pod 환경 변수 조회*

출력된 환경 변수 중 `ConfigMap`에 설정한 `conn_info`와 `conn_url`이 보입니다.

### 6.1.2 Secret

그렇다면 DB 비밀번호도 ConfigMap에 넣으면 될까요? 비밀번호는 ConfigMap에 넣으면 안 됩니다. **Secret** 이라는 별도 리소스가 있습니다.

ConfigMap이 일반적인 환경 설정이라면, Secret은 **금고** 입니다. 비밀번호나 API 키처럼 민감한 정보는 설정표에 적어두면 안 됩니다. 금고에 따로 보관해야 합니다.

> **Secret** 은 비밀번호, 토큰, 인증 키처럼 민감한 정보를 안전하게 저장하고 관리하기 위한 리소스입니다. ConfigMap과 구조는 비슷하지만 Secret의 값은 Base64로 인코딩되어 저장됩니다. 단, Base64는 암호화가 아닌 단순 인코딩이므로 보안을 보장하지는 않습니다.

**[참고]** Github 프로젝트의 `yaml/secret-password.yml`을 참고합니다.

**yaml/secret-password.yml**
```yaml
apiVersion: v1              # API 버전
kind: Secret                # 리소스 종류
metadata:
  name: secret-password     # Secret 이름
stringData:                 # 평문을 자동으로 Base64 변환
  password: metacoding1234  # 비밀번호 설정
```

**[실습]** `Secret`을 생성합니다. stringData 속성을 쓰면 평문이 자동으로 Base64로 변환됩니다.
```bash
kubectl apply -f secret-password.yml  # Secret 생성
```

**[실습]** `Secret`의 내부를 YAML 형태로 출력합니다.
```bash
kubectl get secret secret-password -o yaml  # Secret 내용을 YAML 형태로 출력
```

![](../assets/CH05/chap03-48.png)
*Secret의 Base64 인코딩 확인*

`Secret`을 YAML 형태로 출력해보면 비밀번호가 Base64로 인코딩되어 있습니다.

### 6.1.3 환경 변수 추가

deploy-ex03.yml에 `Secret`을 추가해보겠습니다. `secretRef`를 쓰면 `Secret`에 정의된 값을 환경 변수로 `Pod`에 넣을 수 있습니다.

앞에서 작성한 deploy-ex03.yml의 `envFrom` 항목에 `secretRef`를 추가합니다. 추가된 부분만 표시합니다.

**yaml/deploy-ex03.yml**
```yaml
          # ... 생략

          envFrom:
            - configMapRef:
                name: configmap-conn         # ConfigMap 연결
            - secretRef:
                name: secret-password        # Secret 연결 (추가)
```

**[실습]** 변경된 `Deployment`를 적용합니다.
```bash
kubectl apply -f deploy-ex03.yml     # 변경된 Deployment 적용
```

**[실습]** `Pod`의 환경 변수를 조회하면 `Secret`에 저장된 비밀번호가 주입되어 출력됩니다.
```bash
kubectl get pod                       # Pod 목록 조회
kubectl exec -it <Pod명> -- env       # Pod 환경 변수 조회
```

![](../assets/CH05/13_secret-env.png)
*Pod 환경 변수에 Secret 값 확인*

`Secret`에 Base64로 인코딩된 비밀번호는 `Pod`에서 사용될 때 자동으로 평문으로 변환됩니다.

### 6.1.4 환경 변수 수정

운영 중에 DB 주소가 바뀌었습니다. ConfigMap을 수정하고 `kubectl apply`를 실행했는데, Pod에 바로 반영될까요? 그렇지 않습니다.

![](../assets/CH05/fig-3-6.png)
*ConfigMap 변경 후 Pod 재시작으로 반영되는 흐름*

환경 변수 같은 실행 환경 설정은 프로세스가 시작될 때 한 번만 적용됩니다. 변경된 설정을 반영하려면 **Pod를 재시작** 해야 합니다.

실습을 위해 configmap-conn.yml의 `conn_info` 포트를 90으로 수정해보겠습니다.

**yaml/configmap-conn.yml**
```yaml
# ... 생략

  conn_info: "localhost:90"          # 환경변수 수정
```

**[실습]** 변경된 `ConfigMap`을 적용하고 `Pod`를 재시작합니다.
```bash
kubectl apply -f configmap-conn.yml   # 변경된 ConfigMap 적용
kubectl rollout restart deployment nginx-config-secret  # 재시작
```

![](../assets/CH05/chap03-52.png)
*ConfigMap 수정 후 Pod 재시작*

**[실습]** 재시작된 `Pod`의 환경 변수를 확인합니다.
```bash
kubectl exec -it <Pod명> -- env       # Pod 환경 변수 조회
```

![](../assets/CH05/chap03-53.png)
*변경된 환경 변수 확인*

`conn_info` 변수의 포트가 90으로 변경되었습니다.

**[실습]** 다음 실습을 위해 생성한 리소스를 제거합니다.

```bash
kubectl delete deployment nginx-config-secret  # Deployment 삭제
kubectl delete configmap configmap-conn        # ConfigMap 삭제
kubectl delete secret secret-password          # Secret 삭제
```

### CoreDNS : 클러스터의 전화번호부

6.3절의 웹사이트 예제에서 ConfigMap에 **db-service:3306**, **redis-service:6379** 처럼 IP 대신 서비스 이름을 적게 됩니다. 이것이 가능한 이유는 쿠버네티스 안에 **CoreDNS** 라는 전용 DNS 서버가 돌고 있기 때문입니다.

5장의 Docker→Kubernetes 대응표에서 "Docker DNS → CoreDNS"를 기억하시죠? 3장에서 Docker DNS(127.0.0.11)가 사용자 정의 네트워크에서 컨테이너 이름을 IP로 변환해 주었듯이, CoreDNS는 Service 이름을 ClusterIP로 변환합니다.

Service가 생성되면 CoreDNS에 **서비스명.네임스페이스.svc.cluster.local** 형태의 DNS 레코드가 자동 등록됩니다. 같은 네임스페이스라면 서비스 이름만으로 충분합니다.

![](../assets/CH05/net-09-coredns.png)
*CoreDNS는 서비스 이름을 ClusterIP로 변환합니다*

DB Pod가 죽고 새로 태어나 IP가 바뀌더라도, 서비스 이름과 ClusterIP는 그대로이므로 설정을 바꿀 필요가 없습니다.

## 6.2 Volume : 데이터 보존

2장에서 컨테이너를 삭제하면 데이터가 날아가는 문제를 마운트로 해결했습니다. 쿠버네티스에서도 같은 문제가 있습니다. `Pod` 안에서 생성한 파일은 `Pod`이 재시작되면 모두 사라집니다. 로그 파일이나 데이터베이스처럼 데이터를 보존해야 한다면 `Volume`이 필요합니다.

> **볼륨(Volume)** 은 Pod 내부 컨테이너가 사용할 수 있는 외부 저장 공간을 의미합니다.

Volume에는 여러 종류가 있습니다.

| 종류 | 설명 | 데이터 유지 |
|------|------|------------|
| **emptyDir** | Pod 생성 시 만들어지는 임시 저장 공간. 같은 Pod 안의 컨테이너끼리 데이터를 공유할 때 사용 | Pod 삭제 시 함께 삭제 |
| **hostPath** | 워커 노드(호스트)의 특정 경로를 Pod에 마운트 | 노드에 남아 있지만, Pod가 다른 노드로 이동하면 접근 불가 |
| **PV / PVC** | 클러스터 외부에 영구 저장소를 만들고, 요청서(PVC)를 통해 Pod에 연결 | Pod가 삭제되어도 유지 |

실무에서 가장 많이 사용하는 `PV / PVC`를 실습해 보겠습니다.

### 6.2.1 Persistent storage

**Persistent storage** 는 Pod가 종료되어도 데이터가 사라지지 않는 영구 저장소입니다. 실제 저장 공간인 `PV`(PersistentVolume)와 그 공간을 요청하는 `PVC`(PersistentVolumeClaim)로 구성됩니다.

![](../assets/CH05/k8s-step4b.png)
*PV는 실제 저장 공간, PVC는 요청서. PVC를 통해 Pod에 저장소를 연결한다*

`PV`는 **창고** 공간이고, `PVC`는 **"10평짜리 창고가 필요합니다"라는 신청서**입니다. Pod는 PVC로 조건에 맞는 PV를 찾아 연결합니다. 실습 순서는 PV 생성 → PVC 생성 → Pod 연결입니다.

#### PV(PersistentVolume)

> **PV(PersistentVolume)** 는 실제 데이터가 저장되는 저장소입니다.

이번 실습에서는 미니큐브 내부의 경로를 저장소로 사용합니다.

**[참고]** Github 프로젝트의 `yaml/volume-pv.yml`을 참고합니다.

**yaml/volume-pv.yml**
```yaml
apiVersion: v1             # API 버전
kind: PersistentVolume     # 리소스 종류
metadata:
  name: volume-pv          # PV 이름
spec:                      # 상세 설정
  capacity:
    storage: 1Gi           # 1Gi 용량 할당
  accessModes:
    - ReadWriteOnce        # 읽기/쓰기 권한
  storageClassName: ""     # PVC가 볼륨을 자동으로 생성 못하게 방지
  hostPath:
    path: /mnt/data        # 볼륨 경로 지정
    type: DirectoryOrCreate # 경로가 없으면 자동 생성
```

`hostPath`의 `/mnt/data`는 미니큐브 내부 경로입니다. `type: DirectoryOrCreate`를 지정하면 해당 경로가 없을 때 자동으로 생성됩니다.

#### PVC(PersistentVolumeClaim)

저장 공간(PV)이 준비되었으니, 신청서(PVC)를 만듭니다.

> **PVC(PersistentVolumeClaim)** 는 Pod가 사용할 저장소의 조건(용량, 접근 모드 등)을 정의한 요청서입니다.

**[참고]** Github 프로젝트의 `yaml/volume-pvc.yml`을 참고합니다.

**yaml/volume-pvc.yml**
```yaml
apiVersion: v1                 # API 버전
kind: PersistentVolumeClaim    # 리소스 종류
metadata:
  name: volume-pvc             # pod가 참조하는 pvc명
spec:                          # 상세 설정
  accessModes:
    - ReadWriteOnce        # 읽기 쓰기 권한
  storageClassName: ""     # PVC가 자동으로 PV 생성하지 않도록 설정
  resources:
    requests:
      storage: 1Gi         # 용량
  volumeName: volume-pv    # 참조할 PV명
```

`PVC`가 `PV`와 바인딩되려면 `accessModes`와 `storageClassName` 설정이 서로 일치해야 하고, 요청 용량이 `PV` 용량 이하여야 합니다.

PV와 PVC가 준비되었으니 Pod에 연결해 보겠습니다.

**[참고]** Github 프로젝트의 `yaml/volume-pod.yml`을 참고합니다.

**yaml/volume-pod.yml**
```yaml
apiVersion: v1                   
kind: Pod                        
metadata:
  name: volume-pod               
spec:                            # 상세 설정
  containers:                    
  - name: nginx-volume           
    image: nginx                 
    volumeMounts:                # 사용할 볼륨 마운트
    - name: storage              # 볼륨 이름
      mountPath: /mnt/data       # 컨테이너에서 접근할 볼륨 위치
  volumes:                       # 볼륨 정의
  - name: storage                # 볼륨 이름
    persistentVolumeClaim:       # PVC 연결
      claimName: volume-pvc      # 참조할 PVC
```

**[실습]** `PV`, `PVC`, `Pod`를 순서대로 생성합니다.
```bash
kubectl apply -f volume-pv.yml        # PV 생성
kubectl apply -f volume-pvc.yml       # PVC 생성
kubectl apply -f volume-pod.yml       # Pod 생성
```

**[실습]** `PV`와 `PVC`의 바인딩 상태를 확인합니다. `STATUS` 값이 **BOUND**이면 정상입니다.
```bash
kubectl get pv,pvc            # PV와 PVC 바인딩 상태 확인
```

![](../assets/CH05/chap03-60.png)
*PV와 PVC 바인딩 상태 확인*

**[실습]** 컨테이너 내부에 접속하여 `/mnt/data` 경로에 파일을 생성합니다.
```bash
kubectl exec -it volume-pod -- /bin/bash  # Pod 내부 접속
touch /mnt/data/c.txt                    # 볼륨 경로에 파일 생성
ls /mnt/data                             # 파일 목록 확인
exit                                     # Pod에서 빠져나오기
```

![](../assets/CH05/chap03-61.png)
*볼륨 경로에 파일 생성*

`/mnt/data` 경로에 파일이 정상적으로 생성되었습니다. 이제 Pod를 삭제하고 다시 만들어도 파일이 남아있는지 확인해 보겠습니다.

**[실습]** `Pod`를 삭제한 뒤 다시 생성하고, 파일이 보존되었는지 확인합니다.
```bash
kubectl delete pod volume-pod             # Pod 삭제
kubectl apply -f volume-pod.yml           # 같은 PVC로 Pod 재생성
kubectl exec -it volume-pod -- /bin/bash  # 파일 확인
ls /mnt/data                              # 파일 확인
```

![](../assets/CH05/42_volume-pod-preserved.png)
*Pod 재생성 후에도 파일이 보존됨*

`c.txt`가 그대로 남아 있습니다. Pod는 사라졌지만 PV에 저장된 데이터는 유지되기 때문입니다. 2장의 볼륨 마운트와 같은 원리이지만, 범위가 클러스터 전체로 확장된 것입니다.

정리하면 다음과 같습니다.

- **인프라 운영자**는 PV(실제 스토리지 자원)를 생성하고 관리합니다.
- **개발자**는 PVC(스토리지 사용 요청)를 정의해 필요한 저장 공간을 요청합니다.
- **Pod**는 애플리케이션이 실행되는 최소 단위입니다.
- **PVC**는 Pod가 사용할 스토리지를 요청하는 신청서입니다.
- **PV**는 그 요청에 응답하는 실제 스토리지 자원입니다.

**[실습]** 다음 실습을 위해 생성한 리소스를 제거합니다.

```bash
kubectl delete pod volume-pod          # Pod 삭제
kubectl delete pvc volume-pvc          # PVC 삭제
kubectl delete pv volume-pv            # PV 삭제
```

## 6.3 웹사이트 : Kubernetes 배포

지금까지 배운 모든 것을 하나로 합칠 때가 왔습니다. 3장에서는 프론트 서버 + 백엔드 서버 + DB 서버를 Docker Compose로 실행했습니다. 이번에는 Redis 서버를 추가해 미니큐브 환경에서 실행해 보겠습니다. Docker Compose로 돌리던 것을 쿠버네티스로 옮기면 자동 복구에 무중단 배포까지 모두 가능해집니다.

> 실습 코드는 https://github.com/metacoding-10-linux-docker/docker/tree/master/ex08 에서 확인할 수 있습니다.

### 6.3.1 아키텍처

배포할 애플리케이션은 프론트엔드(Nginx), 백엔드(Spring Boot), DB(MySQL), Redis, 총 4개의 서비스로 구성됩니다.

![](../assets/CH05/fig-3-7-v2.png)
*ex08 Kubernetes 웹사이트 아키텍처*

쿠버네티스에서는 외부 요청이 클러스터 내부로 바로 들어갈 수 없어 `Ingress`가 앞단에 놓입니다. 브라우저 요청은 `Ingress`가 받아 `Frontend Service`로 넘기고, 이후 프론트엔드 -> 백엔드 -> DB/Redis 순으로 흐릅니다.

### 6.3.2 이미지 폴더

**[EX08 패키지 구조]**

```
ex08/
├── backend/
│   ├── Dockerfile
│   └── entrypoint.sh
├── db/
│   ├── Dockerfile
│   └── init.sql
├── frontend/
│   ├── Dockerfile
│   ├── index.html
│   └── nginx.conf
├── redis/
│   └── Dockerfile
└── k8s/
```

EX08 폴더에는 이미지 생성을 위한 backend, db, frontend, redis 폴더와 쿠버네티스 배포 설정을 담은 k8s 폴더가 있습니다.

> Backend, DB, Frontend, Redis 폴더는 3장의 EX07과 동일한 구조입니다. 설명이 필요한 부분만 코드로 표시합니다.

Redis를 추가하기 위해 Dockerfile을 작성합니다.

**ex08/redis/Dockerfile**
```dockerfile
FROM redis:7.4-alpine       # Redis 이미지 사용
CMD ["redis-server"]         # Redis 서버 실행
```

backend 폴더의 entrypoint.sh에서 `Git clone` 주소를 수정합니다.

**ex08/backend/entrypoint.sh**
```bash
#!/bin/bash
git clone https://github.com/metacoding-10-linux-docker/backend-redis-server  # 백엔드 서버 내려받기
cd backend-redis-server      # 내려받은 폴더로 이동
chmod +x gradlew             # 실행 권한 부여
./gradlew build              # 스프링 프로젝트 빌드
java -jar -Dspring.profiles.active=prod build/libs/*.jar  # 빌드된 파일 실행
```

수정된 백엔드 서버는 API 요청 시 회원 정보와 Redis에 저장된 방문 횟수를 함께 돌려줍니다.

**UserController.java**
```java
@GetMapping("/api/users")
public ResponseEntity<?> findAll() {

    List<User> users = userRepository.findAll();       // DB에서 회원 목록 조회

    Long count = redisTemplate.opsForValue()
            .increment("cnt:/api/users:total");        // Redis 방문 횟수 증가

    Map<String, Object> response = new HashMap<>();
    response.put("users", users);                      // 회원 목록
    response.put("count", count);                      // 방문 횟수

    return Resp.ok(response);
}
```

프론트엔드의 index.html에서 방문 횟수를 표시하는 부분이 추가되었습니다.

**ex08/frontend/index.html** (핵심 부분 발췌)
```html
<h1>사용자 리스트</h1>
<h2>방문 횟수: <span id="visit-count">0</span></h2>

<script>
  fetch('/api/users')                    // nginx가 backend로 프록시
    .then(response => response.json())
    .then(data => {
      const users = data.body.users;     // 회원 목록
      const count = data.body.count;     // 방문 횟수

      users.forEach(user => {            // 응답 데이터를 테이블에 렌더링
        $("#user-list").append(render(user));
      });

      $("#visit-count").text(count);     // 방문 횟수 표시
    });
  // ... 생략
</script>
```

nginx.conf의 upstream 서버 주소를 Kubernetes Service명(backend-service)으로 바꿉니다.

**ex08/frontend/nginx.conf**
```nginx
events {}

http {
    # 백엔드 서버 주소 (K8s Service명으로 수정)
    upstream backend {
        server backend-service:8080;
    }

    server {
        listen 80;
        server_name _;

        # 정적 파일 제공
        location / {
            root   /usr/share/nginx/html;
            index  index.html;
        }

        # API 요청은 백엔드로 프록시
        location /api/ {
            proxy_pass http://backend;
        }
    }
}
```

### 6.3.3 k8s 폴더

ex08 폴더 내에 k8s 폴더가 있습니다.

> **k8s 폴더** 는 Kubernetes 배포 설정 파일을 모아둔 폴더입니다.

**[k8s 패키지 구조]**

```
k8s/
├── backend/
│   ├── backend-configmap.yml
│   ├── backend-deploy.yml
│   ├── backend-secret.yml
│   └── backend-service.yml
├── db/
│   ├── db-deploy.yml
│   ├── db-pv.yml
│   ├── db-pvc.yml
│   ├── db-secret.yml
│   └── db-service.yml
├── frontend/
│   ├── frontend-deploy.yml
│   ├── frontend-ingress.yml
│   └── frontend-service.yml
├── redis/
│   ├── redis-deploy.yml
│   └── redis-service.yml
└── namespace.yml
```

| 파일 | 설명 |
|------|------|
| namespace.yml | 리소스를 논리적으로 구분하는 `Namespace` 생성 |
| *-deploy.yml | 각 서버의 `Deployment` (Pod 생성 및 관리) |
| *-service.yml | 각 서버의 `Service` (고정 IP로 Pod 접근) |
| frontend-ingress.yml | 외부 요청을 프론트엔드 `Service`로 라우팅하는 `Ingress` |
| backend-configmap.yml | 백엔드 환경 변수 (DB 주소, Redis 주소) |
| backend-secret.yml | 백엔드 민감 정보 (DB 계정/비밀번호) |
| db-secret.yml | DB 민감 정보 (MySQL 계정/비밀번호) |
| db-pv.yml / db-pvc.yml | DB 데이터 영구 저장을 위한 `PV`/`PVC` |

#### Namespace

지금까지 실습에서 만든 Deployment, Service, ConfigMap 등은 모두 **default** 라는 기본 공간에 생성되었습니다. 리소스가 몇 개 안 될 때는 상관없지만, 여러 서비스의 리소스가 한 곳에 섞이면 관리하기 어렵습니다.

Namespace는 회사 건물의 **층** 과 같습니다. 1층은 프론트엔드, 2층은 백엔드, 3층은 데이터 팀. 층을 나누면 각 팀 공간이 분리됩니다. Namespace도 마찬가지입니다. 리소스가 분리되어 이름이 겹칠 걱정 없이 독립적으로 관리할 수 있습니다.

![](../assets/CH05/k8s-namespace.png)
*같은 Cluster 안에서 Namespace로 리소스를 분리한다*

> **Namespace** 는 쿠버네티스 리소스를 논리적으로 구분하는 가상의 공간입니다. 별도로 지정하지 않으면 모든 리소스는 **default** 네임스페이스에 생성됩니다.

이번 실습에서는 `metacoding`이라는 Namespace를 만들어 모든 리소스를 그 안에 생성합니다. 각 YAML 파일의 `metadata`에 `namespace: metacoding`이 들어가 있는 이유가 여기 있습니다.

**ex08/k8s/namespace.yml**
```yaml
apiVersion: v1           # API 버전
kind: Namespace          # 리소스 종류
metadata:
  name: metacoding       # 네임스페이스 이름
```

Namespace를 지정한 리소스를 조회할 때는 `-n` 옵션으로 Namespace를 밝혀야 합니다.

**[예시]** Namespace를 지정하여 `Pod`를 조회합니다.
```bash
kubectl get pod -n metacoding        # metacoding 네임스페이스의 Pod 조회
```

#### backend-deploy.yml

backend-deploy.yml은 이번 실습에서 가장 많은 리소스를 조합한 설정입니다. `replicas: 2`로 `Pod`를 2개 생성하고, `envFrom`으로 `ConfigMap`과 `Secret`을 연결해 환경 변수를 주입합니다.

**ex08/k8s/backend/backend-deploy.yml**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend-deploy
  namespace: metacoding                        # namespace 설정
spec:
  replicas: 2                                  # pod 2개 생성
  selector:
    matchLabels:
      app: backend                             # app: backend 라벨을 가진 pod 관리
  template:
    metadata:
      labels:
        app: backend                           # pod에 app: backend 라벨 붙임
    spec:
      containers:
        - name: backend-server
          image: metacoding/backend:1
          ports:
            - containerPort: 8080               # 8080 포트 사용
          envFrom:
            - configMapRef:
                name: backend-configmap         # configmap 연결
            - secretRef:
                name: backend-secret            # secret 연결
```

`ConfigMap`에는 DB 주소, Redis 주소 등 일반 설정을, `Secret`에는 DB 계정/비밀번호를 넣습니다. `Service`, `ConfigMap`, `Secret` 파일은 앞에서 배운 구조와 동일하므로 Github을 참고합니다.

#### db-deploy.yml

db-deploy.yml은 `volumeMounts`와 `PVC`를 연결해 DB 데이터를 영구적으로 저장합니다.

**ex08/k8s/db/db-deploy.yml**
```yaml
apiVersion: apps/v1                    # API 버전
kind: Deployment                       
metadata:
  name: db-deploy                      
  namespace: metacoding                # namespace 설정
spec:                                  
  replicas: 1                          # Pod 1개 유지
  selector:                            # 관리할 Pod 선택 조건
    matchLabels:
      app: db                          # app: db 라벨을 가진 pod 관리
  template:
    metadata:
      labels:
        app: db                        # pod에 app: db 라벨 부여
    spec:
      containers:
        - name: db-server
          image: metacoding/db:1
          ports:
            - containerPort: 3306      # 3306 포트 사용
          envFrom:
            - secretRef:
                name: db-secret        # DB 접속을 위한 환경 변수 연결
          volumeMounts:
            - name: data
              mountPath: /var/lib/mysql  # volume 경로 설정
      volumes:
        - name: data
          persistentVolumeClaim:
            claimName: db-pvc            # PVC 연결
```

5.2에서 배운 PV/PVC를 여기서 적용합니다. `Secret`, `PV`, `PVC`, `Service` 파일은 앞에서 본 구조와 동일하므로 Github을 참고합니다.

#### 나머지 설정

frontend, redis의 `Deployment`와 `Service`는 backend와 같은 구조입니다. 이미지명, 라벨, 포트만 다릅니다. 전체 코드는 Github을 참고합니다.

| 항목 | frontend | redis |
|------|----------|-------|
| image | metacoding/frontend:1 | metacoding/redis:1 |
| containerPort | 80 | 6379 |
| replicas | 1 | 1 |
| Service port | 80 | 6379 |

#### frontend-ingress.yml

`Ingress` 리소스를 작성합니다. 모든 외부 요청을 `frontend-service`의 80번 포트로 전달하는 규칙을 정의합니다.

**ex08/k8s/frontend/frontend-ingress.yml**
```yaml
apiVersion: networking.k8s.io/v1         # API 버전
kind: Ingress                            # 리소스 종류
metadata:
  name: frontend-ingress                 # Ingress 이름
  namespace: metacoding                  # 네임스페이스 지정
spec:                                    # 상세 설정
  rules:                                 # 라우팅 규칙
    - http:                              # HTTP 규칙
        paths:                           # 경로 설정
          - path: /                       # 모든 경로
            pathType: Prefix             # 경로 매칭 방식
            backend:                     # 요청을 전달할 대상
              service:                   # 서비스 지정
                name: frontend-service    # 프론트엔드 Service로 연결
                port:                    # 포트 설정
                  number: 80             # 서비스 포트 번호
```

**path** 는 어떤 경로의 요청을 받을지 정하는 설정입니다. `/`로 지정하면 모든 경로의 요청을 받아 `frontend-service`의 80번 포트로 넘깁니다.

> 전체 k8s 설정 파일은 https://github.com/metacoding-10-linux-docker/docker/tree/master/ex08/k8s 에서 확인할 수 있습니다.

### 6.3.4 실행하기

**[실습]** 미니큐브가 실행되어 있지 않다면 먼저 미니큐브를 실행합니다.
```bash
minikube start                        # 미니큐브 클러스터 시작
```

#### Ingress Controller 활성화

`Ingress` 리소스가 동작하려면 `Ingress Controller`가 먼저 설치되어 있어야 합니다. 미니큐브에서는 애드온(addon)으로 활성화합니다.

**[실습]** Nginx Ingress Controller를 활성화합니다.
```bash
minikube addons enable ingress        # Ingress Controller 활성화
```

![](../assets/CH05/chap03-ingress-addon.png)
*Ingress Controller 활성화*

**[실습]** Ingress Controller가 정상 실행 중인지 확인합니다. `ingress-nginx-controller` Pod의 STATUS가 `Running`이면 정상입니다.
```bash
kubectl get pod -n ingress-nginx      # Ingress Controller Pod 상태 확인
```

![](../assets/CH05/chap03-ingress-controller-running.png)
*Ingress Controller 실행 확인*

#### 이미지 빌드

> **minikube image build**: 미니큐브는 별도의 가상 환경(Docker 컨테이너 또는 VM) 안에서 동작합니다. 로컬 PC에서 **docker build** 로 만든 이미지는 미니큐브 내부에서 접근할 수 없습니다. **minikube image build** 명령을 사용하면 미니큐브 내부에 직접 이미지를 빌드해 별도의 이미지 레지스트리 없이도 Pod에서 바로 사용할 수 있습니다.

**[실습]** EX08 폴더로 이동한 뒤 각 서버의 Docker 이미지를 미니큐브 내부에 빌드합니다.
```bash
minikube image build -t metacoding/db:1 ./db            # DB 이미지 빌드
minikube image build -t metacoding/backend:1 ./backend   # 백엔드 이미지 빌드
minikube image build -t metacoding/frontend:1 ./frontend # 프론트엔드 이미지 빌드
minikube image build -t metacoding/redis:1 ./redis       # Redis 이미지 빌드
```

![](../assets/CH05/chap03-67.png)
*미니큐브 이미지 빌드*

#### 리소스 생성

**[실습]** `Namespace`를 생성합니다.
```bash
kubectl apply -f k8s/namespace.yml    # Namespace 생성
```

![](../assets/CH05/chap03-68.png)
*Namespace 생성*

**[실습]** k8s 폴더의 모든 리소스를 생성합니다. `--recursive` 옵션을 붙이면 하위 폴더의 YAML 파일도 모두 적용됩니다.
```bash
kubectl apply -f k8s/ --recursive     # k8s 폴더의 모든 리소스 일괄 생성
```

![](../assets/CH05/chap03-69.png)
*k8s 리소스 일괄 생성*

**[실습]** 생성된 리소스 정보를 확인합니다.
```bash
kubectl get deploy,pod,service -n metacoding  # Deployment, Pod, Service 조회
```

![](../assets/CH05/chap03-70.png)
*Deployment, Pod, Service 조회*

#### 컨테이너 실행 확인

**[실습]** 각 서버의 로그를 확인합니다.
```bash
kubectl logs deploy/db-deploy -n metacoding --tail=5       # DB 서버 로그 확인
kubectl logs deploy/frontend-deploy -n metacoding --tail=5 # 프론트엔드 서버 로그 확인
kubectl logs deploy/backend-deploy -n metacoding --tail=5  # 백엔드 서버 로그 확인
```

![](../assets/CH05/chap03-71.png)
*서버 로그 확인*

> **Pod** 가 Running 상태라고 해서 서버가 바로 정상 동작하는 건 아닙니다. 실행에 시간이 필요할 수 있으니 **kubectl logs** 명령어를 활용해 각 서버의 로그를 확인하며 정상적으로 동작하는지 확인합니다.

#### Ingress로 서버 연결

리소스가 모두 생성되었으니 `Ingress`를 통해 프론트엔드에 접속해보겠습니다.

**[실습]** 생성된 `Ingress` 정보를 확인합니다. ADDRESS에 IP가 표시되면 정상입니다. 1~2분 정도 기다려야 할 수 있습니다.
```bash
kubectl get ingress -n metacoding     # Ingress 리소스 조회
```

![](../assets/CH05/chap03-ingress-get.png)
*Ingress 리소스 확인*

**[실습]** `minikube tunnel` 명령어를 실행합니다. Docker Desktop 드라이버를 쓰는 경우 로컬 PC에서 미니큐브 내부 IP로 직접 접근할 수 없어 터널이 필요합니다.

> **minikube tunnel**은 포그라운드로 실행되어 현재 터미널을 점유합니다. 이후 명령어는 **새 터미널 창을 열어서** 입력합니다. 터널 터미널을 종료하면 접속이 끊기니 접속 확인이 끝날 때까지 유지합니다.

```bash
minikube tunnel                       # 로컬 PC에서 클러스터 접근을 위한 터널 생성
```

![](../assets/CH05/chap03-ingress-tunnel.png)
*minikube tunnel 실행*

**[실습]** 브라우저에서 `http://127.0.0.1`로 접속합니다.

![](../assets/CH05/chap03-ingress-result.png)
*Ingress를 통한 웹사이트 접속*

DB에서 조회된 데이터가 화면에 표시됩니다. 여러 번 요청을 보내면 방문 횟수가 늘어납니다.

![](../assets/CH05/chap03-ingress-result2.png)
*방문 횟수 증가 확인*

자동 복구에 무중단 배포까지 갖춰졌습니다.

`minikube service`로 임시 URL을 만들어 접속하던 것과 달리, `Ingress`는 도메인 기반 라우팅을 지원해 실제 운영 환경에 더 가까운 구조입니다.

`Pod` 내부를 확인해보겠습니다. `minikube tunnel`이 실행 중인 터미널은 그대로 두고, 새 터미널 창을 엽니다.

**[실습]** 전체 `Pod` 목록을 확인합니다.
```bash
kubectl get pod -n metacoding         # metacoding 네임스페이스의 Pod 목록 조회
```

![](../assets/CH05/chap03-75.png)
*전체 Pod 목록 확인*

**[실습]** 각 백엔드 서버의 로그를 확인합니다. `replicas: 2`로 Pod가 2개이므로 각각 확인합니다.
```bash
kubectl logs deploy/backend-deploy -n metacoding --tail=10  # 백엔드 서버 로그 확인 (Pod 하나씩 반복 실행)
```

![](../assets/CH05/chap03-76.png)
*백엔드 서버 1 로그*

![](../assets/CH05/chap03-77.png)
*백엔드 서버 2 로그*

로그에서 회원 정보를 조회하는 `SELECT문`이 출력됩니다. `backend-service`가 로드밸런싱을 수행해 요청이 두 서버로 분산되었습니다.

### 전체 패킷 경로

방금 브라우저에서 **http://127.0.0.1** 을 입력했을 때, 패킷은 다음 관문을 차례로 통과합니다. 5장에서 배운 전체 흐름이 실전에서 작동하는 모습입니다.

```
브라우저 -> minikube tunnel -> Ingress Controller(Nginx Pod)
        -> frontend-service -> Frontend Pod
        -> (프론트엔드가 /api/users 요청)
        -> backend-service -> Backend Pod
        -> db-service -> DB Pod / redis-service -> Redis Pod
```

모든 서비스 간 통신에서 IP 주소 대신 **서비스 이름** (CoreDNS)이 사용되고, 각 Service 뒤에서 **kube-proxy의 iptables 규칙** 이 실제 Pod으로 DNAT합니다. 5장에서 배운 "Ingress(L7) → Service(Label-Selector) → kube-proxy(iptables) → Pod(비즈니스 로직)" 흐름 그대로입니다.

![](../assets/CH05/net-10a-full-path.png)
*전체 경로 (1) --- 브라우저 -> Ingress -> frontend Service -> frontend Pod*

![](../assets/CH05/net-10b-full-path.png)
*전체 경로 (2) --- frontend Pod -> backend Service -> backend Pod -> DB/Redis*


## 이것만은 기억하자

오픈이가 이번 장에서 배운 것들을 한 장의 노트에 정리했습니다.

- **설정은 밖에서, 데이터는 영구히.** ConfigMap과 Secret으로 코드와 설정을 분리하고, PV/PVC로 컨테이너가 사라져도 데이터를 보존합니다.

- **CoreDNS는 클러스터의 전화번호부입니다.** 3장의 Docker DNS가 클러스터 규모로 확장된 것입니다. Service 이름만으로 Pod끼리 통신할 수 있는 이유가 여기 있습니다.

- **문제가 생기면 logs -> describe -> events 순서로 확인합니다.** 대부분의 문제는 이 세 명령어로 원인을 찾을 수 있습니다.

Docker와 Kubernetes를 향한 여정이 마무리되었습니다. 2장에서 컨테이너 하나를 띄우는 것으로 시작해, 3장에서 Docker Compose로 여러 컨테이너를 한 번에 관리했습니다. 4장에서 쿠버네티스의 핵심(Pod, Deployment)을 익혔고, 5장에서 네트워킹으로 연결하고, 6장에서 설정 관리와 웹사이트 배포까지 완성했습니다.

이제 새벽에 알람이 와도 쿠버네티스가 먼저 움직입니다. 물론 알람이 안 오는 것이 제일 좋긴 합니다.
