tar cypzf backup.tgz --exclude=/lost+found --exclude=/backup.tgz -- exclude=/mnt --exclude=/sys/
dir tar cypzf backup.tgz --exclude=/lost+found --exclude=/backup.tgz --exclude=/mnt --exclude=/sys/
tar cypzf backup.tgz --exclude=/lost+found --exclude=/backup.tgz -- exclude=/mnt --exclude=/sys/
tar cypzf backup.tgz --exclude=/proc --exclude=/lost+found --exclude=/backup.tgz --exclude=/mnt --exclude=/sys /
tar cvpzf backup.tgz --exclude=/proc --exclude=/lost+found --exclude=/backup.tgz --exclude=/mnt --exclude=/sys --exclude=/opt/teamviewer/ /
service eslworking stop
vi /etc/init.d/eslworking
ln -s /home/instore/hanshow hanshow
mv shopweb-plugin-abm-auchan-20170607-3* software/
service eslworking start
tail -f eslworking.log
service eslworking stop
cp bin/tomcat-juli.jar ../store1/shopweb/bin
cd ../store1/shopweb/
vi /etc/init.d/shopweb1
chkconfig add shopweb1
chkconfig --add shopweb1
chmod +x /etc/init.d/shopweb1
/etc/init.d/shopweb1 start
vi /etc/init.d/shopweb1
service shopweb1 start
cd apache-tomcat-8.5.15/bin
export CATALINA_HOME=/home/instore/hanshow/apache-tomcat-8.5.15
cp -rf store1/shopweb/webapps/shopweb apache-tomcat-8.5.15/webapps/
vi /etc/init.d/shopweb1
vi /etc/init.d/shopweb1
service shopweb1 start
systemctl daemon-reload
./catalina.sh run
netstat -an | grep 8080
tail -f shopweb-core-info.log
cat shopweb-core-info.log | grep ERROR
chkconfig --level 234 shopweb1 on
service shopweb1 start
service eslworking start
cp /etc/init.d/shopweb1 /etc/init.d/integration
vi /etc/init.d/integration
service integration start
systemctl status integration.service
vi /etc/init.d/integration
vi /etc/init.d/shopweb1
systemctl daemon-reload
service integration start
ps -ef | grep integration
sh /home/instore/hanshow/integration/startup.sh
service integration start
systemctl daemon-reload
service integration start
cd /home/instore/hanshow/integration && java -Xms1024M -Xmx1024M -Djava.ext.dirs=lib com.hanshows.cdi.proxi.DataExtractor 1>/dev/null 2>&1
cd /home/instore/hanshow/integration && java -Xms1024M -Xmx1024M -Djava.ext.dirs=lib com.hanshows.cdi.proxi.DataExtractor
service integration start
vi /etc/init.d/integration
vi /etc/init.d/integration
service integration start
ps -ef | grep Data
cd log
tail -f proxi.log
vi proxi.log
cd ..
vi config.properties
history >>/home/instore/cmd.log
+++++++++++++++++++++++++++++
sudo nano /etc/sysconfig/network-scripts/ifcfg-eno1
sudo /etc/sysconfig/network-scripts/ifcfg-eno1
sudo gedit /etc/sysconfig/network-scripts/ifcfg-eno1
sudo nano /etc/sysconfig/network-scripts/ifcfg-eno1
open text file centos
sudo nano /etc/sysconfig/network-scripts/ifcfg-eno1
sudo vi /etc/sysconfig/network-scripts/ifcfg-eno1
sudo apt-get insta update
yum -y groups insta "GNOME Desktop"
sudo yum -y groups insta "GNOME Desktop"
sudo systemctl set-default graphical.target
uname --hardware-platform
tar -zxvf jdk-8u131-linux-x64.tar.gz
sudo mkdir /usr/local/java
sudo mv jdk-8u131-linux-x64.tar.gz /usr/local/java/
tar -zxvf jdk-8u131-linux-x64.tar.gz
sudo tar -zxvf jdk-8u131-linux-x64.tar.gz
sudo gedit ~/.bashrc
sudo vi /etc/profile
sudo gedit /etc/profile
cat /etc/profile
wget -O /home/instore/hanshow/tomcat8.tar.gz export JAVA_HOME=/usr/local/java/jdk1.8.0_131
export JRE_HOME=${JAVA_HOME}/jre
export CLASSPATH=.:${JAVA_HOME}/lib:${JRE_HOME}/lib
export  PATH=${JAVA_HOME}/bin:$PATH
wget -O /home/instore/hanshow/tomcat.tar.gz http://ftp.meisei-u.ac.jp/mirror/apache/dist/tomcat/tomcat-8/v8.5.15/bin/apache-tomcat-8.5.15.tar.gz
curl 127.0.0.1:8080
wget -O /home/instore/hanshow/boost.7z https://jaist.dl.sourceforge.net/project/boost/boost/1.63.0/boost_1_63_0.7z
yum –y insta p7zip
yum insta -y cmake make gcc gcc-c++
yum insta -y cmake
cd /etc/yum.repos.d/
cd shopweb-plugin-abm-auchan-20170607-3/
/user[Bjava -jar shopweb-plugin-abm-auchan-20170607-3.jar
cd shopweb-plugin-abm-auchan-20170607-3/
./java -jar shopweb-plugin-abm-auchan-20170607-3.jar
cd shopweb-plugin-abm-auchan-20170607-3/
sudo ./java -jar shopweb-plugin-abm-auchan-20170607-3.jar
./java -jar shopweb-plugin-abm-auchan-20170607-3.jar
/usr/local/java/jdk1.8.0_131/bin/java -jar shopweb-plugin-abm-auchan-20170607-3.jar
rpm -e --nodeps java-1.8.0-openjdk-headless-1.8.0.131-3.b12.el7_3.x86_64
sudo rpm -e--nodeps java-1.8.0-openjdk-1.8.0.131-3.b12.el7_3.x86_64
sudo rpm -qa|grep java
wget http://dev.mysql.com/get/mysql57-community-release-el7-8.noarch.rpm
yum localinsta mysql57-community-release-el7-8.noarch.rpm
sudo yum localinsta mysql57-community-release-el7-8.noarch.rpm
yum insta mysql-community-server
sudo yum insta mysql-community-server
systemctl start mysqld
systemctl mysqld status
sudo systemctl enable mysqld
grep 'temporary password' /var/log/mysqld.log
sudo systemctl restart mysqld
java -jar shopweb-plugin-abm-auchan-20170607-3.jar
lvcreate --size --snapshot --name snap /dev/vg00/lvol1
sudo lvcreate --size --snapshot --name snap /dev/vg00/lvol1
vi log/eslworking.log
tail -f log/eslworking.log
cd hanshow/eslworking-2.2.1/
tail -f log/eslworking.log
ssh root@192.168.1.104
./eslworking.sh run
./eslworking.sh stop
./eslworking.sh start
./eslworking.sh run
cd /etc/sysconfig/network-scripts/
vi ifcfg-eno1
cd /hanshow/apache-tomcat-8.5.15/bin
vi startup.sh
sudo vi /etc/rc.d/rc.local
mv jdk-8u131-linux-x64.tar.gz /hanshow/software/
sudo mv jdk-8u131-linux-x64.tar.gz /hanshow/software/
mv shopweb-plugin-abm-proxi-20170618.zip /hanshow/integration/
mv business_fields.properties /hanshow/apache-tomcat-8.5.15/webapps/shopweb/WEB-INF/classes/
cd component_script/
cd /hanshow/apache-tomcat-8.5.15/bin/
sudo chown instore:instore -R  apache-tomcat-8.5.15/
unzip shopweb-plugin-abm-proxi-20170618.zip
mv shopweb-plugin-abm-proxi-20170618 /hanshow/software/
unzip shopweb-plugin-abm-proxi-20170618.zip
mv shopweb-plugin-abm-proxi-20170618.zip /hanshow/software/
cd shopweb-plugin-abm-proxi-20170618/
mv business_fields.properties business_fields.properties.bak
mv  inits-config.js /hanshow/apache-tomcat-8.5.15/webapps/shopweb/hanshow-plugins-webpda/component_script/
cd /hanshow/apache-tomcat-8.5.15/bin/
mv /home/instore/inits-config.js /hanshow/apache-tomcat-8.5.15/webapps/shopweb/hanshow-plugins-webpda/component_script/
gedit config.properties
sudo chkconfig iptables off
sudo service iptables stop
cd /home/instore/
unzip template1.zip
cd template/
mv *.ttf /hanshow/eslworking-2.2.1/data/usr/fonts/
mv NORMAL_2*/ /hanshow/eslworking-2.2.1/data/usr/python/temp_json/
cd /hanshow/apache-tomcat-8.5.15/bin
vi startup.sh
sudo vi /etc/rc.d/rc.local
cd /hanshow/apache-tomcat-8.5.15/bin
sudo vi /etc/rc.d/rc.local
rpm -ivh google-chrome-stable_current_x86_64.rpm
sudo yum insta *b* -y
sudo yum insta libXss*  -y
sudo rpm -ivh google-chrome-stable_current_x86_64.rpm
chkconfig iptables off
sudo chkconfig iptables off
service iptables status
sudo vi  /etc/rc.d/rc.local
cat language.jsp
cat inits-config.js
cd /hanshow/integration/
cd shopweb-plugin-abm-proxi-20170618/
vi config.properties
cat ~/.bashrc
cd /usr/local/java/jdk1.8.0_131/
sudo rm -rf apache-tomcat-8.5.15/
cd /hanshow/eslworking-2.2.1/bin/
vi eslworking.sh
sudo cp eslworking.sh /etc/init.d eslworking
sudo mv eslworking.sh eslworking
sudo chkconfig --add eslworking
ping http://10.10.10.56/login
cd /hanshow/integration/
cd shopweb-plugin-abm-proxi-20170618/
cd /etc/init.d/
history >>/home/instore/cmd.log
