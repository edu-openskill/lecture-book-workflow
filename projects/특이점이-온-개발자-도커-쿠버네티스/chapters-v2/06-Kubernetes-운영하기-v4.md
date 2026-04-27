# Ch.6 Kubernetes 운영하기

## 6.1 설정을 코드 밖으로

오픈이는 금요일 오후, 운영팀에서 온 메시지를 받고 모니터를 들여다봤습니다. DB 비밀번호를 교체해야 한다는 요청이었습니다. 개발 환경은 그대로 쓰고 운영 환경만 새 비밀번호를 적용하면 됐습니다.

그걸 처리하려고 오픈이는 백엔드 프로젝트의 설정 파일을 열었습니다. DB 주소와 비밀번호가 환경별로 나뉘어 있었지만, 결국 같은 이미지 안에 같이 들어가는 값이었습니다. 비밀번호 한 줄을 바꾸자 프로젝트를 다시 빌드해야 했고, 이미지를 다시 찍어 Docker Hub에 올려야 했고, Deployment의 이미지 태그를 바꿔 새로 배포해야 했습니다.

*비밀번호 한 자리 바꾸는데 이미지까지 다시 찍어야 한다고.*

빌드가 돌아가는 동안 오픈이는 의자 등받이에 몸을 기댔습니다. 앞쪽 모니터에서는 Gradle 로그가 줄지어 내려가고, 선풍기 돌아가는 소리만 사무실에 남아 있었습니다. 개발용 비밀번호까지 Git 로그에 그대로 남을 거라는 생각이 들자 마음이 불편해졌습니다.

팀장이 뒤에서 화면을 슬쩍 보더니 한 마디 했습니다.

**팀장**: "설정은 코드 밖에 있어야지."

코드 밖이 어딘지 처음엔 감이 안 왔습니다. 설정 파일을 따로 두더라도 그 파일이 이미지 안에 들어가는 건 마찬가지였습니다. 선배가 끼어들었습니다.

**선배**: "본사가 매장에 내려보내는 **메뉴판**(ConfigMap)이랑 **금고 안 극비 정보**(Secret). 둘을 나눠서 관리해."

*메뉴판과 금고.*

1장에서 팀장이 심어둔 씨앗이 그제야 되살아났습니다. 본사, 가맹점, 매장, 메뉴판, 공용 금고. 매장에 뿌리는 영업 시간이나 가격표 같은 공개 정보는 메뉴판에 적어 내려보냅니다. 본사 통장이나 비밀 레시피 같은 극비 정보는 금고 안에 둡니다. 쿠버네티스도 똑같이 나눈다는 뜻이었습니다. 이미지에는 코드만 담고, 값은 밖에서 주입한다.

![](../assets/CH05/k8s-step4a.png)

*그림 6-1 ConfigMap과 Secret은 이미지와 별개로 Pod에 설정과 민감 정보를 주입*

### 6.1.1 ConfigMap : 매장에 뿌리는 메뉴판

ConfigMap은 일반 설정 값을 바깥에서 관리하는 리소스입니다. DB 주소, 접속 URL, 로그 레벨처럼 환경마다 바뀔 수 있는 값을 여기에 적어둡니다. 값이 바뀌면 이 파일만 고치면 됩니다. 이미지는 건드리지 않습니다. 본사가 영업 시간을 바꾼다고 가맹점을 새로 짓지 않는 것과 같은 이치입니다.

> **참고: ConfigMap**
> 일반 설정 값을 코드 밖에서 관리하는 리소스. 키-값 형태로 값을 담아두고, Pod는 이를 환경 변수나 파일로 주입받아 사용한다.

오픈이는 선배가 알려준 대로 `configmap-conn.yml`을 하나 만들었습니다.

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

`data` 아래에 키-값 쌍을 적어두기만 하면 됩니다. YAML 자체는 크게 특별한 구조가 아니었습니다.

이 ConfigMap을 Pod가 쓰려면 Deployment 쪽에서 끌어와야 합니다. `envFrom.configMapRef`를 쓰면 ConfigMap의 모든 키가 한꺼번에 환경 변수로 주입됩니다.

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

`envFrom` 아래 `configMapRef`로 `configmap-conn`을 지목했습니다. 이 한 줄로 ConfigMap의 `conn_info`와 `conn_url`이 Pod 안에서 환경 변수로 올라옵니다.

주입 시점이 중요합니다. **Pod가 생성될 때** 쿠버네티스가 ConfigMap의 키-값을 컨테이너의 환경 변수로 설정합니다. 생성된 이후에 ConfigMap을 바꿔도, 이미 떠 있는 Pod 안에는 옛 값이 남아 있습니다. 이 함정은 6.1.4에서 다시 마주치게 됩니다.

오픈이가 익숙했던 Spring Boot 코드에서는 `application.yml`의 `${DB_URL}` 같은 placeholder 자리가 환경 변수를 읽어오는 창구였습니다. `@Value("${DB_URL}")`로 필드에 주입받던 그 값. 로컬 개발에서는 `.env` 파일이나 IDE 실행 프로필에서 내려주던 환경 변수가, 쿠버네티스에서는 ConfigMap에서 꽂혀 들어오는 구조입니다. Spring 쪽 코드는 한 줄도 바꾸지 않아도 됩니다.

```bash
kubectl apply -f configmap-conn.yml   # ConfigMap 생성
kubectl apply -f deploy-ex03.yml     # Deployment 생성
```

오픈이는 두 리소스를 차례로 적용한 뒤 Pod 안에 환경 변수가 실제로 들어갔는지 확인해 봤습니다.

```bash
kubectl get pod                       # Pod 목록 조회
kubectl exec -it <Pod명> -- env       # Pod 환경 변수 조회
```

![](../assets/CH05/chap03-46.png)

*그림 6-2 Pod 안의 환경 변수 목록에서 ConfigMap의 값이 보*

출력을 쭉 내리자 `conn_info=localhost:80`과 `conn_url=config.test`가 보였습니다. ConfigMap에 적어둔 그대로 환경 변수로 꽂혀 있었습니다. 이미지를 건드리지 않고 설정 값만 밖에서 주입했다는 사실이 눈으로 확인됐습니다.

### 6.1.2 Secret : 본사 금고에 넣는 극비 정보

DB 비밀번호도 같은 방식으로 ConfigMap에 적어두면 될까. 오픈이는 잠깐 그렇게 하려다 멈췄습니다. 팀장이 일부러 "ConfigMap 말고 Secret"이라는 단어를 따로 썼던 게 떠올랐습니다.

비밀번호와 토큰 같은 민감한 값은 메뉴판 위에 그대로 적어두면 안 됩니다. 쿠버네티스에는 이런 값을 담기 위한 별도 리소스 **Secret** 이 있습니다. ConfigMap이 바깥에 펼쳐두는 메뉴판이라면, Secret은 **본사 금고 안에만 있는 극비 정보** 에 가깝습니다. 담는 값의 성격이 다르기 때문에 리소스 종류부터 나눈 것입니다.

> **참고: Secret과 Base64**
> 비밀번호, 토큰, 인증 키처럼 민감한 정보를 담기 위한 리소스. ConfigMap과 구조는 비슷하지만 값이 Base64로 인코딩되어 저장된다. 단, Base64는 **암호화가 아니라 단순 인코딩** 이다. `kubectl get secret -o yaml`로 뽑아 디코딩하면 원문이 그대로 보인다. 실제 보안은 RBAC으로 조회 권한 제한, etcd 암호화, 외부 Vault 연동 중 하나를 붙여 확보하며, 이 책의 범위를 벗어난다. 이 단계에서는 "Secret은 ConfigMap과 구분해 관리한다"는 신호로만 이해하면 된다.

이제 실제로 Secret을 만들어 봅니다.

**yaml/secret-password.yml**
```yaml
apiVersion: v1              # API 버전
kind: Secret                # 리소스 종류
metadata:
  name: secret-password     # Secret 이름
stringData:                 # 평문을 자동으로 Base64 변환
  password: metacoding1234  # 비밀번호 설정
```

`stringData`에 평문을 적으면 쿠버네티스가 자동으로 Base64로 인코딩해서 저장합니다. `data` 항목에 직접 Base64 값을 넣어도 되지만, YAML을 손으로 쓸 때는 `stringData`가 편합니다.

```bash
kubectl apply -f secret-password.yml  # Secret 생성
kubectl get secret secret-password -o yaml  # Secret 내용을 YAML 형태로 출력
```

![](../assets/CH05/chap03-48.png)

*그림 6-3 Secret 내부를 보면 비밀번호가 Base64로 인코딩된 상태*

YAML 결과를 보면 `password` 값이 `bWV0YWNvZGluZzEyMzQ=` 같은 Base64 문자열로 바뀌어 있었습니다. 원문 복원은 한 줄이면 끝나기 때문에, 이 단계에서 챙길 것은 "값이 감춰져 있다"가 아니라 **"민감한 값은 별도 리소스로 관리한다"** 는 구분 그 자체입니다.

### 6.1.3 Secret을 Pod에 주입

만든 Secret을 Pod에 주입합니다. 방식은 ConfigMap과 똑같이 `envFrom`을 쓰되, `configMapRef` 옆에 `secretRef`를 한 줄 더 붙입니다.

