
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector
import yaml
import sys
import os


def ryaml(key, peer="control"):
    # read yaml file
    homept = os.path.expanduser('~')
    _f = open(f"./run.yml", "r", encoding="utf8")
    config = yaml.load(_f.read(), Loader=yaml.Loader)
    conf = config[peer]
    _f.close()
    return conf[key]


def sql_info(sql_idx='jqfb'):
    _sys = sys.platform
    _f = open(r"./sql.yml", "r", encoding="utf8")
    config = yaml.load(_f.read(), Loader=yaml.Loader)
    ele_dict = config.get("mysql")
    _f.close()
    return ele_dict.get(sql_idx)


def shu_zhu(l):
    n_l = list()
    for i in l:
        n_l.append('\n'.join(i))
        # n_l.append(new)
    # print(n_l)
    return n_l


class msq:
    def __init__(self):
        self.conn = mysql.connector.connect(host=ryaml("host", "db"), user=ryaml("user", "db"),
                                            password=ryaml("password", "db"),
                                            database=ryaml("dbname", "db"), use_unicode=True)
        self.cursor = self.conn.cursor()

    def search(self, sql):
        self.cursor.execute(sql)
        select_data = self.cursor.fetchall()
        print("sql result:={}".format(select_data))
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


class conerShow:
    """
    所有角球的趋势图
    """
    def __init__(self, level='C', year='j22'):
        self.level = level
        self.year = year
        self.cn = f"select round,sum(zc+kc),sum(zj+kj) from {year} where level='{level}' group by round"

    def cn_show(self):
        # 角球数
        s = msq().search(self.cn)
        round_list = list()
        cn_list = list()
        goals_list = list()
        for i in s:
            round_list.append(i[0])
            cn_list.append(i[1])
            goals_list.append(i[2])
        print(round_list, cn_list, goals_list)

        # data = pd.read_excel('./ft.xls')
        # print(data)
        # year = data['round'].to_numpy()
        # round_ = round_list.to_numpy()
        round_ = np.array(round_list)
        cn_data = np.array(cn_list)
        jinqiu = np.array(goals_list)
        # cn_data = cn_list.to_numpy()
        # jinqiu = goals_list.to_numpy()

        N = len(round_)
        x = np.arange(N)

        fig = plt.figure()
        sub = fig.add_subplot(111)

        wid = 0.4
        x1 = x - wid / 2
        x2 = x + wid / 2
        sub.bar(x1, cn_data, label='jiaoqiu', width=wid, alpha=0.75, edgecolor='k', hatch='')
        sub.bar(x2, jinqiu, label='jinqiu', width=wid, alpha=0.75, edgecolor='k', hatch='')

        for i in range(N):
            sub.text(x1[i], cn_data[i], '{:.1f}'.format(cn_data[i]), verticalalignment='bottom',
                     horizontalalignment='center')
            sub.text(x2[i], jinqiu[i], '{:.1f}'.format(jinqiu[i]), verticalalignment='bottom',
                     horizontalalignment='center')
        sub.tick_params(axis='x', length=0)
        sub.set_xticks(x)
        sub.set_xticklabels(x)
        # sub.set_xlabel(f'2022 year match round', fontsize=15)
        # sub.set_ylabel('total coner', fontsize=15)
        sub.set_xlabel(f'{self.year[1::]} year {self.level} match round', fontsize=15)
        sub.set_ylabel(f'{self.year[1::]} year total coner', fontsize=15)

        plt.show()
        """
        cn_data = data.iloc[:, 1].to_numpy()
        jinqiu = data.iloc[:, 2].to_numpy()
        print(year)
        print(cn_data)

        """

    def banquanchang(self):
        # 半全场,横向对比每年的半全场比例
        s = msq().search(self.bqc)
        type_list = list()
        # cn_list = list()
        goals_list = list()
        for i in s:
            type_list.append(i[0])
            # cn_list.append(i[1])
            goals_list.append(i[1])
        print(type_list, goals_list)

        banquan = np.array(type_list)
        cn_data = np.array(goals_list)

        N = len(banquan)
        x = np.arange(N)

        fig = plt.figure()
        sub = fig.add_subplot(111)

        wid = 0.4
        x1 = x - wid / 2
        x2 = x + wid / 2
        sub.bar(x1, banquan, label='banchangchang', width=wid, alpha=0.75, edgecolor='k', hatch='')
        sub.bar(x2, cn_data, label='jinqiu', width=wid, alpha=0.75, edgecolor='k', hatch='')
        for i in range(N):
            sub.text(x1[i], banquan[i], '{}'.format(cn_data), verticalalignment='bottom',
                     horizontalalignment='center')
            sub.text(x2[i], cn_data[i], '{:.1f}'.format(cn_data[i]), verticalalignment='bottom',
                     horizontalalignment='center')
        sub.tick_params(axis='x', length=0)
        sub.set_xticks(x)
        sub.set_xticklabels(x)
        sub.set_xlabel(f'{self.year[1::]} year {self.level} match round', fontsize=15)
        sub.set_ylabel(f'{self.year[1::]} year total coner', fontsize=15)
        plt.show()

    def every_round_data(self):
        # 进球次数分配
        _sql = sql_info('jqfb')
        sql_ = _sql.format(year='j22', level='A', round=1)
        s = msq().search(sql_)

        type_list = list()
        result_list = list()
        for i in s:
            type_list.append(i[0])
            result_list.append(i[1])
        print(type_list, result_list)

        type_ = np.array(type_list)
        result_ = np.array(result_list)

        N = len(result_)
        x = np.arange(N)

        fig = plt.figure()
        sub = fig.add_subplot(111)

        wid = 0.4
        x1 = x - wid / 2
        y1 = x + wid / 2
        sub.bar(x1, type_, label='进球个数', width=wid, alpha=0.75, edgecolor='k', hatch='')
        sub.bar(y1, result_, label='出现次数', width=wid, alpha=0.75, edgecolor='k', hatch='')

        # for i in range(N):
        #     sub.text(x1[i], type_[i], '{:.1f}'.format(type_[i]), verticalalignment='bottom', horizontalalignment='center')
        #
        #     sub.text(x2[i], result_[i], '{:.1f}'.format(result_[i]), verticalalignment='bottom',  horizontalalignment='center')

        sub.tick_params(axis='x', length=0)
        sub.set_xticks(x)
        sub.set_xticklabels(x)
        sub.set_xlabel(f'{self.year[1::]} year {self.level} match round', fontsize=15)
        sub.set_ylabel(f'{self.year[1::]} year total coner', fontsize=15)
        plt.show()

    def single_bar_cno(self):

        _sql = sql_info('cno')
        sql_ = _sql.format(year='j21', level='A', round=1)
        s = msq().search(sql_)

        _key_list = list()
        _val_list = list()
        for i in s:
            _key_list.append(i[0])
            _val_list.append(i[1])

        print(_key_list, _val_list)
        # 数据

        type_ = np.array(_key_list)
        result_ = np.array(_val_list)

        N = len(type_)
        x = np.arange(N)

        fig = plt.figure()
        sub = fig.add_subplot(111)

        x1 = y1 = 3
        wid= 0.4

        for i in range(N):
            sub.text(x1[i], type_[i], '{:.1f}'.format(type_[i]), verticalalignment='bottom', horizontalalignment='center')
            sub.text(x2[i], result_[i], '{:.1f}'.format(result_[i]), verticalalignment='bottom',  horizontalalignment='center')


        sub.bar(x1, type_, label='进球个数', width=wid, alpha=0.75, edgecolor='k', hatch='')
        sub.bar(y1, result_, label='出现次数', width=wid, alpha=0.75, edgecolor='k', hatch='')

        sub.tick_params(axis='x', length=0)
        sub.set_xticks(x)
        sub.set_xticklabels(x)
        sub.set_xlabel(f'{self.year[1::]} year {self.level} match round', fontsize=15)
        sub.set_ylabel(f'{self.year[1::]} year total coner', fontsize=15)
        plt.show()

    def bar_demo(self, l):
        data_l = l
        data_element_len = data_l[0].__len__()
        martix = [[] for _ in range(data_element_len)]

        n = 0
        while n < len(martix):
            for i in data_l:
                martix[n].append(i[n])
            n += 1

        for i in range(data_element_len):
            name = f"data_{i}"
            name = np.array(martix[i])

        x = np.arange(len(martix[0]))

        fig = plt.figure()
        sub = fig.add_subplot(111)

    def check_sql(self):
        _sql = sql_info('wwl')
        sql_ = _sql.format(year='j22', level='A', round=1)
        s = msq().search(sql_)

    def create_plt(self):
        fig = plt.figure(figsize=(20, 1))    # figsize(15,5) 15=长，单位 英尺   5=宽， 单位英尺
        axg1 = fig.add_subplot(121)             # 121  整个figure分成1行2列，共2个子图，这里子图在第一行第一列
        axg2 = fig.add_subplot(122)             # 122 表示子图在第一行第二列
        axg2.axis('off')                        # 关闭axg2 的显示
        axg1.set_title('axg1 de title ' )       # 设置axg1 的title
        axg1.imshow()
        plt.show()

    def single(self):
        YEAR = 'j20'
        LEVEL = 'A'
        ROUND = 1

        _info = sql_info('bqc')
        sql_ = _info.get('sql').format(year=YEAR, level=LEVEL, round=ROUND)
        s = msq().search(sql_)

        _key_list = list()
        _val_list = list()
        for i in s:
            _key_list.append(i[0])
            _val_list.append(i[1])

        plt.figure(figsize=(20, 15), dpi=90)                            # figsize(15,5) 15=长，单位 英尺   5=宽， 单位英尺
        plt.rcParams["font.sans-serif"] = ['SimHei']
        plt.rcParams["axes.unicode_minus"] = False

        for i in range(len(_key_list)):
            plt.bar(_key_list[i], _val_list[i], alpha=1, width=1)

        plt.title(_info.get('des').format(year=YEAR, level=LEVEL, round=ROUND))
        plt.xlabel(_info.get('xlabel').format(year=YEAR, level=LEVEL, round=ROUND))
        plt.ylabel(_info.get('ylabel').format(year=YEAR, level=LEVEL, round=ROUND))

        for i in range(len(_key_list)):
            plt.text(_key_list[i], _val_list[i], _val_list[i], ha='center', fontsize=15)       # 给柱状图顶端标注值

        plt.show()
        plt.close('all')

    def run(self):
        # self.cn_show()
        # self.banquanchang()
        # self.every_round_data()
        # self.single_bar_cno()
        # self.check_sql()
        # self.bar_demo(l)
        # self._single_test()
        # self.every_round_data()
        # self.create_plt()
        self.single()


if __name__ == '__main__':
    # conerShow().run()
    import re

