# docker command ###

###
1, first pull program 
`[root@mycentos ~]# docker pull nginx:latest`

2, chakan images   
`[root@mycentos ~]# docker images`

3,qidong docker images  
`[root@mycentos ~]# docker run --name nginx-test -p 80:80 -d nginx`

4,peizhi ngnxi canshu 


5,jin ru docker bash   
`[root@mycentos ~]# docker exec -it cf846306dbea /bin/bash`

6,chakan docker
```[root@mycentos ~]# docker ps -a
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                NAMES
cf846306dbea        nginx               "/docker-entrypoin..."   4 days ago          Up 4 days           0.0.0.0:80->80/tcp   nginxt
```
7,stop docker service   
`[root@mycentos ~]# docker stop cf`

8,shanchu id=d4 de images  
`[root@mycentos ~]# docker rmi d43ad45d223b`

[root@mycentos ~]#docker run --name nginxj0k -d -p 80:80 -v /home/joker/ngnx_web:/usr/share/nginx/html -v /home/joker/ngnx_web/nginx/conf.d:/etc/nginx/conf.d  -v /home/joker/ngnx_web/nginx/log:/var/log/nginx  -v /home/joker/ngnx_web/nginx/conf/nginx.conf:/etc/nginx/nginx.conf nginx
9,check image status  
`[root@mycentos ~]# docker container ls`


### docker install v2ray
1,centos install docker 
yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
yum install docker-ce

2,create log conf folder
```
[root@mycentos ~]# vi /etc/v2ray/config.json
[root@mycentos ~]# mkdir /var/log/v2ray /etc/v2ray
[root@mycentos ~]# systemctl start docker.service
[root@mycentos ~]# systemctl status docker.service
[root@mycentos ~]# docker pull v2ray/official
[root@mycentos ~]# docker images
```
3,docker start v2ray --first  
`[root@mycentos ~]# docker run -d --restart=always --name v2ray -v /etc/v2ray:/etc/v2ray -p 55535:55535 v2ray/official  v2ray -config=/etc/v2ray/config.json`
4,docker stop ronqqi  
`[root@mycentos ~]# docker stop {CONTAINER ID}`

4,docker chakan stop ronqqi  
`[root@VM_0_7_centos v2ray]# docker ps -a`

4,docker start rongqi  
`[root@VM_0_7_centos v2ray]# docker start {CONTAINER ID}`

5，docker start trojan
`[root@VM_0_7_centos v2ray]# docker pull teddysun/trojan`

5,chan kan wangluo suanfa   
`root@centos:/home/joker# sysctl net.ipv4.tcp_congestion_control
net.ipv4.tcp_congestion_control = cubic`

5,start bbr suanfa 
```
sudo bash -c 'echo "net.core.default_qdisc=fq" >> /etc/sysctl.conf'
sudo bash -c 'echo "net.ipv4.tcp_congestion_control=bbr" >> /etc/sysctl.conf'
sudo sysctl -p
```