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



### jdk  
```
sudo mkdir /usr/local/jdk
sudo gedit ~/.bashrc  
export JAVA_HOME=/usr/local/jdk
export JRE_HOME=${JAVA_HOME}/jre
export CLASSPATH=.:${JAVA_HOME}/lib:${JRE_HOME}/lib
export PATH=${JAVA_HOME}/bin:$PATH
source ~/.bashrc
sudo update-alternatives --install /usr/bin/java java /usr/local/jdk/bin/java 300
sudo update-alternatives --install /usr/bin/javac javac /usr/local/jdk/bin/javac 300
sudo update-alternatives --install /usr/bin/jar jar /usr/local/jdk/bin/jar 300
sudo update-alternatives --install /usr/bin/javah javah /usr/local/jdk/bin/javah 300
sudo update-alternatives --install /usr/bin/javap javap /usr/local/jdk/bin/javap 300
移除 openjdk包:<br>
sudo apt-get purge openjdk*
卸载 OpenJDK 相关包：<br>
sudo apt-get purge icedtea-* openjdk-*
检查所有 OpenJDK包是否都已卸载完毕<br>
dpkg --list |grep -i jdk
```
### static IPAddress
sudo vi /etc/network/interfaces
auto lo
iface lo inet loopback
auto eth0
iface eth0 inet static
address 192.168.1.103
netmask 255.255.255.0
gateway 192.168.1.1


### ubuntu change dns
sudo apt install resolvconf
sudo vi /etc/resolvconf/resolv.conf.d/base
nameserver 202.106.0.20
nameserver 202.16.196.115
sudo gedit /etc/NetworkManager/NetworkManager.conf
true
/etc/init.d/networking restart


####git 放弃修改，重置本地代码。
git fetch --all
git reset --hard origin/master
git pull
```
### kali Mysql使用普通用户
update user set plugin='' where user='root';
flush privileges;

###debian ssh
sudo apt-get install openssh-server
sudo vi /etc/ssh/sshd_config
sudo /etc/init.d/ssh restart
PermitRootLogin yes
PubkeyAuthentication no
AuthorizedKeysFile .ssh/authorized_keys
PasswordAuthentication yes

### 常用DNS服务器
168.95.192.1    168.95.192.2  
139.175.55.244  139.175.252.16  
203.80.96.9     203.80.96.10  #feiqi
202.106.0.20    202.16.196.115  
##static ip address
sudo vi /etc/network/interfaces
auto lo
iface lo inet loopback
auto eth0
iface eth0 inet static
address 192.168.2.233
netmask 255.255.255.0
gateway 192.168.2.254

### DNS
#### ubuntu
sudo vi /etc/resolvconf/resolv.conf.d/base
nameserver 202.106.0.20
nameserver 202.16.196.115
sudo gedit /etc/NetworkManager/NetworkManager.conf
true
/etc/init.d/networking restart

###debian
sudo apt-get install resolvconf
sudo vi /etc/network/interfaces
nameserver 168.95.192.1 168.95.192.2
/etc/init.d/networking restart

###debian不显示WiFi
打开新力得 Broadcom-sta-dkms inter
root@root:rfkill unblock all
reboot

###双系统删除linux
wget http://www.linuxidc.com/Linux/2007-11/8785.htm download MbrFix.exe
MbrFix /drive 0 fixmbr
You are about to Fix MBR,are you sure <Y/N>? Y
delete linux system



### centos ftp
vi /etc/selinux/config
SELINUX=disabled
useradd -d /var/ftp/ -s /sbin/nologin hans
passwd hans
vi /etc/vsftpd/vsftpd.conf

*vsftpd/ftpusers：位于/etc目录下。它指定了哪些用户账户不能访问FTP服务器，例如root等。
vsftpd/user_list：位于/etc目录下。该文件里的用户账户在默认情况下也不能访问FTP服务器，仅当vsftpd .conf配置文件里启用userlist_enable=NO选项时才允许访问*
*anonymous_enable=YES*
*local_enable=YES*
*write_enable=YES*
*local_umask=022*
*pam_service_name=vsftpd*
*userlist_enable=YES*
*tcp_wrappers=YES*
*ftp_username=hanshow*
*local_root=/var/ftp*
*anon_root=/var/ftp*j@11
chkconfig vsftpd on
ftp localhost

###debian 阿里源
deb http://mirrors.aliyun.com/debian/ jessie main non-free contrib
deb http://mirrors.aliyun.com/debian/ jessie-proposed-updates main non-free contrib
deb-src http://mirrors.aliyun.com/debian/ jessie main non-free contrib
deb-src http://mirrors.aliyun.com/debian/ jessie-proposed-updates main non-free contrib


###kali 源
deb http://mirrors.aliyun.com/kali kali-rolling main non-free contrib
deb-src http://mirrors.aliyun.com/kali kali-rolling main non-free contrib

###kali 数字签名错误
wget -q -O - https://archive.kali.org/archive-key.asc | apt-key add

###debian fcitx前段ui库(更新新系统后才可以用)
apt-get install fcitx-ui-classic && apt-get install fcitx-ui-light
apt-get install fcitx-googlepinyin
root@root:$ fcitx-configtool

###chrome隐私浏览
sudo vi /usr/bin/google-chrome
exec -a "$0" "$HERE/chrome" "$@" --incognito

###chrome安装包下载url
http://www.google.com/chrome/eula.html?hl=zh-CN&standalone=1
http://www.google.com/chrome/eula.html?hl=zh-CN&standalone=1&extra=devchannel

###安卓7.0/7.1消除感叹号
adb shell settings delete global captive_portal_server
adb shell settings put global captive_portal_detection_enabled 0
adb shell settings put global captive_portal_https_url https://www.google.cn/generate_204

###移除CNNIC证书
sudo gedit /etc/ca-certificates.conf
删除CNNIC
sudo update-ca-certificates

###硬盘格式EXT4分区
apt-get install gparted

###notepad++显示空格
视图(V) ⇒ 显示符号 ⇒ 显示空格与制表符

###python3 -- python3-pip install
python3 -m pip install *.* == version0
export ALL_PROXY=socks5://127.0.0.1:1080
wget https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py

###安装新力得包管理器
apt-get install synaptic


sudo vi /etc/default/atftpd
sudo sed -e 's/^USE_INETD=true/USE_INETD=false/g' -i /etc/default/atftpd
systemctl enable atftpd
systemctl restart atftpd

sudo apt install -y atftp  *atftp client*
echo "hell" | sudo tee /srv/tftp/hello.txt
win7 : tftp.exe -i 10.140.177.206 put jietu.py


### proxychains
sudo apt-get install proxychains
sudo vi /etc/proxychains.conf
socks 127.0.0.1 1080

### android_home
`export ANDROID_HOME=/home/root/Android/Sdk/home/root/sdk`
`export PATH=${JAVA_HOME}/bin:${ANDROID_HOME}/platform-tools:${ANDROID_HOME}/tools:$PATH`

###火狐浏览器配置
`root@root:~# firefox -ProfileManager -no-remote`

