# Ch.3 Docker 다루기

며칠 뒤, 팀 회의에서 새 프로젝트 이야기가 나왔습니다. 사내용 웹 서비스를 하나 만들어야 했습니다. 프론트엔드가 있고, 백엔드가 있고, 데이터를 담을 DB도 필요했습니다. 팀장이 오픈이를 봤습니다.

**팀장**: "환경 구성은 Docker로 해. 네가 이번에 공부했잖아."

오픈이는 고개를 끄덕이면서도 머릿속이 복잡해졌습니다. 챕터 2에서 컨테이너를 띄우고 이미지를 만드는 것까지는 해봤습니다. 그런데 실제 서비스를 구성하려면 앱 하나만 띄워서는 안 됩니다. 프론트엔드, 백엔드, DB가 각각 컨테이너로 떠서 서로 맞물려야 했습니다.

퇴근 후 노트북을 열었습니다. 프로젝트에 필요한 것들을 하나씩 Docker로 세워보기로 했습니다.

## 3.1 Dockerfile — 환경을 자동으로 만들기

### 3.1.1 매번 수동으로 깔기는 지친다

가장 먼저 떠오른 건 그 과정이었습니다. 컨테이너에 들어가 `apt update`를 치고 vim을 깔고 index.html을 만든 뒤 `docker commit`으로 이미지를 남겼던 것. 한 번은 재미있었죠. 두 번째는 손이 무거웠습니다.

*'프로젝트 세팅할 때마다 이걸 반복해야 돼?'*

패키지명을 한 글자만 잘못 치면 처음부터 다시였습니다. 설정을 살짝 고치면 전 과정을 처음부터 반복해야 했습니다. 프로젝트를 본격적으로 세우기 전에, 이 수동 작업부터 자동화해야 했습니다.

![](../assets/CH03/chap02-provisioning.png)

*그림 3-1 수동 세팅과 Dockerfile 자동화 비교*

요리 레시피 카드랑 비슷합니다. 재료와 순서만 적어두면 누가 만들어도 같은 맛이 나죠. **Dockerfile**이 그 레시피입니다.

> **참고: Dockerfile**
> 컨테이너가 실행될 때 필요한 환경을 자동으로 구성해 주는 이미지를 만들기 위한 스크립트입니다. 베이스 이미지, 설치할 패키지, 복사할 파일, 실행할 명령을 순서대로 적어둡니다.

### 3.1.2 Dockerfile에서 컨테이너까지의 세 단계

Dockerfile에서 컨테이너가 실제로 뜨기까지는 세 단계를 거칩니다.

![](../assets/CH03/chap02-1.png)

*그림 3-2 Dockerfile → 이미지 → 컨테이너의 세 단계*

1. **Dockerfile 작성**: 환경 구성을 텍스트 파일에 적습니다.
2. **docker build**: Docker 엔진이 Dockerfile을 위에서 아래로 읽으며 각 줄을 실행합니다. 결과물이 **이미지**로 저장됩니다.
3. **docker run**: 이미지를 기반으로 **컨테이너**를 실행합니다.

컨테이너를 지워도 이미지는 남으니, 같은 환경을 언제든 다시 띄울 수 있습니다. 어제 수동 commit으로 만든 이미지의 자리를, 이제는 Dockerfile이 자동으로 채워줍니다.

### 3.1.3 Dockerfile 기본 문법

자주 쓰는 지시어는 이 정도입니다.

| 지시어 | 역할 |
|--------|------|
| `FROM` | 베이스 이미지 |
| `WORKDIR` | 작업 디렉토리 지정 |
| `COPY` | 호스트 파일을 컨테이너로 복사 |
| `RUN` | 이미지 빌드 시 실행할 리눅스 명령 (패키지 설치 등) |
| `ENV` | 환경 변수 |
| `CMD` | 컨테이너 시작 시 실행되는 기본 명령 |
| `ENTRYPOINT` | 컨테이너 시작 시 반드시 실행되는 메인 프로세스 |

첫 실습으로 Ubuntu 기반에 vim이 깔린 이미지를 Dockerfile로 만들어봤습니다.

```dockerfile
# Dockerfile
FROM ubuntu:24.04                      # 베이스 이미지
RUN apt update && apt install -y vim   # vim 패키지 설치
CMD ["/bin/bash"]                      # 컨테이너 시작 시 bash 실행
```

같은 폴더에서 빌드 명령을 쳤습니다.

```bash
docker build -t ubuntu-vim .   # . 은 현재 폴더의 Dockerfile을 읽겠다는 뜻
```

![](../assets/CH03/chap02-7.png)

*그림 3-3 docker build 실행 결과*

빌드 로그가 한 줄씩 올라가더니 이미지가 완성됐습니다. 컨테이너를 띄우자 별도 설치 명령 없이 vim이 바로 열렸습니다.

![](../assets/CH03/chap02-10.png)

*그림 3-4 vim이 이미 설치된 상태로 컨테이너 실행*

어제 "컨테이너 들어가 → apt update → apt install → exit → commit"로 다섯 번 손을 움직이던 작업이, **파일 한 장에 한 줄 명령**으로 줄었습니다.

그런데 패키지만 깔았지 아직 프로젝트 파일은 컨테이너 안에 없었습니다. **WORKDIR**와 **COPY**를 얹으면 호스트의 파일을 컨테이너 안으로 끌어올 수 있습니다. WORKDIR는 이후 명령이 실행될 기본 폴더를 지정하고, COPY는 호스트의 파일을 컨테이너 내부로 옮겨 놓습니다.

오픈이는 Dockerfile이 있는 폴더 안에 **index.html** 파일을 하나 만들어뒀습니다. 내용은 비어 있어도 상관없었습니다.

![](../assets/CH03/chap02-11.png)

*그림 3-5 폴더 및 파일 구조*

그리고 Dockerfile에 WORKDIR와 COPY를 얹었습니다. 작업 디렉토리를 `/app`으로 지정하고, 로컬의 `index.html`을 컨테이너의 같은 경로로 복사하도록 했습니다.

```dockerfile
FROM ubuntu:24.04                      # 베이스 이미지
WORKDIR /app                           # 작업 경로를 /app으로 설정
COPY ./index.html ./index.html         # 로컬의 index.html을 컨테이너의 /app으로 복사
RUN apt update && apt install -y vim   # vim 패키지 설치
CMD ["/bin/bash"]                      # 컨테이너가 시작될 때 자동으로 실행할 명령
```

