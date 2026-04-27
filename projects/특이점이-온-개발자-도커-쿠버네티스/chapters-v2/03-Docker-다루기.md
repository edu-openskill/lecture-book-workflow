# Ch.3 Docker 다루기

> 한 줄 요약: 여러 컨테이너를 자동으로 구성하고 Docker Compose로 한 번에 띄운다
> 핵심 개념: Dockerfile, NGINX, Redis, MySQL, Docker Compose

지금까지 도커의 기본기를 익혔습니다. 하지만 컨테이너를 만들 때마다 매번 똑같은 설치 과정을 반복하는 것은 꽤 번거로운 일입니다. 장을 보고 재료를 손질하는 수고 대신, 봉지만 뜯으면 요리가 완성되는 **'밀키트'** 같은 방법은 없을까요?

## 3.1 프로비저닝 : 환경을 자동으로 구성하다

매번 수동으로 환경을 만드는 번거로움을 해결하기 위해 등장한 개념이 있습니다. 필요한 패키지와 설정을 미리 정의해두고, 컨테이너 환경을 자동으로 구축하는 것을 **프로비저닝(Provisioning)** 이라고 합니다.
![](../assets/CH03/chap02-provisioning.png)
*수동 세팅과 프로비저닝*

> **프로비저닝(Provisioning)**: 도커에서 프로비저닝은 컨테이너가 처음 생성될 때 필요한 환경을 자동으로 세팅하는 과정을 의미합니다. 컨테이너가 실행되면 쓸 수 있는 설정, 패키지, 파일 등을 미리 준비하는 작업입니다.

밀키트에 담긴 레시피대로 요리가 뚝딱 만들어지듯, 프로비저닝을 이용하면 개발 환경을 만드는 수고를 줄일 수 있습니다. 도커에서는 **Dockerfile** 이라는 레시피를 통해 이 자동화 과정을 구현합니다.

### 3.1.1 Dockerfile : 프로비저닝 설계도

> **Dockerfile**: 컨테이너가 실행될 때 필요한 환경을 자동으로 구성해주는 이미지를 생성하기 위한 스크립트로, 컨테이너를 만들기 위한 설계도입니다.

Dockerfile은 환경을 정의한 **설계도**입니다. 도커는 이 파일을 읽어 **이미지**를 만들고, 이 이미지로 **컨테이너**를 실행합니다.

Dockerfile에서 컨테이너가 실행되기까지 세 단계를 거칩니다.

![](../assets/CH03/chap02-1.png)
*Dockerfile에서 이미지 생성 및 컨테이너 실행 과정*

**1단계 — Dockerfile 작성.** 텍스트 파일에 환경 구성을 적습니다. 베이스 이미지, 설치할 패키지, 복사할 파일, 실행할 명령을 순서대로 기록합니다.

**2단계 — docker build.** Docker 엔진이 Dockerfile을 위에서 아래로 읽으며 각 줄을 실행합니다. 결과물이 **이미지(Image)** 로 저장됩니다. 이미지는 읽기 전용이며 한 번 만들어지면 변하지 않습니다.

**3단계 — docker run.** 이미지를 기반으로 **컨테이너(Container)** 를 생성하고 실행합니다. 하나의 이미지에서 컨테이너를 몇 개든 만들 수 있습니다. 컨테이너를 삭제해도 이미지는 그대로 남아 있으므로 다시 실행하면 동일한 환경이 만들어집니다.

아래는 Dockerfile에서 사용하는 주요 설정입니다.

**[참고]** Dockerfile 주요 설정 구조

```dockerfile
FROM  <베이스 이미지명>

WORKDIR <기준 작업 경로 설정>

COPY <파일을 컨테이너 내부로 복사>

RUN <이미지 빌드 시 실행할 리눅스 명령 (패키지 설치 등)>

ENV <환경 변수 설정>

CMD <컨테이너 시작 시 메인 프로세스에 실행되는 명령어>

ENTRYPOINT <메인 프로세스를 지정하는 명령어>
```

