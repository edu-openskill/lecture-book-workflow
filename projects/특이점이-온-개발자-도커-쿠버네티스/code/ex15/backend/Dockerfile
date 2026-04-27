FROM eclipse-temurin:21-jdk

WORKDIR /var/current/app

COPY entrypoint.sh /entrypoint.sh

RUN apt-get update && apt-get install -y git

ENTRYPOINT ["/entrypoint.sh"]