WORKDIR 덕에 컨테이너 기본 경로가 `/app`이 되고, COPY가 그 안에 `index.html`을 꽂아 넣습니다.

새 이미지로 빌드하고 바로 띄워봤습니다.

```bash
docker build -t ubuntu-html .    # . 은 현재 경로를 기준으로 Dockerfile을 읽어옴
docker run -it ubuntu-html       # ubuntu-html 이미지로 컨테이너 실행
ls
```

![](../assets/CH03/chap02-13.png)

*그림 3-6 실행 결과 확인*

터미널이 `/app`으로 떨어지고, 그 안에 `index.html`이 그대로 들어 있었습니다. 확인이 끝난 뒤 `exit`으로 컨테이너에서 빠져나왔습니다.

### 3.1.4 CMD와 ENTRYPOINT

CMD와 ENTRYPOINT는 컨테이너가 시작될 때 무엇을 실행할지 정합니다. 성격은 조금 다릅니다. 식당에 비유하면 **CMD는 기본 메뉴**, **ENTRYPOINT는 수저와 물**입니다. 기본 메뉴는 손님이 다른 걸 시키면 바뀝니다. 수저와 물은 어떤 주문에도 반드시 깔립니다.

> **참고: CMD와 ENTRYPOINT**
> - **CMD**: 컨테이너가 시작될 때 실행할 **기본 명령**입니다. `docker run` 뒤에 다른 명령을 주면 덮어씁니다.
> - **ENTRYPOINT**: 컨테이너가 시작될 때 **반드시 실행되어야 하는 메인 프로세스**입니다. 외부 옵션과 상관없이 고정됩니다.
> - 둘을 같이 쓰면 `ENTRYPOINT` + `CMD` 순으로 합쳐져 실행됩니다. ENTRYPOINT는 골격, CMD는 인자로 쓰는 방식입니다.

실제 동작을 눈으로 보려고 오픈이는 Dockerfile에 ENTRYPOINT를 한 줄 더 얹었습니다. echo로 메시지를 출력하는 간단한 구성이었습니다.

```dockerfile
FROM ubuntu:24.04                      # 베이스 이미지
WORKDIR /app                           # 작업 경로를 /app으로 설정
COPY ./index.html ./index.html         # 로컬의 index.html을 컨테이너의 /app으로 복사
RUN apt update && apt install -y vim   # vim 패키지 설치
CMD ["/bin/bash"]                      # ENTRYPOINT 뒤에 붙어서 실행됨
ENTRYPOINT ["echo", "컨테이너 실행"]     # 컨테이너 시작 시 실행되는 명령
```

ENTRYPOINT와 CMD가 함께 있으면 둘은 하나로 합쳐져 실행됩니다. 새 이미지로 빌드해서 바로 띄워봤습니다.

```bash
docker build -t ubuntu-entry .         # 이미지 생성
docker run -it ubuntu-entry            # 컨테이너 실행
```

![](../assets/CH03/chap02-15.png)

*그림 3-7 ENTRYPOINT 실행 결과*

결과 화면에 **컨테이너 실행 /bin/bash**라는 문자열이 찍히고 프로세스가 즉시 종료됐습니다. ENTRYPOINT가 있으면 CMD는 독립적으로 실행되지 않고 뒤에 인자로 붙어 `echo "컨테이너 실행" /bin/bash`가 된 셈입니다. `echo`는 뒤에 오는 내용을 그대로 출력하고 끝나는 명령이라, 그 글자만 화면에 찍고 메인 프로세스가 끝나니 컨테이너도 함께 꺼졌습니다.

같은 조합은 실제 앱 이미지에도 그대로 쓸 수 있습니다. ENTRYPOINT에 "런타임 실행"을 고정하고, CMD에 "실행할 파일명"만 바꿔 끼우면 같은 이미지를 여러 용도로 재활용할 수 있습니다.

*'수동으로 치던 한 시간짜리 설정이 파일 한 장에 담겼네.'*

이미지를 자동으로 만드는 방법은 갖춰졌습니다. 이제 프로젝트에 필요한 것들을 하나씩 세울 차례였습니다. 프론트엔드와 백엔드가 따로 있는 구조에서, 사용자의 요청을 받아 알맞은 서버로 보내주는 앞단이 필요했습니다.

## 3.2 NGINX — 요청을 앞에서 받아 나눠주기

### 3.2.1 왜 서버 앞에 NGINX를 둘까

프로젝트 구조를 그려보니 앱이 하나가 아니었습니다. 프론트엔드 서버, 백엔드 서버가 따로 떠야 했고, 사용자는 하나의 주소로 접속합니다. 그 주소 뒤에서 요청을 받아 알맞은 서버로 나눠주는 창구가 필요했습니다.

**팀장**: "서버 앞에 하나 두는 거야. 다 이렇게 쓴다."

그 창구 역할을 하는 것이 **NGINX**입니다.

![](../assets/CH03/chap02-17.png)

*그림 3-8 NGINX가 앞에서 요청을 받아 뒤의 서버들로 전달*

NGINX는 웹 서버이자 요청을 중계하는 **리버스 프록시**입니다. 사용자의 요청을 NGINX가 중간에서 받아 뒤쪽 서버로 넘기고, 응답도 NGINX가 받아 사용자에게 돌려줍니다. 실제 서버 주소를 바깥에 노출하지 않아 보안에도 좋습니다. 요청을 여러 서버로 나눠주는 **로드밸런싱**까지 됩니다. 오늘 풀스택 구성에서 앱 앞에 꼭 서 있어야 할 요소입니다.

> **참고: 프록시 / 리버스 프록시 / 로드밸런싱**
> - **프록시**: 클라이언트 대신 요청을 전달하는 중간자입니다. 방향은 "내부 → 외부"입니다.
> - **리버스 프록시**: 반대편 서버 쪽에서 외부 요청을 받아 내부 서버로 전달합니다. 방향은 "외부 → 내부"이며, NGINX가 맡는 역할이 이쪽입니다.
> - **로드밸런싱**: 여러 서버에 요청을 골고루 나눠주는 방식입니다. 뒤에서 설명합니다.

### 3.2.2 NGINX 기본 문법 세 가지

NGINX 설정 파일(`nginx.conf`)은 세 가지 지시어로 돌아갑니다. 배달 앱 주문 흐름을 떠올리면 쉽습니다.

