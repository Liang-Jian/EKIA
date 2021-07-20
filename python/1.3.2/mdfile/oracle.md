Oracle silent 11g


[root@localhost root]#dd if=/dev/zero of=/home/swap bs=1024 count=2097152
[root@localhost root]#mkswap /home/swap
[root@localhost root]#swapon /home/swap

[root@localhost root]#systemctl stop firewalld.service
[root@localhost root]#close selinux
[root@localhost root]
check package

32wei
#########
[root@localhost root]# rpm -q  binutils   compat-libstdc++-33   elfutils-libelf   elfutils-libelf-devel   expat   gcc   gcc-c++   glibc   glibc-common   glibc-devel   glibc-headers   libaio   libaio-devel   libgcc   libstdc++   libstdc++-devel   make   pdksh   sysstat   unixODBC   unixODBC-devel | grep "not installed" 
#########

64
#########
[root@localhost root]# rpm -q binutils compat-libcap1 compat-libstdc++-33 gcc gcc-c++ glibc glibc-devel ksh libaio libaio-devel libgcc libstdc++ libstdc++-devel libXi libXtst  make sysstat  unixODBC unixODBC-devel | grep "not installed"
#########

[root@localhost root]# vi /etc/redhat-release
redhat-4
Red Hat Enterprise Linux 6

[root@localhost root]# groupadd oinstall
[root@localhost root]# groupadd dba
[root@localhost root]# useradd -g oinstall -G dba oracle
[root@localhost root]# passwd oracle

更改用户 oracle 的密码 。
新的 密码：
无效的密码： 密码少于 8 个字符
重新输入新的 密码：
passwd：所有的身份验证令牌已经成功更新。
[root@localhost root]# id oracle
uid=1001(oracle) gid=1001(oinstall) 组=1001(oinstall),1002(dba)
[root@internal_pc /]# mkdir  /opt/oracle
[root@internal_pc /]# chown -R oracle:oinstall /opt/
[root@internal_pc /]# chmod -R 775 /opt/*
[root@localhost root]#vi /etc/syrootl.conf
fs.aio-max-nr = 1048576
fs.file-max = 6815744
kernel.shmall = 2097152
kernel.shmmax = 536870912
kernel.shmmni = 4096
kernel.sem = 250 32000 100 128
net.ipv4.ip_local_port_range = 9000 65500
net.core.rmem_default = 262144
net.core.rmem_max = 4194304
net.core.wmem_default = 262144
net.core.wmem_max = 1048576

[root@localhost root]#syrootl -p
[root@localhost root]# vi /etc/security/limits.conf
oracle           soft    nproc          2047
oracle           hard    nproc          16384
oracle          soft     nofile         1024
oracle          hard     nofile         65536
oracle          soft     stack          10240
[root@localhost root]# vi /etc/pam.d/login
session required /lib/security/pam_limits.so
session required pam_limits.so

[root@localhost root]# vi /etc/oraInst.loc
inventory_loc=/opt/oracle/oraInventory
inst_group=oinstall

[root@localhost root]# source /etc/oraInst.loc
[oracle@localhost database] vi db1_install.rsp
###########################
oracle.install.responseFileVersion=/oracle/install/rspfmt_dbinstall_response_schema_v11_2_0
oracle.install.option=INSTALL_DB_SWONLY
ORACLE_HOSTNAME=localhost.localdomain
UNIX_GROUP_NAME=oinstall
INVENTORY_LOCATION=/opt/oracle/oraInventory