### 3.1.2 Dockerfile : 스크립트 작성

vim이 깔린 Ubuntu 이미지를 하나 만들어 보겠습니다.

CURSOR IDE에서 `Dockerfile`을 생성 후, 아래의 스크립트를 작성합니다. **(별도 확장자 없이 파일명만 Dockerfile로 입력하면 됩니다.)**

![](../assets/CH03/chap02-6.png)
*Dockerfile 생성 완료*

**[작성]** `Dockerfile`을 아래와 같이 작성합니다.

```dockerfile
FROM ubuntu:24.04                      # 베이스 이미지
RUN apt update && apt install -y vim   # vim 패키지 설치
CMD ["/bin/bash"]                      # 컨테이너가 시작될 때 자동으로 실행할 명령
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

터미널에 설치 명령어를 적지 않았는데 vim이 바로 됩니다. Dockerfile에 써둔 설정이 실행됐기 때문입니다. Dockerfile 하나면 컨테이너의 원하는 환경을 동일하게 재현할 수 있습니다.

### 3.1.3 WORKDIR, COPY : 작업 경로와 파일 복사

> **WORKDIR**: 명령어가 실행될 기본 폴더를 지정합니다. 이후에 나오는 모든 작업은 이 폴더를 기준으로 진행됩니다.
> **COPY**: 호스트PC에 있는 파일이나 폴더를 컨테이너 내부로 복사합니다.

3.1.3에서 생성한 폴더 내부에 **index.html** 파일을 생성합니다. index.html의 내부는 비어있는 빈 파일입니다.

![](../assets/CH03/chap02-11.png)
*폴더 및 파일 구조*

Dockerfile에 **WORKDIR**와 **COPY** 설정을 추가합니다. WORKDIR로 작업 디렉토리를 `/app`으로 지정하고 COPY로 로컬의 파일을 컨테이너로 복사하면 됩니다.

**[작성]** `Dockerfile`에 아래와 같이 html 파일을 복사하도록 수정합니다.

```dockerfile
FROM ubuntu:24.04                      # 베이스 이미지
WORKDIR /app                           # 작업 경로를 /app으로 설정
COPY ./index.html ./index.html         # 로컬의 index.html을 컨테이너의 /app으로 복사
RUN apt update && apt install -y vim   # vim 패키지 설치
CMD ["/bin/bash"]                      # 컨테이너가 시작될 때 자동으로 실행할 명령
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

### 3.1.4 CMD, ENTRYPOINT : 기본 명령과 고정 명령

CMD와 ENTRYPOINT는 컨테이너가 시작될 때 무엇을 실행할지 결정하지만, 성격은 조금 다릅니다.

식당에 비유하면 CMD는 '기본 메뉴'와 같습니다. 주방에서 미리 정해둔 메뉴가 있지만, 손님이 원하면 얼마든지 다른 메뉴로 바꿀 수 있습니다. 반면 ENTRYPOINT는 '수저와 물' 같은 기본 세팅입니다. 어떤 메뉴를 주문하든 반드시 준비되어야 하는 필수 요소와 같습니다.

> **CMD** : CMD: 컨테이너가 시작될 때 실행할 **기본 명령** 을 지정합니다. docker run 명령 뒤에 별도의 명령어를 입력하면 CMD에 **설정된 내용은 무시되고** 입력한 명령이 우선 실행됩니다.
> **ENTRYPOINT**: 컨테이너가 시작될 때 **반드시 실행되어야** 하는 메인 프로세스를 지정합니다. 외부에서 어떤 옵션을 주더라도 이 프로세스는 바뀌지 않고 실행됩니다.

Dockerfile에 **ENTRYPOINT**를 추가해 echo 명령으로 메시지를 출력하도록 설정합니다.

**[작성]** `Dockerfile`에 ENTRYPOINT를 추가합니다.

