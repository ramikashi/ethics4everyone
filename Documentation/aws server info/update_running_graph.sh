#!/bin/bash

tar -xvf flask-nginx5.tar
docker cp flask-nginx:/var/log/nginx/access.log ~/logs/nginx/access_temp.log
docker cp flask-nginx:/var/log/nginx/error.log ~/logs/nginx/error_temp.log
mv ~/logs/nginx/access.log ~/logs/nginx/access_old.log
cat ~/logs/nginx/access_old.log ~/logs/nginx/access_temp.log > ~/logs/nginx/access.log
mv ~/logs/nginx/error.log ~/logs/nginx/error_old.log
cat ~/logs/nginx/error_old.log ~/logs/nginx/error_temp.log > ~/logs/nginx/error.log
docker stop flask-nginx
docker rm flask-nginx
docker rmi flask-nginx-img
docker build -t flask-nginx-img flask-nginx5
rm -r flask-nginx5
docker run -p 80:80 --name flask-nginx flask-nginx-img
