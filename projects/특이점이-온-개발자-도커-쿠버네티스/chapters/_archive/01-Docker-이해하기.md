# 챕터 1. Docker 이해하기

## 학습 목표

- 컨테이너의 개념과 등장 배경을 이해한다.
- Docker를 설치하고 컨테이너를 실행·조작한다.
- 컨테이너를 이미지로 저장하고 Dockerhub에 공유한다.
- 마운트를 사용하여 컨테이너 삭제 후에도 데이터를 보존한다.

## 1.1 말콤 맥린 : 컨테이너의 아버지

### 1.1.1 해상 운송의 초기

Docker를 이해하려면 '컨테이너'라는 개념이 어디서 왔는지부터 살펴야 합니다. 그 시작은 의외로 바다 위에 있습니다.

컨테이너가 등장하기 전, 해상 물류는 온전히 사람의 힘에 의존했습니다. 항구에 배가 도착하면 수백 명의 노동자가 화물을 하나씩 내리고 분류하고 다시 트럭에 옮겨 실어야 했습니다. 길게는 몇 주씩 걸리는 작업이었습니다.

<!-- image-prompt: Minimal black line drawing on white background, very few details, icon-like simplicity, 4:3 aspect ratio, 800x600px. With Korean labels: An old harbor scene with workers carrying sacks and crates from a cargo ship (labeled "화물선") to the dock (labeled "부두"), showing the inefficient process of early maritime logistics, with a label "수작업 하역" above the workers -->

![초기 해상 물류](images/chap01-1.png)
*그림 1-1: 초기 해상 물류의 수작업 하역 과정*

배로 물건을 보내는 비용보다 사람이 짐을 싣고 내리는 인건비가 더 비쌌습니다. 트럭 운전사들도 화물을 기다리느라 항구에서 며칠씩 대기하기 일쑤였습니다.

### 1.1.2 컨테이너의 도입

이 비효율을 가장 가까이에서 체감한 사람이 있었습니다. 바로 트럭 운전사 말콤 맥린입니다.

항구에서 화물이 하나씩 옮겨지는 걸 반복적으로 지켜보던 그는 단순하지만 강력한 의문을 품습니다. **"왜 짐을 박스째로 통째로 옮기지 않는 걸까?"**

이 질문에서 컨테이너라는 개념이 탄생했습니다. 화물을 낱개로 다루는 대신, 표준 규격의 큰 상자 하나에 담아서 통째로 옮기자는 아이디어였습니다.

크레인으로 컨테이너를 그대로 배에 올리고, 도착지에서도 같은 방식으로 내리면 됩니다. 운송 속도와 효율은 이전과는 비교할 수 없을 정도로 올라갔습니다.

<!-- image-prompt: Minimal black line drawing on white background, very few details, icon-like simplicity, 4:3 aspect ratio, 800x600px. With Korean labels: A modern container port with a large crane (labeled "크레인") lifting a standardized shipping container (labeled "표준 컨테이너") from a truck (labeled "트럭") onto a cargo ship (labeled "화물선"), showing the efficient and automated container logistics system -->

![컨테이너 운송](images/chap01-2.png)
*그림 1-2: 표준 컨테이너와 크레인을 활용한 현대 해상 운송*

물론 처음부터 순탄하지는 않았습니다. 기존 선박은 컨테이너를 싣는 걸 전제로 만들어진 것이 아니었기 때문에 공간 활용이 어려워 기대만큼의 성과가 나오지 않았습니다.

맥린은 여기서 멈추지 않았습니다. 아예 컨테이너 전용 선박을 직접 만들어 버립니다.

그 상상은 결국 현실이 되었습니다. 컨테이너는 해상 운송의 표준으로 자리 잡았고 전 세계 물류 체계를 바꿔 놓았습니다.

### 1.1.3 IT에서의 컨테이너

그렇다면 이 이야기가 IT와 무슨 관련이 있을까요? 사실 IT에서 말하는 '컨테이너'도 해상 운송의 컨테이너와 본질은 같습니다.

> **컨테이너(Container)** 는 어디서든 동일하게 실행되는 표준화된 실행 환경을 의미합니다.

<!-- image-prompt: Minimal black line drawing on white background, very few details, icon-like simplicity, 4:3 aspect ratio, 800x600px. With Korean labels: A developer frustrated at their desk with two monitors showing different environments - left monitor shows "개발 환경 OK" with green checkmark, right monitor shows "운영 환경 ERROR" with red X mark, illustrating environment mismatch problems -->

![개발 환경과 운영 환경의 차이로 인한 오류 발생](images/chap01-3.png)
*그림 1-3: 개발 환경과 운영 환경의 차이로 인한 오류 발생*

개발 환경에서 아무리 열심히 테스트해도 운영 환경에 배포하는 순간 또 다른 변수가 기다리고 있습니다.

컨테이너는 바로 이 문제를 해결합니다. 애플리케이션이 실행되는 데 필요한 라이브러리와 설정 파일, 의존성을 전부 하나의 상자에 담아 버립니다. 말콤 맥린이 화물을 표준 컨테이너에 넣어 어디서든 똑같이 옮길 수 있게 한 것과 같은 원리입니다.

<!-- image-prompt: Minimal black line drawing on white background, very few details, icon-like simplicity, 4:3 aspect ratio, 800x600px. With Korean labels: A shipping container metaphor for software - a standardized box (labeled "컨테이너") containing "애플리케이션 코드", "라이브러리", and "설정 파일", being deployed identically across three targets labeled "개발 노트북", "테스트 서버", and "운영 클라우드 서버" -->

![컨테이너를 통한 일관된 실행 환경](images/chap01-4.png)
*그림 1-4: 컨테이너를 통한 일관된 실행 환경*


## 1.2 Docker : 작동 원리

### 1.2.1 가상화 : 하나의 컴퓨터를 여러 개로 사용하는 법

말콤 맥린은 "상자에 넣으면 어디서든 똑같이 옮길 수 있다"는 걸 증명했습니다. Docker도 같은 원리입니다. 그렇다면 Docker는 이 "상자"를 어떻게 만들까요? 그 출발점은 **가상화** 입니다.

> **가상화(Virtualization)** 는 하나의 물리 서버를 논리적으로 여러 대처럼 나누어 쓰는 기술입니다. 가상화를 도입하면 서버를 효율적으로 쓸 수 있고 서로 다른 환경을 안전하게 격리할 수 있습니다.

주방에 비유해 보겠습니다.

하나의 주방에 네 명의 요리사가 일하고 있습니다. 그런데 냉장고와 가스레인지가 각각 하나뿐이라 한 번에 한 명만 쓸 수 있는 구조입니다.

