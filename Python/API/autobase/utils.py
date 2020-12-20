import mysql.connector
from autobase.functionLibs import *
'''
get other daba source

'''
_str = "${sql(select * from py_class_rule where class_rule_name=${selfRandom('建校')})}"
def sql2str(s):
    # cutsql = ""
    if "{sql(" not in s: return s
    removesql_str = s.replace("${sql(","")[:-2]
    print(removesql_str)
    # if "${" in cutsql:
    if "${" not in removesql_str: return removesql_str
    index = removesql_str.index("${")
    end   = removesql_str.index("}")
    print(removesql_str[index+2:-1])
    randomMake = eval(removesql_str[index+2:-1])
    print(randomMake)

    finalstr = removesql_str.replace(removesql_str[index:end+1],"'"+randomMake+"'")
    print(finalstr)
    return  finalstr

class CommonDataExtractor:
    pass


class ExcelHelper:
    pass


class JsonUtil:
    pass


class XmlFormatter:
    pass


class TestCaseEntity:
    pass


class SqlService2:

    jdbcUrl = "jdbc:oracle:thin:@10.130.201.118:1521:tkpi"
    user    = "upiccore"
    passwd  = "xueersi"

    def setConnection(self,url,us,ps):
        SqlService2.jdbcUrl = url
        SqlService2.user    = us
        SqlService2.passwd  = ps

    # def getconn(self):
    #     return getConnection(jdbcUrl,use,passwd)


class MsqService:
    def __init__(self):
        self.conn = mysql.connector.connect(host='10.10.200.210', user='education', password='lexue123',database='peiyou',
                                            use_unicode=True)

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
