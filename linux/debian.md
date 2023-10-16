## debian Ubuntu kali smp


#### 安装树莓派smb
```
sudo apt-get install samba
sudo apt-get install samba-common-bin
```

#### smb.conf末尾添加以下内容
[smb]
path = /smb
browsable =yes
writable = yes
guest ok = yes
read only = no
create mask=0777
directory mask=0777
public = yes


#### 修改主机名
joker@raspberrypi:~/EKIA $ sudo vi /etc/hosts
joker@raspberrypi:~/EKIA $ sudo vi /etc/hostname


#### 树莓派镜像
https://downloads.raspberrypi.org/raspios_arm64/images/raspios_arm64-2021-05-28/

#### 树莓派周二定时重启
```
sudo vi /etc/crontab
1 1 * * 2   root    reboot
55 23 * * * /usr/bin/python3 /home/jleague.py
```

#### 挂载U盘
```
sudo mount -t vfat /dev/sda1 /mnt/usb/
sudo umount /dev/sda1
```

#### 树莓派修改时区
sudo dpkg-reconfigure tzdata


#### frp config
```frpc
[common]
server_addr = 101.101.81.174
server_port = 6666
token = 1234556 

[ssh]
type = tcp
local_ip = 127.0.0.1
local_port = 22
remote_port = 8888

frps

[common]
bind_port = 6666
token = 1234556 

# frp管理后台端口，请按自己需求更改
dashboard_port = 5000
# frp管理后台用户名和密码，请改成自己的
dashboard_user = admin
dashboard_pwd = admin
enable_prometheus = true

# frp日志配置
log_file = /var/log/frps.log
log_level = info
log_max_days = 3


```

#### 树莓派启动内网frp
```
[root@VM-0-7-centos ~]# vi /etc/init.d/start.sh
#!/bin/bash
### BEGIN INIT INFO
# Provides:          frpstart
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: start frpc
# Description:       start frpc
### END INIT INFO

sleep 15

./var/frpc -c /var/frpc.ini &
echo 'success' >> /media/test.txt
exit 0

```
#### sh文件加到自启
```

sudo chmod a+x start.sh 
sudo update-rc.d start.sh defaults
```


#### 安装蓝牙
```
apt-get install blueman
service bluetooth start
```


#### git 配置
```
sudo apt-get install git  
git init  
git config --global user.name  "QQ"  
git config --global user.email "\*@gmail.com"  
ssh-keygen -C 's@gmail.com' -t rsa  
cat ~/.ssh/id_rsa.pub  
ssh -T git@github.com  
git clone git@192.168.5.95:lzhang/PublicDocument.git  
git remote add origin git@github.com:billfeller/historyBrowsing.git  

Agent admitted failure to sign using the key"  
eval "$(ssh-agent -s)"  
ssh-add
```

###kali ftp安装
```
sudo apt install vsftpd  
sudo netstat -antup |grep ftp
tcp6       0      0 :::21                   :::*                    LISTEN      1196/vsftpd  
sudo vi  /etc/vsftpd/  


#禁止匿名登录FTP服务器
anonymous_enable=NO
#允许本地用户登录FTP服务器
local_enable=YES
#设置本地用户登录后所在的目录
local_root=/srv/ftp/pi
#写权限
write_enable=YES
#全部用户被限制在主目录
chroot_local_user=YES
#启用例外用户名单
chroot_list_enable=YES
#指定例外用户列表，这些用户不被锁定在主目录
chroot_list_file=/etc/chroot_list#主目录可写权限allow_writeable_chroot=YES
#配置其他参数
allow_writeable_chroot=YES
local_umask=022
dirmessage_enable=YES
xferlog_enable=YES
connect_from_port_20=YES
xferlog_std_format=YES
listen=YES
pam_service_name=vsftpd
tcp_wrappers=YES
```

###右键终端(ubuntu)
sudo apt-get install nautilus-open-terminal


#### 安装 rz sz
sudo apt-get install lrzsz


#### 修改/etc/passwd 改默认权限
pi:x:0:0::/home/pi:/bin/bash


#### 树莓派修改 
pi@centos:~ $ echo /opt/vc/lib > pi_vc_core.conf
pi@centos:~ $ sudo chown root.root pi_vc_core.conf
pi@centos:~ $ sudo mv pi_vc_core.conf /etc/ld.so.conf
pi@centos:~ $ sudo ldconfig
pi@centos:~ $ ldconfig -p | grep libmmal
	libmmal_vc_client.so (libc6) => /opt/vc/lib/libmmal_vc_client.so
	libmmal_util.so (libc6) => /opt/vc/lib/libmmal_util.so
	libmmal_core.so (libc6) => /opt/vc/lib/libmmal_core.so
	libmmal_components.so (libc6) => /opt/vc/lib/libmmal_components.so
	libmmal.so (libc6) => /opt/vc/lib/libmmal.so