**yaml/deploy-ex03.yml**
```yaml
          # ... 생략

          envFrom:
            - configMapRef:
                name: configmap-conn         # ConfigMap 연결
            - secretRef:
                name: secret-password        # Secret 연결 (추가)
```

```bash
kubectl apply -f deploy-ex03.yml     # 변경된 Deployment 적용
```

Pod가 새로 뜰 때 `secret-password`의 값이 환경 변수로 함께 주입됩니다. 환경 변수 안에서 값은 이미 **평문**입니다. Base64는 쿠버네티스가 저장할 때만 쓰는 내부 형식이고, Pod에서 읽을 때는 자동으로 풀어서 넣어주기 때문입니다. Spring Boot에서는 그대로 `@Value("${password}")`로 받으면 `metacoding1234`가 주입됩니다.

```bash
kubectl get pod                       # Pod 목록 조회
kubectl exec -it <Pod명> -- env       # Pod 환경 변수 조회
```

![](../assets/CH05/13_secret-env.png)

*그림 6-4 환경 변수 목록에 Secret의 값이 평문으로 들어와*

환경 변수 목록에 `password=metacoding1234`가 평문으로 찍혔습니다. 이미지 안에는 비밀번호가 없고, 실행 시점에 Secret에서 끌어와서 꽂힌 값입니다. 비밀번호 교체가 필요해지면 Secret만 수정하면 됩니다. 로컬에서 `.env` 하나만 바꿔 Spring 서버를 재시작하던 리듬이 그대로 쿠버네티스 위로 올라왔습니다.

### 6.1.4 환경 변수 수정 : 수정이 안 되는 함정

다음 날 오후, 운영팀에서 DB 주소가 바뀌었다는 연락이 왔습니다. 오픈이는 가볍게 `configmap-conn.yml`을 열어 `conn_info`의 포트만 90으로 바꿨습니다.

**yaml/configmap-conn.yml**
```yaml
# ... 생략

  conn_info: "localhost:90"          # 환경변수 수정
```

```bash
kubectl apply -f configmap-conn.yml   # 변경된 ConfigMap 적용
```

ConfigMap은 바로 업데이트됐다고 메시지가 떴습니다. 오픈이는 Pod 환경 변수를 확인했습니다.

```bash
kubectl exec -it <Pod명> -- env
```

출력에 `conn_info=localhost:80`이 그대로 있었습니다. 조금 전 90으로 바꿨는데 반영이 안 되어 있었습니다.

*어라. 분명히 apply됐다고 했는데.*

오픈이는 한참을 보다가 다시 apply를 해봤지만 결과는 같았습니다. ConfigMap 자체는 분명히 새 값이었습니다. `kubectl get configmap configmap-conn -o yaml`로 다시 확인해도 90으로 바뀌어 있었습니다. 문제는 Pod 안쪽이었습니다.

옆자리 선배가 모니터를 보더니 한 마디를 던졌습니다.

**선배**: "환경 변수는 프로세스가 시작될 때만 꽂히는 거야."

오픈이는 그제야 감이 왔습니다. 리눅스에서 환경 변수는 프로세스가 시작될 때 한 번 꽂히는 값입니다. 부모 프로세스의 환경을 자식에게 복사해주고, 그 뒤로는 각자의 메모리에 올라간 값을 그대로 들고 돕니다. 바깥에서 ConfigMap을 바꿔도 이미 떠 있는 컨테이너 프로세스의 메모리 안쪽은 건드리지 못합니다. 2장에서 `docker run -e`로 넣어봤던 환경 변수도 같은 성질이었습니다.

> **참고: 환경 변수는 언제 꽂히는가**
> 리눅스에서 프로세스가 뜰 때(fork/exec) 부모 프로세스의 환경이 자식 프로세스로 복사됩니다. 그 이후로는 각 프로세스가 자기 메모리의 값만 봅니다. 바깥에서 ConfigMap을 바꾸거나 환경 변수 값을 덮어써도, 이미 실행 중인 프로세스의 값은 바뀌지 않습니다. ConfigMap을 바꿨다면 **Pod를 재시작해야** 새 값이 꽂힙니다.

![](../assets/CH05/fig-3-6.png)

*그림 6-5 ConfigMap을 수정한 뒤에는 Pod를 재시작해야 값이 환경 변수로 반영*

새 값을 반영하려면 Pod를 **재시작**해야 합니다. 그냥 `kubectl delete pod`로 지워도 Deployment가 알아서 새 Pod를 만들기는 하지만, 여러 개 떠 있는 Pod를 한꺼번에 안전하게 갈아끼우려면 **`kubectl rollout restart`** 쪽이 편합니다. Deployment 단위로 하나씩 교체해 줍니다.

```bash
kubectl apply -f configmap-conn.yml   # 변경된 ConfigMap 적용
kubectl rollout restart deployment nginx-config-secret  # 재시작
```

![](../assets/CH05/chap03-52.png)

*그림 6-6 ConfigMap을 반영하기 위해 Deployment를 재시작하는 모습*

롤아웃 메시지가 찍히고 잠시 뒤 Pod가 새 것으로 교체됐습니다. 오픈이는 다시 환경 변수를 확인했습니다.

```bash
kubectl exec -it <Pod명> -- env       # Pod 환경 변수 조회
```

![](../assets/CH05/chap03-53.png)

*그림 6-7 재시작된 Pod의 환경 변수에서 포트가 90으로 바뀌어*

이번엔 `conn_info=localhost:90`이 제대로 찍혔습니다. Pod를 새로 뜨는 순간 ConfigMap의 새 값이 그제서야 환경 변수로 꽂힌 것이었습니다.

*apply만으로는 절반이고, 반영까지는 재시작이 있어야 한다.*

오픈이는 이걸 머릿속에 적어 뒀습니다. 설정 파일 기반으로 마운트해서 쓰면 자동 반영되는 방법도 따로 있지만, 환경 변수로 주입하는 이 방식에서는 재시작이 한 단계로 따라온다는 사실이 중요했습니다.

실습이 끝나면 다음 실습을 위해 리소스를 정리합니다.

```bash
kubectl delete deployment nginx-config-secret  # Deployment 삭제
kubectl delete configmap configmap-conn        # ConfigMap 삭제
kubectl delete secret secret-password          # Secret 삭제
```

### 6.1.5 CoreDNS : 클러스터의 전화번호부

6.3에서 실제 서비스를 올릴 때, ConfigMap 안에 DB 주소를 `db-service:3306`, Redis 주소를 `redis-service:6379`처럼 **IP가 아니라 서비스 이름** 으로 적게 됩니다. IP는 Pod가 죽었다 살아날 때마다 바뀌는데 서비스 이름은 고정되어 있기 때문입니다.

이게 가능한 이유는 쿠버네티스 안에 **CoreDNS** 라는 전용 DNS 서버가 돌고 있기 때문입니다. 2장 4.3에서 봤던 Docker DNS와 원리는 같습니다. Docker는 사용자 정의 네트워크에 붙은 컨테이너가 생기는 순간 컨테이너 이름을 내부 DNS에 자동 등록했습니다. 쿠버네티스의 CoreDNS는 **Service가 생성되는 순간** 해당 이름을 DNS에 자동 등록합니다. 규모만 다르고 원리는 그대로입니다. 등록 대상이 "컨테이너"에서 "Service"로 바뀌었을 뿐입니다.

> **참고: CoreDNS**
> 쿠버네티스 클러스터 안에 기본 내장된 DNS 서버. Service가 생성되는 순간 자동으로 DNS 레코드가 등록되어, Pod는 IP 대신 Service 이름으로 상대를 부를 수 있다.

Service가 생성되면 CoreDNS에 아래 형식의 DNS 레코드가 자동 등록됩니다.

```
서비스명.네임스페이스.svc.cluster.local
```

같은 네임스페이스 안에서는 이 긴 주소 전부를 쓸 필요 없이 **서비스명만** 넣어도 됩니다. 다른 네임스페이스의 서비스를 부를 때만 `서비스명.네임스페이스` 형태가 필요합니다. `svc.cluster.local`까지 전부 붙이는 건 완전한 FQDN(Fully Qualified Domain Name)이 필요한 특수한 경우뿐입니다.

![](../assets/CH05/net-09-coredns.png)

*그림 6-8 CoreDNS가 Service 이름을 ClusterIP로 변환해 Pod 간 통신을 연결*

DB Pod가 어느 순간 죽어서 새로 태어나고 IP가 바뀌어도, Service의 ClusterIP는 그대로이기 때문에 설정을 따라 바꿀 필요가 없습니다. Docker DNS가 하던 일을 이름만 바꿔서 **클러스터 규모로 확장**한 구조입니다. 2장 4.4의 대응표를 다시 꺼내 보면 "Docker DNS → CoreDNS" 자리가 바로 이것입니다.

## 6.2 Volume : 데이터가 증발하지 않도록

오픈이는 ConfigMap 실습으로 가벼워진 마음에 점심을 먹고 들어왔습니다. 점심 직전에 실습용 DB Pod에 테스트 데이터를 잔뜩 넣어뒀던 참이었습니다. 회원 더미 100개, 주문 내역 몇 건. 오후 실습에 쓰려고 만든 데이터였습니다.

자리로 돌아와 `kubectl get pod`를 쳤습니다. DB Pod의 AGE가 `2m`이었습니다.

*어, 방금 뜬 건데?*

