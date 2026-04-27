# Ch.3 Docker 다루기

> 한 줄 요약: 여러 컨테이너를 자동으로 구성하고 Docker Compose로 한 번에 띄운다
> 핵심 개념: Dockerfile, NGINX, Redis, MySQL, Docker Compose

오픈이는 Docker의 기본기를 익혔습니다. 컨테이너를 띄우고, 리눅스 명령어로 내부를 탐색하고, 이미지를 만들어 공유하는 것까지. 그런데 하나 불만이 생겼습니다. 컨테이너를 새로 만들 때마다 vim을 또 설치해야 한다는 겁니다.

> **오픈이**: "선배, 컨테이너 새로 만들 때마다 apt update, apt install... 또 해야 돼요?"
>
> **선배**: "당연히 그러면 안 되지. 밀키트 알지? 재료랑 양념 다 들어있어서 봉지만 뜯으면 되잖아. Docker에도 그런 게 있어. **Dockerfile** 이라고."

## 3.1 프로비저닝 : 환경을 자동으로 구성하다

매번 장을 보고 재료를 손질하고 양념을 만드는 과정을 반복하는 대신 밀키트를 쓰는 것과 같습니다. 밀키트는 재료와 양념이 이미 준비되어 있어 봉지만 뜯으면 바로 조리할 수 있습니다. 프로비저닝도 마찬가지입니다. 필요한 패키지와 설정을 미리 정의해두면 컨테이너를 만들 때마다 자동으로 환경이 구성됩니다.

![](../assets/CH03/chap02-provisioning.png)
*수동 세팅과 프로비저닝*

> **프로비저닝(Provisioning)**: 도커에서 프로비저닝은 컨테이너가 처음 생성될 때 필요한 환경을 자동으로 세팅하는 과정을 의미합니다. 컨테이너가 실행되면 쓸 수 있는 설정, 패키지, 파일 등을 미리 준비하는 작업입니다.

### 3.1.1 Dockerfile : 프로비저닝 설계도

Docker에서는 프로비저닝을 위해 **Dockerfile** 을 사용합니다.

> **Dockerfile**: 컨테이너가 실행될 때 필요한 환경을 자동으로 구성해주는 이미지를 생성하기 위한 스크립트로, 컨테이너를 만들기 위한 레시피입니다.

Dockerfile은 한 번 작성하면 누가, 어디서 실행해도 같은 환경이 만들어지는 자동 조립 설명서입니다. Dockerfile에 필요한 설정을 작성하고 `docker build` 명령을 실행하면 Docker 엔진이 Dockerfile을 읽고 이미지를 생성합니다.

이렇게 만들어진 이미지를 `docker run`으로 실행하면 새로운 컨테이너가 생성되고, Dockerfile에서 구성한 설정이 적용됩니다.

Dockerfile에서 컨테이너가 실행되기까지 세 단계를 거칩니다.

![](../assets/CH03/chap02-1.png)
*Dockerfile에서 이미지 생성 및 컨테이너 실행 과정*

**1단계 — Dockerfile 작성.** 텍스트 파일에 환경 구성을 적습니다. 베이스 이미지, 설치할 패키지, 복사할 파일, 실행할 명령을 순서대로 기록합니다.

**2단계 — docker build.** Docker 엔진이 Dockerfile을 위에서 아래로 읽으며 각 줄을 실행합니다. 결과물이 **이미지(Image)** 로 저장됩니다. 이미지는 읽기 전용이며 한 번 만들어지면 변하지 않습니다.

**3단계 — docker run.** 이미지를 기반으로 **컨테이너(Container)** 를 생성하고 실행합니다. 하나의 이미지에서 컨테이너를 몇 개든 만들 수 있습니다. 컨테이너를 삭제해도 이미지는 그대로 남아 있으므로 다시 실행하면 동일한 환경이 만들어집니다.

아래는 Dockerfile에서 사용하는 주요 설정입니다.

**[참고]** Dockerfile 주요 설정 구조

```dockerfile
FROM  <이미지명>

WORKDIR <기준 작업 경로 설정>

COPY <파일을 컨테이너 내부로 복사>

RUN <이미지 빌드 시 실행할 리눅스 명령 (패키지 설치 등)>

ENV <환경 변수 설정>

CMD <컨테이너 시작 시 메인 프로세스에 실행되는 명령어>

ENTRYPOINT <메인 프로세스를 지정하는 명령어>
```

### 3.1.2 빌드 시점과 실행 시점

설정이 많은데, 중요한 건 **언제 실행되느냐**입니다. Dockerfile의 지시어는 두 시점으로 나뉩니다.

#### 빌드 시점 — `docker build`를 실행할 때 처리

이 설정은 실행된 결과가 이미지에 기록됩니다.

| 지시어 | 역할 | 예시 |
|--------|------|------|
| `FROM` | 사용할 이미지를 선택합니다. 모든 Dockerfile의 첫 줄입니다. | `FROM ubuntu:24.04` |
| `WORKDIR` | 이후 지시어가 실행될 기본 경로를 지정합니다. 경로가 없으면 자동 생성됩니다. | `WORKDIR /app` |
| `RUN` | 이미지 안에서 명령어를 실행합니다. 패키지 설치, 설정 변경 등에 사용합니다. | `RUN apt install -y vim` |
| `COPY` | 호스트(내 PC)의 파일을 이미지 내부로 복사합니다. | `COPY index.html /app/` |
| `ENV` | 환경 변수를 설정합니다. 빌드 시 이미지에 기록되고, 컨테이너 실행 시에도 유지됩니다. | `ENV MYSQL_DATABASE=metadb` |

#### 실행 시점 — `docker run`으로 컨테이너가 시작될 때 실행

`docker build`로 이미지를 만들 때는 무시되고, `docker run`으로 컨테이너를 띄우는 순간 비로소 실행됩니다.

| 지시어 | 역할 | 예시 |
|--------|------|------|
| `CMD` | 컨테이너가 시작될 때 실행할 명령을 지정합니다. Dockerfile에 작성하지 않으면 베이스 이미지에 설정된 CMD가 실행됩니다. | `CMD ["/bin/bash"]` |
| `ENTRYPOINT` | 컨테이너가 시작될 때 항상 실행되는 고정 명령입니다. `CMD`와 함께 쓰면 `CMD`가 `ENTRYPOINT` 뒤에 붙어서 실행됩니다. | `ENTRYPOINT ["nginx"]` |

### 3.1.3 Dockerfile : 스크립트 작성

선배가 오픈이에게 파일을 작성하게 했습니다.

> **선배**: "vim 깔린 Ubuntu 이미지 하나 만들어 봐. 세 줄이면 끝이야."

CURSOR IDE에서 `Dockerfile`을 생성 후, 아래의 스크립트를 작성합니다. **(별도 확장자 없이 파일명만 Dockerfile로 입력하면 됩니다.)**

![](../assets/CH03/chap02-6.png)
*Dockerfile 생성 완료*

**[작성]** `Dockerfile`을 아래와 같이 작성합니다.

```dockerfile
FROM ubuntu:24.04                      # Ubuntu 24.04 이미지 사용
RUN apt update && apt install -y vim   # vim 패키지 설치
CMD ["/bin/bash"]                      # 컨테이너 시작 시 bash 실행
```

#### 실습해보기

**[실습]** 터미널을 Dockerfile이 위치한 폴더로 이동 후, 다음 명령어를 실행합니다.

```bash
docker build -t ubuntu-vim .       # . 은 현재 경로를 기준으로 Dockerfile을 읽어옴
```

![](../assets/CH03/chap02-7.png)
*docker build 실행 결과*

생성된 이미지를 기반으로 컨테이너를 생성합니다.

**[실습]** ubuntu-vim 이미지로 컨테이너를 실행하는 명령어입니다.

```bash
docker run -it ubuntu-vim   # ubuntu-vim 이미지로 컨테이너 실행
```

![](../assets/CH03/chap02-9.png)
*컨테이너 실행 및 접속*

컨테이너 내부 터미널창에서 `vim` 명령어를 실행하면 vim 편집 에디터 창이 뜹니다.

**[실습]** vim 에디터로 파일을 생성하는 명령어입니다.

```bash
vim a.txt   # a.txt 파일 생성
```

![](../assets/CH03/chap02-10.png)
*vim 에디터 실행 확인*

apt install 한 줄도 안 쳤는데 vim이 바로 됩니다. Dockerfile에 써둔 `RUN apt update && apt install -y vim`이 빌드 시점에 이미 실행됐기 때문입니다. Dockerfile 하나면 컨테이너의 원하는 환경을 동일하게 재현할 수 있습니다.

다음 실습을 위해 실행한 컨테이너를 종료합니다.

```bash
docker stop $(docker ps -q)   # 실행 중인 컨테이너 모두 중지
docker rm $(docker ps -aq)    # 중지된 컨테이너 모두 삭제
```

### 3.1.4 WORKDIR, COPY : 작업 경로와 파일 복사

> **WORKDIR**: 기본 작업 폴더를 설정하는 옵션입니다.
> **COPY**: 파일을 컨테이너 내부로 복사하는 옵션입니다.

3.1.3에서 생성한 폴더 내부에 **index.html** 파일을 생성합니다. index.html의 내부는 비어있는 빈 파일입니다.

![](../assets/CH03/chap02-11.png)
*폴더 및 파일 구조*

Dockerfile에 **WORKDIR**와 **COPY** 설정을 추가합니다. WORKDIR로 작업 디렉토리를 `/app`으로 지정하고 COPY로 로컬의 파일을 컨테이너로 복사하면 됩니다.

**[작성]** `Dockerfile`에 아래와 같이 html 파일을 복사하도록 수정합니다.

```dockerfile
FROM ubuntu:24.04                      # Ubuntu 24.04 이미지 사용
WORKDIR /app                           # 기본 작업 경로를 /app으로 설정
COPY ./index.html ./index.html         # 로컬의 파일을 컨테이너의 /app으로 복사
RUN apt update && apt install -y vim   # vim 패키지 설치
CMD ["/bin/bash"]                      # 컨테이너 시작 시 bash 실행
```

#### 실습해보기

**[실습]** WORKDIR와 COPY가 적용된 이미지를 빌드하는 명령어입니다.