- **upstream** — 요청을 실제로 처리할 서버 그룹에 이름을 붙이는 곳. "A식당"이라는 간판을 다는 단계.
- **location** — 어떤 URL 경로로 들어온 요청을 잡을지 정하는 곳. "짜장면 주문이 들어오면"이라는 조건.
- **proxy_pass** — 그 요청을 어느 upstream으로 보낼지 지정하는 곳. "A식당으로 배달"이라는 전달 지시.

세 지시어가 어떻게 맞물리는지 개념만 먼저 보이면 이렇습니다.

```nginx
# 개념 소개용 발췌
upstream backend {                           # backend라는 이름으로 서버 그룹 등록
    server host.docker.internal:8080;        # 그룹에 속한 실제 서버 주소
}

server {
    listen 80;                               # 80번 포트로 들어오는 요청 대기
    server_name localhost;

    location / {                             # 모든 경로(/) 요청에 대해
        proxy_pass http://backend;           # backend로 넘김
    }
}
```

이 뼈대 위에 옵션을 얹는 형태로 다양한 패턴이 나옵니다. 이번 절에서는 세 가지를 차례로 봅니다. **경로 기반 라우팅, 로드밸런싱, 캐싱**입니다.

### 3.2.3 실습 ① 경로 기반 라우팅

URL 경로별로 서로 다른 서버로 요청을 보내는 경우입니다. `/app1`은 1번 서버, `/app2`는 2번 서버로 갑니다. 회원 API와 상품 API가 각자 다른 컨테이너로 나뉘어 있을 때 앞단에서 이렇게 갈라줍니다.

![](../assets/CH03/chap02-18.png)

*그림 3-9 경로 기반 라우팅 구조*

> 실습 코드: https://github.com/metacoding-10-linux-docker/docker/tree/master/ex01

폴더 구조는 이렇습니다. 세 컨테이너(app1, app2, lb)가 각자의 Dockerfile로 이미지가 되고, 개별 컨테이너로 실행됩니다.

```
ex01/
├── app1/         # 첫 번째 웹 서버 (nginx + index.html)
├── app2/         # 두 번째 웹 서버 (nginx + index.html)
└── lb/           # 로드밸런서 (NGINX + nginx.conf)
```

lb의 `nginx.conf`가 이번 실습의 핵심입니다.

**ex01/lb/nginx.conf**
```nginx
upstream app1 {
    server host.docker.internal:8000;     # 호스트의 8000번 포트 = app1 컨테이너
}

upstream app2 {
    server host.docker.internal:9000;     # 호스트의 9000번 포트 = app2 컨테이너
}

server {
    listen 80;
    server_name localhost;

    location /app1 {                      # /app1 요청은
        proxy_pass http://app1/;          # app1 upstream으로
    }

    location /app2 {                      # /app2 요청은
        proxy_pass http://app2/;          # app2 upstream으로
    }
}
```

세 컨테이너를 띄웁니다.

```bash
docker build -t app1 ./app1 && docker run -dit -p 8000:80 app1
docker build -t app2 ./app2 && docker run -dit -p 9000:80 app2
docker build -t lb ./lb && docker run -dit -p 80:80 lb
```

> Linux에서 실행한다면 `lb`를 띄울 때 `--add-host=host.docker.internal:host-gateway` 옵션을 덧붙여야 컨테이너 안에서 `host.docker.internal`이 해석됩니다. Windows/macOS용 Docker Desktop에서는 기본 해석됩니다.

브라우저에서 `localhost:80/app1`로 들어가니 app1 서버가, `/app2`로 들어가니 app2 서버가 응답했습니다.

![](../assets/CH03/chap02-21.png)

*그림 3-10 /app1 경로로 접속한 결과*

![](../assets/CH03/chap02-22.png)

*그림 3-11 /app2 경로로 접속한 결과*

URL 경로만 달라졌는데 서로 다른 서버가 응답했습니다. `location`이 요청을 잡고, `proxy_pass`가 해당 `upstream`으로 넘긴 결과입니다.

*'포트 두 개가 경로 하나로 묶이네.'*

#### host.docker.internal이 왜 필요했나

`nginx.conf`에서 오픈이 눈에 걸리는 지점이 하나 있었습니다. `host.docker.internal:8000`이라는 주소입니다. lb 컨테이너가 app1 컨테이너를 곧장 부르지 않고 **호스트 PC를 한 번 경유하는** 구조였습니다.

![](../assets/CH03/ex01-lb-to-host.png)

*그림 3-12 lb 컨테이너 → 호스트 PC → app1 컨테이너로 가는 우회 경로*

이유는 챕터 2.5.4에서 예고한 그 지점이었습니다. 세 컨테이너를 `docker run`으로 **각각 따로** 실행했기 때문에 기본 bridge 네트워크로 들어갔고, 거기서는 컨테이너 이름으로 서로를 부를 수 없습니다. 그래서 "lb → 호스트 포트 → app1"로 호스트를 한 번 거쳐 갔습니다.

> **참고: host.docker.internal**
> 컨테이너 내부에서 "호스트 PC"를 가리키는 특수 주소입니다. 컨테이너 안에서 `localhost`는 컨테이너 자기 자신을 가리키기 때문에, 호스트 PC에 접근하려면 이 이름을 써야 합니다. Linux에서는 기본 해석되지 않아 `--add-host=host.docker.internal:host-gateway` 옵션이 필요합니다.

이 우회가 번거롭다는 인상이 남았다면, **3.3**에서 사용자 정의 네트워크로 깨끗하게 치우게 됩니다.

### 3.2.4 실습 ② 로드밸런싱

이번엔 같은 서비스를 **여러 대로 복제**해서 NGINX가 요청을 번갈아 뿌려주는 구조입니다. 놀이공원 매표소 창구 두 곳이 손님을 번갈아 받는 방식입니다. **라운드 로빈**이라고 부릅니다. 앱도 사용자가 늘어나면 복제해야 하니 꼭 익혀둘 포인트입니다.

![](../assets/CH03/chap02-23.png)

*그림 3-13 라운드 로빈 로드밸런싱 구조*

> 실습 코드: https://github.com/metacoding-10-linux-docker/docker/tree/master/ex02

EX01과 달라지는 부분은 세 곳입니다. **app2 폴더가 사라지고**, `nginx.conf`의 `upstream app1` 블록에 `server` 줄이 두 개로 늘어나고, `upstream app2` 블록과 `location /app2` 블록이 통째로 빠집니다.