점심 전에는 한 시간 넘게 살아 있던 Pod였습니다. 오픈이는 `kubectl logs`로 이전 로그를 확인했지만 방금 올라온 것밖에 없었습니다. 점심 중에 DB Pod가 어떤 이유로 죽었고, Deployment가 알아서 살려낸 모양이었습니다. Pod는 다시 떴지만 **안에 있던 데이터는 흔적도 없이 사라진 상태** 였습니다.

*DB를 Pod에 넣어둔 게 사실 문제였나.*

Pod는 기본적으로 **휘발성** 입니다. Pod 안에서 만든 파일은 그 Pod의 수명과 함께합니다. Pod가 죽으면 같이 사라집니다. 개발용 로그야 괜찮지만, DB 데이터나 업로드된 파일처럼 **사라지면 안 되는 값** 을 Pod 안에 두는 건 위험한 선택이었습니다.

2장 2.8에서 배운 Docker의 **마운트** 가 떠올랐습니다. 호스트나 별도 볼륨에 데이터를 빼놓고, 컨테이너는 그 경로를 끌어다 쓰는 방식이었습니다. 컨테이너가 죽어도 데이터는 호스트나 볼륨에 남아 있었습니다. 쿠버네티스에서 같은 문제를 푸는 방식이 있을까. 당연히 있었습니다.

> **참고: 볼륨(Volume)**
> Pod 내부 컨테이너가 사용할 수 있는 외부 저장 공간. Pod 수명과 분리되어 있어, Pod가 사라져도 데이터가 남을 수 있다.

쿠버네티스의 Volume에는 여러 종류가 있습니다.

| 종류 | 설명 | 데이터 유지 |
|------|------|------------|
| **emptyDir** | Pod 생성 시 만들어지는 임시 저장 공간. 같은 Pod 안의 컨테이너끼리 데이터를 공유할 때 사용 | Pod 삭제 시 함께 삭제 |
| **hostPath** | 워커 노드(호스트)의 특정 경로를 Pod에 마운트 | 노드에 남아 있지만, Pod가 다른 노드로 이동하면 접근 불가 |
| **PV / PVC** | 클러스터 외부에 영구 저장소를 만들고, 요청서(PVC)를 통해 Pod에 연결 | Pod가 삭제되어도 유지 |

실무에서 DB처럼 영구 데이터를 다룰 때 거의 항상 쓰는 건 세 번째인 **PV/PVC** 입니다. 나머지 둘은 "임시 스크래치 공간", "노드 로그 모아두기"처럼 용도가 다릅니다.

### 6.2.1 PV와 PVC : 창고와 신청서

PV/PVC 구조는 처음 보면 이름이 비슷해서 헷갈립니다. 선배가 종이에 간단히 그려줬습니다.

![](../assets/CH05/k8s-step4b.png)

*그림 6-9 PV는 실제 저장 공간, PVC는 저장 공간을 요청하는 신청서*

**PV(PersistentVolume)** 는 실제 저장 공간, 즉 **창고** 입니다. 몇 평짜리 창고가 있고, 어떤 성격(읽기 전용/읽기 쓰기)이며, 어디에 붙어 있는지가 PV에 정의됩니다.

**PVC(PersistentVolumeClaim)** 는 창고를 쓰겠다고 올리는 **신청서** 입니다. "나는 10Gi짜리 읽기 쓰기 가능한 창고가 필요하다"라고 적어두면, 쿠버네티스가 조건(용량, accessMode, storageClassName)에 맞는 PV를 찾아 **자동으로** PVC와 연결합니다. 사람이 승인해주는 절차는 없습니다. 이 자동 연결을 **바인딩(Binding)** 이라고 부릅니다.

Pod는 PV를 직접 건드리지 않고 **PVC만** 붙여 씁니다. 실제 창고 위치는 PVC가 알아서 연결해 주기 때문에, Pod 입장에서는 "10Gi짜리 공간 하나"가 붙어 있는 것처럼 보입니다. 오픈이에게 익숙했던 Spring의 `DataSource`도 비슷한 구조였습니다. 애플리케이션 코드는 DB 서버의 실제 위치를 모릅니다. `DataSource` 설정에 주소만 맡겨두고, 커넥션이 필요할 때 가져다 씁니다. Pod와 PVC 사이도 같은 관계입니다.

실습 순서는 PV 생성 → PVC 생성 → Pod 연결입니다.

#### PV 만들기

먼저 창고에 해당하는 PV를 만듭니다. 이번 실습에서는 별도의 외부 스토리지 없이 미니큐브 내부의 경로를 저장소로 사용합니다.

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

`hostPath`의 `/mnt/data`는 미니큐브 내부 경로입니다. `type: DirectoryOrCreate`를 지정하면 해당 경로가 없을 때 쿠버네티스가 알아서 만들어 줍니다.

#### PVC 만들기

창고가 준비됐으니 신청서를 작성합니다.

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

PVC가 PV와 제대로 바인딩되려면 세 가지가 맞아야 합니다. `accessModes`가 같고, `storageClassName`이 같고, 요청 용량이 PV 용량 이하일 것. 하나라도 틀리면 PVC가 **Pending** 상태에 빠져 바인딩되지 않습니다.

#### Pod에 붙이기

마지막으로 Pod에서 이 PVC를 `volumes` 항목으로 선언하고, `volumeMounts`로 컨테이너 안 경로에 마운트합니다.

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

Pod 입장에서는 `/mnt/data`라는 폴더가 하나 더 생긴 것처럼 보입니다. 그 폴더에 뭘 쓰면 실제 바이트는 PV가 가리키는 미니큐브 내부의 `/mnt/data` 경로에 저장됩니다. 이는 2장 2.8에서 본 Docker의 볼륨 마운트와 원리가 그대로 같습니다. 호스트의 `docker run -v /host/path:/container/path`가 쿠버네티스 버전으로는 Pod의 `volumeMounts` + PVC + PV 세 층으로 나뉘었을 뿐입니다. 애플리케이션 입장에서는 똑같이 "외부 저장소 경로가 하나 붙어 있는" 상태입니다.

```bash
kubectl apply -f volume-pv.yml        # PV 생성
kubectl apply -f volume-pvc.yml       # PVC 생성
kubectl apply -f volume-pod.yml       # Pod 생성
```

세 리소스를 순서대로 만들고, PV와 PVC의 바인딩 상태를 확인했습니다.

```bash
kubectl get pv,pvc            # PV와 PVC 바인딩 상태 확인
```

![](../assets/CH05/chap03-60.png)

*그림 6-10 STATUS가 BOUND면 PV와 PVC가 연결된 상태*

두 리소스 모두 `STATUS`가 `Bound`로 찍혔습니다. 이 순간부터 Pod의 `/mnt/data`에 쓰인 데이터는 Pod 수명과 분리됩니다.

#### 실제로 파일이 살아남는지 확인

Pod 안에 들어가 파일을 하나 만들었습니다.

```bash
kubectl exec -it volume-pod -- /bin/bash  # Pod 내부 접속
touch /mnt/data/c.txt                    # 볼륨 경로에 파일 생성
ls /mnt/data                             # 파일 목록 확인
exit                                     # Pod에서 빠져나오기
```

![](../assets/CH05/chap03-61.png)

*그림 6-11 Pod 안의 `/mnt/data`에 `c.txt` 파일이 만들어졌*

오픈이는 Pod를 일부러 삭제하고, 같은 PVC를 참조하는 Pod를 다시 만들어 파일이 남아 있는지 봤습니다.

```bash
kubectl delete pod volume-pod             # Pod 삭제
kubectl apply -f volume-pod.yml           # 같은 PVC로 Pod 재생성
kubectl exec -it volume-pod -- /bin/bash  # 파일 확인
ls /mnt/data                              # 파일 확인
```

![](../assets/CH05/42_volume-pod-preserved.png)

*그림 6-12 Pod가 새로 태어났는데도 `c.txt`가 그대로 남아*

Pod는 분명히 새 것이었는데 `c.txt`가 그대로 있었습니다. 파일의 실체는 Pod가 아니라 PV에 있고, PVC는 새 Pod에게도 같은 창고를 이어준 것이었습니다. 2장 2.8에서 본 볼륨 마운트의 원리가 이름과 리소스 종류만 바뀌어서 다시 나온 셈이었습니다. 범위가 호스트 한 대에서 클러스터 전체로 넓어졌을 뿐입니다.

*점심 먹으러 갔을 때 날아간 데이터가, 이제는 안 날아간다.*

정리하면 역할 분담이 다음처럼 됩니다.

- **인프라 운영자**: PV를 만들고 관리한다. 실제 저장 공간이 어디 있고 얼마나 큰지.
- **애플리케이션 개발자**: PVC를 작성한다. "얼마짜리 창고가 필요하다"는 요청.
- **Pod**: PVC를 참조해 창고를 이어 쓴다.

실습이 끝나면 리소스를 정리합니다.

```bash
kubectl delete pod volume-pod          # Pod 삭제
kubectl delete pvc volume-pvc          # PVC 삭제
kubectl delete pv volume-pv            # PV 삭제
```

## 6.3 웹사이트를 K8s에 단계별로 올리기

ConfigMap도 해봤고, Secret도 해봤고, 데이터가 증발하지 않는 것도 확인했습니다. 각각은 돌아가는 걸 봤지만, 이게 실제 서비스 한 덩어리가 되면 어떤 느낌인지는 아직 감이 없었습니다.

