## 실행 명령어

### 서버 1 실행

- docker build -t app1 ex01/app1
- docker run -dit -p 8000:80 app1

### 서버 2 실행

- docker build -t app2 ex01/app2
- docker run -dit -p 9000:80 app2

### nginx 실행

- docker build -t lb ex01/lb
- docker run -dit -p 80:80 lb

### 실행

- http://localhost:80/app1
- http://localhost:80/app2