<!-- image-prompt: Minimal black line drawing on white background, very few details, icon-like simplicity, 4:3 aspect ratio, 800x600px. With Korean labels: A single kitchen (labeled "주방 1개") with four chefs (labeled "요리사 4명") crowded around one refrigerator (labeled "냉장고") and one stove (labeled "가스레인지"), waiting for their turn, illustrating resource contention -->

![하나의 주방을 공유하는 네 명의 요리사](images/chap01-5.png)
*그림 1-5: 하나의 주방을 공유하는 네 명의 요리사*

네 명이 동시에 요리하려면 어떻게 해야 할까요? 방법은 크게 두 가지입니다.

**첫 번째 방법** 은 요리사 수만큼 주방을 통째로 복제하는 것입니다. 냉장고, 가스레인지, 싱크대까지 전부 따로 마련해서, 각자 완전히 독립된 주방에서 일하게 합니다.

<!-- image-prompt: Minimal black line drawing on white background, very few details, icon-like simplicity, 4:3 aspect ratio, 800x600px. With Korean labels: Four separate complete kitchens (each labeled "독립 주방") side by side, each with its own "냉장고", "가스레인지", and "싱크대", one chef per kitchen working independently - representing hypervisor virtualization (labeled "하이퍼바이저 가상화") -->

![요리사별 독립 주방 — 주방 전체를 복제하는 방식](images/chap01-6.png)
*그림 1-6: 요리사별 독립 주방 — 주방 전체를 복제하는 방식*

서로 방해받을 일이 없다는 게 장점이지만, 설비를 전부 네 벌씩 갖춰야 하니 비용이 크게 발생합니다.

**두 번째 방법** 은 냉장고나 칼 같은 공용 설비는 함께 쓰되 조리대만 각자 따로 마련하는 것입니다.

<!-- image-prompt: Minimal black line drawing on white background, very few details, icon-like simplicity, 4:3 aspect ratio, 800x600px. With Korean labels: One kitchen with shared equipment (labeled "공용 설비") including "냉장고" and "칼" in the center, but four separate small cooking stations (each labeled "개별 조리대") around it, each chef working at their own station - representing container virtualization (labeled "컨테이너 가상화") -->

![기본 설비 공유 + 개별 조리대 — 컨테이너 가상화 비유](images/chap01-7.png)
*그림 1-7: 기본 설비 공유 + 개별 조리대 — 컨테이너 가상화 비유*

이 방식은 자원을 알뜰하게 쓰면서도 각자의 작업 공간을 확보할 수 있습니다. 다만 공용 설비를 함께 쓰는 만큼 서로 방해하지 않기 위한 규칙이 필요합니다.

첫 번째 방식은 격리가 확실하지만 비용이 크고, 두 번째 방식은 자원을 아끼면서도 독립적인 작업 공간을 유지합니다. Docker의 컨테이너 가상화가 바로 두 번째 방식입니다.

### 1.2.2 컨테이너 가상화 : OS 없이 격리하다

> **컨테이너 가상화(Container Virtualization)** 는 하나의 운영 체제를 함께 쓰면서 애플리케이션이 실행되는 환경만 따로 분리하는 방식입니다.

하나의 서버에는 OS가 설치되어 있고, 그 핵심에는 **커널** 이 있습니다. 컨테이너 가상화는 이 커널을 여러 애플리케이션이 함께 공유하되 각 애플리케이션의 실행 공간만 독립적으로 분리하는 방식입니다. 분리된 실행 공간 하나하나가 바로 **컨테이너** 입니다.

컨테이너 안에는 앱 실행에 필요한 라이브러리, 설정, 파일시스템만 들어 있습니다. OS 전체를 복제하지 않고, 커널은 호스트의 것을 함께 쓰면서 실행 환경만 격리합니다.

<!-- image-prompt: Minimal black line drawing on white background, very few details, icon-like simplicity, 4:3 aspect ratio, 800x600px. With Korean labels: Diagram showing container virtualization architecture - at the bottom "하드웨어", above it "호스트 OS 커널", then "컨테이너 엔진" layer, and on top multiple containers (each labeled "컨테이너") each containing "앱" and "라이브러리", sharing the same OS kernel -->

![컨테이너 가상화 구조](images/chap01-8.png)
*그림 1-8: 컨테이너 가상화 구조*

컨테이너마다 파일시스템, 네트워크, 프로세스 공간이 분리되어 있어서 컨테이너 A에서 설치한 라이브러리가 컨테이너 B에 영향을 주지 않습니다.

컨테이너 가상화에서는 **컨테이너 엔진(Container Engine)** 이 컨테이너의 생성, 실행, 중지, 삭제를 맡습니다. Docker가 대표적인 컨테이너 엔진으로, 이미지 관리부터 컨테이너 실행까지 운영에 필요한 기능을 두루 갖추고 있습니다.

### 1.2.3 Docker : 이미지에서 컨테이너까지

Docker는 어떻게 컨테이너를 만들까요? 명령어 하나를 따라가며 흐름을 살펴보겠습니다.

지금은 명령어를 실행하지 않아도 됩니다. 동작 흐름만 이해하면 충분합니다.

**[참고]** nginx 컨테이너를 실행하는 명령어입니다.

```bash
docker run nginx   # nginx 컨테이너 실행
```

이 명령어를 실행하면 **Docker 엔진**이 요청을 받습니다. Docker 엔진이 직접 컨테이너를 만들지는 않습니다. OS **커널**에 "격리된 프로세스를 하나 만들어 줘"라고 요청할 뿐입니다.

커널은 건물의 관리사무소 같은 존재입니다. 전기, 수도, 엘리베이터를 관리사무소가 관리하듯 커널은 컴퓨터의 CPU, 메모리, 프로세스를 관리합니다. 프로세스를 만들고 격리하고 자원을 나눠주는 것은 오직 커널만 할 수 있습니다.

> **커널(Kernel)** 은 운영체제(OS)의 핵심 구성 요소로, 프로세스를 만들고 실행 순서를 정하며, 프로세스끼리 서로 간섭하지 않도록 메모리를 보호합니다.

Docker 엔진의 요청을 받은 커널은 격리된 환경에서 새 프로세스를 만듭니다. 이것이 컨테이너입니다.

<!-- image-prompt: Minimal black line drawing on white background, very few details, icon-like simplicity, 4:3 aspect ratio, 800x600px. Flow diagram with Korean labels: "docker run nginx" on the left, arrow pointing to "Docker 엔진", arrow pointing to "OS 커널", arrow pointing to a dashed-border box labeled "컨테이너 (격리된 프로세스)", showing the complete request flow from command to container creation in a single diagram -->

![docker run 실행 흐름](images/chap01-9.png)
*그림 1-9: docker run 실행 흐름*

### 1.2.4 Docker 이미지

컨테이너는 격리된 프로세스이지만 빈 깡통이 아닙니다. 무언가를 담아야 실행할 수 있습니다. 그 "무언가"가 바로 **이미지**입니다.

