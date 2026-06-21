FROM ubuntu:24.04                      # 베이스 이미지
WORKDIR /app                           # 작업 디렉토리 설정
COPY ./index.html ./index.html         # 로컬의 index.html을 컨테이너의 /app으로 복사
RUN apt update && apt install -y vim   # vim 패키지 설치
CMD ["/bin/bash"]                      # ubuntu의 기본 프로세스
ENTRYPOINT ["echo", "컨테이너 실행"]     # 컨테이너 시작 시 echo 실행
