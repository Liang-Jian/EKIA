## Centos 7.5 command

#### 安装unzip
[root@VM-0-7-centos ~]# yum install -y unzip


### 添加自动启动命令
```
[root@VM-0-7-centos ~]# vi /etc/rc.local
#!/bin/bash
# test auto run
/media/chisel server -p 6666 --reverse
./media/chisel client -v {{publicip}}:6666 R:0.0.0.0:8888:192.168.2.174:22
```

## 树莓派脚本
#### auto reboot
```
sudo vi /etc/crontab
1 */4   * * *   root    reboot  # 每隔4小时1分重启s
```


#### 树莓派镜像
https://downloads.raspberrypi.org/raspios_full_armhf/images/raspios_full_armhf-2021-05-28/2021-05-07-raspios-buster-armhf-full.zip


#### smb.conf末尾添加以下内容
[jk]
path = /smb
valid users = joker
writeable=Yes
create mask=0777
directory mask=0777
public=no


#### 修改主机名
joker@raspberrypi:~/EKIA $ sudo vi /etc/hosts
joker@raspberrypi:~/EKIA $ sudo vi /etc/hostname


#### 自启动脚本
30 22 * * * /etc/init.d/auto.sh start



javascript:document.body.contentEditable='true';document.designMode='on'; void 0