```bash
docker build -t ubuntu-html .    # . 은 현재 경로를 기준으로 Dockerfile을 읽어옴
```

컨테이너를 생성합니다. 터미널에 접속하면 기본 경로가 `/app`으로 설정되어 있고 이 경로 안에서 `index.html` 파일을 확인할 수 있습니다.

**[실습]** 컨테이너를 실행하고 파일 목록을 확인하는 명령어입니다.

```bash
docker run -it ubuntu-html   # ubuntu-html 이미지로 컨테이너 실행
ls
```

![](../assets/CH03/chap02-13.png)
*실행 결과 확인*

실습 후 **exit** 명령어를 입력해 컨테이너에서 빠져나옵니다.

### 3.1.5 CMD, ENTRYPOINT : 기본 명령과 고정 명령

**CMD**는 `docker run`에서 다른 명령을 지정하면 그 명령이 대신 실행됩니다. 반면 **ENTRYPOINT**는 무슨 옵션을 주든 항상 실행됩니다. 식당에 비유하면 CMD는 "기본 메뉴"라서 손님이 바꿀 수 있지만, ENTRYPOINT는 "수저, 물 같은 기본 세팅"과 같습니다.

> **CMD** : 컨테이너가 시작될 때 실행할 명령을 지정합니다. Dockerfile에 작성하지 않으면 베이스 이미지에 설정된 CMD가 실행됩니다.
> **ENTRYPOINT**: 컨테이너가 시작될 때 반드시 실행되어야 하는 메인 프로세스를 지정하는 명령어입니다.

Dockerfile에 **ENTRYPOINT**를 추가해 echo 명령으로 메시지를 출력하도록 설정합니다.

**[작성]** `Dockerfile`에 ENTRYPOINT를 추가합니다.

```dockerfile
FROM ubuntu:24.04                      # Ubuntu 24.04 이미지 사용
WORKDIR /app                           # 기본 작업 경로를 /app으로 설정
COPY ./index.html ./index.html         # 로컬의 index.html을 컨테이너의 /app으로 복사
RUN apt update && apt install -y vim   # vim 패키지 설치
CMD ["/bin/bash"]                      # ENTRYPOINT가 있으면 CMD는 뒤에 붙어서 실행됨
ENTRYPOINT ["echo", "컨테이너 실행"]     # 컨테이너 시작 시 항상 실행되는 명령
```

#### 실습해보기

**[실습]** ENTRYPOINT가 적용된 이미지를 빌드 및 실행하는 명령어입니다.

```bash
docker build -t ubuntu-entry .         # 이미지 생성
docker run -it ubuntu-entry            # 컨테이너 실행
```

결과를 확인하면 **ENTRYPOINT**에 작성한 **컨테이너 실행 /bin/bash** 이 출력되고 프로세스는 즉시 종료됩니다. 왜 그럴까요?

![](../assets/CH03/chap02-15.png)
*ENTRYPOINT 실행 결과*

ENTRYPOINT가 있으면 CMD는 독립적으로 실행되지 않고, ENTRYPOINT 뒤에 붙어서 함께 실행됩니다. 즉 `echo "컨테이너 실행"` + `/bin/bash`가 합쳐져서 `echo "컨테이너 실행" /bin/bash`가 된 것입니다.

`echo`는 뒤에 오는 내용을 그대로 출력하고 끝나는 명령이라, "컨테이너 실행 /bin/bash"라는 글자만 화면에 찍고 종료됩니다. 메인 프로세스가 끝났으니 컨테이너도 즉시 종료됩니다.

다음 실습을 위해 실행한 컨테이너를 종료합니다.

```bash
docker stop $(docker ps -q)   # 실행 중인 컨테이너 모두 중지
docker rm $(docker ps -aq)    # 중지된 컨테이너 모두 삭제
```

Dockerfile로 환경 자동화를 할 수 있게 됐습니다. 그런데 프로젝트가 점점 커지면서 프론트엔드 페이지도 필요하고, 백엔드 API도 따로 돌아가야 했습니다. 한 서버에 전부 넣자니 뒤엉켜서 관리가 안 됩니다.

> **오픈이**: "선배, 프론트엔드랑 백엔드를 따로 띄우면 요청을 어떻게 나눠요?"
>
> **선배**: "NGINX라는 게 있거든. 요청 들어오면 URL 보고 맞는 서버로 보내줘."

## 3.2 NGINX : 웹 서버와 리버스 프록시

2장에서 nginx 이미지를 실행해 봤는데, 사실 NGINX는 단순히 HTML을 보여주는 것 외에도 강력한 기능을 갖추고 있습니다.

> **NGINX**: 웹 서버이자 프록시 서버로, 정적 파일을 매우 빠르게 처리하고 백엔드 서버에 요청을 중계합니다. 로드밸런싱과 HTTPS 처리는 물론 캐싱 기능까지 제공해 대규모 트래픽을 안정적으로 처리하는 데 널리 사용됩니다.

### 3.2.1 NGINX : 동작 원리

클라이언트가 서버로 요청을 보내면 NGINX가 가장 앞단에서 요청을 분석한 뒤 로드밸런싱, 정적 파일 제공, 캐싱 처리를 담당합니다.

<!-- image-prompt: Minimal black line drawing on white background, very few details, icon-like simplicity, 4:3 aspect ratio, 800x600px. with Korean labels: Diagram with exactly one 클라이언트 on the left sending a request arrow to NGINX in the center. From NGINX, three arrows branch out to the right pointing to 로드밸런싱, 정적 파일 제공, 캐싱. Only one client icon, no duplicates. -->

![](../assets/CH03/chap02-17.png)
*NGINX의 주요 기능*

> **리버스 프록시**: NGINX처럼 서버를 대신해 요청을 받는 서버를 리버스 프록시라고 합니다. 서버를 외부에 직접 노출하지 않도록 보호하고 들어오는 트래픽을 분산해 서버의 부하를 줄여줍니다.

### 3.2.2 경로 기반 라우팅 : URL로 요청을 나누다

> **경로 기반 라우팅**: 클라이언트가 요청한 URL 경로를 기준으로 해당 서버나 서비스로 트래픽을 전달하는 방식입니다.

아래 그림처럼 클라이언트가 `/users`, `/products` 경로로 API 요청을 보내면 NGINX는 그 경로에 매핑된 서버로 요청을 전달합니다.

<!-- image-prompt: Minimal black line drawing on white background, very few details, icon-like simplicity, 4:3 aspect ratio, 800x600px. with Korean labels: Diagram showing NGINX 경로 기반 라우팅 - 클라이언트 요청 /users goes to 서버 1, 요청 to /products goes to 서버 2, illustrating location-based 트래픽 분배 -->

![](../assets/CH03/chap02-18.png)
*경로 기반 라우팅 구조*

#### 실습해보기

> 실습 코드는 https://github.com/metacoding-10-linux-docker/docker/tree/master/ex01 에서 확인할 수 있습니다.

app1, app2, lb 폴더에 있는 Dockerfile은 개별 이미지를 생성하며, 각각 독립적인 컨테이너로 실행됩니다.

**[EX01 패키지 구조]**

```
ex01/
├── app1/                # 첫 번째 웹 서버
│   ├── Dockerfile
│   └── index.html
├── app2/                # 두 번째 웹 서버
│   ├── Dockerfile
│   └── index.html
└── lb/                  # 로드밸런서 (NGINX)
    ├── Dockerfile
    └── nginx.conf       # 라우팅 설정
```

#### app 이미지

app1과 app2는 nginx 이미지를 기반으로 각각의 index.html을 복사하여 서버를 구성합니다.

| 파일 | 설명 |
|------|------|
| `app1/Dockerfile`, `app2/Dockerfile` | nginx 이미지 기반, index.html 복사 후 포그라운드 실행 |
| `app1/index.html`, `app2/index.html` | 각 서버를 구분하는 HTML (Server1, Server2) |

#### lb 이미지

lb 폴더의 Dockerfile은 로컬에 있는 nginx.conf를 컨테이너 내부로 복사하여 이미지를 생성합니다.

**[참고]** `lb/Dockerfile`

**ex01/lb/Dockerfile**
```dockerfile
FROM nginx                                          # NGINX 이미지 사용
COPY nginx.conf /etc/nginx/conf.d/default.conf      # 로컬의 nginx.conf를 컨테이너의 NGINX 설정 경로로 복사
ENTRYPOINT ["nginx", "-g", "daemon off;"]            # NGINX를 포그라운드로 실행
```

nginx.conf 파일은 다음과 같습니다. nginx.conf는 NGINX가 어떤 방식으로 요청을 처리할지 정의하는 파일입니다.

**[참고]** `lb/nginx.conf`

**ex01/lb/nginx.conf**
```nginx
upstream app1 {                           # 요청을 전달할 목적지를 app1이라는 이름으로 등록
    server host.docker.internal:8000;     # 이 그룹에 속한 서버 (여러 개 등록하면 자동 분산)
}

upstream app2 {                           # "app2" 서버 그룹
    server host.docker.internal:9000;
}

server {
    listen 80;
    server_name localhost;

    location /app1 {                  # /app1 경로 요청을 잡아서
        proxy_pass http://app1/;      # proxy_pass에 등록된 서버로 전달. 서버 주소나 업스트림 이름을 넣음
    }

    location /app2 {
        proxy_pass http://app2/;
    }
}
```

여러 설정이 있지만 핵심은 `location`과 `upstream` 두 블록입니다. `location`은 "이 경로로 들어오면"이라는 조건이고, `upstream`은 **"여기로 보내라"라는 목적지입니다.** `proxy_pass`가 이 둘을 연결합니다.

이 설정이 실제로 어떻게 동작하는지 브라우저에서 `localhost:80/app1`을 입력한 경우를 따라가 보겠습니다.

브라우저 요청이 호스트 PC의 80번 포트로 들어옵니다. 이 포트는 `-p 80:80`으로 lb 컨테이너와 연결되어 있으므로, 요청이 lb 컨테이너의 NGINX에 도달합니다.

![](../assets/CH03/ex01-host-routing-1.png)
*브라우저 → lb 컨테이너*

