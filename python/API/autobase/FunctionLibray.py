import datetime,random,string,os,datetime,calendar,yaml,zipfile
from autobase.Logger import Logi
'''
all func libs , create 4 bit random word .write to txt file . 
first read txt before run all flow ,as all flow icon . like uuid 

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
        msg = open(os.path.abspath("..") + "/autodata/template/temp.tmp" , "w",encoding="utf-8")
        msg.write(randomstr)
    except (Exception) as e:
        print(e)
    finally:
        msg.close()
gen_text()


def get_text():
    allflow_icon = open(os.path.abspath("../") + "/autodata/template/temp.tmp" , "r",encoding="utf-8")
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

def calClassDay(icon=1):
    if icon == 1:
        start = "00:00:00"
        end = "00:15:00"
    elif icon == 2:
        start = "01:00:00"
        end = "01:15:00"
    elif icon == 3:
        pass
    td= datetime.date.today()                  # today
    st= datetime.date.today()                  # saturday
    sn= datetime.date.today()                  # sunday
    today = datetime.date.today()
    # print(td.isoweekday())
    if td.isoweekday() == 7:                # 如果是星期日取下个周六
        b_t = td.strftime('%Y-%m-%d {}'.format(start))
        a_t = getNextSaturday() + " {}".format(end)
        return b_t,a_t

    oneday = datetime.timedelta(days=1)
    while st.weekday() != 5:
        st += oneday
    while sn.weekday() != 6:
        sn += oneday
    b_t = st.strftime('%Y-%m-%d {}'.format(start))
    a_t = sn.strftime('%Y-%m-%d {}'.format(end))
    # print(b_t,a_t)
    return b_t,a_t

def classTime(icon=1):
    # 00:00~00:15,00:00:00,00:15:00
    if   icon == 1:
        return ["00:00~00:15","00:00:00","00:15:00"]
    elif icon == 2:
        return ["01:00~01:15","01:00:00","01:15:00"]
    elif icon == 3:
        pass
    elif icon == 4:
        pass

def calWeekDay():
    # return: ['周六','周日'] or ['周日','周六']
    td = datetime.date.today()
    if td.isoweekday() == 7:
        return ['周日','周六']
    return ['周六','周日']



def readYaml(key, peer="pycms_controller"):
    # read yaml file
    file = open(os.path.abspath('..') + "/configure/baseinfo.yml", "r", encoding="utf8")
    config = yaml.load(file.read(), Loader=yaml.Loader)
    conf = config[peer]
    return conf[key]

def readYam(peer="pycms_controller"):
    # read all yaml peer
    file = open(os.path.abspath('..') + "/configure/baseinfo.yml", "r", encoding="utf8")
    config = yaml.load(file.read(), Loader=yaml.Loader)
    conf = config[peer]
    return conf


def zipDir(dirpath):
    # zip dir
    outFullName = os.path.abspath('..') + "/autodata/resultfile/线上执行报告.zip"
    zip = zipfile.ZipFile(outFullName,"w",zipfile.ZIP_DEFLATED)
    for path,dirnames,filenames in os.walk(dirpath):
        # 去掉目标跟路径，只对目标文件夹下边的文件及文件夹进行压缩
        fpath = path.replace(dirpath,'')

        for filename in filenames:
            zip.write(os.path.join(path,filename),os.path.join(fpath,filename))
    Logi("file compresstion complete")
    zip.close()

def deleteFile(src):
    # delete file
    if os.path.isfile(src):
        try:
            os.remove(src)
        except:
            pass
    elif os.path.isdir(src):
        for item in os.listdir(src):
            itemsrc=os.path.join(src,item)
            deleteFile(itemsrc)
    Logi(f"delete file {src} success")
    #     try: # delete dir
    #         os.rmdir(src)
    #     except:
    #         pass


def sqlValue(ele):
    # [(375,)] -> 375
    _t  = None
    _t1 = None
    if len(ele)== 1 and isinstance(ele,list):
        _t = ele[0]
        if isinstance(_t,tuple) and _t.__len__() == 1:
            _t1 = _t[0]
    return _t1