**ex02/lb/nginx.conf** (달라진 블록)
```nginx
upstream app1 {
    server host.docker.internal:8000;     # 첫 번째 서버
    server host.docker.internal:8001;     # 같은 그룹에 두 번째 서버 추가
}

server {
    listen 80;
    location /app1 {
        proxy_pass http://app1/;          # 자동으로 두 서버에 번갈아 분배 (라운드 로빈)
    }
}
```

같은 이미지로 컨테이너를 두 번 띄웁니다. 포트만 다르게 합니다.

```bash
docker build -t app1 ./app1
docker run -dit -p 8000:80 app1   # 서버 1
docker run -dit -p 8001:80 app1   # 서버 2 (같은 이미지, 다른 포트)

docker build -t lb ./lb
docker run -dit -p 80:80 lb
```

브라우저로 `localhost:80/app1`을 새로고침해도 응답 HTML 자체는 똑같았습니다. 두 컨테이너가 같은 이미지에서 올라와 같은 `index.html`을 돌려주기 때문입니다. 대신 각 컨테이너의 access 로그(`docker logs <컨테이너>`)를 보면 새로고침마다 8000번 컨테이너와 8001번 컨테이너로 요청이 번갈아 들어간 것이 확인됩니다.

![](../assets/CH03/chap02-26.png)

*그림 3-14 8000 포트 컨테이너 로그에 찍힌 요청*

![](../assets/CH03/chap02-27.png)

*그림 3-15 8001 포트 컨테이너 로그에 찍힌 요청*

`server` 한 줄 추가했을 뿐인데 NGINX가 트래픽을 두 대에 나눠 보냈습니다. 별도 설정 없이 기본값이 라운드 로빈입니다.

*'줄 하나로 서버 두 대가 엮인다.'*

### 3.2.5 실습 ③ 캐싱

같은 파일이 초당 수백 번 요청되는 상황이라면, 이미지 한 장을 백엔드가 매번 응답하는 건 낭비입니다. 자주 꺼내 입는 옷을 옷걸이에 미리 걸어두는 것처럼, 자주 요청되는 파일을 **NGINX 앞단에 잠시 보관**해두는 겁니다. 이 저장 과정을 **캐싱**이라고 부릅니다.

캐싱 결과를 확인할 때 두 가지 상태가 번갈아 나옵니다. **MISS**는 캐시에 저장된 파일이 없어 백엔드까지 요청이 갔다 온 상태, **HIT**은 캐시에 이미 있는 파일을 백엔드 접근 없이 바로 돌려준 상태입니다.

![](../assets/CH03/cache-miss.png)

*그림 3-16 첫 번째 요청 (MISS) — 캐시가 비어있어 백엔드까지 요청 후 응답을 캐시에 저장*

![](../assets/CH03/cache-hit.png)

*그림 3-17 두 번째 요청 (HIT) — 캐시에 저장된 응답을 바로 반환, 백엔드 접근 없음*

> 실습 코드: https://github.com/metacoding-10-linux-docker/docker/tree/master/ex03

이번 실습은 뒤쪽 서버가 HTML만 주던 EX01과 달리, 이미지 파일까지 응답하는 **Flask 기반 API 서버**로 구성됩니다. 초점은 `nginx.conf`의 캐시 설정입니다.

```
ex03/
├── api/                 # 백엔드 (Flask)
│   ├── app.py
│   ├── Dockerfile
│   └── image.png
└── nginx/               # NGINX (캐싱 + 프록시)
    ├── Dockerfile
    └── nginx.conf
```

앞의 두 예제와 달라지는 지시어는 두 개입니다. 파일 최상단의 `proxy_cache_path`와 `location` 안의 `proxy_cache`.

**ex03/nginx/nginx.conf**
```nginx
# 캐시 저장 경로와 메모리 공간 이름을 선언 (http{} 블록 내부에 위치)
proxy_cache_path /var/cache/nginx keys_zone=my_cache:10m;

server {
    listen 80;

    location / {
        proxy_pass http://host.docker.internal:5000;
        proxy_cache off;                              # 이 경로는 캐시 끔
    }

    location = /image.png {                           # /image.png 요청만
        proxy_pass http://host.docker.internal:5000;
        proxy_cache my_cache;                         # 위에서 선언한 캐시 사용
        proxy_cache_valid 200 1m;                     # 200 응답을 1분 동안 보관
        add_header X-Cache-Status $upstream_cache_status always;  # 응답 헤더에 HIT/MISS 표시
        proxy_ignore_headers Cache-Control Expires;   # 백엔드가 보낸 캐시 제어 헤더 무시
    }
}
```

포인트는 두 가지입니다. `proxy_cache_path`로 **어디에 얼마만큼 보관할지**를 선언해 두고, `location`마다 `proxy_cache`로 **이 경로에서 그 캐시를 쓸지 말지**를 결정합니다. EX01/EX02의 뼈대(`upstream` / `location` / `proxy_pass`)는 그대로 살아 있고, 그 위에 캐시 관련 줄이 얹힌 모양입니다.

```bash
# api 서버 실행 (Flask — 5000번 포트)
docker build -t api ./api
docker run -dit -p 5000:5000 api

# nginx 실행
docker build -t nginx-cache ./nginx
docker run -dit -p 80:80 nginx-cache
```

`localhost:80/image.png`로 요청하면 이미지가 응답됩니다.

![](../assets/CH03/chap02-32.png)

*그림 3-18 캐싱 실습 — 이미지 응답*

브라우저의 **F12 > Network > Headers** 탭을 열고, 브라우저 자체 캐시가 결과를 흐리지 않도록 Disable cache를 체크했습니다. Response Headers의 `X-Cache-Status` 값이 처음엔 `MISS`였습니다. 캐시에 데이터가 없어 원본 서버까지 다녀온 상태입니다.

![](../assets/CH03/chap02-33.png)

*그림 3-19 X-Cache-Status: MISS 확인*

새로고침을 한 번 더 하니 `HIT`으로 바뀌었습니다. 캐시에 저장된 파일을 서버 요청 없이 바로 돌려준 겁니다.

*'어, 진짜 HIT이 떴네.'*

![](../assets/CH03/chap02-34.png)

*그림 3-20 X-Cache-Status: HIT 확인*

