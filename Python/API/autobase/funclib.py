import logging
import logging.handlers
import random,string,os
import datetime

'''
all function libs
create by Joker

'''


def randomStr(n):
    str_list = [random.choice(string.digits + string.ascii_letters) for i in range(n)]
    random_str = "".join(str_list)
    return random_str



def generate_random_str(randomlength):
    '''
    生成一个指定长度的随机字符串，其中
    string.digits = 0123456789
    string.ascii_letters = abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
    :param randomlength: 位数
    :return:
    '''
    str_list = [random.choice(string.digits + string.ascii_letters) for i in range(randomlength)]
    random_str = "".join(str_list)
    return random_str



def idNum(ageFlag,sex,x1,cur_cule):
    count = 1231234324

    return count



def selfRandom(word,numbercount):
    '''
    :param word: 自动化
    :param numbercount: 几位int
    :return:
    '''
    seeds = string.digits
    random_str = random.choices(seeds, k=numbercount)
    return word+ "".join(random_str)






def CalDate(day, isTime=1):
    '''
    :param day: 前一天 -1 ， 后一天 1
    :param isTime: 1:有小时 其他没有小时
    :return:
    '''
    if isTime ==  1:
        date_time_string = (datetime.date.today() + datetime.timedelta(days=day)).strftime('%Y-%m-%d %H:%M:%S')
    else:
        date_time_string = (datetime.date.today() + datetime.timedelta(days=day)).strftime('%Y-%m-%d')
    # print(date_time_string)
    return date_time_string