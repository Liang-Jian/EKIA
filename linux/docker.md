# docker command ###

###
1, first pull program 
`[root@mycentos ~]# dcocker pull nginx:latest`

2, chakan images   
`[root@mycentos ~]# docker images`

3,qidong docker images  
`[root@mycentos ~]# docker run --name nginx-test -p 80:80 -d nginx`

4,peizhi ngnxi canshu 


5,jin ru docker bash   
`[root@mycentos ~]# docker exec -it cf846306dbea /bin/bash`

6,chakan docker
```[root@mycentos ~]# docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                NAMES
cf846306dbea        nginx               "/docker-entrypoin..."   4 days ago          Up 4 days           0.0.0.0:80->80/tcp   nginxt
```
7,stop docker service   
`[root@mycentos ~]# docker stop cf`

8,shanchu id=d4 de images  
`[root@mycentos ~]# docker rmi d43ad45d223b`

[root@mycentos ~]# docker run --name docker-test   -d  -p 80:80 \
  -v /data/nginx/log:/var/log/nginx  \
  -v /data/ngnix/conf/nginx.conf:/etc/nginx/nginx.conf \
  -v /data/ngnix/conf.d:/etc/nginx/conf.d  \
  -v /data/ngnix/html:/usr/share/nginx/html \
  nginx


9,check image status
`[root@mycentos ~]# docker container ls`