세 예제를 돌려보니 `nginx.conf`의 뼈대는 늘 같았습니다. upstream, server, 캐시 옵션 중 어디를 건드렸느냐만 달랐습니다. 프로젝트에 들어갈 NGINX도 이 중에서 필요한 옵션만 골라 쓰면 됩니다.

서버를 여러 대 돌리는 것까지는 됐습니다. 그런데 서버를 두 대로 복제하면 로그인이 풀리진 않을까. 갑자기 그 생각이 들었습니다.

## 3.3 Redis — 서버가 여러 대일 때 세션은 어디에

### 3.3.1 서버 여러 대면 생기는 세션 문제

로드밸런싱으로 서버를 여러 대 돌리면 편해 보이지만, 복제 자체가 새 문제를 만드는 경우가 있습니다. 사용자가 로그인하고 장바구니에 상품을 담은 뒤 결제 페이지로 넘어갔을 때 로그인이 풀리는 증상입니다. 내부에 로그인 기능이 있는 앱이라면 이 문제를 피해 갈 수 없습니다.

원인은 이렇습니다. 많은 백엔드 프레임워크가 로그인 상태를 **서버 메모리**에 보관합니다. 이 정보를 **세션**이라고 부릅니다. 서버가 한 대일 때는 같은 서버가 받은 요청이니 같은 메모리에서 읽으면 됩니다. 그런데 서버가 두 대로 갈라지는 순간, 각 서버의 메모리는 서로의 세션을 모르는 **별개의 공간**이 됩니다. 로그인 요청은 1번 서버 메모리에 세션을 남기고, 다음 결제 요청이 2번 서버로 넘어가면 2번 서버 메모리엔 세션이 없습니다.

![](../assets/CH03/session-problem.png)

*그림 3-21 세션 불일치 — 1번 서버에 저장된 세션이 2번 서버엔 없어 로그인 풀림*

*'서버 늘리면 해결되는 줄 알았더니, 늘릴수록 로그인이 풀린다고?'*

> **참고: 세션(Session)**
> 사용자가 로그인했을 때 서버가 생성하는 임시 기록입니다. "이 사용자는 인증되었습니다"라는 정보를 서버가 보관하고, 이후 요청이 올 때마다 이 기록을 확인해 로그인 상태를 유지합니다.

### 3.3.2 Redis는 서버들이 공유하는 사물함

**세션을 서버 메모리 대신, 서버들 바깥의 공용 저장소에 두면** 됩니다.

**선배**: "각자 서랍에 넣지 말고 공용 사물함에 넣으라고 하면 되잖아."

회사에서 각자 개인 서랍에 물건을 넣으면 내 서랍은 나만 씁니다. 공용 사물함에 넣으면 같은 사물함 번호를 아는 사람은 누구나 꺼낼 수 있습니다. 이 공용 저장소 역할을 하는 것이 **Redis**입니다.

![](../assets/CH03/session-redis.png)

*그림 3-22 Redis로 해결 — 세션을 공용 저장소에 보관하여 어느 서버에서든 조회 가능*

1번 서버가 Redis에 세션을 저장하면 2번 서버도 같은 Redis를 열어 그 세션을 꺼냅니다. 어느 서버가 요청을 처리하든 동일한 데이터에 접근합니다. 이 조합이 앱에 들어가면 복제 서버 어디로 요청이 가도 로그인이 유지됩니다.

> **참고: Redis**
> 메모리 기반의 키-값 데이터베이스입니다. 디스크가 아닌 메모리에 저장하기 때문에 속도가 매우 빨라, 캐싱·세션 저장소처럼 빠른 읽기/쓰기가 필요한 곳에 주로 쓰입니다.

### 3.3.3 사용자 정의 네트워크 — 이름으로 부르기

Redis 컨테이너와 API 컨테이너가 서로를 **어떻게 부를 것인가**. 챕터 2에서 예고했던 "사용자 정의 네트워크"가 여기서 실제로 쓰입니다.

3.2에서 오픈이는 컨테이너를 `docker run`으로 각각 실행했더니 기본 bridge에 들어갔고, 이름으로 부르는 게 불가능해서 `host.docker.internal`로 호스트를 경유해야 했습니다. 사용자 정의 네트워크는 이 우회를 제거합니다. 같은 네트워크에 들어간 컨테이너들은 Docker 내장 DNS가 이름을 IP로 바꿔줍니다. **컨테이너 이름을 그대로 도메인처럼 쓸 수 있습니다**.

![](../assets/CH03/net-05-docker-dns.png)

*그림 3-23 사용자 정의 네트워크 — 같은 네트워크 안의 컨테이너끼리 이름으로 호출*

기본 명령은 세 가지면 충분합니다.

| 명령 | 역할 |
|------|------|
| `docker network create <이름>` | 새 네트워크 생성 |
| `docker run ... --network <이름>` | 컨테이너를 해당 네트워크에 참여 |
| `docker network ls` | 네트워크 목록 조회 |

| 배치 방식 | 컨테이너끼리 이름 호출 | 호스트 경유 필요 |
|----------|-------------------|---------------|
| 기본 bridge (그냥 `docker run`) | 불가 | 필요 (`host.docker.internal`) |
| 사용자 정의 네트워크 (`--network`) | 가능 | 불필요 |

> **참고: 사용자 정의 네트워크**
> `docker network create`로 사용자가 직접 만드는 bridge 네트워크입니다. 기본 bridge와 달리 **Docker 내장 DNS**가 자동 활성화됩니다. 실무에서는 거의 모든 경우에 사용자 정의 네트워크를 씁니다.

*'이제 host.docker.internal 안 써도 되겠네. 이름으로 바로 부르자.'*

### 3.3.4 실습: Redis로 세션 공유

> 실습 코드: https://github.com/metacoding-10-linux-docker/docker/tree/master/ex04

폴더 구조는 api 하나입니다(Redis는 공식 이미지를 그대로 씁니다).

```
ex04/
└── api/
    ├── Dockerfile
    └── app.py         # Redis에 값을 저장/조회하는 간단한 API
```

`app.py`는 `/save`로 값을 넣고 `/read`로 꺼내는 단순한 서버입니다. 핵심은 딱 한 줄입니다. Redis 주소를 **`host='redis'`** 로 지정한 부분. IP가 아니라 컨테이너 이름을 그대로 썼습니다.

**ex04/api/app.py** (핵심)
```python
import redis
# 'redis'는 사용자 정의 네트워크 안의 컨테이너 이름
r = redis.Redis(host='redis', port=6379, db=0)
```

