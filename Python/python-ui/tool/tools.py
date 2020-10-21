import datetime
import random
import string




# random int
def random_num(count):
    count = int(count)
    s = '0123456789'
    r = ''
    while count > 0:
        r += random.choice(s)
        count -= 1
    return r

def driver_num(driver_rul):
    if driver_rul == 'driver-001':
        return ''
    #证件号码允许录入7个字符
    elif driver_rul == 'driver-002':
        return random_num(7)
    #证件号码允许录入20个字符
    elif driver_rul == 'driver-003':
        return random_num(20)
    #证件号码允许录入10个字符
    elif driver_rul == 'driver-004':
        return random_num(10)
    #证件号码允许录入小于7个字符，6个
    elif driver_rul == 'driver-005':
        return random_num(6)
    #证件号码允许录入大于20个字符
    elif driver_rul == 'driver-006':
        return random_num(21)
    else:
        return '根据规则无法生成驾驶证号！'


def hkmacao_num(HMT_rul):
    if HMT_rul == 'HMT-001':
        return ''
    #证件号码允许录入8个字符
    elif HMT_rul == 'HMT-002':
        return random_num(8)
    #证件号码允许录入20个字符
    elif HMT_rul == 'HMT-003':
        return random_num(20)
    #证件号码允许录入10个字符
    elif HMT_rul == 'HMT-004':
        return random_num(10)
    #证件号码允许录入小于8个字符，7个
    elif HMT_rul == 'HMT-005':
        return random_num(7)
    #证件号码允许录入大于20个字符
    elif HMT_rul == 'HMT-006':
        return random_num(21)
    else:
        return '根据规则无法生成港台同胞证！'




def passport_num(passport_rul):
    if passport_rul == 'passport-001':
        return ''
    #证件号码允许录入7个字符
    elif passport_rul == 'passport-002':
        return random_num(7)
    #证件号码允许录入20个字符
    elif passport_rul == 'passport-003':
        return random_num(20)
    #证件号码允许录入10个字符
    elif passport_rul == 'passport-004':
        return random_num(10)
    #证件号码允许录入小于7个字符，6个
    elif passport_rul == 'passport-005':
        return random_num(6)
    #证件号码允许录入大于20个字符
    elif passport_rul == 'passport-006':
        return random_num(21)
    else:
        return '根据规则无法生成护照号！'


def id_card_mum(birth,sex=1):
    #生成身份证号1991-01-01
    birth = str(birth)
    year = birth[0:4]
    month = birth[5:7]
    day = birth[8:]
    cid_list = ['110101', '110102', '110105', '110106', '110107', '110108', '110109', '110111', '110112', '110113', '110114', '110115',\
    '110116', '110117', '110228', '110229', '120106', '120107', '120108', '120109', '120110', '120111', '120112', '120113', '120114', '120115', \
    '120200', '120221', '120223', '120225', '130100', '130101', '130104', '130105', '130107', '130108', '130121', '130123', '130124', '130125', \
    '140100', '140105', '140106', '140107', '140108', '140109', '140110', '140121', '140122', '140123', '140181', '140200', '140202', '140203', \
    '320100', '320102', '320104', '320105', '320106', '320111', '320113', '320114', '320115', '320116', '320124', '320125', '320200', '320202']
    last = ["1", "0", "X", "9", "8", "7", "6", "5", "4", "3", "2"]
    cid = random.choice(cid_list) + str(year) + str(month).zfill(2) + str(day).zfill(2) + str(random.randrange(int(sex),999,2)).zfill(3)
    #计算校验码
    sum_mum = int(cid[0])*7 + int(cid[1])*9 + int(cid[2])*10 + int(cid[3])*5 + int(cid[4])*8 + int(cid[5])*4 + int(cid[6])*2+int(cid[7])*1 \
    + int(cid[8])*6 + int(cid[9])*3 + int(cid[10])*7 + int(cid[11])*9 + int(cid[12])*10 + int(cid[13])*5 + int(cid[14])*8 + int(cid[15])*4 + int(cid[16])*2
    cid = cid + last[sum_mum%11]
    return cid

# print(id_card_mum('2015-01-01',1))