```dockerfile
FROM ubuntu:24.04                      # 베이스 이미지
WORKDIR /app                           # 작업 경로를 /app으로 설정
COPY ./index.html ./index.html         # 로컬의 index.html을 컨테이너의 /app으로 복사
RUN apt update && apt install -y vim   # vim 패키지 설치
CMD ["/bin/bash"]                      # ENTRYPOINT 뒤에 붙어서 실행됨
ENTRYPOINT ["echo", "컨테이너 실행"]     # 컨테이너 시작 시 실행되는 명령
```

#### 실습해보기

**[실습]** ENTRYPOINT가 적용된 이미지를 빌드 및 실행하는 명령어입니다.

```bash
docker build -t ubuntu-entry .         # 이미지 생성
docker run -it ubuntu-entry            # 컨테이너 실행
```

![](../assets/CH03/chap02-15.png)
*ENTRYPOINT 실행 결과*

결과를 확인하면 **ENTRYPOINT**에 작성한 **컨테이너 실행 /bin/bash** 이 출력되고 프로세스는 즉시 종료됩니다. 왜 그럴까요?

ENTRYPOINT가 있으면 CMD는 독립적으로 실행되지 않고, ENTRYPOINT 뒤에 붙어서 함께 실행됩니다. 즉 **echo "컨테이너 실행"** + **/bin/bash** 가 합쳐져서 **echo "컨테이너 실행" /bin/bash** 가 된 것입니다.

**echo** 는 뒤에 오는 내용을 그대로 출력하고 끝나는 명령이라, "컨테이너 실행 /bin/bash"라는 글자만 화면에 찍고 종료됩니다. 메인 프로세스가 끝났으니 컨테이너도 즉시 종료됩니다.

## 3.2 NGINX : 웹 서버와 리버스 프록시

챕터 2에서 가볍게 실행해 본 NGINX는 단순히 웹페이지를 띄우는 것보다 훨씬 많은 일을 할 수 있습니다.

> **NGINX**: 웹 서버이자 요청을 중계하는 프록시 서버입니다. 이미지나 HTML 같은 파일을 빠르게 처리하고, 사용자의 요청을 백엔드 서버로 연결해 주는 역할을 합니다. 로드밸런싱, 보안(HTTPS) 처리, 캐싱 기능을 모두 갖추고 있어 대규모 서비스를 운영할 때 필수적으로 사용됩니다.

NGINX는 백엔드 서버 앞을 지키는 대리인 역할을 합니다. 사용자의 요청을 서버가 직접 받지 않고 NGINX가 중간에서 대신 받아 전달하는 방식입니다. 이 과정에서 실제 서버의 주소를 숨겨 보안을 높이고, 들어오는 요청을 여러 서버로 나누어 보내는 로드밸런싱을 수행합니다.

<!-- image-prompt: Minimal black line drawing on white background, very few details, icon-like simplicity, 4:3 aspect ratio, 800x600px. with Korean labels: Diagram with exactly one 클라이언트 on the left sending a request arrow to NGINX in the center. From NGINX, three arrows branch out to the right pointing to 로드밸런싱, 정적 파일 제공, 캐싱. Only one client icon, no duplicates. -->

![](../assets/CH03/chap02-17.png)
*NGINX의 주요 기능*

또, 요청이 올 때마다 매번 새로운 프로세스를 만드는 대신, 적은 수의 프로세스로 수많은 요청을 번갈아 가며 처리합니다. 한 명의 직원이 여러 테이블을 동시에 응대하는 것과 비슷해서, 많은 사용자가 동시에 접속해도 메모리 낭비가 적고 속도가 빠릅니다.

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

nginx.conf는 NGINX가 요청을 어떻게 처리할지 정의하는 설계도입니다. 핵심은 세 가지 설정입니다.

| 설정 | 역할 | 예시에서 하는 일 |
|------|------|-----------------|
| `location` | URL 경로에 따라 요청을 분기 | `/app1` 경로로 들어온 요청을 `proxy_pass`로 넘김 |
| `proxy_pass` | 요청을 다른 서버로 전달 | `http://app1/` — upstream app1으로 요청을 보냄 |
| `upstream` | 실제 서버 주소에 이름을 붙임 | `app1`이라는 이름에 `host.docker.internal:8000`을 등록 |

