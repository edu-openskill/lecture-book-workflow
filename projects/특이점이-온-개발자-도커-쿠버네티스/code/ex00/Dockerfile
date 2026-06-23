FROM ubuntu:24.04                     
WORKDIR /app                           
COPY ./index.html ./index.html         
RUN apt update && apt install -y vim   
CMD ["/bin/bash"]                      
ENTRYPOINT ["echo", "컨테이너 실행"]     