이제 네트워크를 만들고 세 컨테이너를 모두 같은 네트워크에 띄웁니다.

```bash
# 1. 사용자 정의 네트워크 생성
docker network create myNetwork

# 2. Redis 컨테이너 실행 (-p는 호스트에서 확인용으로 노출, 같은 네트워크 내 통신에는 불필요)
docker run -d --name redis --network myNetwork -p 6379:6379 redis

# 3. API 서버 두 대 실행 (같은 이미지, 다른 포트)
docker build -t api ./api
docker run -d --name api1 --network myNetwork -p 5001:5000 api
docker run -d --name api2 --network myNetwork -p 5002:5000 api
```

api1 서버의 `localhost:5001/save`로 값을 저장한 뒤, api2 서버의 `localhost:5002/read`로 조회해 봤습니다. api1이 저장한 값이 api2에서 그대로 **나왔습니다**.

![](../assets/CH03/chap02-40.png)

*그림 3-24 api1에서 데이터 저장*

![](../assets/CH03/chap02-41.png)

*그림 3-25 api2에서 같은 데이터 조회*

세 컨테이너가 같은 `myNetwork` 안에 있으니 api1·api2가 `host='redis'`만 써도 Redis 컨테이너에 닿습니다.

*'데이터를 서버 밖으로 빼두기만 해도 이 문제가 통째로 사라지네.'*

## 3.4 MySQL — 영구 데이터는 DB 서버에

세션 문제는 Redis로 풀렸습니다. 그런데 Redis는 메모리 기반이라 컨테이너를 재시작하면 데이터가 사라집니다. 세션처럼 잠깐 들고 있는 데이터는 괜찮지만, 회원 정보나 주문 내역처럼 **영구히 보관되어야 하는 데이터**는 다른 곳에 둬야 했습니다. 프로젝트에도 사용자 데이터를 담을 DB가 필요했습니다. MySQL 역시 컨테이너로 띄울 수 있습니다.

> 실습 코드: https://github.com/metacoding-10-linux-docker/docker/tree/master/ex05

**ex05/db/Dockerfile**
```dockerfile
FROM mysql                                    # MySQL 공식 이미지
COPY init.sql /docker-entrypoint-initdb.d     # 첫 기동 시 자동 실행될 SQL
ENV MYSQL_USER=metacoding                     # 사용자 이름
ENV MYSQL_PASSWORD=metacoding1234             # 사용자 비밀번호
ENV MYSQL_ROOT_PASSWORD=root1234              # root 비밀번호
ENV MYSQL_DATABASE=metadb                     # 기본 생성할 DB 이름
CMD ["--character-set-server=utf8mb4", "--collation-server=utf8mb4_unicode_ci"]
```

눈여겨볼 곳은 두 군데입니다.

1. **`/docker-entrypoint-initdb.d`** 는 MySQL 공식 이미지가 **첫 기동 시** 자동으로 실행해 주는 특수 경로입니다. 여기에 `init.sql`을 넣어두면 테이블과 초기 데이터가 알아서 만들어집니다.
2. **환경 변수 네 개**로 계정과 기본 DB 이름을 세팅합니다. 실제 접속 시 이 값들이 그대로 쓰입니다.

실습 편의를 위해 `FROM mysql`로 태그를 생략했지만, 실무에서는 재현성을 위해 `FROM mysql:8.0`처럼 버전을 고정하는 것이 안전합니다.

빌드하고 실행합니다.

```bash
docker build -t db ./db
docker run -dit -p 3306:3306 db
```

![](../assets/CH03/chap02-43.png)

*그림 3-26 MySQL 컨테이너 실행 로그*

컨테이너 안으로 들어가 데이터를 확인합니다. `docker ps`로 실행 중인 컨테이너 ID를 확인한 뒤, `docker exec -it <컨테이너ID> bash`로 내부 셸에 진입했습니다.

```bash
docker ps                    # 실행 중인 컨테이너 확인
docker exec -it 1fc2 bash   # MySQL 컨테이너 내부 접속
```

![](../assets/CH03/chap02-44.png)

*그림 3-27 MySQL 컨테이너 내부 진입*

컨테이너 안에서 MySQL 클라이언트를 띄웁니다. 접속 형식은 `mysql -u <사용자명> -p`이고, 사용자명과 비밀번호는 앞서 Dockerfile에 환경 변수로 심어 둔 값을 그대로 씁니다.

```bash
mysql -u metacoding -p       # MySQL 접속
```

비밀번호를 입력할 때는 보안상 화면에 표시되지 않지만, 그대로 치면 접속됩니다.

![](../assets/CH03/chap02-45.png)

*그림 3-28 MySQL 접속 성공*

접속한 뒤에는 `show databases`로 DB 목록을, `use metadb`로 DB를 고르고, `show tables`로 테이블 목록을, `select * from user_tb`로 데이터를 차례로 확인했습니다.

```sql
show databases;
use metadb;
show tables;
select * from user_tb;
```

![](../assets/CH03/chap02-46.png)

*그림 3-29 데이터베이스 목록 확인*

![](../assets/CH03/chap02-47.png)

*그림 3-30 user_tb 데이터 조회 결과*

`init.sql`에서 만든 ssar, cos 계정이 user_tb에 그대로 남아 있었습니다.

*'이미지에 SQL 한 장 넣어두면 DB가 알아서 자리를 잡는다.'*

DB까지 컨테이너로 준비할 수 있게 됐습니다. 그런데 터미널 히스토리를 올려보다 멈췄습니다.

## 3.5 Docker Compose — 여러 컨테이너를 한 번에

### 3.5.1 docker run을 매번 치는 게 지친다

네트워크 만들고, Redis 띄우고, API 두 대 띄우고, MySQL 띄우고, NGINX 띄우기. 여기까지 오면서 `docker run` 명령을 다섯 번 넘게 쳤습니다. 챕터 시작할 때 수동 설치가 피곤해서 Dockerfile을 배웠는데, 이번엔 `docker run`을 반복하고 있었습니다.

*'이거 매번 다 쳐야 돼?'*

![](../assets/CH03/chap02-48.png)

*그림 3-31 기존 방식 — 개별 빌드 및 실행 반복*

**여러 컨테이너를 하나의 파일에 적어두고 명령어 하나로 실행**하면 되지 않을까. **Docker Compose**가 그 도구입니다. 악보 한 장에 악기별 파트를 적어두고 지휘 한 번에 연주를 시작하는 것과 같습니다.