마침 그때 팀장이 자리에서 일어서며 한 마디 던졌습니다.

**팀장**: "저번에 Compose로 띄우던 거, 이번엔 K8s로 올려봐."

3장에서 Docker Compose로 돌리던 **프론트 + 백엔드 + DB** 구성에 **Redis** 한 대를 더해서 쿠버네티스 위에 올리는 작업이었습니다. Compose에서는 사용자가 늘어나면 수동으로 스케일을 바꿔야 했고, 하나가 죽으면 수동으로 띄워야 했습니다. 쿠버네티스로 옮기면 자동 복구와 무중단 배포까지 따라옵니다.

오픈이는 의자를 바짝 당겨 앉았습니다. 챕터 하나를 쭉 읽는 것과, 실제 서비스 네 개를 엮어서 한 번에 올리는 건 분명 달랐습니다. 화면을 보는 속도가 평소보다 조금 빨라졌습니다.

*네 개를 한 번에 올린다고? 일단 좀 나눠서 해보자.*

오픈이는 처음부터 네 서비스를 몰아치지 않기로 했습니다. 이전 실습들에서 ConfigMap 따로, Secret 따로, PV/PVC 따로 손에 익혀본 이유가 있었습니다. 쿠버네티스의 강점은 **조각을 차례로 얹어도 같은 방식으로 맞물린다**는 점입니다. Frontend부터 한 대만 먼저 띄우고, Backend를 붙이고, 마지막으로 DB와 Redis까지 더하는 순서로 가기로 했습니다.

> 실습 코드는 https://github.com/metacoding-10-linux-docker/docker/tree/master/ex08 에서 확인할 수 있습니다.

### 6.3.1 전체 그림

배포할 애플리케이션은 네 개의 서비스로 구성됩니다. **프론트엔드(Nginx)**, **백엔드(Spring Boot)**, **DB(MySQL)**, **Redis**.

![](../assets/CH05/fig-3-7-v2.png)

*그림 6-13 ex08 Kubernetes 웹사이트의 전체 구성*

쿠버네티스에서는 외부 요청이 클러스터 안으로 바로 들어갈 수 없습니다. 그래서 앞단에 **Ingress** 가 놓입니다. 브라우저 요청은 Ingress를 거쳐 **Frontend Service** 로 넘어가고, 프론트엔드가 `/api/...` 요청을 받으면 **Backend Service** 로 넘깁니다. 백엔드는 **DB Service** 와 **Redis Service** 를 호출합니다. Spring Boot가 내부적으로 띄우는 Tomcat의 기본 포트 8080이 그대로 `containerPort: 8080`이 되고, Backend Service는 그 8080을 `targetPort`로 지목합니다.

모든 Pod 간 통신은 **Service 이름** 으로 이뤄집니다. CoreDNS가 이름을 ClusterIP로 바꿔주고, kube-proxy의 iptables 규칙이 실제 Pod로 요청을 꽂아 넣습니다. 5장에서 본 흐름이 그대로 동작하는 현장이 됩니다.

#### 폴더 구조와 이번 절의 진행 방식

EX08 폴더는 이미지를 찍는 부분(backend, db, frontend, redis)과 쿠버네티스 배포 설정(k8s)으로 나뉩니다.

```
ex08/
├── backend/
├── db/
├── frontend/
├── redis/
└── k8s/
    ├── namespace.yml
    ├── backend/
    ├── db/
    ├── frontend/
    └── redis/
```

Backend, DB, Frontend 이미지 레이어 자체는 3장의 EX07과 거의 같습니다. **차이는 딱 두 가지**입니다. Redis 이미지가 새로 추가된 것과, 백엔드 코드에 방문 횟수 카운터가 들어가면서 프론트엔드도 그 숫자를 표시하도록 살짝 수정된 것. 이미지 제작 흐름은 3장에서 이미 다뤘으니 여기서는 반복하지 않고 **변경된 부분만** 아래 표로 정리하고 넘어갑니다.

| 폴더 | 3장과 달라진 점 |
|------|-------------|
| redis/ | **새로 추가**. `FROM redis:7.4-alpine`만 있는 짧은 Dockerfile. 공식 이미지를 그대로 띄움 |
| backend/ | `entrypoint.sh`의 `git clone` 주소가 Redis 연동 버전으로 교체. `UserController`에 `redisTemplate.opsForValue().increment()` 한 줄 추가 |
| frontend/ | `index.html`에 `<h2>방문 횟수</h2>` 영역 추가. `nginx.conf`의 `upstream backend`가 Compose 때의 컨테이너명에서 **K8s Service명(`backend-service:8080`)** 으로 바뀜 |
| db/ | 변경 없음. 3장 EX07과 동일 |

이제 쿠버네티스 리소스를 한 덩어리로 쏟아붓지 않고 **세 단계**로 나누어 올립니다.

1. **1단계 — Frontend만**: Namespace + Frontend Deployment + Service + Ingress. 최소 세트를 눈으로 확인.
2. **2단계 — Backend 추가**: Backend Deployment + Service + ConfigMap + Secret. 환경 변수 주입이 실제 서비스에서 어떻게 꽂히는지 확인.
3. **3단계 — DB/Redis 추가**: DB Deployment/Service + PV/PVC + Redis Deployment/Service. 영구 저장소와 방문 횟수 카운터까지 붙여 최종 완성.

단계마다 Pod를 띄우고 결과를 눈으로 확인합니다. 한 단계씩 얹을 때마다 전체가 어떻게 자라는지 감이 잡힙니다.

> 전체 k8s 설정 파일은 https://github.com/metacoding-10-linux-docker/docker/tree/master/ex08/k8s 에서 확인할 수 있습니다.

#### 공통 준비 : 미니큐브 + Ingress Controller + 이미지

세 단계 모두 미니큐브와 Ingress Controller, 네 이미지가 필요합니다. 단계 순서에 상관없이 미리 한 번 돌려두면 뒤는 편해집니다.

```bash
minikube start                                              # 미니큐브 클러스터 시작
minikube addons enable ingress                              # Ingress Controller 활성화
kubectl get pod -n ingress-nginx                            # Controller Pod Running 확인
```

![](../assets/CH05/chap03-ingress-addon.png)

*그림 6-14 애드온으로 Nginx Ingress Controller가 설치*

![](../assets/CH05/chap03-ingress-controller-running.png)

*그림 6-15 ingress-nginx-controller Pod가 Running 상태면 정상*

미니큐브는 별도의 가상 환경 안에서 도는 클러스터입니다. 로컬 PC에서 `docker build`로 찍은 이미지를 미니큐브는 바로 알아보지 못합니다. 별도 레지스트리에 올리지 않고 그대로 쓰려면 **`minikube image build`** 로 미니큐브 내부에 직접 이미지를 찍어야 합니다.

```bash
minikube image build -t metacoding/db:1 ./db            # DB 이미지 빌드
minikube image build -t metacoding/backend:1 ./backend   # 백엔드 이미지 빌드
minikube image build -t metacoding/frontend:1 ./frontend # 프론트엔드 이미지 빌드
minikube image build -t metacoding/redis:1 ./redis       # Redis 이미지 빌드
```

![](../assets/CH05/chap03-67.png)

*그림 6-16 미니큐브 내부에 네 이미지가 차례로 빌드*

준비는 여기까지. 이제 1단계부터 차례로 올려봅니다.

### 6.3.2 1단계 : Frontend만 먼저 올려보기

첫 단계는 가장 단순한 조합입니다. Namespace를 만들고, 프론트엔드 Pod 하나를 띄우고, Service로 대표 주소를 뽑고, Ingress로 외부 요청을 받는 데까지. Backend도 DB도 없는 상태에서 **정적 페이지만 먼저 눈으로 확인**하는 게 목표입니다.

1단계에서 사용할 YAML은 네 개뿐입니다.

| 파일 | 역할 |
|------|------|
| `k8s/namespace.yml` | `metacoding` 네임스페이스 생성 |
| `k8s/frontend/frontend-deploy.yml` | Frontend Pod 1개 배포 |
| `k8s/frontend/frontend-service.yml` | Pod의 80포트를 `frontend-service`라는 이름으로 묶음 |
| `k8s/frontend/frontend-ingress.yml` | 외부 `/` 요청을 `frontend-service`로 연결 |

ConfigMap, Secret, PV/PVC는 이 단계에서 아직 등장하지 않습니다. 정적 HTML만 서빙하는 데는 추가 설정이 필요 없기 때문입니다. 2단계에서 백엔드가 들어올 때 ConfigMap과 Secret이 따라 붙고, 3단계에서 DB가 들어올 때 PV/PVC가 마지막으로 얹힙니다.

#### Namespace : 층을 나눈다

지금까지 오픈이가 만든 리소스는 전부 `default`라는 기본 공간에 생겼습니다. `metadata`에 `namespace`를 적지 않으면 쿠버네티스는 그 리소스를 **default 네임스페이스**에 올립니다. 혼자 실습할 때는 괜찮지만, 팀의 여러 서비스가 한 `default`에 섞이면 이름 충돌이 시작됩니다. 프론트엔드 팀의 `backend-service`와 결제팀의 `backend-service`가 같은 네임스페이스에 있으면 이름이 겹쳐서 만들 수 없습니다.

**Namespace** 는 회사 건물의 **층** 과 같습니다. 1층은 프론트엔드, 2층은 백엔드, 3층은 데이터 팀. 같은 건물 안에서 층만 나눠도 각 팀이 독립적으로 공간을 관리할 수 있습니다. 이름도 층마다 따로 씁니다.

