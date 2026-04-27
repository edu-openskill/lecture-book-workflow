## 실행 명령어

### api 서버 실행

docker build -t api ex03/api
docker run -dit -p 5000:5000 api

### nginx 실행

docker build -t nginx-cache ex03/nginx
docker run -dit -p 80:80 nginx-cache

### 실행

- http://localhost:80
- http://localhost:80/image.png