![](../assets/CH03/chap02-49.png)

*그림 3-32 Docker Compose 방식 — 한 번에 생성 및 연결*

Compose가 해주는 일은 세 가지입니다.

- **순서**: `depends_on`으로 어떤 컨테이너를 먼저 띄울지 지정.
- **네트워크**: 같은 Compose 파일에 정의된 컨테이너는 자동으로 하나의 네트워크에 묶임. `docker network create`를 따로 할 필요 없음.
- **일괄 관리**: `docker compose up` 한 줄로 시작, `docker compose down` 한 줄로 정리.

> **참고: Docker Compose**
> 여러 컨테이너를 하나의 YAML 파일에 묶어 명령 하나로 실행·관리하는 도구입니다. 컨테이너 간 네트워크와 의존 관계를 자동으로 구성해 줍니다.

### 3.5.2 docker-compose.yml 기본 구조

```yaml
services:
  <서비스명>:
    container_name: <컨테이너명>       # 컨테이너 이름
    image: <이미지명>                # Hub에서 가져올 이미지
    build: <경로>                    # Dockerfile로 직접 빌드 (image 대신 선택)
    ports:
      - "호스트포트:컨테이너포트"
    depends_on:
      - <먼저 떠야 할 서비스>
    environment:
      - KEY=VALUE
    volumes:
      - <호스트경로:컨테이너경로>
    networks:
      - <네트워크명>

volumes:
  <볼륨명>:

networks:
  <네트워크명>:
```

전부 쓰진 않습니다. 실습에서 쓰는 건 이 정도입니다.

| 옵션 | 필수 여부 | 언제 쓰나 |
|------|---------|----------|
| `services.<이름>` | 필수 | 컨테이너 하나당 하나 |
| `image` 또는 `build` | 둘 중 하나 | Hub에서 받을지, Dockerfile로 빌드할지 |
| `ports` | 선택 | 외부 접근이 필요할 때 |
| `environment` | 선택 | 설정값 주입 |
| `depends_on` | 선택 | 시작 순서 지정 (단, **준비 완료**까지는 보장 X) |
| `networks` | 선택 | 같은 파일 안이면 자동이라 대부분 생략 |

### 3.5.3 실습: Compose로 EX01 다시 만들기

EX01의 세 컨테이너(app1/app2/lb)를 Compose로 바꿔봤습니다. Dockerfile과 index.html은 그대로, docker-compose.yml만 새로 씁니다.

> 실습 코드: https://github.com/metacoding-10-linux-docker/docker/tree/master/ex06

**ex06/docker-compose.yml**
```yaml
services:
  app1:
    build:
      context: ./app1
    ports:
      - 8000:80
    networks:
      - ex06-network
  app2:
    build:
      context: ./app2
    ports:
      - 9000:80
    networks:
      - ex06-network
  lb:
    build:
      context: ./lb
    ports:
      - 80:80
    networks:
      - ex06-network

networks:
  ex06-network:
```

그리고 `ex06/lb/nginx.conf`에서 upstream 주소가 EX01과 결정적으로 달라졌습니다. 이전엔 `host.docker.internal:8000`이었는데, 이제는 **`app1:80`**, **`app2:80`** 처럼 서비스 이름으로 바로 부릅니다. Compose가 자동으로 사용자 정의 네트워크를 만들어 세 서비스를 묶어주기 때문입니다.

![](../assets/CH03/net-06-compose-network.png)

*그림 3-33 Compose가 자동 생성한 네트워크에서 서비스 이름으로 통신*

실행은 이 한 줄입니다.

```bash
docker compose up        # 모든 컨테이너 한 번에 실행
docker compose down      # 모든 컨테이너 중지 및 삭제
```

![](../assets/CH03/chap02-52.png)

*그림 3-34 docker compose up 실행 결과*

결과는 EX01과 같았는데, `docker build` + `docker run` 여섯 명령이 `docker compose up` 한 줄로 줄었습니다.

*'아, 이걸 쓰면 되는구나.'*

### 3.5.4 자주 쓰는 Compose 명령어

| 명령어 | 설명 |
|--------|------|
| `docker compose up` | 모든 서비스 빌드 + 실행 |
| `docker compose up -d` | 백그라운드 실행 |
| `docker compose down` | 모든 서비스 중지 + 삭제 |
| `docker compose ps` | 실행 중인 서비스 목록 |
| `docker compose logs` | 서비스 로그 |
| `docker compose build` | 이미지만 빌드 |

## 3.6 종합 실습 — 풀스택 웹사이트

프로젝트에 필요한 것들을 하나씩 컨테이너로 세워봤고, Compose로 묶는 것까지 배웠습니다. 이제 실제 프로젝트와 비슷한 구조를 처음부터 끝까지 조립해볼 차례입니다. **프론트엔드(NGINX) + 백엔드(Spring Boot) + DB(MySQL)** 세 서비스를 Compose 한 파일에 담고, `docker compose up` 한 줄로 전체를 띄우는 구성입니다.

> 실습 코드: https://github.com/metacoding-10-linux-docker/docker/tree/master/ex07

### 3.6.1 전체 아키텍처

![](../assets/CH03/fig-1-v2.png)

*그림 3-35 세 컨테이너로 구성되는 웹 애플리케이션 아키텍처*

각 서비스의 역할은 이렇습니다.

- **Frontend (NGINX)**: 브라우저에 HTML을 응답. `/api/` 요청은 백엔드로 프록시.
- **Backend (Spring Boot)**: `/api/users` API를 처리. DB에서 사용자 목록을 조회.
- **DB (MySQL)**: 사용자 데이터 영구 저장.

*'앞에서 하나씩 해본 게 그대로 들어가네.'*

폴더 구조는 이렇습니다.

```
ex07/
├── backend/             # Spring Boot 백엔드
│   ├── Dockerfile
│   └── entrypoint.sh
├── db/                  # MySQL (ex05와 동일)
│   ├── Dockerfile
│   └── init.sql
├── frontend/            # NGINX + HTML
│   ├── Dockerfile
│   ├── index.html
│   └── nginx.conf
└── docker-compose.yml
```

### 3.6.2 Backend: 시작 시 소스 내려받아 빌드

학습 편의를 위해, 백엔드 이미지는 컨테이너가 뜨는 순간 Github에서 Spring Boot 소스를 clone 받고 빌드하도록 구성했습니다. 독자가 소스를 로컬에 받아두지 않아도 실습이 돌아가게 만든 구성입니다.