![](../assets/CH05/k8s-namespace.png)

*그림 6-17 같은 클러스터 안에서 Namespace가 리소스를 층처럼 분리*

> **참고: Namespace**
> 쿠버네티스 리소스를 논리적으로 구분하는 가상 공간. 별도로 지정하지 않으면 모든 리소스는 **default** 네임스페이스에 들어간다.

이번 실습에서는 `metacoding`이라는 네임스페이스를 만들어 모든 리소스를 그 안에 넣습니다.

**ex08/k8s/namespace.yml**
```yaml
apiVersion: v1           # API 버전
kind: Namespace          # 리소스 종류
metadata:
  name: metacoding       # 네임스페이스 이름
```

```bash
kubectl apply -f k8s/namespace.yml    # Namespace 생성
```

![](../assets/CH05/chap03-68.png)

*그림 6-18 `metacoding` 네임스페이스 생성*

각 리소스 YAML의 `metadata`에 `namespace: metacoding`이 들어가 있는 이유가 여기 있습니다. 팀 단위로 분리하려면 이렇게 명시하는 게 관례입니다. 조회할 때는 `-n metacoding`을 붙여야 합니다.

#### Frontend Deployment + Service + Ingress

세 리소스를 한 번에 훑어봅니다. 이미지는 방금 빌드한 `metacoding/frontend:1`입니다. Nginx가 80포트에서 정적 HTML을 서빙하고, `/api/...` 요청은 아직 존재하지 않는 `backend-service`로 프록시하도록 설정되어 있습니다. 프록시 대상이 없으니 1단계에서는 `/api/...`만 502가 뜰 뿐, 정적 페이지 자체는 정상적으로 떠야 합니다.

**ex08/k8s/frontend/frontend-deploy.yml** (핵심 부분)
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend-deploy
  namespace: metacoding              # namespace 설정
spec:
  replicas: 1                        # pod 1개 생성
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
        - name: frontend-server
          image: metacoding/frontend:1
          ports:
            - containerPort: 80      # Nginx 80 포트
```

Frontend Service는 프론트엔드 Pod의 80포트를 클러스터 안 대표 번호로 묶고, Ingress는 외부 요청 `/`를 이 Service로 넘깁니다.

**ex08/k8s/frontend/frontend-ingress.yml**
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: frontend-ingress
  namespace: metacoding
spec:
  rules:
    - http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: frontend-service    # 프론트엔드 Service로 연결
                port:
                  number: 80
```

`path: /`는 모든 경로를 받는다는 뜻입니다. 어떤 URL이든 프론트엔드로 넘기고, `/api/...`에서 갈라지는 프록시는 nginx.conf가 내부에서 처리합니다.

#### 1단계 올리기

```bash
kubectl apply -f k8s/frontend/        # 프론트엔드 리소스 일괄 생성
kubectl get pod,svc,ingress -n metacoding   # 프론트엔드 리소스 상태 확인
```

Pod STATUS가 `Running`으로 바뀌고 Ingress ADDRESS가 채워질 때까지 1~2분 정도 기다립니다. 그동안 `minikube tunnel`을 새 터미널에서 켜둡니다.

```bash
minikube tunnel                       # 로컬 PC에서 클러스터 접근을 위한 터널 생성
```

브라우저에 `http://127.0.0.1`을 찍었습니다. 잠시 로딩이 돌더니 `<h1>사용자 리스트</h1>` 헤더와 함께 정적 페이지가 떴습니다. 회원 리스트 영역은 비어 있고, 방문 횟수 자리에도 기본값 `0`만 찍혀 있었습니다. `/api/users` 호출은 개발자 도구 네트워크 탭에서 502로 떨어지고 있었습니다.

*아직 백엔드도 DB도 없는데 일단 프론트가 뜨니까 안심이다.*

정적 페이지가 뜬다는 건 **Ingress → Frontend Service → Frontend Pod** 의 최소 경로가 끊기지 않았다는 뜻이었습니다. 나머지는 이 위에 덧붙이기만 하면 됩니다. 오픈이는 터미널로 돌아와 Pod와 Service가 각자 자리를 잡은 상태를 한 번 더 눈에 담았습니다.

- Namespace 하나가 `default`와 분리된 자기 공간을 만들어줬다.
- Deployment → Pod로 프론트엔드가 떠 있다.
- Service가 Pod의 80포트를 대표 주소로 묶고 있다.
- Ingress가 외부 `/` 요청을 Service로 꽂아준다.

이 네 덩어리가 **쿠버네티스 배포의 최소 세트**입니다. 2단계와 3단계는 이 위에 Backend와 DB/Redis를 얹는 과정일 뿐입니다. 실제 터미널에서는 다음 세 명령으로 상태를 확인해 둡니다.

```bash
kubectl get pod -n metacoding             # Pod가 Running인지 확인
kubectl get svc -n metacoding             # Service 목록과 ClusterIP 확인
kubectl get ingress -n metacoding         # Ingress ADDRESS가 채워졌는지 확인
```

Pod `STATUS`가 `Running`, Service에 `frontend-service`가 찍혀 있고, Ingress `ADDRESS`가 IP 한 줄로 채워져 있으면 1단계가 끝난 상태입니다.

### 6.3.3 2단계 : Backend 추가하기

1단계에서 뚫린 틀 위에 백엔드를 올립니다. Backend Deployment와 Service를 추가하고, 그 과정에서 **ConfigMap과 Secret이 실제 서비스에서 어떻게 꽂히는지**를 눈으로 봅니다. 6.1에서 `nginx-container`로 연습했던 구조가 Spring Boot 백엔드로 옮겨붙는 자리입니다.

1단계와 달라지는 자리는 두 곳입니다. 첫째, 환경 변수입니다. Spring Boot는 DB 주소와 비밀번호를 환경 변수로 받는데, 이 값들이 이미지 안에 박히면 안 됩니다. ConfigMap과 Secret으로 바깥에 두고 Deployment에서 끌어옵니다. 둘째, 포트입니다. 프론트엔드는 80이었지만 Spring Boot는 내부적으로 Tomcat의 기본 포트 8080을 씁니다. `containerPort: 8080`, `targetPort: 8080`으로 맞춰 Service에 연결합니다.

2단계에서 추가되는 YAML은 네 개입니다.

| 파일 | 역할 |
|------|------|
| `k8s/backend/backend-configmap.yml` | DB 주소, Redis 주소 같은 일반 설정 |
| `k8s/backend/backend-secret.yml` | DB 계정과 비밀번호 |
| `k8s/backend/backend-deploy.yml` | Backend Pod 2개 배포. `envFrom`으로 ConfigMap + Secret 주입 |
| `k8s/backend/backend-service.yml` | Pod의 8080포트를 `backend-service`라는 이름으로 묶음 |

Frontend YAML은 1단계에서 만든 그대로 남아 있고, 따로 손대지 않습니다. 새로 추가되는 네 개만 apply하면 됩니다.

#### Backend의 환경 변수 : ConfigMap + Secret

`backend-configmap`에는 DB 주소와 Redis 주소 같은 일반 설정이 들어가고, `backend-secret`에는 DB 계정과 비밀번호가 들어갑니다. DB Pod는 아직 없지만, ConfigMap 안에 **서비스 이름** 으로 `db-service:3306`, `redis-service:6379`를 적어둡니다. 3단계에서 DB와 Redis Service가 생성되는 순간 CoreDNS가 그 이름을 ClusterIP로 풀어주기 시작합니다. 일단 주소만 먼저 적어두고 실제 연결은 나중에 맞추는 구조입니다.

**ex08/k8s/backend/backend-configmap.yml** (핵심 부분)
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: backend-configmap
  namespace: metacoding
data:
  SPRING_DATASOURCE_URL: "jdbc:mysql://db-service:3306/metadb"   # DB 접속 URL (Service명)
  SPRING_REDIS_HOST: "redis-service"                              # Redis 호스트 (Service명)
  SPRING_REDIS_PORT: "6379"                                       # Redis 포트
```

`db-service`, `redis-service`는 **Service명**입니다. IP를 직접 쓰지 않는 이유는 6.1.5에서 다뤘습니다. Pod가 죽었다 살아도 Service 이름은 그대로입니다.

**ex08/k8s/backend/backend-secret.yml** (핵심 부분)
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: backend-secret
  namespace: metacoding
stringData:
  SPRING_DATASOURCE_USERNAME: "metauser"          # DB 계정
  SPRING_DATASOURCE_PASSWORD: "metacoding1234"    # DB 비밀번호
```

#### Backend Deployment : 모든 개념이 모이는 곳

`backend-deploy.yml`은 이번 실습에서 가장 많은 개념이 한 파일에 모이는 자리입니다. `replicas: 2`로 Pod를 두 개로 띄우고, `envFrom`으로 ConfigMap과 Secret을 한꺼번에 가져와 환경 변수로 주입합니다.

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

Spring Boot는 그 환경 변수를 `application.yml`의 placeholder로 자동으로 끌어다 씁니다. 6.1에서 연습한 구조 그대로입니다. 로컬에서 `application-prod.yml`을 따로 두고 환경마다 `-Dspring.profiles.active=prod`로 갈아끼우던 방식이, K8s에서는 **Secret/ConfigMap을 환경마다 다르게 적용**하는 방식으로 올라온 셈입니다.

