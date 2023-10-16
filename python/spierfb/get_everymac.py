import time
import datetime
from pymongo import MongoClient
from collections import Counter
# import pymysql

# by bruce shi
CI = 'mongodb://101.201.81.174:27017/'
DB = 'esl'
# DB = 'esl17sct9'
COLLECT = 'esl'
WL=r"D:\debug_test2\test\white_list.txt"


class msq:
    def __init__(self):
        self.conn = pymysql.connect(host="jms.hanshow.online", port=33060, user="c1ada694-81da-4aaa-8b9a-89d63ed4b3d1", password="xBSC92zAzyFKaD7M", database="eslworkingp5")
        self.cursor = self.conn.cursor()
        # self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def search(self, sql):
        self.cursor.execute(sql)
        select_data = self.cursor.fetchall()
        # print(f"sql result:={select_data}")
        return select_data

    def update(self, sql):
        self.cursor.execute(sql)
        self.conn.commit()

    def close(self):
        try:
            self.conn.close()
            self.cursor.close()
        finally:
            pass


def get_white_list(fileName=WL):
    f = open(fileName, 'r',encoding='utf8')
    esl_id_list = list()
    _line = f.readlines()
    for each_line in _line:
        id_ = each_line.replace("=wumart.001","").strip()
        esl_id_list.append(id_)
    f.close()
    return esl_id_list


def calc_count(l):
    _report_list = Counter(l).most_common()
    _repeat_list = list()
    for i in _report_list:
        if i[1] > 1:
            _repeat_list.append(i)
    return _repeat_list


def get_nosync_eslid(ci=CI, db=DB, collect=COLLECT):
    # 获取失步价签eslid 和总数
    _client = MongoClient(ci)
    _db = _client[db]
    _collect = _db[collect]
    all_count = 0
    all_nosync_esl = list()
    for x in _collect.find():
        if x.get("synced") is False:
            all_count += 1
            all_nosync_esl.append(x.get("eslId"))
    print(f"失步总数:={all_count},失步价签ESL:={all_nosync_esl}")
    return


def get_bind_eslid(ci=CI, db=DB, collect=COLLECT):
    # 获取绑定基站的esl
    _client = MongoClient(ci)
    _db = _client[db]
    _collect = _db[collect]
    all_count = 0
    all_nobind_esl = list()

    for x in _collect.find():
        if x.get("apMac") == "" or None:
            all_count += 1
            all_nobind_esl.append(x.get("eslId"))
    print(f"获取未绑定基站总数:={all_count} ,价签ESL:={all_nobind_esl}")


def get_setWor(ci=CI, db=DB, collect=COLLECT):
    # 获取听帧的
    _client = MongoClient(ci)
    _db = _client[db]
    _collect = _db[collect]
    all_count = 0
    setWor_set = set()
    db = _collect.find({})
    for i in db:
        _t = i.get("setWor")
        setWor_set.add(_t)
        all_count += 1
    print(f"数据中存在的setWor:={list(setWor_set)}")
    print(f"价签总数:={all_count}")


def insert_db(_d, ci=CI, db=DB, collect=COLLECT):
    _client = MongoClient(ci)
    _db = _client[db]
    _collect = _db[collect]

    esl_list = list()
    db = _collect.find({})
    _split = _d[0].split("|")
    # print(_split)
    for i in db:
        if i.get("setId") == _split[0]:
            # print(i)
            if i.get("groupId") == int(_split[1]) and i.get('subnet') == int(_split[2]):
                # print(i.get("eslId"))
                esl_list.append(i.get("eslId"))
    # print(esl_list)
    return esl_list

def insert_db_mysql(d):
    # print(_split)
    # print(d.split('|')[0])
    # for i in d:
    m = msq()
    s = m.search(f"select esl_id from t_esl where set_id='{d.split('|')[0]}' and group_id='{d.split('|')[1]}' and subnet='{d.split('|')[2]}'")
    # print(s)
    esl_id = list()
    for i in s:
        esl_id.append(i[0])
    # print(esl_id)
    return esl_id


def is_repeatmysql():
    m = msq()
    s = m.search("select set_id,group_id,subnet from t_esl where version='16'")
    ele_list = list()
    all_count = 0
    for i in s:
        _ele = str(i[0]) + '|' + str(i[1]) + '|' + str(i[2])
        ele_list.append(_ele)
        all_count += 1

    print(f"version=16的esl个数:={ele_list.__len__()}")
    print(f"总共资源个数:={list(set(ele_list)).__len__()}")

    no_repeat_list = calc_count(ele_list)
    print("重复资源组数:=", len(no_repeat_list))
    anser = input("是否需要打印重复资源? n:不需要 y:需要")
    an_low = anser.lower()
    if an_low == "n":
        return
    elif an_low == "y":
        for i in no_repeat_list:
            # print(i)
            _esl = insert_db_mysql(i[0])
            # _esl = insert_db_mysql(i,db=DB)
            print(f"setId={i[0].split('|')[0]},groupId={i[0].split('|')[1]},subnet={i[0].split('|')[2]},esl:={_esl}")
    else:
        return

