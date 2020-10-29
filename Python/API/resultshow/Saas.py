# -*- encoding:utf-8 -*-
import json
from datetime import datetime
import allure
from sourcefile.Contrast import DictCmp
from sourcefile.HttpMethods import HttpMethods
from sourcefile.signatureUtil import Signature
import sourcefile.tools  as tl
import dataready.global_var as gl
from database.ConnMysql import ConnMysql
gl.init()
gl.set_value("token", "123")
def get_list(length):
    new_list = []
    if length > 0:
        for i in range(length):
            new_list.append(str(i))
    return new_list


def saas_case(url,sql,user, header, req, method, expect, remark,relation,parameterization):
    with allure.step("用例描述：  {0}".format(remark)):
        pass

    with allure.step("测试时间：  {0}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))):
        pass

    with allure.step("测试步骤1、获取入参"):
        # url="http://"+user+".bms.lexue.com"+url
        url="https://pycmspre.lexue.com"+url
        header = header.replace("tenantId_value", user)
        if parameterization:
           arg2 = parameterization.split(",")
           print(arg2)
           if len(arg2) == 1:
              t1 = tl.getAllDef(arg2[0])
              print(t1)
              req = req.replace(arg2[0]+"_value",t1)
              sql = sql.replace(arg2[0] + "_value", t1)
           elif len(arg2) == 2:
              t1=tl.getAllDef(arg2[0])
              t2=tl.getAllDef(arg2[1])
              req = req.replace(arg2[0] + "_value", t1)
              req = req.replace(arg2[1] + "_value", t2)
              sql = sql.replace(arg2[0] + "_value", t1)
              sql = sql.replace(arg2[1] + "_value", t2)
           elif len(arg2) == 3:
              t1 = tl.getAllDef(arg2[0])
              t2 = tl.getAllDef(arg2[1])
              t3 = tl.getAllDef(arg2[2])
              req = req.replace(arg2[0] + "_value",t1)
              req = req.replace(arg2[1] + "_value", t2)
              req = req.replace(arg2[2] + "_value", t3)
              sql = sql.replace(arg2[0] + "_value", t1)
              sql = sql.replace(arg2[1] + "_value", t2)
              sql = sql.replace(arg2[2] + "_value", t3)
        if relation:
            arg1 = relation.split(",")
            if "YES" not in relation:
                dic_data = json.loads(req)
                login_sginature = Signature().get_signature(dic_data)
                str_headers = header.replace("signature_value", login_sginature)
                str_headers2 = str_headers.replace("token_value", gl.get_value("token"))
                allure.attach(str(str_headers2), "最终header值")
                result = HttpMethods().get_result(url, method, json.loads(str_headers2), str(req))
                if len(arg1) == 1:
                    str3 = result.json()[arg1[0]]
                    str4 = arg1[0]
                elif len(arg1) == 2:
                    str3 = result.json()[arg1[0]][arg1[1]]
                    str4 = arg1[1]
                elif len(arg1) == 3:
                    str3 = result.json()[arg1[0]][arg1[1]][arg1[2]]
                    str4 = arg1[2]
                elif len(arg1) == 4:
                    str3 = result.json()[arg1[0]][arg1[1]][arg1[2]][arg1[3]]
                    str4 = arg1[3]
                gl.set_value(str4, str3)
            else:
                str7 = gl.get_value(arg1[1])
                req = req.replace("variable_value", str7)
                dic_data = json.loads(req)
                login_sginature = Signature().get_signature(dic_data)
                str_headers = header.replace("signature_value", login_sginature)
                str_headers2 = str_headers.replace("token_value", gl.get_value("token_value"))
                allure.attach(str(req), "获取关联值后的请求")
                allure.attach(str(str_headers2), "获取最后head值")
                result = HttpMethods().get_result(url, method, json.loads(str_headers2), str(req))

        else:
            dic_data = json.loads(req)
            login_sginature = Signature().get_signature(dic_data)
            str_headers1 = header.replace("signature_value", login_sginature)
            str_headers2 = str_headers1.replace("token_value", gl.get_value("token"))
            allure.attach(str(str_headers2), "最终header值")
            allure.attach(str(req), "获取关联值后的请求")
            result = HttpMethods().get_result(url, method, json.loads(str_headers2), str(req))
        res1=True
        if sql:
            sql_data = ConnMysql().search_db(sql)
            res1 =len(sql_data)==True
    with allure.step("测试步骤2、获取响应结果"):
        allure.attach(str(json.dumps(result.json(), indent=4, ensure_ascii=False)),"响应结果")
    res=False

    res4 = DictCmp().compare_dict(result.json(), json.loads(expect))
    if res4 and res1:
       res=True

    with allure.step("测试步骤3、断言校验结果: {0}".format("PASS" if res4 else "FAILED")):
        allure.attach(expect,"结果断言设置")
        assert res