NGINX는 요청 경로가 `/app1`인 것을 보고 `location /app1` 블록에 매칭합니다. 이 블록 안의 `proxy_pass http://app1`이 요청을 `upstream app1`으로 넘깁니다.

![](../assets/CH03/upstream.png)
*NGINX 내부 — location → upstream*

그러면 upstream app1에 등록된 서버 주소로 요청이 전달됩니다. 여기서는 `host.docker.internal:8000`이 등록되어 있습니다.

> **오픈이**: "근데 왜 app1 주소를 직접 안 쓰고 **host.docker.internal** 을 쓰는 거예요?"
>
> **선배**: "지금 컨테이너를 따로따로 띄우고 있잖아. 그러면 서로를 모르거든. 호스트를 거쳐야 돼."

이 예제에서는 컨테이너를 `docker run`으로 각각 따로 실행합니다. 이렇게 개별 실행된 컨테이너들은 서로의 존재를 모르기 때문에, lb 컨테이너가 app1 컨테이너를 직접 찾을 수 없습니다. 대신 호스트 PC를 경유해야 합니다.

> **host.docker.internal** 은 컨테이너 안에서 '호스트 PC'를 가리키는 특수한 주소입니다. 컨테이너 내부에서 localhost를 입력하면 호스트 PC가 아닌 컨테이너 자기 자신을 가리키게 됩니다. 따라서 바깥에 있는 호스트 PC로 요청을 보낼 때는 반드시 이 주소를 사용해야 합니다.

`host.docker.internal:8000`은 호스트 PC의 8000번 포트를 가리킵니다. 이 포트는 `-p 8000:80`으로 app1 컨테이너와 연결되어 있으므로, 최종적으로 app1 컨테이너에 도달합니다.

### 🔍 네트워크 돋보기 ④: 컨테이너가 서로를 못 찾는 이유

> **"같은 컴퓨터에서 실행 중인데, 왜 컨테이너끼리 직접 통신을 못 하지?"**

2장에서 각 컨테이너는 독립된 Network Namespace라고 배웠습니다. 호텔의 각 방이 독립된 공간인 것처럼요. 문제는 **"각 방에 내선 전화번호부가 없다"**는 점입니다.

`docker run`으로 개별 실행한 컨테이너들은 기본 bridge(docker0)에 연결됩니다. 이 상태에서는 **컨테이너 이름으로 서로를 찾을 수 없습니다.** IP 주소(172.17.0.2)를 직접 알면 통신은 가능하지만, IP는 컨테이너를 재시작할 때마다 바뀔 수 있어서 불안정합니다.

그래서 `host.docker.internal`이라는 우회 경로를 쓰는 것입니다:

![](../assets/CH03/net-04-host-routing.png)

컨테이너 → 호스트 → 포트포워딩 → 다른 컨테이너. 멀리 돌아가는 경로이지만, 기본 bridge에서 이름으로 찾을 수 없으니 어쩔 수 없습니다.

> 💡 **한 줄 정리**: 기본 bridge 네트워크에서는 컨테이너 이름으로 서로를 찾을 수 없다. 그래서 호스트를 경유하는 `host.docker.internal`이 필요하다. 돋보기 ⑤에서 이 문제를 근본적으로 해결하는 방법을 배운다.

![](../assets/CH03/ex01-host-routing-2.png)
*upstream → 호스트 PC → app1 컨테이너*

이제 이미지를 실행해보겠습니다. 다음 명령어를 순차적으로 실행합니다.

챕터 2에서 배운 **포트포워딩**을 `-p 호스트포트:컨테이너포트` 형식으로 설정합니다.

**[실습]** EX01 폴더로 이동 후, 터미널에서 app1, app2, lb 이미지를 빌드하고 컨테이너를 실행합니다.

```bash
#서버 1 실행
docker build -t app1 ./app1       # app1 이미지 빌드
docker run -dit -p 8000:80 app1   # NGINX가 host.docker.internal:8000으로 접근하므로 호스트 8000번 포트를 열어줌

#서버 2 실행
docker build -t app2 ./app2       # app2 이미지 빌드
docker run -dit -p 9000:80 app2   # NGINX가 host.docker.internal:9000으로 접근하므로 호스트 9000번 포트를 열어줌

#lb 실행
docker build -t lb ./lb
docker run -dit -p 80:80 lb
```

명령어를 실행하면 Docker Desktop에서 생성된 컨테이너를 볼 수 있습니다.

<!-- image-prompt: Docker Desktop showing three running containers: app1, app2, and lb -->

![](../assets/CH03/chap02-20.png)
*Docker Desktop에서 컨테이너 확인*

브라우저에서 `localhost:80/app1` 으로 요청을 보내면 `app1` 서버가 응답합니다.

**URL 주소는 NGINX 설정의 `location`에 설정한 경로입니다.**

<!-- image-prompt: Browser showing "Nginx Server1" text when accessing localhost/app1 -->

![](../assets/CH03/chap02-21.png)
*/app1 경로 응답 결과*

`localhost:80/app2`로 요청을 보내면 `app2` 서버가 응답합니다.

<!-- image-prompt: Browser showing "Nginx Server2" text when accessing localhost/app2 -->

![](../assets/CH03/chap02-22.png)
*/app2 경로 응답 결과*

URL 경로만 바꿨을 뿐인데 서로 다른 서버가 응답합니다.

다음 실습을 위해 실행한 서버를 종료합니다.

**[실습]** 터미널 -- 실행 중인 모든 컨테이너를 중지하고 삭제합니다.

```bash
docker stop $(docker ps -q)   # 실행 중인 컨테이너 모두 중지
docker rm $(docker ps -aq)    # 중지된 컨테이너 모두 삭제
```

### 3.2.3 라운드 로빈 : 요청을 골고루 나누다

오픈이의 서비스에 사용자가 늘어났습니다. 서버 한 대로는 응답이 느려지기 시작했습니다.

> **오픈이**: "서버가 느려졌는데, 같은 서버를 여러 대 돌릴 수는 없어요?"
>
> **선배**: "NGINX upstream에 서버 여러 개 등록하면 어떻게 될 것 같아?"

놀이공원 매표소가 3개 있을 때, 손님을 1번→2번→3번→1번 순서로 배정하는 것처럼 **라운드 로빈 라우팅(Round-Robin Routing)** 은 여러 서버에 요청을 순차적으로 번갈아 가며 분배하는 로드밸런싱 방식입니다.

API 요청이 있다면 순서대로 서버 1, 서버 2, 서버 3, 서버 1...의 순으로 트래픽이 분배됩니다.

<!-- image-prompt: Minimal black line drawing on white background, very few details, icon-like simplicity, 4:3 aspect ratio, 800x600px. with Korean labels: 라운드 로빈 로드밸런싱 diagram. Left: one 클라이언트 with a single arrow to center NGINX, labeled "요청 x3" on the arrow to show three requests were made. Right: NGINX sends exactly three arrows - 요청 1 to 서버 1, 요청 2 to 서버 2, 요청 3 to 서버 3. No extra arrows. -->

![](../assets/CH03/chap02-23.png)
*라운드 로빈 로드밸런싱 구조*

#### 실습해보기

> 실습 코드는 https://github.com/metacoding-10-linux-docker/docker/tree/master/ex02 에서 확인할 수 있습니다.

**[EX02 패키지 구조]**

```
ex02/
├── app1/                # 웹 서버 (2개 컨테이너로 실행)
│   ├── Dockerfile
│   └── index.html
└── lb/                  # 로드밸런서 (NGINX)
    ├── Dockerfile
    └── nginx.conf       # 라운드 로빈 설정
```

EX02는 EX01과 `lb/nginx.conf` 파일을 제외하고 동일한 구조이므로 코드는 생략하겠습니다.

#### lb 이미지

nginx.conf는 다음과 같습니다. `upstream` 설정에 두 개의 서버가 등록되어 있습니다.

NGINX는 별도의 로드 밸런싱 알고리즘을 지정하지 않으면 기본적으로 라운드 로빈 방식을 사용해 트래픽을 자동 분산합니다.

**[참고]** `lb/nginx.conf`

**ex02/lb/nginx.conf**
```nginx
upstream app1 {                               # app1 서버 그룹 정의
    server host.docker.internal:8000;         # 호스트의 8000번 포트로 연결
    server host.docker.internal:8001;         # 호스트의 8001번 포트로 연결
}

server {
    listen 80;                                # 80포트로 요청시 설정 적용
    server_name localhost;

    location /app1 {                          # /app1 요청을 upstream으로 전달
        proxy_pass http://app1/;              # 라운드 로빈으로 분배
    }
}
```

파일 작성 후 다음 명령어를 실행해 app1과 lb의 컨테이너를 생성합니다. 동일한 app1 이미지로 컨테이너 2개를 서로 다른 포트(8000, 8001)로 실행하는 것입니다.

**[실습]** EX02 폴더로 이동 후, 터미널에서 app1 이미지를 빌드하고, 2개의 컨테이너와 lb를 실행합니다.

```bash
#서버 1 2개 생성
docker build -t app1 ./app1       # app1 이미지 빌드

docker run -dit -p 8000:80 app1   # app1 서버 1 실행 (8000번 포트)
docker run -dit -p 8001:80 app1   # app1 서버 2 실행 (8001번 포트)

#nginx 실행
docker build -t lb ./lb
docker run -dit -p 80:80 lb       # 로드밸런서 실행 (80번 포트)
```

<!-- image-prompt: Docker Desktop showing two app1 containers and one lb container running -->

![](../assets/CH03/chap02-25.png)
*라운드 로빈 컨테이너 실행 확인*

테스트를 해보겠습니다. `localhost:80/app1` 주소로 동일한 요청을 반복하면 요청이 두 서버로 번갈아 전달되는 것을 볼 수 있습니다.

<!-- image-prompt: Browser showing the first request result when accessing localhost/app1 -->

![](../assets/CH03/chap02-26.png)
*8000 포트 서버 요청*

<!-- image-prompt: Browser showing the second request result when accessing localhost/app1, demonstrating round-robin switching -->

![](../assets/CH03/chap02-27.png)
*8001 포트 서버 요청*

새로고침할 때마다 요청이 두 서버로 번갈아 전달됩니다.

> **선배**: "그게 라운드 로빈이야. 근데... 이걸로 끝이 아니거든."