def is_repeat(ci=CI, db=DB, collect=COLLECT):
    # 组网资源是否重复
    _client = MongoClient(ci)
    _db = _client[db]
    _collect = _db[collect]
    all_count = 0
    ele_list = list()
    white_list = get_white_list()
    dbdata = _collect.find({"version": 16})
    for i in dbdata:
        eslid = i.get("eslId")
        # print(eslid)
        if eslid in white_list:
            _setid = i.get("setId")
            _groupId = i.get("groupId")
            _subnet = i.get("subnet")
            _ele = str(_setid)+'|'+str(_groupId)+'|'+str(_subnet)
            ele_list.append(_ele)
            all_count += 1
    print(f"总共esl个数:={ele_list.__len__()}")
    print(f"总共资源个数:={list(set(ele_list)).__len__()}")

    no_repeat_list = calc_count(ele_list)
    print("重复资源:=", no_repeat_list)

    for i in no_repeat_list:
        _esl = insert_db(i,db=DB)
        print(f"setId={i[0].split('|')[0]},groupId={i[0].split('|')[1]},subnet={i[0].split('|')[2]},esl:={_esl}")

    def get_nosid():
        dbdata = _collect.find({})
        allesl_id = get_white_list()
        not_true_esl_id = list()
        _esl = list()
        for i in dbdata:
            netlink_true = i.get("extEslid")
            if not netlink_true:
                not_true_esl_id.append(i.get('eslId'))

        for e in not_true_esl_id:
            if e in allesl_id:
                _esl.append(e)
        print(f"组网不确定价签:={_esl}")
        print(f"组网不确定价签总数:={len(_esl)}")

    get_nosid()


def get_all_eslid(ci=CI, db=DB, collect=COLLECT):
    # 获取失步价签eslid 和总数
    _client = MongoClient(ci)
    _db = _client[db]
    _collect = _db[collect]
    all_count = 0
    all_nosync_esl = list()
    all_esl_list = list()
    for x in _collect.find():
        all_esl_list.append(1)
    print(f"失步总数:={len(all_esl_list)}")
    return


def _get_mac_(ci=CI, db=DB, collect=COLLECT):
    # 获取失步价签eslid 和总数
    _client = MongoClient(ci)
    _db = _client[db]
    _collect = _db[collect]

    count = 0
    for i in _collect.find({}):
        # print(i)
        if i.get('apMac') == '98:6D:35:76:6D:B0':
            # if i.get('setId') == '54-11-00-66':
            if i.get('setId') == '51-3A-00-66':
                # print(l)
                count += 1
    print(count)


def get_mac_everyset(ci=CI, db=DB, collect=COLLECT):
    # 获取基站下不同SET和ESL总数
    _client = MongoClient(ci)
    _db = _client[db]
    _collect = _db[collect]
    _info_list = list()
    _dict = dict()

    for i in _collect.find({}):
        # print(i.get('binding'))
        mac = i.get('apMac')
        set_Id = i.get("setId")
        esl = i.get('eslId')
        _info = f"{mac}_{set_Id}|{esl}"
        _info_list.append(_info)


    mac_set_set = set()
    for l in _info_list: mac_set_set.add(l.split("|")[0])
    mac_set_list = list(mac_set_set)
    mac_list = list(set([x.split("_")[0] for x in mac_set_set]))

    # 获取ESL list
    _esl_list = [[] for _ in range(len(mac_set_list))]
    s = 0
    while s < len(mac_set_list):
        for i in _info_list:
            # print(i.split("|")[0])
            if mac_set_list[s] == i.split("|")[0]:
                _idx = mac_set_list.index(mac_set_list[s])
                _esl_list[_idx].append(i.split("|")[-1])
        s += 1

    _mac_set_eslnum = list()
    nn = 0
    while nn < len(mac_set_list):
        i = mac_set_list[nn].split("_")
        _mac_set_eslnum.append((i[0],i[1],len(_esl_list[nn])))
        # _mac_set_eslnum.append((i[0],i[1.txt],_esl_list[nn]))
        nn += 1

    nn = 0
    _fmt = "{:^17}\t{:^12}\t{:^6}"      # 格式化输出
    print(_fmt.format("MAC","SETID","ESL_NUM"))
    while nn < len(mac_list):
        for i in _mac_set_eslnum:
            if mac_list[nn] == i[0]:
                print(_fmt.format(i[0], i[1], i[2]))
        nn += 1