이미지는 컨테이너를 만들기 위한 패키지입니다. 안에는 OS, 애플리케이션, 설정 파일이 레이어(층)로 겹쳐 쌓인 구조입니다. 예를 들어 nginx 이미지 안에는 Linux + nginx + 기본 설정이 들어 있습니다. 레이어 구조의 자세한 동작 방식은 2챕터 Dockerfile에서 다룹니다.

비유하면 이미지는 붕어빵 틀입니다. 틀(이미지) 하나로 붕어빵(컨테이너)을 여러 개 찍어낼 수 있습니다. 틀 자체는 변하지 않고 찍혀 나온 붕어빵은 각각 독립적입니다. 이미지 하나로 똑같은 컨테이너를 몇 개든 만들 수 있습니다.

<!-- image-prompt: Minimal black line drawing on white background, very few details, icon-like simplicity, 4:3 aspect ratio, 800x600px. With Korean labels: On the left, a box labeled "이미지" containing three stacked layers labeled "OS (Linux)", "애플리케이션 (nginx)", and "설정 파일". Three arrows point from this single image box to three identical containers on the right, each labeled "컨테이너 1", "컨테이너 2", "컨테이너 3", showing that one image can create multiple independent containers -->

![하나의 이미지로 여러 컨테이너 생성](images/chap01-12.png)
*그림 1-10: 하나의 이미지로 여러 컨테이너를 만들 수 있다*

이미지는 어디서 올까요? **Docker Hub**라는 저장소에 사람들이 만들어 둔 이미지가 있습니다. 여기서 가져다 쓰면 됩니다. 직접 이미지를 만들어 Docker Hub에 올릴 수도 있습니다.

![Docker의 큰 그림](images/fig-1-bp-0.png)
*그림 1-11: Docker의 흐름*

전체 흐름을 정리하면 이렇습니다. Docker Hub에서 이미지를 내려받아 컨테이너를 실행하고, 컨테이너 안에서 작업한 뒤 수정한 내용을 새 이미지로 저장합니다. 이 이미지를 Docker Hub에 올리면 다른 사람도 가져다 쓸 수 있습니다. 이 챕터에서는 이 흐름을 직접 따라가며 Docker를 익혀보겠습니다.

## 1.3 Docker Desktop : 설치