Backend Service는 Pod 두 개의 8080포트를 묶어 `backend-service`라는 대표 주소로 묶습니다. Frontend의 `nginx.conf`가 이미 `backend-service:8080`을 upstream으로 쓰고 있기 때문에, 이 Service가 뜨는 순간 프론트의 `/api/...` 프록시가 살아납니다.

#### 2단계 올리기

```bash
kubectl apply -f k8s/backend/         # 백엔드 리소스 일괄 생성
```

백엔드 Pod는 내부에서 `git clone`(약 1분)과 Gradle 빌드(약 3~5분), Spring 기동(약 1분)을 차례로 돌립니다. 총 5~7분 정도가 걸립니다. 오픈이는 `kubectl get pod -n metacoding`을 몇 번 새로고침하며 STATUS가 `Running`으로 넘어가는지 지켜봤습니다.

```bash
kubectl logs deploy/backend-deploy -n metacoding --tail=20  # 백엔드 로그 확인
```

로그 맨 아래 `Tomcat started on port 8080` 메시지가 찍히면 Spring이 요청을 받을 준비가 끝난 상태입니다. 브라우저에서 `http://127.0.0.1`을 새로고침했습니다. 이번엔 `/api/users` 호출이 502 대신 500으로 바뀌었습니다. 개발자 도구의 응답을 열어보니 **DB 연결 실패**였습니다.

*요청은 프론트에서 백엔드까지는 도착했는데 DB가 없네.*

이게 오히려 좋은 신호였습니다. 프론트의 `/api/...` 요청이 nginx.conf의 `proxy_pass`를 타고 Backend Service로 들어가고, 그 요청이 두 개의 Backend Pod 중 하나에 꽂혔다는 증거였기 때문입니다. CoreDNS가 `backend-service`를 ClusterIP로 풀어줬고, kube-proxy의 iptables 규칙이 Pod 중 하나로 DNAT을 걸었다는 뜻입니다. 5장에서 배운 흐름이 그대로 작동하고 있었습니다.

남은 문제는 하나입니다. **DB가 없다.**

오픈이가 한숨을 내쉬는 사이 팀장이 지나가며 한 마디를 얹었습니다.

**팀장**: "이제 데이터만 붙이면 되겠네."

2단계에서 확인된 것을 오픈이는 한 번 더 정리해 두었습니다.

- Backend Pod 두 개가 `app: backend` 라벨로 묶여 Deployment의 관리를 받는다.
- ConfigMap과 Secret이 `envFrom` 한 묶음으로 Spring Boot의 환경 변수에 꽂혔다.
- Frontend의 `nginx.conf`가 부르던 `backend-service`라는 이름이 CoreDNS를 거쳐 실제 Pod로 도달한다.
- DB 연결 실패는 **연결이 안 된 것**이 아니라 **연결할 대상이 아직 없는 것**이다.

남은 구멍이 정확히 어디인지 보이니 3단계는 그 자리만 채우면 됩니다.

### 6.3.4 3단계 : DB와 Redis까지 붙이기

마지막 단계에서 DB와 Redis를 올립니다. DB Deployment에는 6.2에서 연습한 **PV/PVC**가 실제로 꽂힙니다. Pod 하나가 죽어도 회원 데이터는 PV에 남습니다. Redis는 방문 횟수 카운터를 맡습니다. 여기까지 얹으면 백엔드의 `/api/users` 요청이 DB에서 회원을 꺼내고, Redis의 카운터를 올리고, 두 값을 함께 돌려주는 최종 흐름이 완성됩니다.

이번 단계에서 확인할 포인트도 두 가지로 줄입니다. 첫째, **영구 저장소**. DB Pod를 일부러 삭제해 봐도 다시 뜬 Pod가 이전 회원 데이터를 그대로 들고 올라오는지. 둘째, **전 구간 연결**. Frontend에서 출발한 요청이 Backend를 거쳐 DB와 Redis까지 한 번에 도달하는지. 두 가지가 모두 확인되면 6.3의 최종 그림이 손에 들어옵니다.

3단계에서 추가되는 YAML은 일곱 개입니다.

| 파일 | 역할 |
|------|------|
| `k8s/db/db-pv.yml` | MySQL 데이터용 실제 저장 공간 |
| `k8s/db/db-pvc.yml` | DB Pod가 요청하는 창고 신청서 |
| `k8s/db/db-secret.yml` | MySQL root 계정/비밀번호 |
| `k8s/db/db-deploy.yml` | DB Pod 1개. `/var/lib/mysql`을 PVC에 마운트 |
| `k8s/db/db-service.yml` | DB Pod의 3306포트를 `db-service`로 묶음 |
| `k8s/redis/redis-deploy.yml` | Redis Pod 1개 배포 |
| `k8s/redis/redis-service.yml` | Redis의 6379포트를 `redis-service`로 묶음 |

Frontend와 Backend YAML은 앞 단계에서 만든 그대로 유지됩니다.

#### DB Deployment + PV/PVC

db-deploy.yml에서는 6.2의 PV/PVC를 실제로 꽂습니다. `volumeMounts`로 컨테이너의 `/var/lib/mysql` 경로를 `db-pvc`에 연결해 놓으면, Pod가 죽어도 MySQL 데이터 파일은 PV에 그대로 남습니다.

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

`volumes`에서 이름을 `data`로 붙여두고, `volumeMounts`에서 같은 이름으로 참조해 컨테이너 경로에 꽂는 구조입니다. `db-pv.yml`, `db-pvc.yml`, `db-secret.yml`, `db-service.yml`의 구조는 앞 절에서 본 형태와 동일합니다.

#### Redis Deployment + Service

Redis는 별도 설정이 거의 필요 없습니다. Deployment에서 이미지와 포트만 지정하고, Service가 `redis-service`라는 이름으로 6379를 묶습니다. Backend의 ConfigMap에 이미 `redis-service:6379`가 적혀 있기 때문에, Redis Service가 생성되는 순간 CoreDNS가 그 이름을 풀어주기 시작합니다.

| 항목 | redis |
|------|-------|
| image | metacoding/redis:1 |
| containerPort | 6379 |
| replicas | 1 |
| Service port | 6379 |

#### 3단계 올리기

```bash
kubectl apply -f k8s/db/              # DB + PV/PVC + Secret + Service 생성
kubectl apply -f k8s/redis/           # Redis Deployment + Service 생성
```

또는 앞 단계들을 이미 올린 상태에서 한 번에 정리하고 싶으면 이렇게도 쓸 수 있습니다.

```bash
kubectl apply -f k8s/ --recursive     # k8s 폴더의 모든 리소스 일괄 적용 (멱등)
```

`--recursive`는 k8s 아래 하위 폴더까지 내려가서 모든 YAML을 순회합니다. 이미 존재하는 리소스는 변경사항만 반영되고, 없던 리소스는 새로 생성됩니다.

![](../assets/CH05/chap03-69.png)

*그림 6-19 백엔드, DB, 프론트엔드, Redis의 모든 리소스가 일괄로 생성*

```bash
kubectl get deploy,pod,service -n metacoding  # 전체 리소스 상태 확인
```

![](../assets/CH05/chap03-70.png)

*그림 6-20 Deployment, Pod, Service가 metacoding 네임스페이스에 나란히 떠*

DB Pod가 Running으로 올라오고, PV와 PVC가 `Bound` 상태인지 확인한 뒤 백엔드 로그를 다시 봅니다.

```bash
kubectl logs deploy/db-deploy -n metacoding --tail=5       # DB 서버 로그 확인
kubectl logs deploy/backend-deploy -n metacoding --tail=20 # 백엔드 서버 로그 확인
```

![](../assets/CH05/chap03-71.png)

*그림 6-21 DB, 프론트엔드, 백엔드의 시작 로그를 확인*

DB는 `ready for connections`가, 백엔드는 `HikariPool-1 - Start completed`와 `Tomcat started on port 8080`가 연달아 찍혀 있어야 합니다. 2단계에서 나던 DB 연결 실패가 이 시점에서 사라집니다. 프론트에서 백엔드, 백엔드에서 DB와 Redis까지 한 줄로 이어졌습니다.

#### 최종 확인 : 방문 횟수가 올라가는가

브라우저에서 `http://127.0.0.1`을 새로고침했습니다. 잠깐 로딩 표시가 돌더니 페이지가 떴습니다. 회원 이름이 표 형태로 쭉 내려오고, 상단에 **방문 횟수: 1** 이라는 숫자가 찍혀 있었습니다.

*떴다.*

![](../assets/CH05/chap03-ingress-result.png)

*그림 6-22 Ingress를 거쳐 웹사이트가 화면에 응답*

오픈이는 F5를 두 번 더 눌렀습니다. 방문 횟수가 **2**, **3** 으로 올라갔습니다. 화면 숫자가 한 칸씩 오를 때마다 안도감 같은 게 뒤늦게 올라왔습니다. 네 개의 Pod가 각자 자리에서 돌고 있고, Service가 이름으로 서로를 부르고 있고, Redis가 카운터를 받아 기록하고 있다는 뜻이었습니다.

![](../assets/CH05/chap03-ingress-result2.png)

*그림 6-23 여러 번 새로고침하면 방문 횟수가 증가*

