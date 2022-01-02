## Centos 7.5 command

#### 安装unzip
[root@VM-0-7-centos ~]# yum install -y unzip


### 添加自动启动命令
```
[root@VM-0-7-centos ~]# chmod +x /etc/rc.d/rc.local
[root@VM-0-7-centos ~]# vi /etc/rc.d/rc.local
#!/bin/bash
# test auto run
/media/chisel server -p 6666 --reverse
```

## 树莓派脚本
####
```

```