1. [Docker 공식 사이트](https://www.docker.com/products/docker-desktop/)에 접속하여 자신의 OS에 맞는 **Docker Desktop** 을 다운로드합니다.
2. 다운로드한 설치 파일을 실행하고, 안내에 따라 설치합니다.
3. 설치가 끝나면 Docker Desktop을 실행합니다.

> **Windows** 의 경우 Docker Desktop 설치 전에 **WSL2(Windows Subsystem for Linux 2)** 를 먼저 설치해야 합니다. Docker는 Linux 커널 기능을 사용해 컨테이너를 실행하는데 Windows에는 Linux 커널이 없으므로, WSL2에서 Linux 커널을 제공받아야 합니다.

설치가 끝났다면 터미널에서 다음 명령어로 정상 설치 여부를 확인합니다.

**[실습]** Docker 설치 상태를 확인하는 명령어입니다.

```bash
docker version   # Docker 버전 확인
```

Client와 Server 정보가 모두 출력되면 Docker가 정상적으로 설치된 것입니다.


## 1.4 Docker CLI : 기본 명령어

### 1.4.1 Docker Desktop 실행

Docker를 사용하려면 먼저 Docker Desktop을 실행합니다.

![Docker Desktop 실행 화면](images/chap01-14.png)
*그림 1-12: Docker Desktop 실행 화면*

### 1.4.2 docker pull : 이미지 다운로드

`docker pull` 명령어는 Docker Hub에서 이미지를 내려받습니다.

CMD 창을 열고 명령어를 실행합니다.

**[실습]** nginx 이미지를 다운로드하는 명령어입니다.

```bash
docker pull nginx   # nginx 이미지 다운로드
```

![실행 결과](images/chap01-15.png)
*그림 1-13: nginx 이미지 다운로드*

### 1.4.3 docker run : 컨테이너 실행

**[실습]** nginx 이미지를 기반으로 컨테이너를 실행하는 명령어입니다. 실행하면 터미널이 잠기면서 추가 입력이 안 됩니다. 정상 동작이니 당황하지 마세요.

```bash
docker run nginx   # nginx 컨테이너 실행
```

명령어를 실행하면 컨테이너가 실행되면서 터미널 창에 컨테이너 내부 로그가 출력됩니다.

> 이번 단계의 목표는 컨테이너를 실행하는 것입니다. 실행 후 컨테이너에 접근하려면 포트 포워딩(-p 옵션)이 필요한데, 이 옵션은 리눅스 챕터에서 다룹니다.

![실행 결과](images/chap01-17.png)
*그림 1-14: nginx 컨테이너 실행*

이 상태에서는 터미널 창에 추가로 명령어를 입력할 수 없습니다. 이를 포그라운드 상태라고 합니다.

> **포그라운드(Foreground)** 는 프로세스가 현재 터미널을 직접 점유하여 동작하는 방식입니다. 포그라운드 상태에서는 컨테이너의 실행 로그가 실시간으로 출력되며, 터미널을 종료하면 컨테이너도 함께 종료됩니다.

실행 중인 프로세스는 `CTRL + C`를 입력하면 빠져나올 수 있습니다.

### 1.4.4 docker run -d : 백그라운드 실행

> **백그라운드(Background)** 는 프로세스가 터미널과 분리된 상태로 동작하는 방식입니다. 백그라운드 상태에서는 컨테이너가 뒤에서 계속 실행되며, 사용자는 터미널을 종료하지 않고도 다른 명령을 자유롭게 실행할 수 있습니다.

**[실습]** -d 옵션을 사용하여 nginx를 백그라운드에서 실행하는 명령어입니다.

```bash
docker run -d nginx   # -d : detached 모드
```

명령어를 실행하면 **컨테이너 ID** 가 출력되고 터미널은 입력 가능한 상태로 돌아옵니다. 컨테이너 ID는 실행할 때마다 달라집니다. 이후 실습에서 `5fcd`, `d2b1` 같은 축약 ID가 나오면 본인의 `docker ps` 결과에서 확인한 ID 앞 4자리를 사용하면 됩니다.

![실행 결과](images/chap01-18.png)
*그림 1-15: 백그라운드 실행 결과*

### 1.4.5 docker ps : 컨테이너 목록 출력

**[실습]** 실행 중인 컨테이너 목록을 출력하는 명령어입니다.

```bash
docker ps   # 실행 중인 컨테이너 출력
```

실행 중인 컨테이너의 정보를 조회할 수 있습니다.

![실행 결과](images/chap01-20.png)
*그림 1-16: 컨테이너 목록 조회*

### 1.4.6 자주 사용하는 Docker 명령어

자주 사용하는 Docker 명령어는 다음과 같습니다.

| 명령어 | 설명 | 예시 |
|--------|------|------|
| `docker pull <이미지명>` | Dockerhub에서 이미지 다운로드 | `docker pull nginx` |
| `docker images` | 로컬에 저장된 이미지 목록 조회 | `docker images` |
| `docker logs <컨테이너ID>` | 컨테이너 로그 출력 | `docker logs 057c` |
| `docker ps -a` | 종료된 컨테이너 포함 전체 목록 출력 | `docker ps -a` |
| `docker stop <컨테이너ID>` | 실행 중인 컨테이너 종료 | `docker stop 057c` |
| `docker rm <컨테이너ID>` | 종료된 컨테이너 삭제 | `docker rm 057c` |
| `docker rmi <이미지ID>` | 이미지 삭제 (`-f`로 강제 삭제) | `docker rmi -f fb01` |


## 1.5 Linux : 컨테이너 안에서 쓰는 명령어

Docker 명령어를 익혔으니 이번에는 컨테이너 내부를 살펴보겠습니다. 컨테이너 안은 리눅스 환경이므로 기본적인 리눅스 명령어를 알아야 자유롭게 돌아다닐 수 있습니다. 이 섹션에서는 Ubuntu 컨테이너에 nginx를 직접 설치하고 실행해 봅니다. Dockerfile 작성, 설정 파일 수정, 로그 확인 등 실제 Docker 작업에서 리눅스 명령어는 계속 나오므로 여기서 한 번 정리하고 넘어가겠습니다.

> 이미 리눅스 명령어에 익숙하다면 1.6 Docker 컨테이너 다루기로 건너뛰어도 됩니다.

### 1.5.1 Ubuntu : 환경 세팅

리눅스 명령어 실습을 위해 Ubuntu 환경을 준비합니다.

**[실습]** Ubuntu 컨테이너를 실행하는 명령어입니다. `-p 80:80`은 포트포워딩 설정으로, 호텔 프런트에서 "305호 손님 찾습니다" 하면 내선전화로 연결해주는 것과 같은 원리입니다.

```bash
docker run -it -p 80:80 ubuntu   # 호스트의 80포트로 요청 시 컨테이너의 80포트로 요청 전달
```

> **포트포워딩(Port Forwarding)** 은 호스트 PC의 특정 포트로 들어오는 요청을 컨테이너 내부의 포트로 전달하는 기능입니다. `-p 호스트포트:컨테이너포트` 형식으로 사용합니다. 예를 들어, `-p 9000:8080`은 호스트의 9000번 포트로 들어온 요청을 컨테이너의 8080번 포트로 전달합니다.

`-it` 옵션은 `-i`(입력 가능), `-t`(터미널 환경 제공)를 조합한 옵션입니다.  

![실행 결과](images/chap01-43.png)
*그림 1-17: Ubuntu 컨테이너 실행*



### 1.5.2 탐색 명령어 : pwd, cd, ls, clear

현재 위치를 확인하고 원하는 디렉토리로 이동하며 파일 목록을 조회하는 기본 명령어입니다.

| 명령어 | 설명 | 예시 |
|--------|------|------|
| `pwd` | 현재 위치 경로 출력 | `/root` |
| `cd <경로>` | 해당 폴더로 이동 | `cd home` |
| `cd ..` | 상위 폴더로 이동 | |
| `ls` | 현재 폴더의 파일/폴더 목록 출력 | |
| `ls -l` | 상세 정보와 함께 목록 출력 | |
| `ls -a` | 숨김 파일 포함 전체 출력 | |
| `ls -la` | 숨김 파일 포함 상세 출력 | |
| `clear` | 터미널 화면 비우기 | |

#### 절대 경로와 상대 경로

> **절대 경로와 상대 경로** 는 최상위 폴더(/)로부터 폴더를 찾아가는 방식을 절대 경로라고 하며, 현재 위치에서 폴더를 찾는 방식을 상대 경로라고 합니다.

예를 들어 /home/ubuntu 경로에서 /bin 폴더로 이동하려면 상대 경로 `cd bin`으로는 찾을 수 없고, 절대 경로 `cd /bin`으로 이동해야 합니다.

먼저 `cd /home/ubuntu`로 이동한 뒤, 상대 경로와 절대 경로의 차이를 확인해 보겠습니다.

![실행 결과](images/chap01-45.png)
*그림 1-18: 절대 경로로 이동*

실습 후 `cd /`로 루트 경로로 돌아갑니다.

### 1.5.3 파일/폴더 관리 : mkdir, touch, rm, cp, mv

폴더를 만들고, 파일을 생성하거나 복사·이동·삭제하는 명령어입니다.

| 명령어 | 설명 | 예시 |
|--------|------|------|
| `mkdir <폴더명>` | 폴더 생성 | `mkdir hello` |
| `touch <파일명>` | 빈 파일 생성 | `touch a.txt` |
| `rm <파일명>` | 파일 삭제 | `rm a.txt` |
| `rm -r <폴더명>` | 폴더 삭제 (하위 포함) | `rm -r hello` |
| `cp <원본> <사본>` | 파일 복사 | `cp a.txt b.txt` |
| `mv <원본> <대상>` | 파일 이동 또는 이름 변경 | `mv a.txt /tmp` |

> `mv`는 같은 경로에서 파일명만 변경하는 용도로도 사용할 수 있습니다. 예: `mv b.txt c.txt`

### 1.5.4 패키지 관리 : apt

컨테이너에는 기본적으로 최소한의 프로그램만 설치되어 있습니다. apt 명령어는 필요한 도구(nginx, vim 등)를 설치할 때 사용하는 패키지 관리 명령어입니다.

| 명령어 | 설명 |
|--------|------|
| `apt update` | 설치 가능한 패키지 목록을 최신 상태로 갱신 |
| `apt list \| grep <키워드>` | 패키지 검색 |
| `apt install -y <패키지명>` | 패키지 설치 (-y: 자동 승인) |

**[실습]** 패키지 목록 갱신 후 nginx를 설치하고 실행하는 명령어입니다.

```bash
apt update           # 패키지 목록 갱신
apt install -y nginx # 패키지 설치
nginx                # 패키지 실행
```

![실행 결과](images/chap01-46.png)
*그림 1-19: nginx 설치 및 실행*

nginx 실행 후 포트 확인을 위해 `net-tools`를 설치합니다.

**[실습]** net-tools를 설치하고 포트 상태를 확인하는 명령어입니다.

```bash
apt install -y net-tools
netstat -nlpt
```

![실행 결과](images/chap01-47.png)
*그림 1-20: 포트 상태 확인*

80 포트가 열려 있는 것을 확인할 수 있습니다. 브라우저에 `localhost:80`으로 접속하면 nginx 페이지가 응답합니다.

![실행 결과](images/chap01-48.png)
*그림 1-21: nginx 페이지 응답*

### 1.5.5 텍스트 편집 : vim

vim은 리눅스에서 흔히 사용되는 텍스트 편집기로, 서버 환경에서 설정 파일을 다룰 때 씁니다. 먼저 vim 패키지를 설치합니다.

**[실습]** vim 패키지를 설치하는 명령어입니다.

```bash
apt install -y vim
```

![실행 결과](images/chap01-vim.png)
*그림 1-22: vim 패키지 설치*

> 설치 도중 Geographic area와 Time zone을 선택하는 화면이 나타납니다. 이때 **Asia** , **Seoul** 을 각각 선택하면 됩니다.


vim의 핵심 사용 흐름은 다음과 같습니다.

| 단계 | 동작 | 키 |
|------|------|----|
| 1 | 파일 열기/생성 | `vim <파일명>` |
| 2 | 입력 모드 전환 | `i` |
| 3 | 내용 편집 | 자유롭게 입력 |
| 4 | 일반 모드로 복귀 | `ESC` |
| 5 | 저장 후 종료 | `:wq` 입력 후 Enter |

**[실습]** vim으로 파일을 생성하는 명령어입니다.

```bash
vim test1.txt   # test1.txt 파일 생성
```

생성된 파일에서 `i`를 눌러 입력 모드로 전환하고 내용을 작성한 뒤 `ESC` → `:wq`로 저장합니다.

![실행 결과](images/chap01-50.png)
*그림 1-23: vim 편집 화면*

`cat` 명령어로 파일 내용을 확인합니다.

**[실습]** 파일 내용을 출력하는 명령어입니다.

```bash
cat test1.txt   # 파일 내용 출력
```

![실행 결과](images/chap01-51.png)
*그림 1-24: 파일 내용 출력*

vim 명령 행 모드에서 `:q`는 종료, `:q!`는 저장하지 않고 강제 종료입니다.

### 1.5.6 프로세스 관리 : ps, kill

실행 중인 프로세스를 확인하고 불필요한 프로세스를 종료할 때 사용하는 명령어입니다.

| 명령어 | 설명 | 예시 |
|--------|------|------|
| `ps -ef` | 실행 중인 전체 프로세스 출력 | |
| `ps -ef \| grep <키워드>` | 특정 프로세스 검색 | `ps -ef \| grep nginx` |
| `kill <PID>` | 프로세스 안전 종료 (SIGTERM) | `kill 357` |
| `kill -9 <PID>` | 프로세스 강제 종료 (SIGKILL) | `kill -9 357` |


### 1.5.7 파일 검색과 로그 확인 : find, tail

설정 파일의 위치를 찾거나 로그 파일의 최근 내용을 확인할 때 사용하는 명령어입니다.

| 명령어 | 설명 | 예시 |
|--------|------|------|
| `find <경로> -name <파일명>` | 파일 이름으로 위치 검색 | `find / -name index.html` |
| `find <경로> -name <패턴>` | 패턴으로 검색 (`*` 사용) | `find / -name index*` |
| `tail <파일>` | 파일 마지막 10줄 출력 | `tail access.log` |
| `tail -n <숫자> <파일>` | 마지막 N줄 출력 | `tail -n 50 access.log` |

**[실습]** 파일 이름으로 위치를 검색하는 명령어입니다.

```bash
find / -name index.html   # index.html 파일 위치 검색
```

![실행 결과](images/chap01-54.png)
*그림 1-25: 파일 검색 결과*

리눅스 명령어가 익숙해졌으니 이제 컨테이너를 좀 더 자유자재로 다루는 법을 살펴보겠습니다.


## 1.6 컨테이너 : 생명주기와 옵션

### 1.6.1 exit vs detach : 빠져나올 때 살아있는 경우 vs 죽은 경우

실행 중인 컨테이너에서 빠져나오는 방법에 따라 컨테이너가 종료될 수도 있고 계속 살아있을 수도 있습니다.

#### 죽은 경우

다음 명령어로 컨테이너를 실행합니다. `--name` 옵션으로 컨테이너의 이름을 지정할 수 있습니다.

**[실습]** 이름을 지정하여 ubuntu 컨테이너를 실행하는 명령어입니다.

```bash
docker run -it --name dead ubuntu   # dead라는 이름의 ubuntu 컨테이너 실행
```

![실행 결과](images/chap01-28.png)
*그림 1-26: 컨테이너 실행*

컨테이너를 빠져나오기 위해 `exit`를 입력합니다.

**[실습]** exit로 빠져나온 후 컨테이너 상태를 확인하는 명령어입니다.

```bash
exit
docker ps   # 실행 중인 컨테이너 확인
```

![실행 결과](images/chap01-29.png)
*그림 1-27: exit 후 컨테이너 종료*

`exit` 명령어를 사용하면 컨테이너를 빠져나오는 동시에 프로세스가 종료됩니다.

#### 살아있는 경우

이번에는 살아있는 경우를 확인해 보겠습니다. 다음 명령어로 컨테이너를 실행합니다.

**[실습]** 새로운 ubuntu 컨테이너를 실행하는 명령어입니다.

```bash
docker run -it --name alive ubuntu   # alive라는 이름의 ubuntu 컨테이너 실행
```

![실행 결과](images/chap01-30.png)
*그림 1-28: alive 컨테이너 실행*

이번에는 `CTRL + P` 입력 후 `CTRL + Q`를 입력해 컨테이너를 빠져나옵니다.

프로세스를 유지한 채 빠져나오는 방법입니다.

**[실습]** 프로세스를 유지한 채 컨테이너에서 빠져나오는 단축키입니다.

```text
CTRL + P -> CTRL + Q
docker ps
```

이번에는 컨테이너를 빠져나와도 컨테이너가 그대로 실행됩니다.

![실행 결과](images/chap01-31.png)
*그림 1-29: 프로세스 유지 확인*

### 1.6.2 -dit : 백그라운드 인터랙티브 실행

`docker run` 사용 시에 `-dit` 옵션은 다음과 같습니다.

| 옵션 | 역할 |
|------|------|
| `-d` | 백그라운드 실행 (detached) |
| `-i` | 입력 가능한 상태 유지 (interactive) |
| `-t` | 터미널 환경 제공 (TTY) |
| `-dit` | 위 세 옵션을 조합하여 백그라운드에서 터미널 입력이 가능한 상태로 실행 |

#### -d 옵션

하나씩 실행해 보겠습니다. 먼저 nginx 컨테이너를 실행합니다.

**[실습]** -d 옵션으로 nginx를 백그라운드에서 실행하는 명령어입니다.

```bash
docker run -d nginx   # nginx 백그라운드 실행
docker ps             # 실행 중인 컨테이너 확인
```

![실행 결과](images/chap01-32.png)
*그림 1-30: nginx 백그라운드 실행*

`-d` 옵션으로 nginx 컨테이너를 실행하면 백그라운드에서 프로세스가 실행됩니다.

이번에는 ubuntu 컨테이너를 실행합니다.

**[실습]** -d 옵션으로 ubuntu를 실행하는 명령어입니다.

```bash
docker run -d ubuntu   # ubuntu 백그라운드 실행
docker ps              # 실행 중인 컨테이너 확인
```

![실행 결과](images/chap01-33.png)
*그림 1-31: ubuntu -d 실행 후 종료*

실행 중인 컨테이너 목록에 ubuntu가 없습니다.

ubuntu 컨테이너는 `-d` 옵션만 쓰면 백그라운드에서 실행되었다가 즉시 종료됩니다.

> Docker 컨테이너는 메인 프로세스가 살아있는 동안만 유지됩니다. nginx는 웹 서버이므로 요청을 기다리며 혼자서 계속 실행됩니다. 반면 ubuntu의 메인 프로세스는 `bash`(사용자 명령을 받아 실행하는 프로그램)입니다. bash는 사용자가 명령을 입력해야 동작하기 때문에, `-it` 옵션으로 터미널을 연결하지 않으면 할 일이 없어 즉시 종료됩니다.

#### -dit 옵션

`-dit` 옵션을 쓰면 어떻게 될까요?

**[실습]** -dit 옵션으로 백그라운드에서 실행하는 명령어입니다.

```bash
docker run -dit ubuntu   # ubuntu 백그라운드 + 인터랙티브 실행
docker ps                # 실행 중인 컨테이너 확인
```

![실행 결과](images/chap01-34.png)
*그림 1-32: ubuntu -dit 실행*

이번에는 ubuntu 컨테이너가 백그라운드에서 정상적으로 실행됩니다.

### 1.6.3 CMD : 컨테이너 시작 명령어 덮어쓰기

> **CMD(COMMAND)** 는 컨테이너가 시작될 때 실행되는 기본 프로세스를 정의하는 명령입니다. `docker run <이미지명> <CMD명령>`으로 직접 명령을 주면 `<CMD명령>` 옵션이 실행되며, 명령을 주지 않으면 이미지에 설정된 기본 CMD가 실행됩니다.

`sleep 1000`은 프로세스가 1000초 동안 대기하도록 만드는 명령입니다.

**[실습]** CMD 명령을 지정하여 ubuntu를 실행하는 명령어입니다.

```bash
docker run -d ubuntu sleep 1000   # sleep 명령으로 ubuntu 컨테이너 유지
docker ps                         # 실행 중인 컨테이너 확인
```

`sleep 1000`이 메인 프로세스가 되어 1000초 동안 대기하므로, ubuntu 컨테이너는 `-d` 옵션만으로도 종료되지 않고 유지됩니다.

![실행 결과](images/chap01-35.png)
*그림 1-33: CMD로 프로세스 유지*

### 1.6.4 attach : 실행 중인 컨테이너에 접근

실행 중인 컨테이너 내부로 접근하는 방법을 살펴보겠습니다. **attach** 와 **exec** 명령어를 씁니다.

> **attach 명령어** 는 현재 실행 중인 **메인 프로세스(PID 1)** 에 직접 접근하는 명령어입니다. `docker attach <컨테이너ID>` 명령어로 실행합니다.

<!-- image-prompt: Minimal black line drawing on white background, very few details, icon-like simplicity, 4:3 aspect ratio, 800x600px. With Korean labels: Diagram showing "docker attach" connecting directly to "메인 프로세스 (PID 1)" inside a container (labeled "컨테이너"), with a warning symbol (labeled "주의: 종료 시 컨테이너도 종료") indicating that exiting will stop the container -->

![attach 명령어의 동작 방식](images/chap01-36.png)
*그림 1-34: attach 명령어의 동작 방식*

ubuntu 컨테이너를 백그라운드로 실행합니다.

`attach` 명령어로 접근하면 ubuntu의 입력 터미널 창이 나타납니다.

**[실습]** attach 명령어로 실행 중인 컨테이너의 메인 프로세스에 접근하는 명령어입니다.

```bash
docker run -dit ubuntu  # ubuntu 백그라운드 실행
docker ps               # 실행중인 컨테이너 확인
docker attach d2b1      # attach로 접근
```

![실행 결과](images/chap01-38.png)
*그림 1-35: attach로 접근*

`attach` 명령어는 **메인 프로세스(PID 1)** 에 직접 연결되므로, 여러 터미널에서 접속해도 모두 같은 화면과 같은 프로세스를 공유합니다.

다만 이 상태에서 잘못 빠져나와 메인 프로세스를 종료하면 컨테이너 전체가 종료되니 주의해야 합니다.

`CTRL + P` 입력 후 `CTRL + Q`를 입력해 프로세스를 빠져나옵니다.

### 1.6.5 exec : 컨테이너에 새 프로세스로 접근

> **exec 명령어** 는 현재 실행 중인 메인 프로세스가 아닌, 메인 프로세스와 동일한 환경의 **새로운 프로세스** 를 생성하여 접근하는 방식입니다. `docker exec <옵션> <컨테이너ID> <CMD>` 명령어로 실행합니다.

<!-- image-prompt: Minimal black line drawing on white background, very few details, icon-like simplicity, 4:3 aspect ratio, 800x600px. With Korean labels: A box labeled "컨테이너" contains two gears side by side: left gear "메인 프로세스 (PID 1)", right gear "새로운 프로세스 (PID 9)". Outside the box on the left, a terminal icon with "docker exec 명령어" has an arrow that SKIPS the left gear (PID 1) and connects directly to the right gear (PID 9). Between the two gears, label "독립적인 프로세스" -->

![exec 명령어의 동작 방식](images/chap01-39.png)
*그림 1-36: exec 명령어의 동작 방식*

다음 명령어로 프로세스 내부에 접근합니다.

**[실습]** exec 명령어로 컨테이너 내부에 새 프로세스를 생성하여 접근하는 명령어입니다.

```bash
docker exec -it d2b1 bash   # 실행 중인 컨테이너에 새 bash 접속
```

![실행 결과](images/chap01-40.png)
*그림 1-37: exec로 접근*

`exec` 명령어로 프로세스에 접근한 뒤 새 터미널 창을 실행합니다.

![실행 결과](images/chap01-41.png)
*그림 1-38: 새 터미널 창 실행*

새 터미널 창에서 다음 명령어를 실행합니다. 컨테이너 내부에서 실행 중인 프로세스 정보를 출력합니다.

**[실습]** 컨테이너 내부에서 실행 중인 프로세스 목록을 출력하는 명령어입니다.

```bash
docker exec d2b1 ps aux   # 컨테이너 내부 프로세스 목록 확인
```

조회 결과에서 PID 1이 메인 프로세스이고 **PID 12** 가 `exec` 명령어로 접근할 때 생성된 프로세스입니다.

![실행 결과](images/chap01-42.png)
*그림 1-39: 프로세스 목록 확인*

`exec` 명령어로 실행된 프로세스는 **메인 프로세스(PID 1)** 에 영향을 주지 않고 독립적으로 명령을 실행합니다.

환경변수는 프로세스마다 따로 관리되므로, 메인 프로세스의 셸에서 추가한 환경변수는 `exec` 프로세스에서 보이지 않습니다.


## 1.7 이미지 : 직접 만들어보기

컨테이너를 실행하고 내부를 조작하는 법까지 익혔습니다. 컨테이너 안에서 작업한 내용을 다른 사람과 공유하려면 컨테이너를 이미지로 만들면 됩니다.

Tomcat 컨테이너를 직접 수정하고 그 상태를 이미지로 구워 보겠습니다.

### 1.7.1 Tomcat : 이미지 내려받기 & 실행하기

다음 명령어로 Tomcat 컨테이너를 실행합니다.

**[실습]** Tomcat 컨테이너를 실행하는 명령어입니다.

```bash
docker run -d -p 8080:8080 tomcat   # Tomcat 컨테이너 백그라운드 실행
```

![실행 결과](images/chap01-56.png)
*그림 1-40: Tomcat 컨테이너 실행*

`docker ps`로 실행 중인 Tomcat 컨테이너를 확인합니다. **컨테이너 ID** 는 `5fcd`입니다.

브라우저에 `localhost:8080`으로 접속하면 Tomcat이 응답한 화면이 나타납니다.

![실행 결과](images/chap01-58.png)
*그림 1-41: Tomcat 404 에러*

별도 컨트롤러가 없다면 슬래시(/)로 들어온 요청은 서버 내의 index.html로 응답합니다. Tomcat 이미지에 기본 index.html이 없으니 응답할 페이지가 없어 404 에러가 발생합니다.

### 1.7.2 Tomcat 컨테이너 수정 : index.html 만들기

Tomcat의 index.html 파일은 webapps/ROOT 폴더에 위치합니다. Tomcat 프로세스 내부로 접근해서 그 경로로 이동해 보겠습니다.

**[실습]** Tomcat 컨테이너 내부로 접근하는 명령어입니다.

```bash
docker exec -it 5fcd bash  # Tomcat 프로세스 연결
cd /usr/local/tomcat/webapps # webapps 경로 이동
```

> webapps 경로는 `find / -name webapps` 등으로 검색해 찾을 수 있습니다.

webapps 폴더에서 `ls` 명령어로 확인하면 내부가 비어 있습니다.

![실행 결과](images/chap01-61.png)
*그림 1-42: webapps 폴더 비어있음*

webapps 폴더에 ROOT 폴더를 만들고 그 안에 index.html 파일을 작성합니다.

index.html 파일을 생성하려면 vim 패키지를 설치해야 합니다. 다음 명령어로 패키지를 설치하고 vim 편집기를 실행합니다.

**[실습]** vim 패키지를 설치하고 index.html 파일을 생성하는 명령어입니다.

```bash
mkdir ROOT          # ROOT 폴더 생성
cd ROOT             # ROOT 폴더로 이동

apt update          # 패키지 최신화
apt install -y vim  # vim 패키지 설치
vim index.html      # index.html 파일 생성
```

편집기에서 `i` 키를 눌러 입력 모드로 전환하고, 내용 입력이 끝나면 `ESC`를 눌러 일반 모드로 돌아온 뒤 `:wq`로 저장합니다.

![실행 결과](images/chap01-64.png)
*그림 1-43: index.html 작성*

브라우저에서 `localhost:8080`으로 접속하면 방금 만든 index.html 페이지가 응답합니다.

![실행 결과](images/chap01-65.png)
*그림 1-44: index.html 응답 확인*

### 1.7.3 docker commit : 이미지 굽기

수정한 Tomcat의 이미지를 저장해 보겠습니다.

먼저 `CTRL + P` 입력 후 `CTRL + Q`를 입력해 컨테이너 프로세스를 빠져나옵니다.

다음 명령어로 commit을 실행합니다.

> **docker commit <컨테이너ID> <dockerhub아이디/이미지명:태그>** 형태로 명령어를 작성합니다. Dockerhub에서 계정과 리포지토리를 찾는 데 사용되므로, 본인의 Dockerhub 아이디로 변경해야 합니다.

**[실습]** 컨테이너의 현재 상태를 새 이미지로 저장하는 명령어입니다.

```bash
docker commit 5fcd <본인-dockerhub-id>/tomcat   # 컨테이너 현재 상태를 이미지로 저장
```

![실행 결과](images/chap01-67.png)
*그림 1-45: 이미지 커밋 완료*

### 1.7.4 docker push : Dockerhub에 저장

`docker login` 명령어로 Dockerhub에 로그인합니다.

**[실습]** Dockerhub에 로그인하는 명령어입니다.

```bash
docker login   # Dockerhub 로그인
```

Username과 Password를 입력한 뒤 ENTER를 누릅니다.

`docker push <이미지명>` 형태로 명령어를 실행하여 내 Dockerhub에 저장합니다.

**[실습]** 이미지를 Dockerhub에 업로드하는 명령어입니다.

```bash
docker push <본인-dockerhub-id>/tomcat   # 이미지를 Dockerhub에 업로드
```

![실행 결과](images/chap01-69.png)
*그림 1-46: 이미지 푸시 완료*

Dockerhub의 Repositories 탭에서 올린 이미지를 확인할 수 있습니다.

![실행 결과](images/chap01-70.png)
*그림 1-47: Dockerhub 저장소 확인*


## 1.8 마운트 : 컨테이너에 저장소 연결하기

컨테이너는 삭제하면 내부 데이터가 모두 사라지는 휘발성 구조입니다. 중요 데이터나 로그를 영구 저장하려면 마운트로 외부 저장소와 연결해야 합니다.

> **마운트(Mount)** 는 컨테이너 내부의 경로를 외부 저장소에 연결하는 기능입니다. 마운트를 사용하면 컨테이너가 삭제되어도 데이터는 외부에 그대로 남아 있습니다.

Docker는 두 가지 마운트 방식을 제공합니다. 로컬 PC의 폴더에 직접 연결하는 **바인드 마운트(Bind Mount)** 와 Docker가 관리하는 저장소를 사용하는 **볼륨 마운트(Volume Mount)** 입니다.

### 1.8.1 바인드 마운트 : 호스트 폴더를 직접 연결

> **바인드 마운트(Bind Mount)** 는 호스트 PC의 실제 폴더를 그대로 컨테이너 내부에 연결하는 방식입니다.

![바인드 마운트](images/bind-mount.png)
*그림 1-48: 호스트 PC의 폴더와 컨테이너 내부 폴더가 직접 연결*

#### 실습해보기

Ubuntu 환경에서 파일을 생성해 로컬 PC에 저장해 보겠습니다.

`docker run -it --mount type=bind,src=<로컬PC 경로>,dst=<컨테이너 경로> <이미지>` 형태로 명령어를 작성합니다.

**[실습]** 바인드 마운트를 설정하여 ubuntu 컨테이너를 실행하는 명령어입니다.

```bash
docker run -it --mount type=bind,src=C:/app/bind,dst=/app/bind ubuntu   # 바인드 마운트로 ubuntu 실행
```

![실행 결과](images/chap01-73.png)
*그림 1-49: 바인드 마운트 실행*

명령어를 실행하면 로컬 PC와 컨테이너 내부에 마운트한 `bind` 폴더가 생성됩니다.

**[실습]** app 폴더의 내부를 확인하는 명령어입니다.

```bash
ls /app
```

![실행 결과](images/chap01-74.png)
*그림 1-50: bind 폴더 확인*

`/app/bind` 폴더에 `a.txt` 파일을 생성합니다.

**[실습]** 마운트된 폴더에 파일을 생성하는 명령어입니다.

```bash
touch /app/bind/a.txt
```

![실행 결과](images/chap01-76.png)
*그림 1-51: 파일 생성 확인*

생성한 파일이 PC의 하드디스크에 저장됩니다.

![실행 결과](images/chap01-77.png)
*그림 1-52: 호스트 PC에 저장 확인*

실습 후 **exit** 명령어로 컨테이너를 빠져나옵니다.

### 1.8.2 볼륨 마운트 : Docker가 관리하는 저장소

> **볼륨 마운트(Volume Mount)** 는 Docker 엔진 내부의 전용 저장 공간(Volume)을 컨테이너 폴더와 연결하는 방식입니다.

![볼륨 마운트](images/volume-mount.png)
*그림 1-53: Docker 엔진이 관리하는 내부 저장 공간에 데이터 저장*

#### 실습해보기

다음 명령어로 현재 연결된 볼륨 정보를 확인합니다.

**[실습]** 현재 볼륨 목록을 확인하는 명령어입니다.

```bash
docker volume ls   # 볼륨 목록 확인
```

![실행 결과](images/chap01-80.png)
*그림 1-54: 볼륨 목록 조회*

연결된 볼륨이 없습니다. 다음 명령어로 볼륨이 연결된 컨테이너를 생성합니다.

`docker run -it --mount type=volume,src=<볼륨명>,dst=<컨테이너경로> <이미지>` 형태로 명령어를 실행합니다.

**[실습]** 볼륨 마운트를 설정하여 ubuntu 컨테이너를 실행하는 명령어입니다.

```bash
docker run -it --mount type=volume,src=metacoding-volume,dst=/app/volume ubuntu   # 볼륨 마운트로 ubuntu 실행
```

![실행 결과](images/chap01-81.png)
*그림 1-55: 볼륨 마운트 실행*

`/app/volume` 폴더가 자동으로 생성됩니다.

![실행 결과](images/chap01-82.png)
*그림 1-56: volume 폴더 생성*

`/app/volume` 폴더 내부에 `b.txt` 파일을 생성합니다.

**[실습]** 볼륨 마운트된 폴더에 파일을 생성하는 명령어입니다.

```bash
touch /app/volume/b.txt
```

![실행 결과](images/chap01-83.png)
*그림 1-57: b.txt 파일 생성*

`b.txt` 파일이 생성되었다면 볼륨에 저장된 것입니다.

`exit` 명령어로 컨테이너를 종료한 뒤 볼륨 정보를 확인합니다.

**[실습]** 컨테이너 종료 후 볼륨이 유지되는지 확인하는 명령어입니다.

```bash
exit
docker volume ls
```

![실행 결과](images/chap01-84.png)
*그림 1-58: 볼륨 유지 확인*

컨테이너는 종료되었지만 볼륨은 유지되고 있습니다.

새 컨테이너에 같은 볼륨을 연결해 보겠습니다.

**[실습]** 새로운 컨테이너에서 기존 볼륨의 데이터를 확인하는 명령어입니다.

```bash
docker run -it --mount type=volume,src=metacoding-volume,dst=/app/volume ubuntu   # 볼륨 마운트로 ubuntu 재실행
ls /app/volume
```

![실행 결과](images/chap01-85.png)
*그림 1-59: 볼륨 데이터 재사용*

새로 만든 컨테이너에서도 이전 컨테이너가 쓰던 볼륨의 데이터를 그대로 볼 수 있습니다. 볼륨이 컨테이너와 독립적으로 유지되기 때문입니다.

| 구분 | 바인드 마운트 | 볼륨 마운트 |
|------|------------|-----------|
| 저장 위치 | 호스트 PC의 지정 폴더 | Docker 엔진 내부 저장 공간 |
| 관리 주체 | 사용자 직접 관리 | Docker 엔진이 관리 |
| 경로 지정 | 절대 경로 필요 | 볼륨 이름만 지정 |
| 사용 사례 | 개발 중 소스 코드 공유, 설정 파일 연결 | DB 데이터 보존, 컨테이너 간 데이터 공유 |

## 이것만은 기억하자

- **상자에 담으면 어디서든 똑같다.** 말콤 맥린이 화물을 표준 컨테이너에 넣어 전 세계 어디든 보낸 것처럼, Docker는 애플리케이션을 컨테이너에 담아 어디서든 동일하게 실행합니다.
- **이미지는 레시피, 컨테이너는 요리.** 하나의 이미지로 여러 컨테이너를 만들 수 있고, 수정한 컨테이너는 `commit`으로 새 이미지를 만들어 Dockerhub에 공유할 수 있습니다.
- **마운트는 외부 USB.** 컨테이너가 사라져도 마운트로 연결한 데이터는 외부에 안전하게 남아있습니다.

컨테이너를 만들고 실행하는 것까지는 할 수 있게 되었습니다. 아직 남은 문제가 있습니다. 컨테이너를 새로 만들 때마다 같은 패키지를 수동으로 설치해야 하고, 사용자가 늘어도 서버 한 대뿐이라 트래픽을 분산할 방법이 없습니다. 여러 컨테이너를 하나씩 따로 실행하고 관리하는 것도 한계입니다.

다음 챕터에서는 이 문제들을 해결합니다. Dockerfile로 환경 구성을 자동화하고, NGINX로 트래픽을 분산합니다. Redis로 서버 간 세션을 공유하고, MySQL로 데이터를 영구 저장합니다. Docker Compose로 이 모든 컨테이너를 한 줄의 명령어로 띄우는 풀스택 웹사이트를 만들어 봅니다.

