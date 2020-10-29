import logging
import logging.handlers
import random,string,os

'''
需要eval() 转换的函数库

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

# switch (cur_rule) {
#     case "X":
#         while (true) {
#             String idnum = generateByAgeFlag(ageFlag, sex, x1);
#             count++;
#             if (StringUtils.equals(idnum.substring(17), "X")) {
#                 result = idnum;
#                 System.out.println("search count:" + count);
#                 break;
#             }
#         }
#         break;
#     case "x":
#         while (true) {
#             String idnum = generateByAgeFlag(ageFlag, sex, x1);
#             count++;
#             if (StringUtils.equals(idnum.substring(17), "X")) {
#                 result = idnum.replace("X", "x");
#                 System.out.println("search count:" + count);
#                 break;
#             }
#         }
#         break;
#     case "18":
#         while (true) {
#             String idnum = generateByAgeFlag(ageFlag, sex, x1);
#             count++;
#             if (!StringUtils.equals(idnum.substring(17), "X")) {
#                 result = idnum;
#                 System.out.println("search count:" + count);
#                 break;
#             }
#         }
#         break;
#     case "15":
#         while (true) {
#             String idnum = generateByAgeFlag(ageFlag, sex, x1);
#             count++;
#             if (!StringUtils.equals(idnum.substring(17), "X")) {
#                 idnum = idnum.substring(0, 6) + idnum.substring(8, 17);
#                 result = idnum;
#                 System.out.println("search count:" + count);
#                 break;
#             }
#         }
#         break;
# }
# return result;
# }