자동 복구와 무중단 배포까지 뒤에 딸려오는 상태였습니다. `minikube service`로 임시 URL을 뽑아 접속하던 4~5장의 방식과 달리, Ingress는 도메인 기반 라우팅이 가능해 실제 운영 환경에 훨씬 가깝습니다.

새 터미널을 하나 더 열고, 실제로 백엔드 두 Pod에 요청이 분산되는지 확인했습니다.

```bash
kubectl get pod -n metacoding         # metacoding 네임스페이스의 Pod 목록 조회
```

![](../assets/CH05/chap03-75.png)

*그림 6-24 Pod 목록에 backend-deploy가 두 개 올라와*

```bash
kubectl logs deploy/backend-deploy -n metacoding --tail=10  # 백엔드 서버 로그 확인
```

![](../assets/CH05/chap03-76.png)

*그림 6-25 백엔드 Pod 1에 요청이 들어와 SELECT 쿼리가 출력된 로그*

![](../assets/CH05/chap03-77.png)

*그림 6-26 백엔드 Pod 2에도 SELECT 쿼리가 찍힙니다. 요청이 분산된 모습*

두 Pod 모두 `SELECT * FROM users` 로그가 남아 있었습니다. `backend-service`가 들어온 요청을 두 Pod에 번갈아 넘기고 있다는 증거였습니다. 5장에서 배운 Service의 로드밸런싱이 눈으로 확인된 순간이었습니다.

#### 전체 패킷 경로

오픈이가 `http://127.0.0.1`을 찍었을 때, 패킷은 아래 관문을 차례로 통과합니다.

```
브라우저 -> minikube tunnel -> Ingress Controller(Nginx Pod)
        -> frontend-service -> Frontend Pod
        -> (프론트엔드가 /api/users 요청)
        -> backend-service -> Backend Pod
        -> db-service -> DB Pod / redis-service -> Redis Pod
```

이 경로에서 모든 서비스 간 호출은 IP가 아니라 **서비스 이름** 으로 일어납니다. CoreDNS가 이름을 ClusterIP로 바꾸고, 각 Service 뒤에 놓인 **kube-proxy의 iptables 규칙** 이 실제 Pod로 DNAT을 수행합니다. 5장의 `Ingress(L7) → Service(Label-Selector) → kube-proxy(iptables) → Pod`가 말 그대로 순서대로 동작하는 현장입니다.

![](../assets/CH05/net-10a-full-path.png)

*그림 6-27 전체 경로 (1) 브라우저에서 Frontend Pod까지 도달하는 과정*

![](../assets/CH05/net-10b-full-path.png)

*그림 6-28 전체 경로 (2) Frontend에서 Backend, DB, Redis까지의 흐름*

세 단계를 돌아보면 쿠버네티스가 한 일은 간단했습니다. **이름만 맞춰두면 나머지는 알아서 맞물린다.** Frontend의 nginx.conf가 `backend-service`라는 이름을 부르고, Backend의 ConfigMap이 `db-service`와 `redis-service`라는 이름을 가리키고, 각 Service가 그 이름으로 등록되는 순간 CoreDNS가 이어줍니다. 1단계에서 뚫어둔 틀 위로 2단계, 3단계가 얹히면서도 한 번도 기존 설정을 되짚어 고칠 필요가 없었습니다.

3단계에서 확인된 것을 마지막으로 묶어 봅니다.

- PV/PVC로 DB 데이터가 Pod 수명과 분리되어 영구 저장소에 남는다.
- Redis Service가 올라오는 순간 Backend의 `redis-service:6379` 호출이 바로 연결된다.
- Backend Pod 두 대에 요청이 번갈아 꽂히는 로드밸런싱이 실제 로그에서 눈으로 확인된다.
- `Ingress → Service → Pod → DB/Redis` 전체 경로가 5장에서 그린 그림 그대로 동작한다.

*한 번에 다 올리든 나눠서 올리든, 쿠버네티스 입장에서는 같은 그림.*

오픈이는 노트에 이 한 줄을 남겨 뒀습니다. 선언적 관리의 감각이 종합실습 수준에서 손에 잡힌 순간이었습니다. 3장의 `docker-compose up` 한 줄이 한 번에 띄워줬던 네 개의 컨테이너가, 쿠버네티스에서는 서비스 단위로 쪼개 얹어도 같은 모습으로 살아납니다. 차이는 분명했습니다. Compose는 "지금 이 순간 네 개를 같이 켜는 명령", 쿠버네티스는 "네 개가 이런 상태여야 한다는 선언". Pod 하나가 죽어도 다시 살아나고, 트래픽이 몰려도 복제가 붙고, 배포를 갈아 끼울 때도 접속이 끊기지 않습니다. 1장의 새벽 알람이 이제는 쿠버네티스가 대신 받아주는 구조가 된 셈입니다.

## 6.4 문제가 생겼을 때 : 디버깅

### 6.4.1 Pending으로 멈춘 Pod

배포를 처음 성공한 다음 날 오후, 오픈이는 코드를 조금 고치고 새로 배포했습니다. 같은 `kubectl apply -f k8s/ --recursive`였는데 이번엔 결과가 달랐습니다.

어떤 문제였는지 이야기하기 전에, 용어부터 한 가지 정리하고 갑니다. Pod의 `STATUS` 칼럼에는 `Running`(떠 있음), `Pending`(뜨려고 시도 중), `CrashLoopBackOff`(계속 재시작), `ImagePullBackOff`(이미지 못 가져옴) 네 가지가 자주 등장합니다. 오픈이가 이번에 만난 상태는 두 번째인 `Pending`이었습니다.

```bash
kubectl get pod -n metacoding
```

Pod 목록을 띄우자 몇 개가 **Pending** 에 머물러 있었습니다. STATUS가 `Running`으로 넘어가지 않고 2분, 3분이 지나도 그대로였습니다. 선풍기 돌아가는 소리가 다시 크게 들렸습니다.

*왜 안 떠.*

어제는 한 번에 됐던 게 오늘은 안 되는 상황이었습니다. 오픈이는 처음엔 `kubectl apply`를 다시 쳤습니다. 결과는 같았습니다. 두 번째로 Pod를 지우고 다시 만들어 봤습니다. 그래도 Pending이었습니다.

선배가 지나가며 모니터를 봤습니다.

**선배**: "지우고 다시 만들지 말고, 왜 안 되는지부터 먼저 봐."

오픈이는 키보드에서 손을 떼고 의자에 잠깐 기댔습니다. `Pending`이라는 상태는 "아직 뜨려고 시도 중" 혹은 "뜨지 못하고 있다"는 신호였습니다. 이유는 쿠버네티스가 **자기 로그에 이미 적어 놓은 상태** 였습니다. 그 로그를 읽기만 하면 됐습니다.

쿠버네티스에는 문제를 진단할 때 네 개의 명령어가 쓰입니다. `logs`, `describe`, `get events`, `get endpoints`. 이 네 개면 대부분 해결됩니다.

### 6.4.2 네 개의 기본 진단 명령어

#### 로그 확인 : kubectl logs

Pod 안 애플리케이션의 stdout/stderr를 그대로 보여줍니다. 앱이 떠 있는데 동작이 이상할 때 가장 먼저 여는 창입니다.

```bash
kubectl logs <Pod명>                  # Pod 로그 확인
kubectl logs <Pod명> --tail=20        # 최근 20줄만 확인
kubectl logs <Pod명> -f               # 실시간 로그 스트리밍
```

#### 상태와 이벤트 확인 : kubectl describe

Pod의 현재 상태, 환경 변수, 마운트 정보, 그리고 하단의 **Events** 섹션에 쿠버네티스가 직접 남긴 메시지가 시간순으로 보입니다. `Pending` 상태의 Pod는 보통 여기에 원인이 적혀 있습니다.

```bash
kubectl describe pod <Pod명>          # Pod 상세 정보 + 이벤트
kubectl describe service <Service명>  # Service 상세 정보
```

#### 클러스터 전체 이벤트 : kubectl get events

특정 리소스가 아니라 클러스터 전체에서 일어난 이벤트를 시간순으로 봅니다.

```bash
kubectl get events --sort-by='.lastTimestamp'  # 최신 이벤트 순 조회
```

#### 연결 상태 확인 : kubectl get endpoints

Service가 실제로 어떤 Pod에 연결되어 있는지 보여줍니다. Service에 요청은 가는데 응답이 없으면 여기가 비어 있는 경우가 많습니다.

```bash
kubectl get endpoints <Service명>
```

### 6.4.3 4단계 진단 순서

오픈이는 선배의 한 마디를 따라 네 단계를 순서대로 돌려봤습니다.

**1단계. Pod 상태 확인**

```bash
kubectl get pod -n metacoding
```

Pending인 Pod 이름을 확인했습니다. backend-deploy의 한 Pod이 Pending에 멈춰 있었습니다.

**2단계. describe로 Events 읽기**

```bash
kubectl describe pod <Pending Pod명> -n metacoding
```

출력 맨 아래 Events 섹션에 이런 줄이 찍혀 있었습니다.

```
Failed to pull image "metacoding/backend:2":
rpc error: ... not found
```

이미지 태그가 `:2`로 박혀 있었는데, 오픈이는 미니큐브 내부에 아직 `:1`까지만 빌드해 놓은 상태였습니다. `backend-deploy.yml`을 수정하면서 이미지 태그를 올려놓고 빌드는 새로 안 돌린 것이었습니다. 증상은 **ImagePullBackOff** 였습니다. `BackOff`는 "실패 후 재시도 간격"이라는 뜻입니다. 이미지를 못 가져와 계속 재시도를 기다리는 중이라는 신호였습니다.

