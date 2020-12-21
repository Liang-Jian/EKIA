import datetime,random,string,os
import calendar
import datetime

'''
all func libs , create 4 bit random word .write to txt file . 
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



def randword(word):
    '''
    :param word: 自动化
    :param numbercount: 几位int
    :return:
    '''
    # seeds = string.digits
    # random_str = random.choices(seeds, k=numbercount)
    random_str = get_text()
    return word+ "".join(random_str)



def midword(word1,word2):
    '''
    :param word: 自动化
    :param numbercount: 几位int
    :return:
    '''
    # seeds = string.digits
    # random_str = random.choices(seeds, k=numbercount)
    random_str = get_text()
    return word1 + "".join(random_str)+ word2



def calDate(day, isTime=1):
    '''
    :param day: 前一天 -1 ， 后一天 1
    :param isTime: 1:有小时 其他没有小时
    :return:
    '''
    if isTime ==  1:
        datetime_string = (datetime.date.today() + datetime.timedelta(days=day)).strftime('%Y-%m-%d %H:%M:%S')
    else:
        datetime_string = (datetime.date.today() + datetime.timedelta(days=day)).strftime('%Y-%m-%d')
    return datetime_string


def calDate1(day):
    '''
    :param day: 前一天 -1 ， 后一天 1
    :param demo: 2020-12-19 18:57:42
    :return:
    '''
    now_time = datetime.datetime.now()
    datetime_string = (now_time + datetime.timedelta(days=day)).strftime("%Y-%m-%d %H:%M:%S")
    # print(datetime_string)
    return datetime_string


def randomTel():
    #随机电话号
    prelist = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "147", "150", "151", "152",
                   "153", "155", "156", "157", "158", "159", "186"]
    return random.choice(prelist) + "".join(random.choice("0123456789") for i in range(8))


def stuTel():
    #学生电话: 187 188
    prelist = [ "187", "188"]
    return random.choice(prelist) + "".join(random.choice("0123456789") for i in range(8))

def randomNum(count):
    #几位数字
    count = int(count)
    s = '123456789'
    r = ''
    while count > 0:
        r += random.choice(s)
        count -= 1
    return r



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

def calClassDay(start="00:00:00",end="00:15:00"):
    td= datetime.date.today()               # today
    st= datetime.date.today()               # saturday
    sn= datetime.date.today()               # sunday
    today = datetime.date.today()

    if td.isoweekday() == 6:                # 如果是星期日取下个周六
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


