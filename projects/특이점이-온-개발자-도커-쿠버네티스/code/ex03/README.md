## 실행 명령어

### 사용자 정의 네트워크 생성 (이미 있으면 생략)

- docker network create ex03-network

### api 서버 실행

- docker build -t api ex03/api
- docker run -dit --name api --network ex03-network api

### nginx 실행

- docker build -t nginx-cache ex03/nginx
- docker run -dit --name nginx-cache --network ex03-network -p 80:80 nginx-cache

### 실행

- http://localhost:80
- http://localhost:80/image.png