`/app1`로 요청이 들어오면 → `location`이 받아서 → `proxy_pass`를 통해 → `upstream`에 등록된 `host.docker.internal:8000`으로 전달됩니다.

이제 이미지를 실행해보겠습니다. 다음 명령어를 순차적으로 실행합니다.

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

#### host.docker.internal

nginx.conf의 upstream을 다시 보면, 목적지가 `host.docker.internal:8000`으로 되어 있습니다. app1 컨테이너로 바로 보내면 될 텐데, 왜 호스트 PC를 경유할까요?

이 예제에서는 컨테이너를 `docker run`으로 각각 따로 실행했습니다. 이렇게 개별 실행된 컨테이너들은 서로의 존재를 모르기 때문에, lb 컨테이너가 app1 컨테이너를 직접 찾을 수 없습니다. 그래서 호스트 PC를 거쳐가는 우회 경로를 사용합니다.

![](../assets/CH03/ex01-lb-to-host.png)
*lb 컨테이너 → 호스트 PC → app1 컨테이너*

> **host.docker.internal :** 컨테이너 내부에서 '호스트 PC'를 가리키는 특수한 주소입니다. 컨테이너 안에서 localhost라고 하면 호스트 PC가 아니라 컨테이너 자기 자신을 가리키게 됩니다. 따라서 호스트 PC의 포트에 접속하려면 반드시 이 주소를 사용해야 합니다.

lb 컨테이너가 `host.docker.internal:8000`으로 요청을 보내면, 호스트 PC의 8000번 포트에 도착합니다. 이 포트는 포트 포워딩(`-p 8000:80`)을 통해 app1 컨테이너와 연결되어 있으므로, 최종적으로 app1이 응답을 돌려줍니다.


### 3.2.3 라운드 로빈 : 요청을 골고루 나누다

NGINX의 upstream 설정을 사용하면 여러 대의 서버를 하나의 그룹으로 묶어 관리할 수 있습니다. 외부 사용자는 하나의 주소로 접속하지만, 실제로는 NGINX가 뒤에 숨어있는 여러 대의 서버로 요청을 적절히 나누어 보내주는 구조입니다.

이렇게 묶인 서버들에 요청을 배분하는 가장 대표적인 방식이 바로 **라운드 로빈(Round Robin)** 입니다. 마치 놀이공원 매표소에 3개의 창구가 있을 때, 손님을 1번 → 2번 → 3번 창구 순으로 번갈아 가며 안내하는 것과 같습니다. 특정 창구에만 줄이 길게 늘어지는 것을 막고 모두가 비슷하게 일을 하도록 만듭니다.

<!-- image-prompt: Minimal black line drawing on white background, very few details, icon-like simplicity, 4:3 aspect ratio, 800x600px. with Korean labels: 라운드 로빈 로드밸런싱 diagram. Left: one 클라이언트 with a single arrow to center NGINX, labeled "요청 x3" on the arrow to show three requests were made. Right: NGINX sends exactly three arrows - 요청 1 to 서버 1, 요청 2 to 서버 2, 요청 3 to 서버 3. No extra arrows. -->

![](../assets/CH03/chap02-23.png)
*라운드 로빈 로드밸런싱 구조*

이처럼 요청을 순차적으로 회전시키며 분배함으로써 특정 서버에 부하가 쏠리는 것을 방지하고, 전체 서비스의 안정성을 높일 수 있습니다.


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

### 3.2.4 캐싱 : 정적 파일을 빠르게 전달하다

자주 입는 옷을 박스에 보관하지 않고 옷걸이에 걸어놓는 것처럼 NGINX의 정적 서버는 HTML, CSS, 이미지와 같은 정적 파일을 보관했다가 클라이언트에게 직접 제공합니다.

> **정적 서버와 캐싱**: 정적 서버는 한 번 제공한 정적 파일을 일정 기간 저장해 둡니다. 이후 동일한 요청이 오면 서버에 다시 조회하지 않고 저장된 파일을 즉시 반환합니다. 이를 캐싱이라고 합니다.