다음 실습을 위해 실행한 서버를 종료합니다.

**[실습]** 터미널에서 실행 중인 모든 컨테이너를 중지하고 삭제합니다.

```bash
docker stop $(docker ps -q)   # 실행 중인 컨테이너 모두 중지
docker rm $(docker ps -aq)    # 중지된 컨테이너 모두 삭제
```

### 3.2.4 캐싱 : 정적 파일을 빠르게 전달하다

자주 입는 옷을 박스에 보관하지 않고 옷걸이에 걸어놓는 것처럼 NGINX의 정적 서버는 HTML, CSS, 이미지와 같은 정적 파일을 보관했다가 클라이언트에게 직접 제공합니다.

> **정적 서버와 캐싱**: 정적 서버는 한 번 제공한 정적 파일을 일정 기간 저장해 둡니다. 이후 동일한 요청이 오면 서버에 다시 조회하지 않고 저장된 파일을 즉시 반환합니다. 이를 캐싱이라고 합니다.

클라이언트가 서버에 처음 이미지 파일을 요청하면 NGINX는 서버에 요청을 전달해 이미지 파일을 응답받습니다.

일정 시간 이내에 동일한 요청이 다시 들어오면 NGINX는 서버 대신 캐시에 저장된 파일을 즉시 반환합니다.

<!-- image-prompt: Minimal black line drawing on white background, very few details, icon-like simplicity, 4:3 aspect ratio, 800x600px. with Korean labels: A clean technical diagram showing NGINX 캐싱 flow with two scenarios in one image, on white background.

Top half labeled "첫 번째 요청 (MISS)":
- Left: "클라이언트" text label, arrow labeled "GET /image.png" to center "NGINX" box
- NGINX box has a dotted box inside labeled "캐시: 비어있음"
- Arrow from NGINX to right "백엔드 서버" box
- Arrow back from 백엔드 서버 to NGINX with image file
- Arrow from NGINX back to 클라이언트
- Small note: "캐시에 응답 저장"

Bottom half labeled "두 번째 요청 (HIT)":
- Left: "클라이언트" text label, arrow labeled "GET /image.png" to center "NGINX" box
- NGINX box has a solid box inside labeled "캐시: 저장됨"
- Arrow from NGINX directly back to 클라이언트
- "백엔드 서버" box grayed out, no arrow connecting to it
- Small note: "캐시에서 응답 제공"

No computer or device icons. Use only simple labeled boxes, text labels, and arrows.
Minimal flat style, light blue and gray tones, technical documentation look. -->

![](../assets/CH03/cache-miss.png)
*첫 번째 요청 (MISS) - 캐시가 비어있어 백엔드 서버에 요청 후 응답을 캐시에 저장*

![](../assets/CH03/cache-hit.png)
*두 번째 요청 (HIT) - 캐시에 저장된 응답을 바로 반환, 백엔드 서버 접근 없음*

#### 실습해보기

> 실습 코드는 https://github.com/metacoding-10-linux-docker/docker/tree/master/ex03 에서 확인할 수 있습니다.

**[EX03 패키지 구조]**

```
ex03/
├── api/                 # 백엔드 서버 (Flask)
│   ├── app.py           # API 코드
│   ├── Dockerfile
│   └── image.png        # 캐싱 테스트용 이미지
└── nginx/               # NGINX (캐싱 + 프록시)
    ├── Dockerfile
    └── nginx.conf       # 캐싱 설정
```

#### api 이미지

Dockerfile은 다음과 같습니다.

**[참고]** `api/Dockerfile`

**ex03/api/Dockerfile**
```dockerfile
FROM python:3.10-alpine                # Python 3.10 경량 이미지 사용
WORKDIR /app                           # 작업 경로를 /app으로 설정
COPY . /app                            # 현재 폴더의 모든 파일을 컨테이너의 /app으로 복사
RUN pip install flask                  # Flask 웹 프레임워크 설치
CMD ["python", "app.py"]               # Flask 서버 실행
```

API 서버는 파이썬으로 작성되어 있습니다. Flask는 Python의 경량 웹 프레임워크로, 실습 코드 작성을 위해 사용합니다. Flask 문법을 익히지 않아도 됩니다.

슬래시(`/`) 주소는 HTML을 응답하고, `/image.png` 주소는 이미지 파일을 응답합니다.

**[참고]** `api/app.py`

**ex03/api/app.py**
```python
# Flask: 파이썬의 경량 웹 프레임워크 (스프링의 @RestController와 유사한 역할)
from flask import Flask, Response, send_file
import os

app = Flask(__name__)
# HTML 응답
@app.route("/")
def index():
    html = """
    <!DOCTYPE html>
    <html>
      <body>
        <h2>NGINX CACHE</h2>
      </body>
    </html>
    """
    return Response(html, mimetype="text/html")

# 이미지 요청
@app.route("/image.png")
def get_image():
    image_path = os.path.join(os.path.dirname(__file__), "image.png")
    return send_file(image_path, mimetype="image/png")

# ... 생략
```

#### NGINX 이미지

nginx의 Dockerfile은 다음과 같습니다.

**[참고]** `nginx/Dockerfile`

**ex03/nginx/Dockerfile**
```dockerfile
FROM nginx                                          # NGINX 이미지 사용
COPY nginx.conf /etc/nginx/conf.d/default.conf      # 로컬의 nginx.conf를 컨테이너의 NGINX 설정 경로로 복사
ENTRYPOINT ["nginx", "-g", "daemon off;"]            # NGINX를 포그라운드로 실행
```

다음으로 nginx.conf 파일입니다. 캐시 저장 경로를 지정하는 `proxy_cache_path`와 캐시 사용 여부를 제어하는 `proxy_cache`가 포함되어 있습니다.

`proxy_cache_path`로 캐시 저장 경로와 메모리 공간을 지정하고 `location` 블록의 `proxy_cache`로 캐시 적용 여부를 제어합니다.

**[참고]** `nginx/nginx.conf`

**ex03/nginx/nginx.conf**
```nginx
# 캐시 관련 설정(캐시 저장 디렉토리, 캐시 이름 설정)
proxy_cache_path /var/cache/nginx keys_zone=my_cache:10m;

server {
    listen 80;

    location / {
        proxy_pass http://host.docker.internal:5000;
        proxy_cache off;                              # 캐시 사용하지 않음
    }

    location = /image.png {
        proxy_pass http://host.docker.internal:5000;
        proxy_cache my_cache;                         # proxy_cache_path에서 설정한 캐시 사용
        proxy_cache_valid 200 1m;                     # 200 상태 응답 1분 동안 캐시
        add_header X-Cache-Status $upstream_cache_status always; # response 헤더에 캐시 여부 표시
        proxy_ignore_headers Cache-Control Expires;   # 백엔드의 캐시 정책을 무시하고 Nginx가 캐시
    }
}
```

아래 명령어를 실행해 컨테이너를 생성합니다. API 서버를 먼저 실행한 뒤, NGINX 캐시 서버를 실행합니다.

**[실습]** EX03 폴더로 이동 후, api 서버와 NGINX 캐시 서버를 빌드하고 실행합니다.

```bash
# api 서버 실행
docker build -t api ./api                                            # API 이미지 빌드
docker run -dit -p 5000:5000 api                                     # API 서버 실행 (5000번 포트)

# nginx 실행
docker build -t nginx-cache ./nginx                                  # NGINX 캐싱 이미지 빌드
docker run -dit -p 80:80 nginx-cache                                 # NGINX 캐싱 서버 실행 (80번 포트)
```

<!-- image-prompt: Browser showing "NGINX CACHE" text when accessing localhost -->

![](../assets/CH03/chap02-31.png)
*캐싱 실습 - HTML 응답*

컨테이너 실행 후 `localhost:80/image.png` 로 요청하면 저장된 이미지 파일이 응답됩니다.

<!-- image-prompt: Browser displaying an image when accessing localhost/image.png -->

![](../assets/CH03/chap02-32.png)
*캐싱 실습 - 이미지 응답*

브라우저 **F12 > Network > Headers** 탭을 확인합니다.

브라우저 자체도 캐시 기능이 있어 확인이 어려울 수 있습니다. 브라우저의 Disable cache를 체크해 브라우저 캐싱을 비활성화합니다.

이 중 Response Headers의 `X-Cache-Status` 값이 `MISS`입니다. `MISS`는 캐시에 요청 데이터가 없어 원본 서버에 요청을 보내 값을 가져온 상태입니다.

<!-- image-prompt: Browser DevTools Network tab showing X-Cache-Status: MISS in response headers -->

![](../assets/CH03/chap02-33.png)
*X-Cache-Status: MISS 확인*

다시 새로고침합니다. 이번에는 `X-Cache-Status` 값이 `HIT`입니다.

`HIT`는 캐시에 저장된 파일을 서버 요청 없이 그대로 응답한 상태입니다.

<!-- image-prompt: Browser DevTools Network tab showing X-Cache-Status: HIT in response headers -->

![](../assets/CH03/chap02-34.png)
*X-Cache-Status: HIT 확인*

다음 실습을 위해 실행한 서버를 종료합니다.

**[실습]** 터미널에서 실행 중인 모든 컨테이너를 중지하고 삭제합니다.

```bash
docker stop $(docker ps -q)   # 실행 중인 컨테이너 모두 중지
docker rm $(docker ps -aq)    # 중지된 컨테이너 모두 삭제
```

## 3.3 Redis : 세션 저장소

로드밸런싱을 적용하고 나니 새로운 문제가 터졌습니다. 사용자가 로그인한 뒤 페이지를 이동하면 갑자기 로그인이 풀리는 것입니다.

> **오픈이**: "선배, 로그인한 사용자가 다음 페이지 가면 로그아웃돼요!"
>
> **선배**: "서버 1에서 로그인했는데 다음 요청이 서버 2로 갔겠지. 서버 2한테는 그 사용자 정보가 없으니까."
>
> **오픈이**: "그럼 어떻게 해요?"
>
> **선배**: "세션을 서버 안에 두지 말고 바깥에 빼. Redis라고, 여러 서버가 같이 쓰는 공용 사물함이 있거든."

