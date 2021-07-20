# esl-working 0.99 版本新增功能说明
## 配置文件说明
### system
	1. dot_temp_file = ./temp_json/esl_temp.txt
		* 点阵模板所在的路径; ./temp_json/
		* 点阵模板的名字 esl_temp.txt (名字和我们创建的模板名需要一致)
	2. dot_temp_dir  = ./temp_json/
	    * json 模板所在的目录
    	* json 模板格式- 用模板生产工具会产生一个压缩包或者文件夹 文件夹名就是模板名
			需要填充到opt4字段里 只需将其解压(针对压缩包)或者复制(文件夹)到这个目录里即可
	3.temp_json = no
		* 是否使用json模板 值为yes 或 no
		* 当为yes的时候,dot_temp_dir 一定要有个合法的路径
	4. 建议:
  		这些配置不要更改,直接往对应的目录里放文件(模板)

#### debug_lever
	1.  -对比log文件-
	2.  error : 只输出错误信息,其他信息一概不输出
	3.  info  : 输出一些必要的信息 python信息 (info的信息 + error信息)
	4.  debug : 输出的信息最全 会输出一些xml等信息

### htp
	1. internal_ftp = yes
		该值为 yes 或 no
			* yes 启用内置ftp, no将使用外部的ftp
				** 内置ftp意思是我们价签系统(python工程自带的ftp)
			* 外置的意思是: 比如之前我们部署过 filezilla vsftpd 等ftp服务器
			* 采用内置我们将不必部署想vsftpd 这样复杂的ftp服务器
	2. ftp_server = 127.0.0.1
		* ftp服务器的ip地址 采用本地回环地址说明ftp服务器就在本机上
		* 如果非本机 ip地址要指向对应的ftp服务器的地址
		* 注: 内置ftp服务器 直接用该地址即可
		    外置的服务器如果部署在本机即是此地址 当ftp服务器不在本机时需要修改
	3. ftp_user = hanshow
		* ftp用户名
	4. ftp_pass = hanshow
		* ftp密码
	5. ftp_port = 9005
		* ftp 端口

	注: 采用内置时,用户名 密码 和端口 可以任意更改 并且重启有效 
			内置ftp端口号请不要用5000以下的端口号 避免和操作系统某些端口重复
		如果使用通用的ftp服务器 如 filezilla 和 vsftpd 端口号都必须配置成21


##数据库

###OP3: 价签通讯类型 比如HS_SA_3002 HS_EL_5032 等
		1. 段码新增价签 如HS_PL_XXX , HS_EL_5007_1 其通讯参数都为HS_EL_5033
		2.	点阵价签一律为 HS_EL_5103
		3.	具体有其他新品 会在新版本中说明
###OP4: 模板名称
		1. 点阵(非json): 比如TEMP_DO_20
		2.	点阵(json): 就是json包的名字 比如 el219
		3.	段码: normal 等 其原理和 点阵非json的一样

###OP5: 价签通讯所需要的一些参数
		点阵举例
			"max_package":512, // 最大包数  *
			"flash_size":16, // 价签flash_size *
			"version":1, // 版本号 *
			"screen_type":"HS_EL_5033",//屏幕类型
			"resolution_x":296, // x最大值 *
			"resolution_y":128, // y 最大值 *
			"resolution_direction":0, // 旋转方向 0: 0度  1: 90度  2: 180度 3:270度 *
			"wid":"55-66-77-66", //组网前wakeupId 
			'chn':77 //channel  组网前的chn 
		段码举例
			"version":1,
			"screen_type" : "HS_SA_3002",

## seg配置文件

### esl_conf.ini
	此文件应关心的有 : 模板名, 是否不显示原价, 属性

	"normal":{
		"title" : ["Price", "Price1",  "salesno"],
		"Price" : {"format":"16s","check_fun":"check_price","maxlen":6},
		"Price1":{"format":"16s", "check_fun":"empty_with_zero","maxlen":6},
		"flags":{"format":"H","check_fun":"int","maxlen":2,"flag":["originalPrice","500g","ST","SN"]},
		"salesno":{"format":"16s", "check_fun":"str","maxlen":15}, 
		"check_key":["Price1","Price2"]
	},
	"normal"; 模板名 即OP4字段的内容
	严重注意:
		修改此文件时应该先备份,防止再改回时出现错误.

