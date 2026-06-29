#!/bin/bash

git clone https://github.com/metacoding-10-linux-docker/backend-redis-server 

cd backend-redis-server

chmod +x gradlew 

./gradlew build  

java -Dspring.profiles.active=prod -jar build/libs/*.jar