###更新火狐浏览器
ln -s /opt/firefox/firefox /usr/bin/firefox

###jetbrain修改背景色为绿色
File -> setting -> Editor -> Color&Fonts -> General -> Text -> Default text -> Background <br>
C7EDCC


### ssh 反弹shell
vi /etc/ssh/sshd_config
GatewayPorts yes

ssh -fCNR 9891:localhost:8920 root@118.25.78.198
ssh root@localhost -p7000


### ssh 服务器段超时设置###
vi /etc/ssh/sshd_config
ClientAliveInterval 600
ClientAliveCountMax 10
TCPKeepAlive yes

### ssh 无密码登录


### kali 笔记本设置
#####合上笔记本不休眠  
vi /etc/systemd/logind.conf
HandleLidSwitch=lock  


### mysql command
./mysqld --initialize --user=root --datadir=/usr/local/mysql/data  --basedir=/usr/local/mysql
./mysqld_safe --user=root &
vi /etc/my.cnf
```
[client-server]
[mysqld]
port=3306
datadir=/usr/local/mysql/data
#socket=/var/lib/mysql/mysql.sock
socket=/tmp/mysql.sock
# Disabling symbolic-links is recommended to prevent assorted security risks
symbolic-links=0

log-error=/var/log/sunpy.err
#pid-file=/var/run/mysqld/mysqld.pid
#user=root
lower_case_table_names = 1
```


### 环境变量
```
export JAVA_HOME=/usr/local/jdk 
export JRE_HOME=${JAVA_HOME}/jre 
export CLASSPATH=.:${JAVA_HOME}/lib:${JRE_HOME}/lib 
export PATH=${JAVA_HOME}/bin:$PATH 
export ANDROID_HOME=/home/joker/sdk 
export ANDROID_NDK=/home/joker/sdk/ndk-bundle
export GRADLE_HOME=/usr/local/gradle

export PATH=${JAVA_HOME}/bin:${GRADLE_HOME}/bin:${ANDROID_HOME}/platform-tools:${ANDROID_NDK}:${ANDROID_HOME}/tools:$PATH 
export ORACLE_SID=orcl 
export LD_LIBRARY_PATH=/home/joker/program/orcl
```

### Linux 添加任务实现自启动

```
[root@VM_0_7_centos ~]# crontab -l

[root@VM_0_7_centos ~]# vi autosshservice
# !/bin/bash
# chkconfig: 2345 80 90
# description:auto_run
# start auto connect script as tiaozhuan
ssh -fCNR 7000:localhost:22 root@118.25.78.198

[root@VM_0_7_centos ~]# crontab -e
0 0 * * * /usr/local/qcloud/YunJing/YDCrontab.sh > /dev/null 2>&1 &
# 每 3个小时10分启动一次sshautologin.sh
10 */3 * * * /etc/init.d/sshautologin.sh start
# 每 3个小时启动一次sshautologin.sh
0 */3 * * * /etc/init.d/autoreboot.sh start

rsync -vaz root@youservice:/home/joker/EKIA/ /home/joker/EKIA/
```