Redis는 여러 서버가 함께 사용하는 **공용 사물함**과 같습니다. 서버 1이 사물함에 데이터를 넣어두면 서버 2도 같은 사물함을 열어 그 데이터를 꺼낼 수 있습니다. 어떤 서버가 요청을 처리하든 동일한 데이터에 접근할 수 있습니다.

> **레디스(Redis)**: 메모리 기반의 데이터베이스로, 관계형 데이터베이스가 아닌 키-값(Key-Value) 구조로 데이터를 저장합니다. 디스크가 아닌 메모리에 저장하기 때문에 속도가 매우 빨라 데이터 캐싱, 세션 저장 등 고성능 처리가 필요한 곳에 주로 사용됩니다.

### 3.3.1 세션 : 왜 외부 저장소가 필요한가

클라이언트가 로그인 요청을 보내면 NGINX는 그 요청을 `서버 1`으로 전달합니다. 이때 로그인에 성공한 사용자의 세션 정보는 `서버 1`에서 생성되어 저장됩니다. 다음 요청이 NGINX에 의해 `서버 2`로 전달되면? `서버 2`는 그 사용자의 세션 정보를 가지고 있지 않기 때문에 요청을 처리할 수 없습니다.

![](../assets/CH03/session-problem.png)
*세션 불일치 - 서버 1에 저장된 세션이 서버 2에는 없어 요청이 실패*

Redis로 이 문제를 해결할 수 있습니다. `서버 1`이 세션을 자체 메모리가 아닌 Redis에 저장하면 이후 요청이 `서버 2`로 전달되더라도 Redis에서 동일한 세션 정보를 조회할 수 있어 요청을 문제없이 처리합니다.

![](../assets/CH03/session-redis.png)
*Redis로 해결 - 세션을 공유 저장소에 보관하여 어떤 서버에서든 조회 가능*

서버에 세션을 저장하는 방식은 서버가 여러 대로 늘어날 때 세션이 분산되어 관리가 어렵습니다. Redis를 사용하면 세션을 한 곳에서 관리할 수 있어 서버가 확장되더라도 세션 공유에 문제가 없습니다.

### 3.3.2 Redis : 실습

아래 Github 주소를 참고합니다.

> 실습 코드는 https://github.com/metacoding-10-linux-docker/docker/tree/master/ex04 에서 확인할 수 있습니다.

Dockerfile은 파이썬 이미지 기반으로 Flask와 Redis 패키지를 설치하고 app.py를 실행합니다. 

**[참고]** `api/Dockerfile`

**ex04/api/Dockerfile**
```dockerfile
FROM python:3.10-alpine                          # Python 3.10 경량 이미지 사용
WORKDIR /app                                     # 작업 경로를 /app으로 설정
COPY app.py .                                    # app.py를 컨테이너의 /app으로 복사
RUN pip install flask && pip install redis        # Flask + Redis 패키지 설치
CMD ["python", "app.py"]                         # Flask 서버 실행
```

`app.py`는 다음과 같습니다.

`/save` 요청이 들어오면 Redis 서버와 연결된 객체 `r`로 값을 저장하고, `/read` 요청이 들어오면 동일한 객체로 Redis에 저장된 값을 조회합니다.

**[참고]** `api/app.py`

**ex04/api/app.py**
```python
# Flask: 파이썬의 경량 웹 프레임워크 (스프링의 @RestController와 유사한 역할)
# @app.route()는 스프링의 @GetMapping과 같은 역할

# Redis 연결 -- 컨테이너 이름 'redis'를 호스트명으로 사용
r = redis.Redis(host='redis', port=6379, db=0)

@app.route("/save")
def save_name():
    r.set("name", "metacoding")       # Redis에 값 저장
    return "이름이 저장되었습니다."

@app.route("/read")
def read_name():
    value = r.get("name")             # Redis에서 값 조회
    if value is None:
        return "저장된 이름이 없습니다."
    return f"name = {value.decode('utf-8')}"

# ... 생략
```

코드에서 `host='redis'`가 눈에 띕니다. 3.2에서는 `host.docker.internal`로 호스트를 경유해야 했는데, 여기서는 컨테이너 이름으로 직접 접속합니다. 비밀은 **사용자 정의 네트워크**에 있습니다.

**--network <네트워크명>** 옵션으로 동일 네트워크에 연결하면 컨테이너 이름으로 통신할 수 있습니다.

**[실습]** EX04 폴더로 이동 후, 네트워크를 생성하고 Redis, API 컨테이너를 실행합니다.

```bash
# 네트워크 만들기
docker network create myNetwork                                     # myNetwork 네트워크 생성
 
# redis 앱 빌드 및 실행
docker run -d --name redis --network myNetwork -p 6379:6379 redis   # Redis 컨테이너 실행, myNetwork 네트워크로 연결

# api 실행
docker build -t api ./api                                           # API 이미지 빌드
docker run -d --name api1 --network myNetwork -p 5001:5000 api      # API 서버 1 실행 (5001번 포트), myNetwork 네트워크로 연결
docker run -d --name api2 --network myNetwork -p 5002:5000 api      # API 서버 2 실행 (5002번 포트), myNetwork 네트워크로 연결
```

### 🔍 네트워크 돋보기 ⑤: docker network create의 마법 — DNS가 열린다

> **"사용자 정의 네트워크를 만들면 왜 갑자기 컨테이너 이름으로 통신이 되는 거지?"**

비밀은 **Docker 내장 DNS 서버**에 있습니다.

사용자 정의 네트워크(예: `myNetwork`)를 만들면, Docker는 그 네트워크 안에 **DNS 서버(127.0.0.11)**를 자동으로 켭니다. 이 DNS 서버는 같은 네트워크에 연결된 모든 컨테이너의 이름과 IP를 자동으로 등록합니다.

스마트폰의 연락처 앱을 생각해 보세요. "김대리"를 검색하면 전화번호가 나오듯, 컨테이너가 "redis"를 요청하면 DNS 서버가 IP(172.18.0.2)를 알려줍니다.

![](../assets/CH03/net-05-docker-dns.png)

ex04의 Python 코드에서 `redis.Redis(host='redis', port=6379)`가 동작하는 이유가 바로 이것입니다. `'redis'`라는 문자열이 Docker DNS를 통해 실제 IP로 변환됩니다.

**기본 bridge에서는 이 DNS가 꺼져 있습니다.** 그래서 돋보기 ④에서 `host.docker.internal`로 우회해야 했던 것입니다.

#### 직접 확인해보기

```bash
# myNetwork에 연결된 컨테이너 안에서 DNS 설정 확인
docker exec api1 cat /etc/resolv.conf
# 출력: nameserver 127.0.0.11

# 컨테이너 이름으로 DNS 조회
docker exec api1 nslookup redis
# 출력: Name: redis  Address: 172.18.0.2
```

| 네트워크 종류 | DNS 지원 | 이름 통신 | 사용 시나리오 |
|-------------|---------|----------|-------------|
| 기본 bridge (docker0) | ❌ | 불가 | 단독 컨테이너 |
| 사용자 정의 bridge | ✅ | 가능 | 다중 컨테이너, Compose |

> 💡 **한 줄 정리**: 사용자 정의 네트워크에는 Docker DNS(127.0.0.11)가 자동으로 켜져서, 컨테이너 이름을 IP로 변환해준다. 기본 bridge에는 이 DNS가 없다.

3개의 컨테이너가 생성되었습니다.

<!-- image-prompt: Docker Desktop showing three running containers: redis, api1, and api2 -->

![](../assets/CH03/chap02-39.png)
*Redis 실습 컨테이너 확인*

브라우저에서 `api1` 서버의 `localhost:5001/save`로 요청을 보내면 이름이 저장되었다는 응답을 확인할 수 있습니다.

<!-- image-prompt: Browser showing a success message when accessing localhost:5001/save -->

![](../assets/CH03/chap02-40.png)
*api1에서 데이터 저장*

`api2` 서버인 `localhost:5002/read`로 요청을 보내면 `api1` 서버에서 저장했던 값을 확인할 수 있습니다. api1에서 저장한 데이터를 api2에서 읽은 것입니다.

Redis 덕분에 컨테이너 간 데이터 공유가 제대로 이루어집니다.

<!-- image-prompt: Browser showing "name = metacoding" when accessing localhost:5002/read, confirming cross-server session sharing via Redis -->

![](../assets/CH03/chap02-41.png)
*api2에서 데이터 조회*

api1에서 저장한 데이터를 api2에서 읽었습니다. Redis 덕분에 서버가 몇 대든 세션이 풀리지 않습니다.

실습이 끝나면 컨테이너와 네트워크를 정리합니다.

**[실습]** 터미널에서 컨테이너를 중지하고 삭제한 뒤 네트워크를 제거합니다.

```bash
docker stop $(docker ps -q)    # 실행 중인 컨테이너 모두 중지
docker rm $(docker ps -aq)     # 중지된 컨테이너 모두 삭제
docker network rm myNetwork    # 네트워크 삭제
```

## 3.4 MySQL : DB 서버 구축

Redis로 세션 데이터를 관리하는 방법을 배웠습니다. Redis는 메모리 기반이라 서버가 종료되면 데이터가 날아갈 수 있습니다. 회원 정보, 게시글, 주문 내역처럼 반드시 보관해야 하는 데이터는 어떻게 저장해야 할까요? 이때 필요한 것이 DB 서버입니다.

### 3.4.1 MySQL : 컨테이너로 DB 서버 생성

#### 실습해보기

> 실습 코드는 https://github.com/metacoding-10-linux-docker/docker/tree/master/ex05 에서 확인할 수 있습니다.

**[EX05 패키지 구조]**

```
ex05/
└── db/                  # MySQL 데이터베이스
    ├── Dockerfile
    └── init.sql         # 초기 테이블 및 데이터 생성 SQL
```

Dockerfile은 MySQL 이미지를 기반으로 환경변수와 초기화 SQL을 설정합니다.

**[참고]** `db/Dockerfile`

