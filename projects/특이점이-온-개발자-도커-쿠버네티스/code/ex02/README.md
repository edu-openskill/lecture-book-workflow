## 실행 명령어

### 사용자 정의 네트워크 생성

- docker network create ex02-network

### 서버(app1) 컨테이너 2대 생성

- docker build -t app1 ex02/app1
- docker run -dit --name app1-1 --network ex02-network app1
- docker run -dit --name app1-2 --network ex02-network app1

### nginx 실행

- docker build -t lb ex02/lb
- docker run -dit --name lb --network ex02-network -p 80:80 lb

### 실행

- http://localhost:80/app1