def _get_rom(esl_list, ci=CI, db=DB, collect=COLLECT):
    # 获取失步价签eslid 和总数
    _client = MongoClient(ci)
    _db = _client[db]
    _collect = _db[collect]

    for i in _collect.find({}):
        for k in esl_list:
            if k == i.get('eslId'):
                print(k, i.get('rom'))

def update_query(ci=CI, db=DB, collect=COLLECT):
    # 使用 mongo sql 修改指定ESL信息
    def __get_info_from_txt(fileName):
        f = open(fileName, 'r')
        esl_id_list = list()
        _line = f.readlines()
        for each_line in _line:
            id_ = each_line.strip()
            esl_id_list.append(id_)
        f.close()
        return esl_id_list

    esl_ = input("enter txt name")
    esl_list = __get_info_from_txt(esl_)
    _client = MongoClient(ci)
    _db = _client[db]
    _collect = _db[collect]
    for i in esl_list:
        myquery = {"eslId": i}
        newvalues = {"$set": {"apOffset": 10,"attribute": 0}}
        x = _collect.update_many(myquery, newvalues)
        print(x.modified_count, "文档已修改")




def get_offset_everyset(ci=CI, db=DB, collect=COLLECT):
    # 获取基站下不同SET和ESL总数
    _client = MongoClient(ci)
    _db = _client[db]
    _collect = _db[collect]
    _info_list = list()
    _dict = dict()

    for i in _collect.find({}):
        # print(i.get('binding'))
        offset = i.get('apOffset')
        set_Id = i.get("setId")
        esl = i.get('eslId')
        _info = f"{offset}_{set_Id}|{esl}"
        _info_list.append(_info)


    mac_set_set = set()
    for l in _info_list: mac_set_set.add(l.split("|")[0])
    mac_set_list = list(mac_set_set)
    mac_list = list(set([x.split("_")[0] for x in mac_set_set]))

    # 获取ESL list
    _esl_list = [[] for _ in range(len(mac_set_list))]
    s = 0
    while s < len(mac_set_list):
        for i in _info_list:
            # print(i.split("|")[0])
            if mac_set_list[s] == i.split("|")[0]:
                _idx = mac_set_list.index(mac_set_list[s])
                _esl_list[_idx].append(i.split("|")[-1])
        s += 1

    _mac_set_eslnum = list()
    nn = 0
    while nn < len(mac_set_list):
        i = mac_set_list[nn].split("_")
        _mac_set_eslnum.append((i[0],i[1],len(_esl_list[nn])))
        # _mac_set_eslnum.append((i[0],i[1.txt],_esl_list[nn]))
        nn += 1

    nn = 0
    _fmt = "{:^17}\t{:^12}\t{:^6}"      # 格式化输出
    print(_fmt.format("APOFFSET","SETID","ESL_NUM"))
    while nn < len(mac_list):
        for i in _mac_set_eslnum:
            if mac_list[nn] == i[0]:
                print(_fmt.format(i[0], i[1], i[2]))
        nn += 1



def get_offset_everyset5(ci=CI, db=DB, collect=COLLECT):
    # 获取基站下不同SET和ESL总数,五代价签
    _client = MongoClient(ci)
    _db = _client[db]
    _collect = _db[collect]
    _info_list = list()
    _dict = dict()

    for i in _collect.find({"version": 16}):
        # print(i.get('binding'))
        offset = i.get('apOffset')
        set_Id = i.get("setId")
        esl = i.get('eslId')
        _info = f"{offset}_{set_Id}|{esl}"
        _info_list.append(_info)


    mac_set_set = set()
    for l in _info_list: mac_set_set.add(l.split("|")[0])
    mac_set_list = list(mac_set_set)
    mac_list = list(set([x.split("_")[0] for x in mac_set_set]))

    # 获取ESL list
    _esl_list = [[] for _ in range(len(mac_set_list))]
    s = 0
    while s < len(mac_set_list):
        for i in _info_list:
            # print(i.split("|")[0])
            if mac_set_list[s] == i.split("|")[0]:
                _idx = mac_set_list.index(mac_set_list[s])
                _esl_list[_idx].append(i.split("|")[-1])
        s += 1

    _mac_set_eslnum = list()
    nn = 0
    while nn < len(mac_set_list):
        i = mac_set_list[nn].split("_")
        _mac_set_eslnum.append((i[0],i[1],len(_esl_list[nn])))
        # _mac_set_eslnum.append((i[0],i[1.txt],_esl_list[nn]))
        nn += 1

    nn = 0
    _fmt = "{:^17}\t{:^12}\t{:^6}"      # 格式化输出
    print(_fmt.format("APOFFSET","SETID","ESL_NUM"))
    while nn < len(mac_list):
        for i in _mac_set_eslnum:
            if mac_list[nn] == i[0]:
                print(_fmt.format(i[0], i[1], i[2]))
        nn += 1


