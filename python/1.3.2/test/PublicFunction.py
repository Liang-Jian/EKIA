#-*- coding:UTF-8 -*-
import sys, unittest, xmlrpclib, time, socket, select, multiprocessing , random ,sqlite3,re
from main import database
import esl_init
from main import create_task_data
from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
import os
from xml.dom import minidom


server = xmlrpclib.ServerProxy('http://127.0.0.1:9000')
db = database.DB()
log ='./log/log.txt'

class ReadXml(object):
    def r(self,elementfirstnode,num,elementsecondnode):  #读xml
        # dom = minidom.parse(".\\testdata.xml")
        dom = minidom.parse(".\\922.xml")
        root = dom.documentElement
        parnote = root.getElementsByTagName(elementfirstnode)[num]
        secondnote = parnote.getElementsByTagName(elementsecondnode)[0].childNodes[0].nodeValue
        return secondnote

    def s(self,type,cmd):   #发送数据模型
        ret,val = server.send_cmd(type,cmd)
        return  ret,val

    def sql(self,cadillac): #连接sqlite
        connection=sqlite3.connect("db.sqlite")
        cursor=connection.cursor()
        cursor.execute(cadillac)
        cursor.close()
        connection.commit()

    def bc(self,a): #绑定模块中查询数据库信息
        db1 = '.\db.sqlite'
        connection=sqlite3.connect(db1)
        cursor=connection.cursor()

        for i in cursor.execute("select * from bind_list where eslid in ('"+a+"')"):
            if a in i:
                print 'OK'
            print 'Not in bind_list'





    def clearlog(self):                                                         #清空log模块
        f = open(log,'w')
        time.sleep(1)
        f.close()
        time.sleep(2)


    def cs(self):
        ''' 找出log里面提示组网成功的信息，取出nw3,set,grp中的值做比较 '''
        re_str = '.*{(.*)}'

        tmp = []
        findstr = ('success','ESL_NETLINK_ACK')
        with open(log) as cadillac:
            try:
                for line in cadillac:
                    for s in findstr:
                        if s in line:

                            tmp = str(line)

                            re_pat = re.compile(re_str)
                            search_ret = re_pat.search(tmp)
                            if search_ret:
                                search_ret.groups()
                            else:
                                continue


                        else:
                            pass
                loginfo = eval('{'+search_ret.groups().__str__()[2:-3]+ '}')
                return  loginfo
            finally:
                pass



    def incmplog(self,nw3,setchn,grpchn):
        ''' 输入的值和log值比较 '''
        retstr = self.cs()
        print 'log info:'
        print  retstr

        if retstr['status'] != 'OK':
            return  'netlink fail'
        else:

            if retstr['nw3'] == nw3 and retstr['setchn'] == int(setchn) and retstr['grpchn'] == int(grpchn):
                return 'OK'
            else:
                return 'failed'




    def incmpdb(self,toyota,nw3,setchn,grpchn):
        ''' 输入的值和数据库的值比较 '''

        retstr = self.cs()


        db1 = '.\db.sqlite'
        connection=sqlite3.connect(db1)
        cursor=connection.cursor()
        try:
            for dv in cursor.execute("select nw3,setchn,grpchn from esl_list where eslid in ('"+toyota+"')"):

                s = list(dv)
                print 'db info:'
                print s
            if  int(s[2]) == int(grpchn)  and int(s[0]) == int(nw3) and int(s[1]) == int(setchn) :
                return 'OK'
            else:
                print 'fail'
        finally:
            pass

    def u(self,id):
        '''更新一个价签，只是在netlink中使用'''
        server.send_cmd("SALES_UPDATA_BUF", [{"sid":"120", "salesno":"1", "Price":id, "Price1":"0", "Price2":"16257", "Price3":"3"}])

    def dbseach(self,a):                                                              #数据库比较
        db1 = '.\db.sqlite'
        connection=sqlite3.connect(db1)
        cursor=connection.cursor()
        cursor.execute(a)
        for r in cursor.fetchall():
            print r


    def b(self,a):                                                              #数据库比较
        db1 = '.\db.sqlite'
        connection=sqlite3.connect(db1)
        cursor=connection.cursor()


        for i in cursor.execute("select setchn,grpchn,nw3 from esl_list where eslid in ('"+a+"')"):
            if a in i:
                s = list(i)
                print s,type(s)
                print s[0],s[1],s[2]                                            #取list中的第一个数组
                return 'OK'                                                     #返回一个比较的字符串
            else:
                print 'no'

if __name__ == '__main__':
    # P = ReadXml()
    # n = "158"
    # s = "158"
    # g = "158"
    # esl = "54-72-C0-99"
    # P.clearlog()
    # print P.incmpdb(esl,'158','158','158')
    # P.sql("INSERT INTO bind_list('eslid', 'salesno', 'apid', 'status') VALUES ('54-72-C0-99', 12345678, 1, NULL)")
    # print server.send_cmd('ESL_NETLINK', [{"eslid":esl, "nw1":"51-01-03-66",  "nw3":n,"op2":"5", "setchn":s, "grpchn":g}])
    # P.bi('\"54-72-C0-99\"')
    # P.bc('54-72-C0-99')
    # P.dbseach('select count() from esl_list')
    print 'only this module can be used'