클라이언트가 서버에 처음 이미지 파일을 요청하면 NGINX는 서버에 요청을 전달해 이미지 파일을 응답받습니다.

![](../assets/CH03/cache-miss.png)
*첫 번째 요청 (MISS) - 캐시가 비어있어 백엔드 서버에 요청 후 응답을 캐시에 저장*


그리고 일정 시간 이내에 동일한 요청이 다시 들어오면 NGINX는 서버 대신 캐시에 저장된 파일을 즉시 반환합니다.

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

API 서버는 파이썬으로 작성되어 있으며, 두 가지 요청을 처리합니다. 전체 코드는 GitHub 레포에서 확인할 수 있습니다.

| 파일 | URL | 기능 |
|------|-----|------|
| `app.py` | `/` | HTML 페이지 응답 |
| `app.py` | `/image.png` | 이미지 파일 응답 |

#### NGINX 이미지

nginx의 Dockerfile은 다음과 같습니다.

**[참고]** `nginx/Dockerfile`

**ex03/nginx/Dockerfile**
```dockerfile
FROM nginx                                          # NGINX 이미지 사용
COPY nginx.conf /etc/nginx/conf.d/default.conf      # 로컬의 nginx.conf를 컨테이너의 NGINX 설정 경로로 복사
ENTRYPOINT ["nginx", "-g", "daemon off;"]           # NGINX를 포그라운드로 실행
```

다음으로 nginx.conf 파일입니다. 캐시 저장 경로를 지정하는 `proxy_cache_path`와 캐시 사용 여부를 제어하는 `proxy_cache`가 포함되어 있습니다.

`proxy_cache_path` 설정으로 캐시 저장 경로와 메모리 공간을 지정하고, `location` 설정의 `proxy_cache`로 캐시 적용 여부를 제어합니다.

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

## 3.3 Redis : 세션 저장소

로드밸런싱을 적용하고 나면 예상치 못한 문제가 발생합니다. 여러 대의 서버를 돌리면 사용자가 로그인을 했는데 페이지를 이동하면 갑자기 로그인이 풀려버리거나, 인증이 되지 않는 현상이 나타납니다.

이 문제를 해결하는 방법 중 하나가 **Redis** 를 활용하는 것 입니다.

### 3.3.1 세션 : 왜 외부 저장소가 필요한가

**세션(Session)** 은 사용자가 로그인했을 때 서버가 생성하는 임시 기록입니다. **"이 사용자는 인증되었습니다"** 라는 정보를 서버 메모리에 저장해두고, 이후 요청이 올 때마다 이 기록을 확인하며 로그인 상태를 유지합니다.

문제는 서버가 여러 대일 때 발생합니다. 클라이언트가 로그인을 요청하면 NGINX는 이 요청을 '서버 1'로 전달합니다. 이때 로그인 정보는 오직 '서버 1'의 메모리에만 기록됩니다. 그런데 다음 요청이 NGINX에 의해 '서버 2'로 전달되면 어떻게 될까요? '서버 2'는 해당 사용자의 세션 정보를 모르기 때문에 다시 로그인을 요구하게 됩니다.

![](../assets/CH03/session-problem.png)
*세션 불일치 - 서버 1에 저장된 세션이 서버 2에는 없어 요청이 실패*

이러한 세션 불일치 문제는 Redis로 해결합니다.

Redis는 여러 서버가 함께 사용하는 **공용 사물함**과 같습니다. 서버 1이 사물함에 데이터를 넣어두면 서버 2도 같은 사물함을 열어 그 데이터를 꺼낼 수 있습니다. 어떤 서버가 요청을 처리하든 동일한 데이터에 접근할 수 있습니다.

