
### 设计思路
数据驱动、模版思想、设计模式
### 实现方式
1，所有的接口数据（Allflowdata: 服务器返回的所有数据)
2，每条的接口数据（casedata：数据以行为单位）
3，其他数据来源 （从sql或者其他方式获取的数据）
4，先从每行数据中取出来模板名字，然后根据模板名字，去单个接口和公共数据数据中取对应列数的数据。
（1）case数据中会用到allflowdata中的某个字段
（2）
5，数据处理，flow(data) 取整个流程中的数据，local(data) 取某一个key的值。发送拼接好所有的报文
6，执行结果发送，通过配置邮件信息发送定时报告。

### 结果展示
1，使用html展示报告  
2，通过率显示优化  
3，邮件发送

### 环境与依赖
1，Python3.6.8/3.7.5  or newlatest  
2，Pip version  
2，安装 : Python3 -m pip install -r piplist_win -i https://pypi.tuna.tsinghua.edu.cn/simple

### 结构介绍
 autobase--代码组成  
 autodata-records--单个case生成的html报告  
 autodata-resultfile--压缩records目录生成的 zip文件  
 autodata-template--模版文件  
 autodata-testcase--用例文件  
 configure--配置信息  
 logdisplay--log文件  
 msg--生成、返回的报文  
 test--测试方法

### 程序入口
ICaseEntityFlow.py

### 使用教程
baseinfo.yml 所有的配置项。


### 注意事项
1，建课时固定使用：在configure 目录下的datainfo.yml，在登录后查询建课所需要的信息。  
2，只有失败的case才会生成html报告。通过的不生成  