**ex05/db/Dockerfile**
```dockerfile
FROM mysql                                    # MySQL 이미지 

COPY init.sql /docker-entrypoint-initdb.d     # 로컬의 init.sql을 MySQL 초기화 폴더로 복사

ENV MYSQL_USER=metacoding                     # 생성할 사용자 이름
ENV MYSQL_PASSWORD=metacoding1234             # 사용자 비밀번호
ENV MYSQL_ROOT_PASSWORD=root1234              # root 비밀번호
ENV MYSQL_DATABASE=metadb                     # 생성할 데이터베이스 이름

CMD ["--character-set-server=utf8mb4", "--collation-server=utf8mb4_unicode_ci"]  # 한글 인코딩 설정
```

`init.sql`은 `user_tb` 테이블을 생성한 뒤 초기 데이터를 입력합니다.

> **init.sql**: 컨테이너가 처음 생성될 때 한 번 실행되는 스크립트입니다. MySQL 공식 이미지는 `/docker-entrypoint-initdb.d` 디렉토리에 있는 SQL 파일을 최초 실행 시 자동으로 실행합니다.

**[참고]** `db/init.sql`

**ex05/db/init.sql**
```sql
CREATE TABLE user_tb (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(50)
) ;

INSERT INTO user_tb (name) VALUES ('ssar');
INSERT INTO user_tb (name) VALUES ('cos');
```

다음 명령어를 실행합니다. MySQL의 기본 포트인 3306으로 포트 포워딩합니다.

**[실습]** EX05 폴더로 이동 후, DB 이미지를 빌드하고 컨테이너를 실행합니다.

```bash
# 이미지 빌드 및 실행
docker build -t db ./db            # DB 이미지 빌드
docker run -dit -p 3306:3306 db    # MySQL 컨테이너 실행 (3306번 포트)
```

컨테이너 로그를 확인하면 MySQL이 정상적으로 실행된 것을 볼 수 있습니다.

<!-- image-prompt: Docker Desktop showing MySQL container logs with "ready for connections" message -->

![](../assets/CH03/chap02-43.png)
*MySQL 컨테이너 실행 로그*

### 3.4.2 MySQL : 데이터 확인

3.4.1에서 DB 서버를 백그라운드로 실행했습니다. 이제 내부 터미널로 접속해 확인합니다.

`docker exec -it <컨테이너ID> bash` 명령어를 사용해 터미널로 접속합니다.

**[실습]** 터미널에서 실행 중인 컨테이너를 확인하고 내부에 접속합니다.

```bash
docker ps                    # 실행 중인 컨테이너 확인
docker exec -it 1fc2 bash   # MySQL 컨테이너 내부 접속
```

<!-- image-prompt: Terminal showing docker ps to find the container ID, then docker exec to enter the MySQL container -->

![](../assets/CH03/chap02-44.png)
*MySQL 컨테이너 접속*

터미널에서 다음 명령어로 MySQL에 접속합니다. 사용자명과 비밀번호는 Dockerfile에 설정한 환경 변수입니다.

`mysql -u <사용자명> -p` 형식으로 접속하며 Dockerfile에 설정한 사용자를 입력합니다.

**[실습]** 터미널에서 MySQL 클라이언트에 접속합니다.

```bash
mysql -u metacoding -p   # MySQL 접속
```

비밀번호를 입력할 때는 보안상 화면에 표시되지 않지만 제대로 입력되고 있으니 그대로 입력하면 됩니다.

<!-- image-prompt: Terminal showing successful MySQL client connection -->

![](../assets/CH03/chap02-45.png)
*MySQL 접속 성공*

다음 SQL문을 사용해 DB 정보를 확인합니다.

**[실습]** MySQL에서 데이터베이스와 테이블 정보를 조회합니다.

```sql
show databases;
use metadb;
show tables;
select * from user_tb;
```

<!-- image-prompt: MySQL client showing SHOW DATABASES result with metadb listed -->

![](../assets/CH03/chap02-46.png)
*데이터베이스 목록 확인*

<!-- image-prompt: MySQL client showing SELECT query result with two rows: ssar and cos -->

![](../assets/CH03/chap02-47.png)
*user_tb 데이터 조회*

`init.sql`에 작성한 데이터가 잘 조회됩니다.

실습 후 터미널에서 빠져나와 컨테이너를 종료합니다.

**[실습]** 컨테이너를 종료 후 삭제하는 명령어입니다.

```bash
exit             # MySQL 클라이언트에서 빠져나옴
exit             # 컨테이너 bash에서 빠져나옴
docker stop $(docker ps -q)
docker rm $(docker ps -aq)
```

## 3.5 Docker Compose : 여러 컨테이너를 한 번에

지금까지 해온 것을 돌아보겠습니다. NGINX + 앱 서버 2개만 돼도 `docker build` 3번, `docker run` 3번, 네트워크도 따로 만들어야 했습니다. Redis까지 추가하면 명령어가 벌써 7~8줄입니다.

> **오픈이**: "이걸 매번 치는 건 진짜 아닌데..."
>
> **선배**: "Docker Compose라는 게 있거든."

컨테이너가 하나일 때는 `docker run` 한 줄이면 충분합니다. 실제 서비스는 프론트엔드, 백엔드, DB처럼 여러 컨테이너가 함께 동작합니다. 컨테이너가 5개라면 `docker run`도 5번, 네트워크 생성도 따로, 내릴 때도 하나씩 내려야 합니다. 시작 순서를 틀리면 에러가 발생합니다. DB가 올라오기 전에 백엔드를 먼저 실행하면 연결에 실패합니다.

**Docker Compose**는 이 문제를 해결합니다. `docker-compose.yml`이라는 YAML 파일 하나에 모든 컨테이너의 구성을 정의합니다.

### 3.5.1 Docker Compose : 왜 필요한가

Docker Compose는 오케스트라 악보와 같습니다. 각 악기(컨테이너)의 역할은 다르지만 하나의 악보로 동시에 연주할 수 있습니다.

> **도커 컴포즈(Docker Compose)**: 하나의 스크립트 파일로 여러 컨테이너를 하나의 환경으로 묶어 관리하는 도구입니다.

지금까지 Dockerfile에 필요한 환경과 설정을 작성한 후 이미지를 생성하고 컨테이너를 실행했습니다.

여러 컨테이너를 함께 실행하려면 Dockerfile마다 이미지를 따로 빌드하고 컨테이너도 하나씩 실행해야 했습니다. 컨테이너끼리 통신하려면 `docker network` 명령어로 네트워크를 직접 만들어야 했습니다.

<!-- image-prompt: Black line drawing on white background, clean technical diagram, 16:9 aspect ratio, 1280x720px. with Korean labels, NO title text. Three horizontal rows with equal spacing. Each row uses the EXACT same icon style: Dockerfile (document icon with folded top-right corner, like a paper sheet) arrow labeled "docker build" to 이미지 (stacked diamond/layer icon, 3-4 layers stacked vertically like the Docker image logo), arrow labeled "docker run" to 컨테이너 (3D shipping container box with vertical lines on the side, like a cargo container). Row 1: Dockerfile → 애플리케이션 이미지 → 애플리케이션 컨테이너. Row 2: Dockerfile → 데이터베이스 이미지 → 데이터베이스 컨테이너. Row 3: Dockerfile → API 이미지 → API 컨테이너. Labels below each icon. Minimal black line drawing style, no fill colors. -->

![](../assets/CH03/chap02-48.png)
*기존 방식 — Dockerfile 개별 빌드 및 실행*

<!-- image-prompt: Black line drawing on white background, clean technical diagram, 16:9 aspect ratio, 1280x720px. with Korean labels, NO title text. Left side: one document icon with folded top-right corner labeled "docker-compose.yml". Single large arrow labeled "docker compose up" pointing right. Right side: three 3D shipping container boxes with vertical lines on the side (애플리케이션 컨테이너, 데이터베이스 컨테이너, API 컨테이너) grouped inside a dashed rounded rectangle. Labels below each icon. Minimal black line drawing style, no fill colors. -->

Docker Compose 스크립트에 이미지 관리 작업을 정의하면 `docker compose up` 명령 한 번으로 여러 이미지를 동시에 실행하고 필요한 환경을 자동으로 구성할 수 있습니다.

Compose가 해결하는 것은 세 가지입니다.

**순서 :** 어떤 컨테이너를 먼저 띄울지 `depends_on`으로 지정할 수 있습니다. 단, 컨테이너가 시작되었다고 해서 내부 서비스가 바로 준비된 것은 아닙니다. DB가 올라오기 전에 백엔드가 연결을 시도하면 실패할 수 있으므로, 애플리케이션 레벨에서 재연결 처리가 필요합니다.

**네트워크 :** 같은 Compose 파일에 정의된 컨테이너는 자동으로 하나의 네트워크에 묶입니다. `docker network create`를 직접 실행할 필요가 없습니다. 컨테이너끼리 서비스 이름으로 통신할 수 있습니다.

**일괄 관리 :** `docker compose up` 한 줄이면 모든 컨테이너가 시작됩니다. `docker compose down` 한 줄이면 모든 컨테이너와 네트워크가 정리됩니다.

![](../assets/CH03/chap02-49.png)
*Docker Compose 방식 — 한 번에 생성 및 연결*

아래는 docker-compose.yml의 기본 구조입니다.

> **image 옵션** 은 Dockerhub에서 가져올 이미지 이름을 지정합니다. **build 옵션** 과 함께 사용하면 Dockerfile로 빌드한 이미지에 그 이름을 지정할 수 있습니다.

**[참고]** docker-compose.yml 기본 구조

```yaml
# 실행할 컨테이너
services:
  <서비스명>:
    container_name: <컨테이너명> # 컨테이너 이름 지정
    image: <이미지명>           # 이미지 이름 지정
    build: <경로>               # Dockerfile 경로 (이미지를 직접 빌드)
    ports:
      - "호스트포트:컨테이너포트" # 포트 매핑
    depends_on:
      - <다른서비스명>           # 이 서비스보다 먼저 시작해야 하는 서비스
    environment:
      - KEY=VALUE               # 환경 변수 설정
    volumes:
      - <호스트경로:컨테이너경로> # 데이터 저장소 연결
    networks:
      - <네트워크명>             # 연결할 네트워크

# 저장소 지정 
volumes:
  <볼륨명>:

# 컨테이너간 통신을 위한 네트워크 선언 
networks:
  <네트워크명>:
```

### 3.5.2 Docker Compose : 실습

아래의 Github 주소를 참고합니다.

