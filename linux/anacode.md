### ancoda 命令
#####
新建一个环境
conda create --name tensotflow python=3.7 

#####
(base) [root@mycentos ~]# conda info --envs
# conda environments:
#
base                  *  /home/joker/anaconda3
tensotflow               /home/joker/anaconda3/envs/tensotflow



###进入到anacona
(base) [root@mycentos ~]# source activate tensotflow
(tensotflow) [root@mycentos ~]# 


####
搜索tensorflow环境

(tensotflow) [root@mycentos ~]#  anaconda search -t conda tensorflow


####安装
conda install --channel https://conda.anaconda.org/jjhelmus tensorflow==1.8.0
