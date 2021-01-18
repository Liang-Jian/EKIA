import mysql.connector,yaml
from autobase.functionLibs import *
from autobase.proceCasedata import *
'''
get other daba source
create by joker

'''



class CommonDataExtractor:
    pass


class ExcelHelper:
    pass


class JsonUtil:
    pass


class XmlFormatter:
    pass



class OraService:
    pass

class SqlService2:

    jdbcUrl = "jdbc:oracle:thin:@10.130.201.118:1521:tkpi"
    user    = "upiccore"
    passwd  = "xueersi"

    def setConnection(self,url,us,ps):
        SqlService2.jdbcUrl = url
        SqlService2.user    = us
        SqlService2.passwd  = ps


class MsqService:

    def __init__(self):
        file = open(os.path.abspath('..') + r"\configure\database.yml", "r", encoding="utf8")
        xlxsObject = ParseExcel().load_work_book(os.path.abspath('..') + "\\autodata\\testcase\\培优接口用例.xlsx").get_sheet_by_name("CMS接口T")
        loginurl = ParseExcel().get_cell_of_value(xlxsObject, rowNo=2, colsNo=2)    # url
        config = yaml.load(file.read(), Loader=yaml.Loader)
        # icon = loginurl.split(".")[0][-3::]                                         # pre tsl dev sas
        icon = "online"                                                               # pre
        conf = config[icon]
        self.host = conf["host"]
        self.port = conf["port"]
        self.name = conf["name"]                                                    # database d
        self.user = conf["user"]
        self.password = conf["password"]
        self.charset = "utf8"
        self.conn = mysql.connector.connect(host=self.host, user=self.user, password=self.password,database=self.name,use_unicode=True)

    def search_db(self,sql):
        self.cursor = self.conn.cursor()
        self.cursor.execute(sql)
        select_data = self.cursor.fetchall()
        print(select_data)
        return select_data

    def update_db(self,sql):
        self.cursor.execute(sql)
        self.conn.commit()

    def close_db(self):
        if self.conn != None:
            self.conn.close()
        if self.cursor !=None:
            self.cursor.close()