def get_mac_everyset5(ci=CI, db=DB, collect=COLLECT):
    # 获取基站下 指定 rom 下的不同SET和ESL总数
    _client = MongoClient(ci)
    _db = _client[db]
    _collect = _db[collect]
    _info_list = list()
    _dict = dict()

    f = open("mac.txt", mode='a+', encoding='utf8')
    for i in _collect.find({"rom": 22}):
        # print(i.get('binding'))
        mac = i.get('apMac')
        set_Id = i.get("setId")
        esl = i.get('eslId')
        _info = f"{mac}_{set_Id}|{esl}"
        _info_list.append(_info)


    mac_set_set = set()
    for l in _info_list: mac_set_set.add(l.split("|")[0])
    mac_set_list = list(mac_set_set)
    mac_list = list(set([x.split("_")[0] for x in mac_set_set]))

    # 获取ESL list
    _esl_list = [[] for _ in range(len(mac_set_list))]
    s = 0
    while s < len(mac_set_list):
        for i in _info_list:
            # print(i.split("|")[0])
            if mac_set_list[s] == i.split("|")[0]:
                _idx = mac_set_list.index(mac_set_list[s])
                _esl_list[_idx].append(i.split("|")[-1])
        s += 1

    _mac_set_eslnum = list()
    nn = 0
    while nn < len(mac_set_list):
        i = mac_set_list[nn].split("_")
        _mac_set_eslnum.append((i[0],i[1],len(_esl_list[nn])))
        # _mac_set_eslnum.append((i[0],i[1.txt],_esl_list[nn]))
        nn += 1

    nn = 0
    _fmt = "{:^17}\t{:^12}\t{:^6}"      # 格式化输出
    print(_fmt.format("MAC","SETID","ESL_NUM"))
    f.write(_fmt.format("MAC","SETID","ESL_NUM \r\n"))
    while nn < len(mac_list):
        for i in _mac_set_eslnum:
            if mac_list[nn] == i[0]:
                print(_fmt.format(i[0], i[1], i[2]))
                f.write(_fmt.format(i[0], i[1], i[2],"\r\n"))
        nn += 1
    f.close()


def is_nosync(ci=CI, db=DB, collect=COLLECT):
    # 组网资源是否重复
    _client = MongoClient(ci)
    _db = _client[db]
    _collect = _db[collect]

    def get_unsync():
        esl_list = list()
        for i in _collect.find({"synced": False}):
            if i.get('rom') == 19:
                esl_list.append(i.get('eslId'))
        return len(esl_list)

    n = 0
    while n < 11520:
        print(f"{n}\t{get_unsync()}\t{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        time.sleep(30)
        n += 1


def find_esl_change():

    __ci = 'mongodb://172.17.120.26:27017/'
    __db = 'esl6ceng4ap97'
    __collect = 'esl'

    macL = ['98:6D:35:79:C5:82','98:6D:35:79:C5:93','98:6D:35:79:C5:B7','98:6D:35:79:C5:AA']
    def get_count(maclist):
        _client = MongoClient(__ci)
        _db = _client[__db]
        _collect = _db[__collect]
        _info_list = list()
        _dict = dict()
        filehandle = open("everymac.csv", mode='a+')
        for m in maclist:
            esl_count = _collect.count_documents({"apMac":f"{m}"})
            print(f"{m}",',',f"{esl_count}",file=filehandle,flush=True)
        filehandle.close()
        _client.close()
    for i in range(10):
        get_count(macL)
        time.sleep(30)

if __name__ == '__main__':
    # esl = input("enter txt")
    # _esl = get_info_from_txt(esl)
    # _get_rom(_esl)
    # is_nosync()
    # get_mac_everyset5()
    # is_repeat()
    # is_repeatmysql()
    # get_mac_everyset()
    find_esl_change()
    # get_bind_eslid()
    # get_mac_everyset()
    # update_query()
    # get_offset_everyset()
    # get_offset_everyset5()
    # get_mac_everyset5()