> **레디스(Redis)**: 메모리 기반의 데이터베이스로, 관계형 데이터베이스가 아닌 키-값(Key-Value) 구조로 데이터를 저장합니다. 디스크가 아닌 메모리에 저장하기 때문에 속도가 매우 빨라 데이터 캐싱, 세션 저장 등 고성능 처리가 필요한 곳에 주로 사용됩니다.

 서버 1이 세션 정보를 자신의 메모리가 아닌 외부 저장소인 Redis에 기록하는 방식입니다. 이렇게 하면 이후 요청이 서버 2로 전달되더라도, 서버 2가 Redis를 확인해 동일한 세션 정보를 읽어올 수 있습니다. 어떤 서버로 요청이 가든 문제없이 로그인이 유지됩니다.

![](../assets/CH03/session-redis.png)
*Redis로 해결 - 세션을 공유 저장소에 보관하여 어떤 서버에서든 조회 가능*

서버 자체에 세션을 저장하는 방식은 서버 대수가 늘어날수록 관리가 매우 까다로워집니다. 하지만 Redis를 사용하면 세션을 한 곳에서 통합 관리합니다. 덕분에 서버를 무수히 늘리는 확장 단계에서도 세션 공유 문제를 완벽하게 해결합니다.

### 3.3.2 Redis : 실습

아래 Github 주소를 참고합니다.

> 실습 코드는 https://github.com/metacoding-10-linux-docker/docker/tree/master/ex04 에서 확인할 수 있습니다.

Dockerfile은 파이썬 이미지 기반으로 Redis 패키지를 함께 설치하고 로컬에 있는 app.py를 컨테이너 내부에서 실행합니다. 

**[참고]** `api/Dockerfile`

**ex04/api/Dockerfile**
```dockerfile
FROM python:3.10-alpine                          # Python 3.10 경량 이미지 사용
WORKDIR /app                                     # 작업 경로를 /app으로 설정
COPY app.py .                                    # app.py를 컨테이너의 /app으로 복사
RUN pip install flask && pip install redis       # Flask + Redis 패키지 설치
CMD ["python", "app.py"]                         # Flask 서버 실행
```

`app.py`는 Redis에 데이터를 저장하고 조회하는 API 서버입니다. 전체 코드는 GitHub 레포에서 확인할 수 있습니다.

| 파일 | URL | 기능 |
|------|-----|------|
| `app.py` | `/save` | Redis에 값을 저장 |
| `app.py` | `/read` | Redis에서 값을 조회 |

3.2에서는 컨테이너끼리 통신하려면 `host.docker.internal`로 호스트를 경유해야 했습니다. 

하지만 챕터 2에서 배운 **사용자 정의 네트워크**로 컨테이너를 묶으면 컨테이너 이름만으로 직접 통신할 수 있습니다.

**[실습]** EX04 폴더로 이동 후, 네트워크를 생성하고 Redis, API 컨테이너를 실행합니다.

```bash
# 네트워크 만들기
docker network create myNetwork                                     # 사용자 정의 네트워크 myNetwork 생성
 
# redis 앱 빌드 및 실행
docker run -d --name redis --network myNetwork -p 6379:6379 redis   # Redis 컨테이너 실행, myNetwork 네트워크로 연결

# api 실행
docker build -t api ./api                                           # API 이미지 빌드
docker run -d --name api1 --network myNetwork -p 5001:5000 api      # API 서버 1 실행 (5001번 포트), myNetwork 네트워크로 연결
docker run -d --name api2 --network myNetwork -p 5002:5000 api      # API 서버 2 실행 (5002번 포트), myNetwork 네트워크로 연결
```

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

API 1에서 저장한 데이터를 API 2에서도 동일하게 조회합니다. Redis 덕분에 서버가 늘어나도 세션이 끊기지 않고 안정적으로 사용할 수 있습니다.

## 3.4 MySQL : DB 서버 구축

Redis로 세션 데이터를 관리하는 방법을 배웠습니다. Redis는 메모리 기반이라 데이터가 영구히 보관되지 않습니다. 회원 정보, 게시글, 주문 내역처럼 반드시 보관해야 하는 데이터는 어떻게 저장해야 할까요? 