**ex07/backend/entrypoint.sh**
```bash
#!/bin/bash
git clone https://github.com/metacoding-10-linux-docker/backend-server
cd backend-server
chmod +x gradlew
./gradlew build
java -jar -Dspring.profiles.active=prod build/libs/*.jar
```

> **참고: 이 구조는 학습용**
> 독자가 로컬에 소스를 내려받지 않고도 실습이 돌아가도록, 컨테이너가 뜰 때마다 git clone과 빌드를 수행하게 만든 구성입니다.

*'실전이면 jar를 이미지에 미리 구워야겠지만, 지금은 일단 돌려보자.'*

### 3.6.3 Frontend: NGINX가 `/`는 정적, `/api/`는 백엔드로

**ex07/frontend/nginx.conf**
```nginx
events {}

http {
    upstream backend {
        server backend:8080;               # Compose 서비스 이름
    }

    server {
        listen 80;
        server_name _;

        location / {                       # / 요청은 정적 파일
            root   /usr/share/nginx/html;
            index  index.html;
        }

        location /api/ {                   # /api 요청은 백엔드로 프록시
            proxy_pass http://backend;
        }
    }
}
```

`server backend:8080`이 이번 구성의 연결 고리입니다. Compose가 같은 네트워크로 묶어주니 frontend 컨테이너에서 `backend`라는 이름으로 바로 닿습니다.

### 3.6.4 docker-compose.yml

**ex07/docker-compose.yml**
```yaml
services:
  backend:
    build:
      context: ./backend
    ports:
      - "8080:8080"
    environment:
      SPRING_DATASOURCE_URL: jdbc:mysql://db:3306/metadb?useSSL=false&serverTimezone=UTC&useLegacyDatetimeCode=false&allowPublicKeyRetrieval=true
      SPRING_DATASOURCE_DRIVER_CLASS_NAME: com.mysql.cj.jdbc.Driver
      SPRING_DATASOURCE_USERNAME: root
      SPRING_DATASOURCE_PASSWORD: root1234
    networks:
      - ex07-network

  db:
    build:
      context: ./db
    ports:
      - 3306:3306
    networks:
      - ex07-network

  frontend:
    build:
      context: ./frontend
    ports:
      - "80:80"
    networks:
      - ex07-network

networks:
  ex07-network:
```

backend의 `SPRING_DATASOURCE_URL`에 들어간 `jdbc:mysql://db:3306/...`이 DB 컨테이너를 이름으로 부르는 지점입니다.

### 3.6.5 한 줄로 전체 띄우기

```bash
docker compose up
```

![](../assets/CH03/chap02-ex07-compose.png)

*그림 3-36 docker compose up 한 줄로 세 컨테이너가 동시에 뜨는 모습*

백엔드 컨테이너는 git clone과 Gradle 빌드를 먼저 돌리느라 몇 분 걸렸습니다. 준비가 끝난 뒤 브라우저에서 `localhost:80`에 접속하니 사용자 목록이 떴습니다.

![](../assets/CH03/chap02-58.png)

*그림 3-37 사용자 목록 조회 성공*

하나씩 따로 띄워보던 것들이 한 줄에 전부 올라갔습니다. 뒤에서 어떤 일이 벌어졌는지 흐름을 따라가 봤습니다.

1. 브라우저가 `localhost:80`으로 `index.html`을 요청.
2. frontend 컨테이너의 NGINX가 `location /`에 매칭해 정적 HTML 응답.
3. 페이지가 뜬 뒤 JS가 `/api/users`를 호출 → 같은 NGINX가 받아 `location /api/`에 매칭 → `proxy_pass http://backend`로 백엔드 컨테이너에 전달.
4. Backend가 `db:3306`으로 MySQL 컨테이너에 붙어 `user_tb`를 조회.
5. JSON 응답이 Spring → NGINX → 브라우저로 돌아가 화면에 표시.

프로젝트에 필요한 세 서비스가 Compose 한 파일 안에서 돌아갔습니다. 이미지에 필요한 모든 것이 들어 있고, Compose가 세 서비스를 하나의 네트워크로 묶어 서비스 이름만으로 서로를 부르게 해주기 때문입니다.

## 3.7 Compose까지 와도 남은 것

프로젝트 환경은 갖춰졌습니다. 그런데 이걸 실제로 운영한다고 생각하니 아직 풀리지 않은 문제가 보였습니다.

**팀장**: "근데 이거 하나 죽으면 누가 살려?"

- **컨테이너가 죽으면 누가 다시 띄우는가**: 예기치 못한 크래시가 나도 자동 복구는 없음.
- **트래픽이 몰리면 어떻게 개수를 조정하는가**: compose 파일을 고쳐 다시 올려야 함.
- **무중단 배포는 어떻게 하는가**: 새 버전 올리고 기존 것 내리는 과정에 공백이 생김.
- **여러 서버에 나눠 띄우려면**: Compose는 기본적으로 한 머신 위에서 도는 도구.
- **설정·비밀값을 이미지와 분리하려면**: 현재는 compose 파일에 적어두는 수준.

이 과제들을 한 묶음으로 풀어주는 자동화 시스템이 다음 챕터의 주제인 **Kubernetes**입니다. 다음 챕터에서 그 관제 시스템 안으로 들어갑니다.

## 이것만은 기억하자

- **Dockerfile**은 환경 구성의 레시피입니다. 한 번 써두면 같은 환경을 몇 번이든 재현합니다.
- **NGINX**는 서버 앞단에 두는 리버스 프록시입니다. 경로 라우팅·로드밸런싱·캐싱이 핵심 역할이고, 세 예제 모두 같은 뼈대 위에 옵션만 달리한 형태입니다.
- **Redis**는 서버들이 공유하는 세션 저장소입니다. 로드밸런싱으로 서버가 여러 대가 돼도 세션이 끊기지 않게 해줍니다.
- **사용자 정의 네트워크**는 컨테이너끼리 **이름으로 통신**하게 해줍니다. `host.docker.internal` 우회가 사라집니다.
- **Docker Compose**는 여러 컨테이너를 한 파일에 묶어 명령 하나로 관리합니다. 서비스 간 네트워크도 자동입니다.
- **Compose까지 와도 자동 복구·스케일링·무중단 배포·다중 서버는 남는다.** 다음 챕터에서 Kubernetes가 이 자리를 가져갑니다.
