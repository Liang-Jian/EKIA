import urllib.parse


def tostr(any):
    if isinstance(any,int): any = str(any)

    print(any)
    print(type(any))
    return any

def strtourlencode(_string):
    url_code_name = urllib.parse.quote(_string)
    print(url_code_name)
    return (url_code_name)


def get_string(dict1):
    string_dict = ""
    if dict1 != {}:
        sorted_list = sorted(dict1.items(), key=lambda d: d[0])
        for i in iter(sorted_list):
            str1 = i[0] + "=" + tostr(i[1]) + "&"
            string_dict += str1
        # print(string_dict)
        print(string_dict[0:-1])

    return string_dict[0:-1]

# d = {"a":"3","b":3}
# get_string(d)
'''
1,${local("A")} -> A  - OK 
2,A -> A.value
3,替换

'''
import re
allflow = {"userid":"12","joker":"william"}
b = '{"mailFlag": "0","editFlag":1,"courseTypeName": "讲座","playType": 1,"ossResourceUrl": "${local("courseTypeName")}","classDateEndTime": "2020-12-13 00:00:00","teacherType": 1}'

# -1-
# name = re.findall('\${local\(.*?\)}',b)
# # name = re.findall('\${local\(\".*\"\)\}\,',b)
# print(name)
# ss = name[0].replace("${local(\"","").replace("\")}","")
# print(ss)
#
# # -2-
#
# # ss = "mailFlag"
# k = re.findall('{}\":(.*?)\,'.format(ss),b)
# print(k)
#
# s1 = b.replace(name[0],k[0])
# print(s1)
#
# s = '{"classId":"119218","classStatus":0}'
def local2str(_str):
    if not isinstance(_str,str): raise ("should be str")
    if len(re.findall('\${local\(.*?\)}',_str)) == 0 : return _str
    # local_value_list = re.findall('\${local\(\".*\"\)\}',_str,1)
    local_value_list = re.findall('\${local\(.*?\)}',_str)

    local_value_str = local_value_list[0]
    local_value_str1 = local_value_str.replace("${local(\"","").replace("\")}","")
    replace_value = re.findall('{}\":(.*?)\,'.format(local_value_str1),_str)[0].replace("\"","")
    all_str = _str.replace(local_value_str,replace_value)
    # Logi("remove local:=%s" % all_str)
    print(all_str)
    return all_str
# local2str(b)
# templetestring g,type(templetestring))= open(r"D:\workspace\dom-po\API\autodata\template\xinjianzhuanban.vm", 'r', encoding='utf-8', errors='ignore').read()
# print(templetestrin
def digui(n):
    if n == 0:
        print('')
        return
    print('*' * n)
    digui(n - 1)

if __name__ == '__main__':
    digui(5)
import datetime
def calDate(day, isTime=1):
    '''
    :param day: 前一天 -1 ， 后一天 1
    :param isTime: 1:有小时 其他没有小时
    :return:
    '''
    if isTime ==  1:
        datetime_string = (datetime.date.today() + datetime.timedelta(days=day)).strftime('%Y-%m-%d %H:%M:%S')
        print(datetime_string)
    else:
        datetime_string = (datetime.date.today() + datetime.timedelta(days=day)).strftime('%Y-%m-%d')
        print(datetime_string)
    return datetime_string
# calDate(+1,1)



from datetime import datetime,timedelta
import time

def last_day(d, day_name):
    days_of_week = ['sunday','monday','tuesday','wednesday',
                        'thursday','friday','saturday']
    target_day = days_of_week.index(day_name.lower())
    print(target_day)
    print(d.isweekday())
    delta_day = target_day - d.isoweekday()
    if delta_day >= 0: delta_day += 7 # go back 7 days
    return d + timedelta(days=delta_day)

# print(last_day(datetime.date() ,'friday'))

import datetime

def get_current_week():
    today = datetime.date.today().day
    saturday, sunday = datetime.date.today(), datetime.date.today()
    print(today)
    one_day = datetime.timedelta(days=1)
    while saturday.weekday() != 5:
        saturday -= one_day
    while sunday.weekday() != 6:
        sunday += one_day

    return saturday, sunday
    # return saturday.day, sunday.day



# nowDate = datetime.datetime.now()
# weekFriday = ''.join(str(nowDate+datetime.timedelta(days=4-date1.weekday())).split()[0].split('-'))
# print(weekFriday)



import calendar
import datetime

'''
1,获取今天的星期数
2，或者本周的周六日
3，如果不是周日 返回周六、 周日的日期
4，如果是  周日 返回本周日， 和下个星期六
'''


def getNextSaturday():
    # 获取下一周 周六
    today = datetime.date.today()
    oneday = datetime.timedelta(days = 1)
    m1 = calendar.SATURDAY
    while today.weekday() != m1:
        today += oneday
    nextMonday = today.strftime('%Y-%m-%d')
    print(nextMonday)
    return nextMonday

# print(getNextSaturday())




def getNextSaturday():
    # 获取下一周 周六
    today = datetime.date.today()
    oneday = datetime.timedelta(days = 1)
    m1 = calendar.SATURDAY
    while today.weekday() != m1:
        today += oneday
    nextMonday = today.strftime('%Y-%m-%d')
    print(nextMonday)
    return nextMonday

def calClassDay(start="00:00:00", end="00:15:00"):
    td= datetime.date.today()               # today
    st= datetime.date.today()               # saturday
    sn= datetime.date.today()               # sunday
    today = datetime.date.today()

    if td.isoweekday() == 6:                # 如果是星期日取本周日和下周六
        b_t = td.strftime('%Y-%m-%d {}'.format(start) )
        a_t = getNextSaturday() + " {}".format(end)
        return b_t,a_t

    oneday = datetime.timedelta(days=1)
    while st.weekday() != 5:
        st += oneday
    while sn.weekday() != 6:
        sn += oneday
    b_t = st.strftime('%Y-%m-%d {}'.format(start))
    a_t = sn.strftime('%Y-%m-%d {}'.format(end))
    print(b_t,a_t)
    return b_t,a_t

