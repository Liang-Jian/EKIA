import mysql.connector
from autobase.FunctionLibray import readYaml

'''
other daba source

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

        loginurl = readYaml("url")                                                  # url
        icon = loginurl.split(".")[0][-3::]                                         # pre tsl dev cms sas
        self.host = readYaml("host", icon)
        self.port = readYaml("port", icon)
        self.name = readYaml("name", icon)                                           # database d
        self.user = readYaml("user", icon)
        self.password = readYaml("password", icon)
        self.charset = "utf8"
        self.conn = mysql.connector.connect(host=self.host, user=self.user, password=self.password,database=self.name,use_unicode=True)
        self.cursor = self.conn.cursor()

    def search_db(self,sql):
        self.cursor.execute(sql)
        select_data = self.cursor.fetchall()
        # print(select_data)
        return select_data

    def update_db(self,sql):
        self.cursor.execute(sql)
        self.conn.commit()

    def close_db(self):
        if self.conn != None:
            self.conn.close()
        if self.cursor !=None:
            self.cursor.close()

    # def __del__(self):
    #     try:
    #         self.conn.close()
    #         self.cursor.close()
    #     finally:
    #         pass