*describe 한 번에 끝났는데, 아까는 왜 apply만 반복했지.*

3단계와 4단계까지 가기 전에 원인이 보였습니다.

**3단계. 앱 에러라면 logs**

`Running`인데 동작이 이상하면 `kubectl logs`로 애플리케이션 에러를 봅니다. Spring이 DB 접속 실패로 죽으면 여기서 스택트레이스가 잡힙니다.

**4단계. Service 연결이 안 되면 endpoints**

Service 호출이 연결 자체가 안 되면 `kubectl get endpoints`를 찍어 봅니다. 결과가 `<none>`이면 Service의 `selector`와 Pod의 `labels`가 안 맞는 경우가 대부분입니다.

### 6.4.4 자주 만나는 에러 모음

| 증상 | 원인 | 해결 |
|------|------|------|
| **ImagePullBackOff** | 이미지 이름 오타 또는 레지스트리 접근 불가 | `kubectl describe pod <Pod명>`으로 이미지명 확인. 오타를 수정하거나 이미지가 레지스트리에 있는지 확인 |
| **CrashLoopBackOff** | 앱 에러로 컨테이너가 반복 재시작 | `kubectl logs <Pod명>`으로 에러 로그 확인. 앱 코드나 환경 변수 설정 점검 |
| **Pending** | 리소스(CPU/메모리) 부족 또는 PVC 바인딩 실패 | `kubectl describe pod <Pod명>`의 Events에서 원인 확인. 노드 리소스나 PV 설정 점검 |
| **Service 접속 불가** | selector와 Pod labels 불일치 | `kubectl get endpoints <Service명>`으로 연결된 Pod가 있는지 확인. labels가 일치하는지 점검 |
| **Ingress 접속 불가** | Ingress Controller 미설치 또는 tunnel 미실행 | `kubectl get pod -n ingress-nginx`로 Controller 확인. `minikube tunnel` 실행 여부 점검 |

오픈이는 이미지 태그를 다시 `:1`로 돌리고 `kubectl apply -f backend-deploy.yml`을 쳤습니다. 롤아웃이 돌더니 Pod 상태가 `Running`으로 바뀌었습니다. 방문 횟수가 다시 한 칸씩 올라갔습니다.

*네 단계. 지우지 말고, 먼저 읽자.*

이게 이번 챕터에서 오픈이가 챙긴 마지막 습관이었습니다.

## 이것만은 기억하자

- **설정은 코드 밖, 데이터는 영구히.** ConfigMap(메뉴판)과 Secret(금고)으로 설정과 민감 정보를 이미지에서 분리하고, PV/PVC로 Pod가 사라져도 데이터가 남도록 합니다. 환경 변수는 프로세스 시작 시점에 한 번만 꽂히므로 ConfigMap을 바꾼 뒤에는 `kubectl rollout restart`로 Pod를 재시작해야 반영됩니다.
- **Secret은 금고가 아니라 본사 금고처럼 더 조심히 다루는 상자다.** Base64는 암호화가 아니므로, 실제 보안은 RBAC으로 조회 권한을 제한하거나 etcd 암호화 혹은 외부 Vault를 붙여 확보합니다.
- **CoreDNS는 클러스터의 전화번호부다.** 2장 Docker DNS가 클러스터 규모로 확장된 것입니다. `서비스명.네임스페이스.svc.cluster.local` 형태의 레코드가 자동 등록되고, 같은 네임스페이스라면 서비스명만으로 서로를 부를 수 있습니다.
- **종합 배포는 한 번에 몰아치지 않아도 된다.** Frontend → Backend → DB/Redis 세 단계로 나눠 얹어도 같은 그림이 완성됩니다. 이름만 맞춰두면 쿠버네티스가 순서에 상관없이 맞물려 줍니다.
- **문제가 생기면 지우지 말고 먼저 읽는다.** `kubectl get pod → describe → logs → get endpoints` 네 단계면 대부분의 문제는 원인까지 따라갑니다.

### 책 전체를 돌아보며

오픈이가 챕터 1에서 처음 겪은 배포 지옥을 다시 떠올려 봅니다. Java 버전이 서로 달라 한 서버에서 세 프로젝트가 충돌했고, 서버 증설 견적은 반려됐고, 환경 차이를 알아낼 수단이 없었습니다. 책을 따라오면서 오픈이는 여섯 개의 관문을 차례로 통과했습니다. 각 관문은 한 줄짜리 질문에서 시작됐습니다.

- **챕터 1.** *"세 프로젝트가 한 서버에서 충돌하는데, 어떻게 표준 상자에 담지?"* 컨테이너라는 아이디어. 표준 상자에 담으면 어디서든 같은 결과가 나온다는 것.
- **챕터 2.** *"그 상자를 한 서버에서 어떻게 격리해서 돌리지?"* Docker 하나의 원리. 격리된 프로세스, 이미지와 컨테이너, 포트포워딩과 볼륨. 컨테이너 하나를 손으로 주무를 수 있게 된 지점.
- **챕터 3.** *"여러 컨테이너를 매번 수동으로 관리하기 지쳤는데, 한 번에 조립할 수 없을까?"* Dockerfile과 Docker Compose. 컨테이너 여러 개를 한 번에 조립하는 법. 서비스라는 단위가 처음 보이기 시작한 자리.
- **챕터 4.** *"새벽에 죽은 Pod를 누가 살려?"* 쿠버네티스의 첫 관문. Pod, Deployment. "원하는 상태를 선언하면 시스템이 맞춘다"는 감각.
- **챕터 5.** *"Pod IP가 바뀌는데 어떻게 찾아?"* 네트워크 조립. Service, Ingress, kube-proxy, CoreDNS. Docker 시절의 용어가 이름만 바꿔 클러스터 규모로 올라가는 장면.
- **챕터 6.** *"비밀번호와 데이터는 어떻게 안전하게?"* 실제 운영. 설정 분리, 데이터 보존, 네 개의 서비스를 단계별로 얹는 종합 배포, 그리고 디버깅. 책을 덮은 뒤에도 남을 습관.

여섯 관문의 지도가 그려졌다면, 이제 책을 덮고 나서도 길을 잃지 않을 수 있습니다. 그 대신, 책을 덮고 나면 `kubectl` 옵션 중 상당수는 기억에서 흐려질 것입니다. 괜찮습니다. 옵션은 공식 문서에 있습니다. 남아야 할 건 **"어떤 문제가 있고, 그 문제를 어떤 도구가 풀어주고, 그 도구끼리는 어떻게 맞물리는가"** 에 대한 지도입니다. 이 지도가 머릿속에 남아 있다면 새로운 에러를 만나도 어느 문서를 펼쳐야 할지 판단할 수 있습니다. 명령어는 잊어도 됩니다. 지도가 남으면 이 책은 제 역할을 한 것입니다.

### 마치며

이 책은 쿠버네티스의 **기초** 를 다룹니다. 독자 한 명이 하나의 클러스터 위에 하나의 서비스를 올리는 데까지. 그 너머 운영의 깊은 영역은 이 책의 범위 밖에 있습니다. 다만 이 책을 마친 뒤에 어디로 이어지는지 한 번 짚어두면 다음 걸음이 조금 덜 막막할 것입니다.

**이 책을 마치면 할 수 있는 것**

- Pod, Deployment, Service, Ingress로 서비스 배포
- ConfigMap/Secret/PV/PVC로 설정과 데이터 관리
- Namespace로 리소스 분리
- 기본 디버깅(logs / describe / events / endpoints) 순서 적용

**다음에 배울 수 있는 것 (제목만)**

- **StatefulSet**: 상태를 가진 Pod (DB 클러스터 등)
- **DaemonSet**: 모든 노드에 배포되는 Pod (로그 수집 등)
- **Job / CronJob**: 일회성 · 정기 작업
- **HPA(HorizontalPodAutoscaler)**: 자동 스케일링
- **RBAC**: 역할 기반 접근 제어
- **NetworkPolicy**: Pod 간 통신 제한
- **Helm**: 패키지 관리

**실무로 나갈 때**

팀이 이미 쓰는 쿠버네티스 배포 방식을 먼저 이해하고, 필요한 개념을 하나씩 깊이 학습하는 것이 효율적입니다. "모든 걸 알고 시작"할 수는 없습니다. 오픈이가 그랬듯, 문제를 만나며 성장합니다. 새로운 에러를 만났을 때 `describe`를 먼저 치는 손끝이 남았다면, 그게 이 책이 가장 바라던 것입니다.

오픈이는 노트북을 덮기 전 한 줄을 적어 뒀습니다.

> "새벽에 알람이 와도 쿠버네티스가 먼저 움직인다. 물론, 알람이 아예 안 오는 게 제일 좋긴 하다."

팀장이 지나가다가 그 화면을 보고 짧게 웃었습니다.

**팀장**: "이제 운영 얘기할 때 낯설지는 않겠네."

선배도 커피잔을 들며 한 마디를 보탰습니다.

**선배**: "명령어보다 지도가 남았으면 된 거야."

오픈이는 그제야 어깨에서 힘을 뺐습니다. 사무실 창밖이 어느새 저녁이 되어 있었습니다.
