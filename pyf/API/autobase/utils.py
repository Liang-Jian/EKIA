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
    passwd  = "sinosoft"

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
    #
    #     switch (cur_rule) {
    #         case "X":
    #             while (true) {
    #                 String idnum = generateByAgeFlag(ageFlag, sex, x1);
    #                 count++;
    #                 if (StringUtils.equals(idnum.substring(17), "X")) {
    #                     result = idnum;
    #                     System.out.println("search count:" + count);
    #                     break;
    #                 }
    #             }
    #             break;
    #         case "x":
    #             while (true) {
    #                 String idnum = generateByAgeFlag(ageFlag, sex, x1);
    #                 count++;
    #                 if (StringUtils.equals(idnum.substring(17), "X")) {
    #                     result = idnum.replace("X", "x");
    #                     System.out.println("search count:" + count);
    #                     break;
    #                 }
    #             }
    #             break;
    #         case "18":
    #             while (true) {
    #                 String idnum = generateByAgeFlag(ageFlag, sex, x1);
    #                 count++;
    #                 if (!StringUtils.equals(idnum.substring(17), "X")) {
    #                     result = idnum;
    #                     System.out.println("search count:" + count);
    #                     break;
    #                 }
    #             }
    #             break;
    #         case "15":
    #             while (true) {
    #                 String idnum = generateByAgeFlag(ageFlag, sex, x1);
    #                 count++;
    #                 if (!StringUtils.equals(idnum.substring(17), "X")) {
    #                     idnum = idnum.substring(0, 6) + idnum.substring(8, 17);
    #                     result = idnum;
    #                     System.out.println("search count:" + count);
    #                     break;
    #                 }
    #             }
    #             break;
    #     }
    #     return result;
    # }



def logConfig():

    logger = logging.getLogger("grape")
    logger.setLevel(logging.DEBUG)# 全局默认级别WARNING

    ch = logging.StreamHandler()# 生成Handler对象
    ch.setLevel(logging.DEBUG)
    # fh = logging.FileHandler("./" + "//log//log.txt", encoding="utf8")
    fh = logging.FileHandler(os.path.abspath("../")+"//resultshow/log.log", encoding="utf8")
    fh.setLevel(logging.DEBUG)

    # 生成formatter对象
    # 把formatter对象 绑定到Handler对象
    file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s %(message)s")
    console_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    # console_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(message)s")
    ch.setFormatter(console_formatter)
    fh.setFormatter(file_formatter)
    logger.addHandler(ch)# 把Handler对象 绑定到logger
    logger.addHandler(fh)
    return logger

log = logConfig()

def logger_debug(msg):
    log.debug(msg)

def logger_info(msg):
    log.info(msg)

def logger_warning(msg):
    log.warning(msg)

def logger_error(msg):
    log.error(msg)

def logger_critical(msg):
    log.critical(msg)

if __name__ == '__main__':
    logger_debug("logger_debug")
    logger_info("logger_info")
    logger_warning("logger_warning")
    logger_error("logger_error")