이때 필요한 것이 DB 서버입니다.

### 3.4.1 MySQL : 컨테이너로 DB 서버 생성

> 실습 코드는 https://github.com/metacoding-10-linux-docker/docker/tree/master/ex05 에서 확인할 수 있습니다.

**[EX05 패키지 구조]**

```
ex05/
└── db/                  # MySQL 데이터베이스
    ├── Dockerfile
    └── init.sql         # 초기 테이블 및 데이터 생성 SQL
```

| 파일 | 역할 |
|------|------|
| `Dockerfile` | MySQL 이미지 기반으로 환경변수와 초기화 SQL을 설정 |
| `init.sql` | 컨테이너 최초 실행 시 테이블 생성 및 초기 데이터 삽입 |

> 전체 코드는 GitHub 레포에서 확인할 수 있습니다.

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


## 3.5 Docker Compose : 여러 컨테이너를 한 번에

### 3.5.1 Docker Compose : 왜 필요한가

지금까지의 과정을 되돌아보겠습니다. NGINX와 앱 서버 2개만 운영하려 해도 각 Dockerfile마다 이미지를 빌드하고, 컨테이너를 하나씩 실행하며 네트워크까지 직접 만들어야 했습니다. 컨테이너 개수가 늘어날수록 관리해야 할 명령어는 걷잡을 수 없이 많아집니다. 이 모든 과정을 매번 수동으로 입력하는 방식은 현실적으로 매우 어렵습니다.

![](../assets/CH03/chap02-48.png)
*기존 방식 — Dockerfile 개별 빌드 및 실행*


Docker Compose는 바로 이 번거로움을 해결해 주는 도구입니다.

Docker Compose는 **'오케스트라의 악보'**와 같습니다. 각 악기(컨테이너)의 역할은 모두 다르지만, 하나의 악보가 있으면 모든 연주자가 동시에 연주를 시작할 수 있는 것과 같은 원리입니다.

> **도커 컴포즈(Docker Compose)**: 여러 개의 컨테이너를 하나의 환경으로 묶어 설정하고, 명령어 한 줄로 한꺼번에 관리할 수 있게 도와주는 도구입니다.

Docker Compose 스크립트에 이미지 관리 작업을 정의하면 `docker compose up` 명령 한 번으로 여러 이미지를 동시에 실행하고 필요한 환경을 자동으로 구성할 수 있습니다.

![](../assets/CH03/chap02-49.png)
*Docker Compose 방식 — 한 번에 생성 및 연결*


Compose가 해결하는 것은 세 가지입니다.

**순서 :** 어떤 컨테이너를 먼저 띄울지 `depends_on`으로 지정할 수 있습니다. 단, 컨테이너가 시작되었다고 해서 내부 서비스가 바로 준비된 것은 아닙니다. 

**네트워크 :** 같은 Compose 파일에 정의된 컨테이너는 자동으로 하나의 네트워크에 묶입니다. `docker network create`를 직접 실행할 필요가 없습니다. 컨테이너끼리 서비스 이름으로 통신할 수 있습니다.

**일괄 관리 :** `docker compose up` 한 줄이면 모든 컨테이너가 시작됩니다. `docker compose down` 한 줄이면 모든 컨테이너와 네트워크가 정리됩니다.

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

> EX06의 각 Dockerfile은 EX01과 동일한 구조입니다.

3.2에서는 컨테이너를 개별 실행했기 때문에 `host.docker.internal`로 호스트를 경유해야 했고, 3.3에서는 사용자 정의 네트워크를 직접 만들어서 컨테이너 이름으로 통신했습니다. 

Docker Compose는 `networks`에 선언된 서비스들을 하나의 네트워크로 자동으로 묶어줍니다. 그래서 nginx.conf의 upstream 주소가 `app1:80`, `app2:80`처럼 서비스 이름으로도 통신이 가능합니다.

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

이번에는 챕터 3에서 배운 내용을 바탕으로 프론트 서버에서 발생한 요청이 백엔드 서버로 전달되고 DB 서버에서 데이터를 조회해 응답하는 웹사이트를 만들어보겠습니다.

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