### Linux 开启bbr加速
`[root@centos ~]# wget --no-check-certificate https://github.com/teddysun/across/raw/master/bbr.sh`
```
[root@centos ~]# echo "net.core.default_qdisc = fq" >> /etc/sysctl.conf
[root@centos ~]# echo "net.ipv4.tcp_congestion_control = bbr" >> /etc/sysctl.conf
[root@centos ~]# sysctl -p 
net.ipv6.conf.all.disable_ipv6 = 0
net.ipv6.conf.default.disable_ipv6 = 0
net.ipv6.conf.lo.disable_ipv6 = 0
kernel.printk = 5
fs.file-max = 1000000
fs.inotify.max_user_instances = 8192
net.ipv4.tcp_syncookies = 1
net.ipv4.tcp_fin_timeout = 30
net.ipv4.tcp_tw_reuse = 1
net.ipv4.ip_local_port_range = 1024 65000
net.ipv4.tcp_max_syn_backlog = 16384
net.ipv4.tcp_max_tw_buckets = 6000
net.ipv4.route.gc_timeout = 100
net.ipv4.tcp_syn_retries = 1
net.ipv4.tcp_synack_retries = 1
net.core.somaxconn = 32768
net.core.netdev_max_backlog = 32768
net.ipv4.tcp_timestamps = 0
net.ipv4.tcp_max_orphans = 32768
net.ipv4.ip_forward = 1
net.core.default_qdisc = fq
net.ipv4.tcp_congestion_control = bbr
net.core.default_qdisc = fq
net.ipv4.tcp_congestion_control = bbr

查看是否开启
[root@centos ~]# sysctl net.ipv4.tcp_available_congestion_control
net.ipv4.tcp_available_congestion_control = reno cubic bbr
[root@centos ~]# sysctl net.ipv4.tcp_congestion_control
net.ipv4.tcp_congestion_control = bbr
```

### Linux 源码安装Python3
```
[root@centos Python37]# yum install gcc openssl-devel bzip2-devel libffi-devel -y
[root@centos Python37]# wget -o  https://www.python.org/ftp/python/3.7.9/Python-3.7.9.tgz
[root@centos Python37]# tar -xzf Python-3.7.9.tgz
[root@centos Python37]# ./configure --enable-optimizations
[root@centos Python37]# make altinstall
```


### 内网反弹
```
ras:
[root@VM-0-7-centos ~]# ./chisel client -v 118.25.78.198:6666 R:0.0.0.0:8888:10.9.104.2:22
service:
[root@centos Python37]# ./chisel server -p 6666 --reverse
host:
[root@centos Python37]# ssh -p 8888 root@118.25.78.198
```

### centos6添加自动启动
```
[root@VM-0-7-centos ~]# chmod +x /etc/rc.d/rc.local
[root@VM-0-7-centos ~]# vi /etc/rc.d/rc.local
/usr/local/qcloud/gpu/nv_gpu_conf.sh >/tmp/nv_gpu_conf.log 2>&1
/var/ftp/pub/chisel server -p 6666 --reverse
```



### centos配置密码安全策略
chattr -ia /var/spool/cron/root

vi /media/getloginip.sh
```
#!/bin/bash
#set -x
list=$(sudo lastb |awk '{print $3}'|sort |uniq -c|awk '{if ($1 >1 ) print $2}')
for ip in ${list}
do
	echo sshd: ${ip} >> /etc/hosts.deny #加入黑名单
	echo > /var/log/btmp
done
```
*/15 * * * * sudo bash /media/getloginip.sh

#### centos安装mongodb
```
[root@VM-0-7-centos ~]# wget -c https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-rhel70-6.0.5.tgz
[root@VM-0-7-centos ~]# tar -zxvf mongodb-linux-x86_64-rhel70-6.0.5.tgz
[root@VM-0-7-centos ~]# mv mongodb-linux-x86_64-rhel70-6.0.5/ mongodb/
[root@VM-0-7-centos ~]# cd /usr/local/ ; mkdir data logs
[root@VM-0-7-centos ~]# cd logs ; touch mongodb.log
[root@VM-0-7-centos ~]# cd ../bin/ ; vi mongodb.conf
# 数据文件存放目录
dbpath = /usr/local/mongodb/data
# 日志文件存放目录
logpath = /usr/local/mongodb/logs/mongodb.log
logappend=true
# 端口
port = 27017
# 以守护程序的方式启用，即在后台运行
fork = false
# 认证模式
auth=false
# 远程连接
bind_ip=0.0.0.0
[root@VM-0-7-centos ~]#  firewall-cmd --zone=public --add-port=27017/tcp --permanent
[root@VM-0-7-centos ~]#  systemctl restart firewalld.service
[root@VM-0-7-centos ~]# ./mongod -f mongodb.conf
