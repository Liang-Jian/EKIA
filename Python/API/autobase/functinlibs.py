import datetime,random,string,os

'''
all func libs , create 5 bit random word .write to txt file . 
first read txt before run all flow ,as all flow icon .

create by Joker
'''



def gen_text():
    # 0ijYx
    number = 5
    source = list(string.ascii_letters)
    for index in range(0,10):
        source.append(str(index))
    randomstr = ''.join(random.sample(source,number))
    try:
        msg = open(os.path.abspath("..") + "\\autodata\\template\\temp.tmp" , "w",encoding="utf-8")
        msg.write(randomstr)
    except (Exception) as e:
        print(e)
    finally:
        msg.close()
gen_text()


def get_text():
    allflow_icon = open(os.path.abspath("../") + "\\autodata\\template\\temp.tmp" , "r",encoding="utf-8")
    return allflow_icon.read()



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



def selfRandom(word):
    '''
    :param word: 自动化
    :param numbercount: 几位int
    :return:
    '''
    # seeds = string.digits
    # random_str = random.choices(seeds, k=numbercount)
    random_str = get_text()
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
    return date_time_string