#### 段码属性表
	"seg_display_propertis":{
					"default_temp" : {"promo":0, "originalPrice":3, "arrow_5032":5, "black_ground":7, "500g":8, "1000g": 9, "sn":15}, 
					"HS_EL_3002" : {"promo":0, "discount":1, "originalPrice":3, "currentPrice":4, "upArrow":5, "downArrow":6,	"twinkle":7, "new_product":14, "clearance":15}, 
					"HS_EL_5031" : {"promo":0, "originalPrice":3, "arrow_5032":5, "black_ground":7, "500g":8, "1000g": 9, "sn":15}, 
					"HS_EL_5032" : {"promo":0, "originalPrice":3, "arrow_5032":5, "black_ground":7, "500g":8, "1000g": 9, "sn":15}, 
					"HS_EL_5033" : {"promo":0, "originalPrice":3, "arrow_5032":5, "black_ground":7, "500g":8, "1000g": 9, "sn":15}, 
					"HS_EL_5007_1" : {"promo":0, "originalPrice":3,"promo_reverse":7, "500g":8, "1000g": 9,"ST":14, "SN":15}, 
					"HS_PL_3002":	{"promo":0,"flash":7,"each":8,"l":9,"kg":10,"lb":11,"R":12,"F":13},
					"HS_SA_3002":	{"promo":0,"flash":7,"each":8,"l":9,"kg":10,"lb":11,"R":12,"F":13},
					"HS_PL_5002" : {"promo":0, "black_ground":7,"ZA":8, "l":9,"kg":10,"szt":11,"money_currency":12}, 
					"HS_SN_3002" : {"twinkle":7}
	}
	
	每个价签都有特有的属性 该属性表现在屏幕上就是:
		原价 现价 sn 促销 箭头等显示效果
	如: "promo":0 
		promo:
			代表的含义是促销 该字段可以任意改名 只要自己明白就行了.
		0:
			具体的段位信息,硬件固定死的,不能修改
#### 属性添加

		"flags":{"format":"H","check_fun":"int","maxlen":2,"flag":["originalPrice","500g","ST","SN"]},
		想显示申明属性只需将上边的属性表里的属性字段填到flag里,注意格式最后一个属性后边不能用逗号, 是json格式要求的

		注意: 对应屏幕类型的价签需要去其对应属性表里找
		如5033的flag 不能填成5007的

#### check_fun 可选项 
	以price为例
	"check_price" :
		如果price没有小数点,会在其后边填上两位0,如 123--> 123.00
		如果有小数点 会将price保留两位小数,
			如 123.321-->123.32 , 456.5 --> 456.50
		本功能的结果是字符串表示的数字如456.5最终形式是"456.50"
	"check_price_int_str":
		功能和 "check_price" 一致 
		就是结果没有小数点, 如 456.567 --> "456"

		注: 这两个功能都没有四舍五入的行为,是直接去掉小数点
	"int" :
		将price改成int类型
	"str" :
		将price 改成 字符串类型
	"empty_with_zero": 当原价小于现价的时候价签上就不会显示
	"empty": 无论内容是什么 价签上都不会显示


#### default_temp
	模板名字不存在时将走默认模板,默认模板不会适应任何价签的,默认模板也不会报错,
	因为不会适应任何价签-言外之意就是刷出的效果可能和预期的不一样.建议更新之前检查好模板名.


## 点阵模板 
	点阵模板 应注意的问题有:
		模板名,字体,区域
	
			模板名: opt4里填入的
			字体 : "font_type" : "Arial 9" 详见pango渲染
			区域: 就是x和y坐标	别超出范围,如果在价签坐标像素内超出区域,顶多显示不全而已
				  如果超过价签的像素范围 将会报错
				  eg:  start_x 0, start_y 104, end_x 295 end_y 127
						此时用大字号字体刷新将会超过y坐标128 将会报错

			建议: 如果更新时出错,先检查边界 将字体改小点看看是否能更新成功

### 中英文字体对照
			宋体 SimSun 
			黑体 SimHei 
			微软雅黑 Microsoft YaHei 
			微软正黑体 Microsoft JhengHei 
			新宋体 NSimSun 
			新细明体 PMingLiU 
			细明体 MingLiU 
			标楷体 DFKai-SB 
			仿宋 FangSong 
			楷体 KaiTi 
			仿宋_GB2312 FangSong_GB2312 
			楷体_GB2312 KaiTi_GB2312 
	以上是部分中英文字体名对照表,字体名对照表红玉曾经发送到各位的邮箱里,具体详见邮箱里信息		
	
### 字体格式
	 "SimSun  Bold Italic underline 12"
	 SimSun 宋体, 
	 Bold 加粗,
	 Italic 斜体
	 strike 中划线
	 underline 下划线
	
	注意 : 1.字体名要在开头, 字号在最后,其他属性在中间 
			字体名有空格时,中间不要插入属性
		   2. 字体名不能是中文
		   3. 如果刷出来的字体是框框 那么该字体不支持中文 应换其他字体


## windows service
 安装服务
 python hanshowService.py install

 让服务自动启动
 python hanshowService.py --startup auto install 

 启动服务
 python hanshowService.py start

 重启服务
 python hanshowService.py restart

 停止服务
 python hanshowService.py stop

 删除/卸载服务
 python hanshowService.py remove

### 服务依赖的包
  解压test目录下python_win32_module.zip
  安装解压后的exe文件, 根据python版本安装目前只有python2.7的依赖包
  如果python是32位的,安装 pywin32-219.win32-py2.7.exe 
  否则安装pywin32-219.win-amd64-py2.7.exe 


## 易出错的问题
### 数据库价签的配置

#### 段码
		在数据库里不能配置为 DOT20
		同样点阵也不能配置成段码的类型
		否则通讯失败
#### nw1
		如果价签是点阵的 不能配置成和段码同一组的 nw1 否则通讯失败 
	
### 工程文件只可增加 不可删除
		