> 실습 코드는 https://github.com/metacoding-10-linux-docker/docker/tree/master/ex06 에서 확인할 수 있습니다.

Dockerfile과 index.html은 EX01과 동일하며, docker-compose.yml이 추가되고 nginx.conf가 서비스 이름 통신 방식으로 변경되었습니다.

**[EX06 패키지 구조]**

```
ex06/
├── app1/                # 첫 번째 웹 서버
│   ├── Dockerfile
│   └── index.html
├── app2/                # 두 번째 웹 서버
│   ├── Dockerfile
│   └── index.html
├── lb/                  # 로드밸런서 (NGINX)
│   ├── Dockerfile
│   └── nginx.conf       # 라우팅 설정
└── docker-compose.yml   # 전체 컨테이너 통합 실행
```

EX06의 각 Dockerfile은 EX01과 동일한 구조입니다.

**[참고]** `app1/Dockerfile` (app2도 동일)

**ex06/app1/Dockerfile**
```dockerfile
FROM nginx                                          # NGINX 이미지 사용
COPY index.html /usr/share/nginx/html               # index.html을 NGINX 기본 경로로 복사
ENTRYPOINT ["nginx", "-g", "daemon off;"]            # NGINX를 포그라운드로 실행
```

**[참고]** `lb/Dockerfile`

**ex06/lb/Dockerfile**
```dockerfile
FROM nginx                                          # NGINX 이미지 사용
COPY nginx.conf /etc/nginx/conf.d/default.conf      # 로컬의 nginx.conf를 컨테이너의 NGINX 설정 경로로 복사
ENTRYPOINT ["nginx", "-g", "daemon off;"]            # NGINX를 포그라운드로 실행
```

EX01에서는 컨테이너를 개별 실행했기 때문에 nginx.conf에서 `host.docker.internal`로 호스트 PC를 경유해야 했습니다. Docker Compose에서는 같은 네트워크에 묶인 서비스끼리 서비스 이름으로 직접 통신할 수 있으므로, nginx.conf의 upstream 주소가 `app1:80`, `app2:80`으로 바뀌었습니다.

### 🔍 네트워크 돋보기 ⑥: Compose 네트워크 — 서비스 이름이 곧 주소다

> **"왜 Docker Compose에서는 host.docker.internal도, IP도 쓰지 않고 서비스 이름만으로 통신이 되지?"**

Docker Compose는 `docker compose up`을 실행할 때 자동으로 **사용자 정의 네트워크**를 만듭니다. 돋보기 ⑤에서 배운 것처럼, 사용자 정의 네트워크에는 DNS가 자동으로 켜집니다.

Compose가 하는 일을 풀어 쓰면 이렇습니다:

```bash
# docker compose up이 내부적으로 하는 일
docker network create ex06-network           # ① 네트워크 생성 (DNS 자동 활성화)
docker run --network ex06-network app1       # ② 컨테이너를 네트워크에 연결
docker run --network ex06-network app2       # ③ DNS에 "app2" → IP 자동 등록
docker run --network ex06-network lb         # ④ DNS에 "lb" → IP 자동 등록
```

그래서 nginx.conf에서 `upstream app1 { server app1:80; }`이 동작합니다. `app1`이라는 서비스 이름이 Docker DNS를 통해 자동으로 해당 컨테이너의 IP로 변환되기 때문입니다.

![](../assets/CH03/net-06-compose-network.png)

이것으로 2장~3장에서 등장한 Docker 네트워크의 전체 진화 과정이 보입니다:

| 단계 | 방식 | 문제점 | 해결책 |
|------|------|--------|--------|
| `docker run` 개별 실행 | 기본 bridge | 이름 통신 불가 | `host.docker.internal` 우회 |
| `docker network create` | 사용자 정의 bridge | 수동 생성 번거로움 | Docker DNS 자동 활성화 |
| `docker compose up` | Compose 자동 네트워크 | — | 네트워크 생성 + DNS + 연결 전부 자동 |

> 💡 **한 줄 정리**: Docker Compose는 네트워크 생성 + DNS 활성화 + 컨테이너 연결을 자동으로 해준다. 서비스 이름 = DNS 이름이 되어, IP를 몰라도 이름으로 통신할 수 있다.

docker-compose.yml 파일은 다음과 같습니다. 하나의 **services** 옵션 안에 `app1`, `app2`, `lb` 세 서비스의 컨테이너 실행 설정이 작성되어 있습니다. `ex06-network`로 세 서비스를 하나의 네트워크에 묶어 서비스 이름으로 통신합니다.

**[참고]** `docker-compose.yml`

**ex06/docker-compose.yml**
```yaml
services:
  app1:                    # 서버 1
    build:
      context: ./app1      # Dockerfile 경로
    ports:
      - 8000:80            # localhost:8000으로 접근
    networks:
      - ex06-network       # 공용 네트워크 연결
  app2:                    # 서버 2
    build:
      context: ./app2      # Dockerfile 경로
    ports:
      - 9000:80            # localhost:9000으로 접근
    networks:
      - ex06-network       # 공용 네트워크 연결
  lb:                      # 로드밸런서
    build:
      context: ./lb        # Dockerfile 경로
    ports:
      - 80:80              # localhost:80으로 접근
    networks:
      - ex06-network       # 공용 네트워크 연결

networks:
  ex06-network:            # 3개 서비스를 하나로 묶는 가상 네트워크
```

아래 명령어를 실행합니다. 빌드와 실행을 한 번에 처리합니다.

**[실습]** EX06 폴더로 이동 후, docker compose up 명령으로 모든 서비스를 한 번에 실행합니다.

```bash
docker compose up   # 모든 컨테이너 한 번에 실행
```

<!-- image-prompt: Terminal showing docker compose up command building and starting three services -->

![](../assets/CH03/chap02-52.png)
*docker compose up 실행*

Docker Desktop에서 컨테이너를 확인하면 `ex06` 컨테이너 내부에 `app1`, `app2`, `lb` 컨테이너가 보입니다.

<!-- image-prompt: Docker Desktop showing ex06 group with app1, app2, and lb containers running -->

![](../assets/CH03/chap02-53.png)
*Docker Desktop에서 Compose 컨테이너 확인*

![](../assets/CH03/chap02-54.png)
*Docker Desktop에서 Compose 로그 확인*

EX01과 동일하게 브라우저에 `localhost:80/app1`, `localhost:80/app2`를 입력하면 각 서버에 접근할 수 있습니다.

실습이 끝나면 다음 명령어로 컨테이너를 종료합니다.

**[실습]** 터미널에서 docker compose down 명령으로 모든 서비스를 종료합니다.

```bash
docker compose down   # 모든 컨테이너 중지 및 삭제
```

### 3.5.3 docker compose : 주요 명령어

docker compose에서 자주 사용하는 하위 명령어를 정리하면 다음과 같습니다.

| 명령어 | 설명 |
|--------|------|
| `docker compose up` | 모든 서비스를 빌드하고 실행 |
| `docker compose up -d` | 백그라운드에서 실행 |
| `docker compose down` | 모든 서비스를 중지하고 삭제 |
| `docker compose ps` | 실행 중인 서비스 목록 확인 |
| `docker compose logs` | 서비스 로그 확인 |
| `docker compose build` | 서비스 이미지만 빌드 |

## 3.6 종합 실습 : 웹 사이트 만들기

Dockerfile, NGINX, Redis, MySQL, Docker Compose까지 지금까지 배운 모든 기술을 하나로 모아볼 시간입니다. Docker Compose를 활용해 프론트 서버에서 발생한 요청이 백엔드 서버로 전달되고 DB 서버에서 데이터를 조회해 응답하는 웹사이트를 만들어보겠습니다.

> 실습 코드는 https://github.com/metacoding-10-linux-docker/docker/tree/master/ex07 에서 확인할 수 있습니다.

**[EX07 패키지 구조]**

```
ex07/
├── backend/             # 백엔드 서버 (Spring Boot)
│   ├── Dockerfile
│   └── entrypoint.sh   # Git clone + 빌드 + 실행 스크립트
├── db/                  # MySQL 데이터베이스
│   ├── Dockerfile
│   └── init.sql         # 초기 테이블 및 데이터 생성 SQL
├── frontend/            # 프론트엔드 (NGINX)
│   ├── Dockerfile
│   ├── index.html       # 화면 페이지
│   └── nginx.conf       # 정적 파일 제공 + API 프록시 설정
└── docker-compose.yml   # 전체 컨테이너 통합 실행
```

### 3.6.1 아키텍처 개요

이번에 만들 웹 사이트는 3개의 서비스로 구성됩니다.

- **Frontend (NGINX)**: 브라우저에 HTML 페이지를 제공하고, `/api/` 요청을 백엔드로 프록시합니다.
- **Backend (Spring Boot)**: `/api/users` API를 제공하여 DB에서 사용자 목록을 조회합니다.
- **DB (MySQL)**: 사용자 데이터를 영구 저장합니다.

프론트 서버와 백엔드 서버, DB 서버는 서로 다른 포트를 가지고 있으며, 전체 요청 흐름은 다음과 같습니다.

![](../assets/CH03/fig-1-v2.png)
*여러 컨테이너가 연동되는 웹 애플리케이션 아키텍처*

3.2에서 NGINX가 URL 보고 요청을 나눠주는 것을 배웠습니다. 여기서도 같은 원리입니다. NGINX가 `/` 요청에는 HTML 페이지를 제공하고, `/api/` 요청은 백엔드로 넘겨줍니다.

### 3.6.2 MySQL : DB 서버 만들기

DB 서버는 3.4와 동일한 구조입니다.

**[참고]** `db/Dockerfile`

**ex07/db/Dockerfile**
```dockerfile
FROM mysql                                    # MySQL 이미지 사용
COPY init.sql /docker-entrypoint-initdb.d     # 로컬의 init.sql을 MySQL 초기화 폴더로 복사
ENV MYSQL_USER=metacoding                     # 생성할 사용자 이름
ENV MYSQL_PASSWORD=metacoding1234             # 사용자 비밀번호
ENV MYSQL_ROOT_PASSWORD=root1234              # root 비밀번호
ENV MYSQL_DATABASE=metadb                     # 생성할 데이터베이스 이름
CMD ["--character-set-server=utf8mb4", "--collation-server=utf8mb4_unicode_ci"]  # 한글 인코딩 설정
```