SELECTED_LANGUAGES=en,zh_CN,zh_TW
ORACLE_HOME=/opt/oracle/product/11c/db_1
ORACLE_BASE=/opt/oracle
oracle.install.db.InstallEdition=EE
oracle.install.db.isCustomInstall=false
oracle.install.db.customComponents=oracle.server:11.2.0.1.0,oracle.sysman.ccr:10.2.7.0.0,oracle.xdk:11.2.0.1.0,oracle.rdbms.oci:11.2.0.1.0,oracle.network:11.2.0.1.0,oracle.network.listener:11.2.0.1.0,oracle.rdbms:11.2.0.1.0,oracle.options:11.2.0.1.0,oracle.rdbms.partitioning:11.2.0.1.0,oracle.oraolap:11.2.0.1.0,oracle.rdbms.dm:11.2.0.1.0,oracle.rdbms.dv:11.2.0.1.0,orcle.rdbms.lbac:11.2.0.1.0
,oracle.rdbms.rat:11.2.0.1.0
oracle.install.db.DBA_GROUP=dba
oracle.install.db.OPER_GROUP=oinstall
oracle.install.db.CLUSTER_NODES=
oracle.install.db.config.starterdb.type=GENERAL_PURPOSE
oracle.install.db.config.starterdb.globalDBName=orc1
oracle.install.db.config.starterdb.SID=dbsrv2
oracle.install.db.config.starterdb.characterSet=AL32UTF8
oracle.install.db.config.starterdb.memoryOption=true
oracle.install.db.config.starterdb.memoryLimit=
oracle.install.db.config.starterdb.installExampleSchemas=false
oracle.install.db.config.starterdb.enableSecuritySettings=true
oracle.install.db.config.starterdb.password.ALL=root
oracle.install.db.config.starterdb.password.SYS=
oracle.install.db.config.starterdb.password.SYSTEM=
oracle.install.db.config.starterdb.password.SYSMAN=
oracle.install.db.config.starterdb.password.DBSNMP=
oracle.install.db.config.starterdb.control=DB_CONTROL
oracle.install.db.config.starterdb.gridcontrol.gridControlServiceURL=
oracle.install.db.config.starterdb.dbcontrol.enableEmailNotification=false
oracle.install.db.config.starterdb.dbcontrol.emailAddress=email@something.com
oracle.install.db.config.starterdb.dbcontrol.SMTPServer=email@something.com
oracle.install.db.config.starterdb.automatedBackup.enable=false
oracle.install.db.config.starterdb.automatedBackup.osuid=
oracle.install.db.config.starterdb.automatedBackup.ospwd=
oracle.install.db.config.starterdb.storageType=
oracle.install.db.config.starterdb.fileSystemStorage.dataLocation=
oracle.install.db.config.starterdb.fileSystemStorage.recoveryLocation=
oracle.install.db.config.asm.diskGroup=
oracle.install.db.config.asm.ASMSNMPPassword=
MYORACLESUPPORT_USERNAME=
MYORACLESUPPORT_PASSWORD=
SECURITY_UPDATES_VIA_MYORACLESUPPORT=false
DECLINE_SECURITY_UPDATES=true
PROXY_HOST=
PROXY_PORT=
PROXY_USER=
PROXY_PWD=
##########################
[oracle@localhost database]$./runInstaller -silent -force -ignorePrereq -ignoreSysPrereqs -responseFile /home/oracle/database/response/db1_install.rsp

############
/opt/oracle/product/11c/db_1/root.sh
要执行配置脚本, 请执行以下操作:
	 1. 打开一个终端窗口
	 2. 以 "root" 身份登录
	 3. 运行脚本
	 4. 返回此窗口并按 "Enter" 键继续

Successfully Setup Software.
############



[root@localhost db_1]# ./root.sh
Check /opt/oracle/product/11c/db_1/install/root_localhost.localdomain_2017-09-
02_16-16-01.log for the output of root script

[oracle@internal_pc bin]$ ./netca -silent -responseFile /home/oracle/database/response/netca.rsp
****DISPLAY environment variable not set!
    Oracle Net Configuration Assistant is a GUI tool
    which requires that DISPLAY specify a location
    where GUI tools can display.
    Set and export DISPLAY, then re-run.

[root@internal_pc opt]# export DISPLAY=:0.0
[root@internal_pc opt]# xhost +
in this terwindows

[root@localhost bin]# ./netca -silent -responseFile /home/oracle/database/response/netca.rsp

正在对命令行参数进行语法分析:
参数"silent" = true
参数"responsefile" = /home/oracle/database/response/netca.rsp
完成对命令行参数进行语法分析。
Oracle Net Services 配置:
完成概要文件配置。
Oracle Net 监听程序启动:
    正在运行监听程序控制:
      /opt/oracle/product/11c/db_1/bin/lsnrctl start LISTENER
    监听程序控制完成。
    监听程序已成功启动。
监听程序配置完成。
成功完成 Oracle Net Services 配置。退出代码是0

[oracle@localhost bin]$ vi ~/.bash_profile
export ORACLE_HOME=/opt/oracle/product/11c/db_1
export ORACLE_SID=dbsrv2
export PATH=$ORACLE_HOME/bin:$PATH

[oracle@localhost bin]$ source  ~/.bash_profile

[oracle@localhost bin]$ ./lsnrctl start

LSNRCTL for Linux: Version 11.2.0.1.0 - Production on 02-SEP-2017 16:57:54

Copyright (c) 1991, 2009, Oracle.  All rights reserved.

TNS-01106: Message 1106 not found; No message file for product=network, facility=TNS	   [LISTENER]


[root@localhost var]# chown -R oracle:oinstall tmp/

restart
Alias                     LISTENER
Version                   TNSLSNR for Linux: Version 11.2.0.1.0 - Production
Start Date                02-SEP-2017 17:35:50
Uptime                    0 days 0 hr. 0 min. 0 sec
Trace Level               off
Security                  ON: Local OS Authentication
SNMP                      OFF
Listener Parameter File   /opt/oracle/product/11c/db_1/network/admin/listener.ora
Listener Log File         /opt/oracle/diag/tnslsnr/localhost/listener/alert/log.xml
Listening Endpoints Summary...
  (DESCRIPTION=(ADDRESS=(PROTOCOL=ipc)(KEY=EXTPROC1521)))
  (DESCRIPTION=(ADDRESS=(PROTOCOL=tcp)(HOST=localhost)(PORT=1521)))
