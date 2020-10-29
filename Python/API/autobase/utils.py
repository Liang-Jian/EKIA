import logging
import logging.handlers
import random,string,os
# from pandas import DataFrame

class CommonDataExtractor:
    pass


class ExcelHelper:
    pass


class JsonUtil:
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


class XmlFormatter:
    pass


class TestCaseEntity:
    pass