### 3.6.2 MySQL : DB 서버 만들기

DB 서버는 3.4와 동일한 구조입니다.

**[참고]** `db/Dockerfile`

**ex07/db/Dockerfile**
```dockerfile
FROM mysql                                    # MySQL 이미지사용
COPY init.sql /docker-entrypoint-initdb.d     # 로컬의 init.sql을 MySQL 초기화 폴더로 복사
ENV MYSQL_USER=metacoding                     # 생성할 사용자 이름
ENV MYSQL_PASSWORD=metacoding1234             # 사용자 비밀번호
ENV MYSQL_ROOT_PASSWORD=root1234              # root 비밀번호
ENV MYSQL_DATABASE=metadb                     # 생성할 데이터베이스 이름
CMD ["--character-set-server=utf8mb4", "--collation-server=utf8mb4_unicode_ci"]  # 한글 인코딩 설정
```

### 3.6.3 Spring Boot : 백엔드 서버

backend 폴더에는 **entrypoint.sh** 파일이 있습니다.

**entrypoint.sh** 는 컨테이너가 시작될 때 자동으로 실행되는 스크립트입니다. 소스 코드 빌드나 서버 가동처럼 컨테이너가 켜지자마자 수행해야 할 작업들을 순서대로 적어둡니다.

Dockerfile와 차이점은 다음과 같습니다.

> **Dockerfile:** 이미지를 **생성(Build)** 하는 단계에서 사용하며, 환경을 구축하기 위해 딱 한 번 실행합니다.
> **entrypoint.sh:** 컨테이너가 **실행(Run)** 되는 시점에 작동하며, 컨테이너를 켤 때마다 매번 실행합니다.

**entrypoint.sh**는 다음과 같습니다.

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

스프링 서버 안에는 다음 API가 있습니다.

| 클래스 | URL | 기능 |
|--------|-----|------|
| `UserController` | `/api/users` | 요청하면 회원 정보 응답 |

Dockerfile은 Java 환경을 준비하고, 컨테이너가 시작되면 `entrypoint.sh`를 실행합니다.

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
    environment:              # DB 연결을 위한 환경변수
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


브라우저에서 `localhost:80`에 접속하면 사용자 목록이 조회됩니다. init.sql에서 입력한 ssar, cos 데이터가 표시됩니다.

> 데이터가 보이지 않으면 백엔드 서버 빌드가 아직 진행 중일 수 있습니다. 잠시 기다린 후 새로고침하면 정상 동작합니다.

<!-- image-prompt: Browser showing a user list table with two rows: ID 1 ssar and ID 2 cos -->

![](../assets/CH03/chap02-58.png)
*사용자 목록 조회 성공*

페이지에 접속하면 백엔드가 DB에서 데이터를 가져옵니다. `docker compose up` 한 줄로 프론트엔드, 백엔드, DB가 연동되는 웹사이트가 올라갔습니다.

실습이 끝나면 다음 명령어로 정리합니다.

## 이것만은 기억하자

- **Dockerfile**에 환경을 한 번 정의하면 어디서든 동일한 컨테이너를 만들 수 있습니다.
- **NGINX**는 URL 경로에 따라 요청을 분기하고, 여러 서버에 트래픽을 분산하며, 정적 파일을 캐싱합니다.
- **Docker Compose**는 여러 컨테이너를 하나의 파일에 정의하고 명령어 한 줄로 실행합니다. Redis로 세션을 공유하고 MySQL로 데이터를 저장할 수 있습니다.

웹사이트까지 완성했습니다. 하지만 이 구성에는 한 가지 약점이 있습니다. 컨테이너가 에러로 멈추거나 서버가 재부팅되면 서비스가 그대로 중단됩니다. 누군가 직접 `docker compose up`을 다시 실행하기 전까지는 복구되지 않습니다.

컨테이너가 죽으면 알아서 다시 살려주는 시스템은 없을까요?