The listener supports no services
The command completed successfully

start listen success

[oracle@localhost bin]$ vi dbcanew.rsp
#########################
[GENERAL]  
RESPONSEFILE_VERSION = "11.2.0"
OPERATION_TYPE = "createDatabase"  
[CREATEDATABASE]  
GDBNAME = "orcl"  
SID = "dbsrv2"  
TEMPLATENAME = "New_Database.dbt"  
SYSPASSWORD = "root"  
SYSTEMPASSWORD = "root"  
SYSMANPASSWORD = "root"  
DBSNMPPASSWORD = "root"  
DATAFILEDESTINATION ="/opt/oracle/oradata"  
STORAGETYPE=FS  
CHARACTERSET = "ZHS16GBK"  
DATABASETYPE = "MULTIPURPOSE"  
AUTOMATICMEMORYMANAGEMENT = "FALSE"
#########################
[oracle@localhost bin]$ ./dbca -silent -responseFIle /home/oracle/database/response/dbcanew.rsp
正在创建并启动 Oracle 实例
1% 已完成
3% 已完成




[oracle@localhost bin]$ ./sqlplus "/ as sysdba"


SQL> conn /as sysdba
Connected.
SQL> startup
ORA-01081: cannot start already-running ORACLE - shut it down first
SQL> shutdown abort;
ORACLE instance shut down.
SQL> startup;
ORACLE instance started.

Total System Global Area  534462464 bytes
Fixed Size		    2215064 bytes
Variable Size		  171967336 bytes
Database Buffers	  352321536 bytes
Redo Buffers		    7958528 bytes
Database mounted.
Database opened.

#手动启动Oracle
[oracle@localhost home]$ lsnrctl start

LSNRCTL for Linux: Version 11.2.0.1.0 - Production on 06-SEP-2017 17:41:17

Copyright (c) 1991, 2009, Oracle.  All rights reserved.

Starting /opt/oracle/product/11c/db_1/bin/tnslsnr: please wait...

TNSLSNR for Linux: Version 11.2.0.1.0 - Production
System parameter file is /opt/oracle/product/11c/db_1/network/admin/listener.ora
Log messages written to /opt/oracle/diag/tnslsnr/localhost/listener/alert/log.xml
Listening on: (DESCRIPTION=(ADDRESS=(PROTOCOL=ipc)(KEY=EXTPROC1521)))
Listening on: (DESCRIPTION=(ADDRESS=(PROTOCOL=tcp)(HOST=localhost)(PORT=1521)))

Connecting to (DESCRIPTION=(ADDRESS=(PROTOCOL=IPC)(KEY=EXTPROC1521)))
STATUS of the LISTENER
------------------------
Alias                     LISTENER
Version                   TNSLSNR for Linux: Version 11.2.0.1.0 - Production
Start Date                06-SEP-2017 17:41:19
Uptime                    0 days 0 hr. 0 min. 0 sec
Trace Level               off
Security                  ON: Local OS Authentication
SNMP                      OFF
Listener Parameter File   /opt/oracle/product/11c/db_1/network/admin/listener.ora
Listener Log File         /opt/oracle/diag/tnslsnr/localhost/listener/alert/log.xml
Listening Endpoints Summary...
  (DESCRIPTION=(ADDRESS=(PROTOCOL=ipc)(KEY=EXTPROC1521)))
  (DESCRIPTION=(ADDRESS=(PROTOCOL=tcp)(HOST=localhost)(PORT=1521)))
The listener supports no services
The command completed successfully
[oracle@localhost home]$ sqlplus /nolog

SQL*Plus: Release 11.2.0.1.0 Production on Wed Sep 6 17:41:37 2017

Copyright (c) 1982, 2009, Oracle.  All rights reserved.

SQL> conn /as sysdba
Connected to an idle instance.
SQL> startup
ORACLE instance started.

Total System Global Area  534462464 bytes
Fixed Size        2215064 bytes
Variable Size     167773032 bytes
Database Buffers    356515840 bytes
Redo Buffers        7958528 bytes
Database mounted.
Database opened.


#oracle服务自启动
[root@localhost bin]# vi /opt/oracle/product/11c/db_1/bin/dbstart
ORACLE_HOME_LISTNER=$1，修改为ORACLE_HOME_LISTNER=$ORACLE_HOME

[root@localhost bin]# vi /etc/oratab
dbsrv2:/opt/oracle/product/11c/db_1:N 修改为 Y

[root@localhost bin]# vi /etc/rc.d/rc.local
su - oracle -lc "/opt/oracle/product/11c/db_1/bin/lsnrctl start"
su - oracle -lc /opt/oracle/product/11c/db_1/bin/dbstart
