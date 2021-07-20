# encoding: utf-8
#

import database, esl_init, os, sys

work_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
if work_dir == '':
	work_dir = '.'
os.chdir(work_dir)

db = database.DB()

def check_ack(ack_list):
	ack_dict = {1:"Database Error", 2:"ESLID Error", 3:"SALESNO Error", 
                        5:"APID Error", 4:"Status Busy", 255:"item exist", 0:"OK",
			"00":"OK", "01":"Database Error",
			}
	for ack in ack_list:
		ack_value = ack['ack']
		if ack_value not in [0,"00", 255]:
			print ack_dict[ack['ack']], ack

#以下四行分别导入价签信息、商品信息、基站信息、绑定关系到数据库中
check_ack(db.updata_from_file(db.esl, sys.argv[1]))
#check_ack(db.updata_from_file(db.sales, esl.sales_updata_file))
#check_ack(db.updata_from_file(db.ap, esl.ap_updata_file))
#check_ack(db.binds(sys.argv[2]))