### 3.6.3 Spring Boot : 백엔드 서버 만들기

> 이 절의 Spring Boot와 Gradle 코드는 실습 동작을 위해 미리 작성된 코드입니다. 코드 내용을 이해할 필요는 없으며, Docker가 어떻게 백엔드 서버를 컨테이너로 실행하는지에 집중하면 됩니다.

GitHub에 있는 Spring Boot 프로젝트를 컨테이너에서 실행하려면 소스를 내려받고 빌드해야 합니다. 이 초기 작업이 `entrypoint.sh`에 정의되어 있습니다.

> `entrypoint.sh`는 컨테이너가 시작될 때 자동으로 실행되는 셸 스크립트입니다. 소스 코드 다운로드, 빌드, 서버 실행처럼 컨테이너가 켜지자마자 해야 할 작업을 순서대로 적어둡니다.
> - `Dockerfile` → 이미지 **설치** 단계 (한 번만 실행)
> - `entrypoint.sh` → 컨테이너 **실행** 단계 (시작할 때마다 실행)

`entrypoint.sh`는 다음과 같습니다.

**[참고]** 컨테이너가 시작되면 GitHub에서 Spring Boot 소스를 내려받은 후 Gradle로 빌드하고 JAR 파일을 실행합니다.

**ex07/backend/entrypoint.sh**
```bash
#!/bin/bash
git clone https://github.com/metacoding-10-linux-docker/backend-server  # 백엔드 서버 Github에서 내려받기
cd backend-server                                  # 내려받은 폴더로 이동
chmod +x gradlew                                   # 실행 권한 부여
./gradlew build                                    # 스프링 프로젝트 빌드
java -jar -Dspring.profiles.active=prod build/libs/*.jar  # 빌드된 파일 실행
```

스프링 서버 안에는 `/api/users` 주소로 요청이 들어오면 회원 정보를 응답하는 컨트롤러가 있습니다.

**[참고]** `entrypoint.sh`에서 내려받는 백엔드 서버의 핵심 API 코드는 다음과 같습니다.

**UserController.java**
```java
@GetMapping("/api/users")                          // /api/users 요청 처리
public ResponseEntity<?> findAll() {
    List<User> users = userRepository.findAll();    // DB에서 회원 목록 조회
    return Resp.ok(users);                          // JSON 응답 반환
}
```
Dockerfile은 Java와 Git을 설치하고 컨테이너가 시작되면 entrypoint.sh를 실행합니다.

**[참고]** `Dockerfile`

**ex07/backend/Dockerfile**
```dockerfile
FROM eclipse-temurin:21-jdk              # JDK 21 베이스 이미지
WORKDIR /var/current/app                 # 작업 디렉토리 설정
COPY entrypoint.sh /entrypoint.sh        # 로컬의 entrypoint.sh를 컨테이너 루트 경로로 복사
RUN apt-get update && apt-get install -y git  # Git 설치
ENTRYPOINT ["/entrypoint.sh"]            # 컨테이너 시작 시 실행
```

### 3.6.4 NGINX : 프론트 서버 만들기

Dockerfile은 nginx 이미지에 nginx.conf와 index.html을 복사합니다.

| 파일 | 설명 |
|------|------|
| `frontend/Dockerfile` | nginx 이미지 기반, nginx.conf와 index.html 복사 |
| `frontend/index.html` | fetch로 `/api/users` 요청 후 사용자 정보를 화면에 표시 |

**[참고]** `frontend/Dockerfile`

**ex07/frontend/Dockerfile**
```dockerfile
FROM nginx                                          # NGINX 이미지 사용
COPY nginx.conf /etc/nginx/nginx.conf               # NGINX 설정 파일 복사
COPY index.html /usr/share/nginx/html/              # HTML 파일을 NGINX 기본 경로로 복사
CMD ["nginx", "-g", "daemon off;"]                  # NGINX를 포그라운드로 실행
```

nginx.conf는 다음과 같습니다. 슬래시(`/`) 요청은 index.html을 응답하고 `/api/` 요청은 백엔드 서비스로 프록시합니다. `server backend:8080`에서 `backend`는 Docker Compose에서 정의한 서비스 이름입니다.

**[참고]** `frontend/nginx.conf`

**ex07/frontend/nginx.conf**
```nginx
events {}

http {
    # 백엔드 서버 주소 (Docker Compose 서비스명)
    upstream backend {
        server backend:8080;
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

### 3.6.5 Docker Compose : 통합 구성

docker-compose.yml은 다음과 같습니다. `backend`, `db`, `frontend` 3개의 컨테이너를 생성합니다. `environment`로 Spring Boot의 DB 접속 정보를 주입하고 `ex07-network`로 세 서비스를 하나의 네트워크에 묶어 서비스 이름으로 통신합니다.

**[참고]** `docker-compose.yml`

**ex07/docker-compose.yml**
```yaml
services:
  backend:                    # 백엔드 서비스 (Spring Boot)
    build:
      context: ./backend      # Dockerfile 경로
    ports:
      - "8080:8080"           # 호스트 8080 → 컨테이너 8080
    environment:              # 환경 변수로 DB 접속 정보 전달
      SPRING_DATASOURCE_URL: jdbc:mysql://db:3306/metadb?useSSL=false&serverTimezone=UTC&useLegacyDatetimeCode=false&allowPublicKeyRetrieval=true
      SPRING_DATASOURCE_DRIVER_CLASS_NAME: com.mysql.cj.jdbc.Driver
      SPRING_DATASOURCE_USERNAME: metacoding
      SPRING_DATASOURCE_PASSWORD: metacoding1234
    networks:
      - ex07-network          # 공용 네트워크 연결

  db:                         # 데이터베이스 서비스 (MySQL)
    build:
      context: ./db           # Dockerfile 경로
    ports:
      - 3306:3306             # 호스트 3306 → 컨테이너 3306
    networks:
      - ex07-network          # 공용 네트워크 연결

  frontend:                   # 프론트엔드 서비스 (Nginx)
    build:
      context: ./frontend     # Dockerfile 경로
    ports:
      - "80:80"               # 호스트 80 → 컨테이너 80
    networks:
      - ex07-network          # 공용 네트워크 연결

networks:
  ex07-network:               # 3개 서비스를 하나로 묶는 가상 네트워크
```

### 3.6.6 통합 실행

이제 명령어를 실행해 컨테이너를 실행합니다.

**[실습]** EX07 폴더로 이동 후, docker compose up 명령으로 전체 서비스를 실행합니다.

```bash
docker compose up   # 여러 컨테이너가 연동되는 웹 애플리케이션 실행
```

> 백엔드 컨테이너는 Gradle 빌드를 실행하므로 처음 실행 시 수 분이 소요될 수 있습니다. 터미널에 로그가 멈춘 것처럼 보여도 정상입니다. 빌드 진행 상황은 `docker compose logs -f backend` 명령으로 확인할 수 있습니다.

![](../assets/CH03/chap02-ex07-compose.png)
*docker compose up 실행 결과*

#### 결과 확인

서버가 모두 실행되면 브라우저에서 결과를 확인합니다. 다음 항목을 순서대로 확인합니다.

1. 브라우저에서 `localhost` 또는 `localhost:80`에 접속하여 "사용자 리스트" 페이지가 표시되는지 확인합니다.
2. 테이블에 ID와 이름 컬럼이 표시되고 init.sql에서 입력한 ssar, cos 데이터가 조회되는지 확인합니다.
3. 데이터가 표시되지 않으면 백엔드 서버 빌드가 아직 진행 중일 수 있으므로 잠시 기다린 후 새로고침합니다. DB 컨테이너보다 백엔드 컨테이너가 먼저 실행되면 DB 연결에 실패할 수 있습니다. 이 경우에도 잠시 기다리면 백엔드가 재연결을 시도하여 정상 동작합니다.

서버와 통신이 성공하면 사용자 목록이 조회됩니다.

<!-- image-prompt: Browser showing a user list table with two rows: ID 1 ssar and ID 2 cos -->

![](../assets/CH03/chap02-58.png)
*사용자 목록 조회 성공*

페이지에 접속하면 백엔드가 DB에서 데이터를 가져옵니다. `docker compose up` 한 줄로 프론트엔드, 백엔드, DB가 연동되는 웹사이트가 올라갔습니다.

실습이 끝나면 다음 명령어로 정리합니다.

**[실습]** 터미널에서 docker compose down 명령으로 전체 서비스를 종료하고 정리합니다.

```bash
docker compose down   # 모든 컨테이너 중지 및 삭제
```

## 이것만은 기억하자

- **레시피만 있으면 누구든 같은 요리를 만든다.** Dockerfile에 환경 설정을 한 번 써두면 어디서든 동일한 컨테이너가 자동으로 만들어집니다. 더 이상 매번 패키지를 수동 설치할 필요가 없습니다.
- **안내 데스크가 있으면 길을 잃지 않는다.** NGINX는 URL 경로를 보고 적절한 서버로 요청을 보내주고 트래픽이 몰려도 여러 서버에 골고루 나눠줍니다. 자주 찾는 파일은 캐시에 보관해 빠르게 응답합니다.
- **컨테이너가 여러 개면, 악보 한 장으로 한꺼번에 띄워라.** Docker Compose는 프론트엔드, 백엔드, DB 등 여러 컨테이너를 `docker-compose.yml` 하나에 정의하고 명령어 한 줄로 전부 실행합니다. 공용 사물함(Redis)으로 세션을 공유하고 영구 보관 창고(MySQL)로 데이터를 안전하게 저장할 수 있습니다.

웹사이트까지 완성했습니다. 하지만 아직 해결하지 못한 문제가 남아 있습니다. 지금 실행 중인 백엔드 컨테이너를 `docker stop`으로 종료하면 사용자는 바로 오류 화면을 만나게 됩니다. 서비스를 복구하려면 개발자가 직접 `docker compose up`을 다시 실행해야 합니다. 새벽에 컨테이너가 죽으면? 누군가 직접 다시 띄워야 합니다.

> **선배**: "근데 새벽에 서버 죽으면 누가 살려줄 건데?"

