## Centos 7.5 command

#### 安装unzip
[root@VM-0-7-centos ~]# yum install -y unzip


### 添加frp内网
```
[root@VM-0-7-centos ~]# vi /etc/rc.local
#!/bin/bash
# test auto run
/media/chisel server -p 6666 --reverse
./media/chisel client -v {{publicip}}:6666 R:0.0.0.0:8888:192.168.2.174:22
```


### 树莓派开机自动启动脚本
[root@centos Python37]# vi /etc/rc.local  
在exit 0前写入：
./home/pi/start.sh &


#### 树莓派镜像
https://downloads.raspberrypi.org/raspios_full_armhf/images/raspios_full_armhf-2021-05-28/2021-05-07-raspios-buster-armhf-full.zip





#### 修改主机名
joker@raspberrypi:~/EKIA $ sudo vi /etc/hosts
joker@raspberrypi:~/EKIA $ sudo vi /etc/hostname


#### 自启动脚本
30 22 * * * /etc/init.d/auto.sh start