#根据规则和出生日期计算身份证号
def certificate_num(birthday,sex,cer_rul):
    if sex == '':
        sex = '1'
    if cer_rul == 'idnumber-001':
        return ''
    #身份证号录入有效15位号码
    elif cer_rul == 'idnumber-002':
        id_mun = id_card_mum(birthday,sex)
        return id_mun[:6] + id_mun[8:17]
    #18位身份证号，不含X
    elif cer_rul == 'idnumber-003':
            while True:
                ID_NUM = id_card_mum(birthday,sex)
                if ID_NUM[-1] == 'X':
                    continue
                else:
                    return ID_NUM
    #身份证号录入位数不是15位也不是18位,给出16位
    elif cer_rul == 'ididnumber-004':
        ID_NUM = id_card_mum(birthday,sex)
        return ID_NUM[:17]
    #18位，含有大写X
    elif cer_rul == 'idnumber-005':
        while True:
            ID_NUM = id_card_mum(birthday,sex)
            if ID_NUM[-1] == 'X':
                return ID_NUM
            else:
                continue
    #18位，含有小写X
    elif cer_rul == 'idnumber-006':
        while True:
            ID_NUM = id_card_mum(birthday,sex)
            if ID_NUM[17] == 'X':
                return ID_NUM[:17] + 'x'
            else:
                continue
    #无效18位
    elif cer_rul == 'idnumber-007':
        return '123456789012345678'
    #是15位
    elif cer_rul == 'idnumber-008':
        id_mun = id_card_mum(birthday,sex)
        return id_mun[0:16]
    else:
        return '根据规则无法生成身份证号！'



def emailNum(email_rul):
    #邮箱非必录
    if email_rul == 'email-001':
        return ''
    #邮箱不含@
    elif email_rul == 'email-002':
        return random_num(9) + 'qq.com'
    #邮箱不含“.”
    elif email_rul == 'email-003':
        return random_num(9) + '@qqcom'
    #邮箱包含特殊字符“_”
    elif email_rul == 'email-004':
        return random_num(9) + '_@qq.com'
    #邮箱长度=50字符
    elif email_rul == 'email-005':
        return random_num(43) + '@qq.com'
    #邮箱长度=51字符
    elif email_rul == 'email-006':
        return random_num(44) + '@qq.com'
    #邮箱格式为“X@X.X”
    elif email_rul == 'email-007':
        return random_num(9) + '@qq.com'
    else:
        return '根据规则无法生成邮箱号'



def phoneNum(email_rul):
    #邮箱非必录
    if email_rul == 'phone-001':
        return ''
    #电话允许是以13开头的11位数字
    elif email_rul == 'phone-002':
        return '13611028273'
    #电话允许是以14开头的11位数字
    elif email_rul == 'phone-003':
        return '14611028273'
    #电话允许是以15开头的11位数字
    elif email_rul == 'phone-004':
        return '15611028273'
    #电话允许是以17开头的11位数字
    elif email_rul == 'phone-005':
        return '17611028273'
    #电话允许是以18开头的11位数字
    elif email_rul == 'phone-006':
        return '18611028273'
    #电话允许是以19开头的11位数字
    elif email_rul == 'phone-007':
        return '19611028273'
    #电话不是以13、14、15、17、18开头的11位数字时
    elif email_rul == 'phone-008':
        return '12611028273'
    #电话后9位连续时
    elif email_rul == 'phone-009':
        return '13123456789'
    #不是11位数字（小于11位）
    elif email_rul == 'phone-010':
        return '1361102823'
    #电话不是11位数字（大于11位）
    elif email_rul == 'phone-011':
        return '136110282733'
    elif email_rul == 'phone-012':
        return '11111111111'
    else:
        return '根据规则无法生手机号'


def randomStr(str_len):
    '''
    生成一个指定长度的随机字符串，其中
    string.digits = 0123456789
    string.ascii_letters = abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
    :param randomlength: 位数
    :return:
    '''
    str_list = [random.choice(string.digits + string.ascii_letters) for i in range(str_len)]
    random_str = "".join(str_list)


    return random_str




def calculate_birthday(start_date, age, days):#计算出生日期
    '''
    :param start_date:
    :param age:
    :param days:
    :return:
    '''
    if age == '' or days == '':
        return ''
    year = str(int(start_date[:4]) - int(age))
    my_date = year + start_date[4:]
    d = datetime.datetime.strptime(my_date, '%Y-%m-%d %H:%M:%S')
    delta = datetime.timedelta(days=int(days))
    date_delta = d - delta
    return date_delta.strftime('%Y-%m-%d')


family_names = '赵钱孙李周吴郑王冯陈楮卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜戚谢邹喻柏水窦章'
def random_gbk2312(count):
    random_CH = ''
    while count > 0:
        head = random.randint(0xB0, 0xCF)
        body = random.randint(0xA, 0xF)
        tail = random.randint(0,0xF)
        val = (head << 8) | (body << 4) | tail
        r_str = "%x" % val
        try:
            random_CH += bytes.fromhex(r_str).decode('gb2312')
        except Exception as e:
            #处理不能被gb2312解码的特殊字符
            count += 1
            print(str(e))
        count -= 1
    return random_CH

def random_name():
    return random.choice(family_names) + random_gbk2312(2)