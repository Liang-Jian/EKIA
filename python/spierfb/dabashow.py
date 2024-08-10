import gc

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
    _f = open(r".\sql.yml", "r", encoding="utf8")
    config = yaml.load(_f.read(), Loader=yaml.Loader)
    ele_dict = config.get("mysql")
    _f.close()
    return ele_dict.get(sql_idx)


def shu_pai(l):
    # 竖排字符串
    n_l = list()
    for i in l:
        n_l.append('\n'.join(i))
    return n_l


def save():
    pass


def listadd(l):
    # list中的元素相邻递增
    step = 1
    b = [sum(l[:i+1]) for i in range(len(l))]
    c = [x * step for x in b]
    # print(c)
    return c


class msq:
    def __init__(self):
        self.conn = mysql.connector.connect(host=ryaml("host", "db"), user=ryaml("user", "db"),
                                            password=ryaml("password", "db"),
                                            database=ryaml("dbname", "db"), use_unicode=True)
        self.cursor = self.conn.cursor()

    def search(self, sql):
        self.cursor.execute(sql)
        select_data = self.cursor.fetchall()
        # print("sql result:={}".format(select_data))
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
    def __init__(self, level='A', year='j23', round=1, team='広島'):
        self.level = level
        self.year = year
        self.round = round
        self.team = team
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
        cn_data = data.iloc[:, 1.txt].to_numpy()
        jinqiu = data.iloc[:, 2].to_numpy()
        print(year)
        print(cn_data)

        """

    # def banquanchang(self):
    #     # 半全场,进球数横向比较
    #     # s = msq().search(self.bqc)
    #     SQL = sql_info('bqc').get('sql')
    #     print(SQL)
    #     s = msq().search(SQL.format(level=self.level,year=self.year))
    #     type_list = list()
    #     # cn_list = list()
    #     goals_list = list()
    #     for i in s:
    #         type_list.append(i[0])
    #         # cn_list.append(i[1.txt])
    #         goals_list.append(i[1])
    #     print(type_list, goals_list)
    #
    #     banquan = np.array(type_list)
    #     cn_data = np.array(goals_list)
    #
    #     N = len(banquan)
    #     x = np.arange(N)
    #
    #     fig = plt.figure()
    #     sub = fig.add_subplot(111)
    #
    #     wid = 0.4
    #     x1 = x - wid / 2
    #     x2 = x + wid / 2
    #     sub.bar(x1, banquan, label='banchangchang', width=wid, alpha=0.75, edgecolor='k', hatch='')
    #     sub.bar(x2, cn_data, label='jinqiu', width=wid, alpha=0.75, edgecolor='k', hatch='')
    #     for i in range(N):
    #         sub.text(x1[i], banquan[i], '{}'.format(cn_data), verticalalignment='bottom',
    #                  horizontalalignment='center')
    #         sub.text(x2[i], cn_data[i], '{:.1f}'.format(cn_data[i]), verticalalignment='bottom',
    #                  horizontalalignment='center')
    #     sub.tick_params(axis='x', length=0)
    #     sub.set_xticks(x)
    #     sub.set_xticklabels(x)
    #     sub.set_xlabel(f'{self.year[1::]} year {self.level} match round', fontsize=15)
    #     sub.set_ylabel(f'{self.year[1::]} year total coner', fontsize=15)
    #     plt.show()

    def banquanchang(self):
        '''半全场的一个分布图, 柱状图'''
        def _autolabel(rects):
            """ 柱状图添加数值 """
            for rect in rects:
                height = rect.get_height()
                plt.text(rect.get_x() + rect.get_width() / 2. - 0.08, 1.03 * height, '%s' % int(height), size=10, family="Times new roman")

        plt.rcParams['font.sans-serif'] = ['SimHei']
        __ICON = "bqc"
        SQL = sql_info(__ICON).get('sql')
        # print(SQL)
        data = msq().search(SQL.format(level=self.level, year=self.year))
        a = np.array(data)
        banquan_x = a[:, 0]
        loop_count_y = [int(x) for x in a[:, 1]]

        cm = plt.bar(banquan_x, loop_count_y, align='center', alpha=1, color=['b', 'g', 'r', 'c', 'm', 'y', 'k',])
        _autolabel(cm)
        plt.yticks(range(0, max(loop_count_y)+2, 3))
        plt.ylabel('总次数', size=12)
        plt.xlabel('半全场', size=13)
        plt.grid(True, linestyle='-', alpha=0.1)
        plt.title(sql_info(__ICON).get('des').format(level=self.level, year=self.year))
        # plt.show()
        plt.savefig(sql_info(__ICON).get('des').format(year=self.year, level=self.level), dpi=440, bbox_inches='tight')# )   # transparent=True,
        plt.close()

    def soccor_detail(self):

        __ICON = "ss"
        '''进球数分布图, 柱状图'''
        def _autolabel(rects):
            for rect in rects:
                height = rect.get_height()
                plt.text(rect.get_x() + rect.get_width() / 2. - 0.08, 1.03 * height, '%s' % int(height), size=10, family="Times new roman")

        plt.rcParams['font.sans-serif'] = ['SimHei']
        SQL = sql_info(__ICON).get('sql')
        data = msq().search(SQL.format(level=self.level, year=self.year))
        a = np.array(data)
        banquan_x = a[:, 0]
        loop_count_y = [int(x) for x in a[:, 1]]
        cm = plt.bar(banquan_x, loop_count_y, align='center', alpha=1, color=['b', 'g', 'r', 'c', 'm', 'y', 'k',])
        _autolabel(cm)
        plt.yticks(range(0, max(loop_count_y)+2, 3))
        plt.xticks(range(0, len(banquan_x) + 1, 1))
        plt.ylabel(sql_info(__ICON).get('ylabel'), size=12)
        plt.xlabel(sql_info(__ICON).get('xlabel'), size=12)
        plt.grid(True, linestyle='-', alpha=0.1)
        plt.title(sql_info(__ICON).get('des').format(level=self.level, year=self.year))
        # plt.show()
        plt.savefig(sql_info(__ICON).get('des').format(year=self.year, level=self.level), dpi=440, bbox_inches='tight')# )   # transparent=True,
        plt.close()
        gc.collect()

    def wld_detail(self):

        __ICON = "wwl"
        '''胜平负分布图, 柱状图'''
        def _autolabel(rects):
            for rect in rects:
                height = rect.get_height()
                plt.text(rect.get_x() + rect.get_width() / 2. - 0.08, 1.03 * height, '%s' % int(height), size=10, family="Times new roman")

        plt.rcParams['font.sans-serif'] = ['SimHei']
        SQL = sql_info(__ICON).get('sql')
        data = msq().search(SQL.format(level=self.level, year=self.year))
        a = np.array(data)
        banquan_x = a[:, 0]
        loop_count_y = [int(x) for x in a[:, 1]]
        cm = plt.bar(banquan_x, loop_count_y, align='center', alpha=1, color=['b', 'g', 'r', 'c', 'm', 'y', 'k',])
        _autolabel(cm)
        plt.yticks(range(0, max(loop_count_y)+2, 5))
        plt.xticks(range(0, len(banquan_x) , 1))
        plt.ylabel(sql_info(__ICON).get('ylabel'), size=12)
        plt.xlabel(sql_info(__ICON).get('xlabel'), size=12)
        plt.grid(True, linestyle='-', alpha=0.1)
        plt.title(sql_info(__ICON).get('des').format(level=self.level, year=self.year))
        # plt.show()
        plt.savefig(sql_info(__ICON).get('des').format(year=self.year, level=self.level), dpi=440, bbox_inches='tight')# )   # transparent=True,
        plt.close()
        gc.collect()

    def conner_detail(self):
        __ICON = "cn"
        '''角球分布图, 柱状图'''
        def _autolabel(rects):
            for rect in rects:
                height = rect.get_height()
                plt.text(rect.get_x() + rect.get_width() / 2. - 0.08, 1.03 * height, '%s' % int(height), size=10, family="Times new roman")

        plt.rcParams['font.sans-serif'] = ['SimHei']
        SQL = sql_info(__ICON).get('sql')
        data = msq().search(SQL.format(level=self.level, year=self.year))
        a = np.array(data)
        banquan_x = a[:, 0]
        loop_count_y = [int(x) for x in a[:, 1]]
        cm = plt.bar(banquan_x, loop_count_y, align='center', alpha=1, color=['b', 'g', 'r', 'c', 'm', 'y', 'k',])
        _autolabel(cm)
        plt.yticks(range(0, max(loop_count_y)+2, 5))
        plt.xticks(range(0, max(banquan_x) + 2, 1))                             # 按照角球数最大的值去做
        plt.ylabel(sql_info(__ICON).get('ylabel'), size=12)
        plt.xlabel(sql_info(__ICON).get('xlabel'), size=12)
        plt.grid(True, linestyle='-', alpha=0.1)
        plt.title(sql_info(__ICON).get('des').format(level=self.level, year=self.year))
        # plt.show()
        plt.savefig(sql_info(__ICON).get('des').format(year=self.year, level=self.level), dpi=440, bbox_inches='tight')# )   # transparent=True,
        plt.close()
        gc.collect()

    def bestzhu(self):
        '''
        主场战绩最好的队伍
        :return:
        '''
        __ICON = "bzhu"
        def _autolabel(rects):
            """ 柱状图添加数值 """
            for rect in rects:
                height = rect.get_height()
                plt.text(rect.get_x() + rect.get_width() / 2. - 0.08, 1.03 * height, '%s' % int(height), size=10, family="Times new roman")
        plt.rcParams['font.sans-serif'] = ['SimHei']        # windows 下忽略字体错误
        # plt.style.use('dark_background')                    # 设置绘图风格
        SQL = sql_info(__ICON).get('sql').format(year=self.year, level=self.level, round=self.round)
        data = msq().search(SQL)
        a = np.array(data)
        team = shu_pai(a[:, 0])
        loop_count = [int(x) for x in a[:, 1]]                                  # 需要转为int类型
        cm = plt.bar(team, loop_count, align='center', alpha=1, color=['b', 'g', 'r', 'c', 'm', 'y', 'k',])
        _autolabel(cm)
        plt.yticks(range(0, max(loop_count)+2, 1))                              # 为了美观，最大值+2
        plt.ylabel(sql_info(__ICON).get('ylabel'), size=12)
        plt.xlabel(sql_info(__ICON).get('xlabel'), size=12)
        plt.title(sql_info(__ICON).get('des').format(year=self.year, level=self.level))
        # plt.show()
        plt.savefig(sql_info(__ICON).get('des').format(year=self.year, level=self.level), dpi=440, bbox_inches='tight')# )   # transparent=True,
        plt.close()
        gc.collect()

    def bestke(self):
        '''客场战绩最好的队伍'''
        __ICON = "bke"
        def _autolabel(rects):
            """ 柱状图添加数值 """
            for rect in rects:
                height = rect.get_height()
                plt.text(rect.get_x() + rect.get_width() / 2. - 0.08, 1.03 * height, '%s' % int(height), size=10, family="Times new roman")
        plt.rcParams['font.sans-serif'] = ['SimHei']        # windows 下忽略字体错误
        # plt.style.use('dark_background')                    # 设置绘图风格
        SQL = sql_info(__ICON).get('sql').format(year=self.year, level=self.level, round=self.round)
        data = msq().search(SQL)
        a = np.array(data)
        team = shu_pai(a[:, 0])
        loop_count = [int(x) for x in a[:, 1]]                                  # 需要转为int类型
        cm = plt.bar(team, loop_count, align='center', alpha=1, color=['b', 'g', 'r', 'c', 'm', 'y', 'k',])
        _autolabel(cm)
        plt.yticks(range(0, max(loop_count)+2, 1))                              # 为了美观，最大值+2
        plt.ylabel(sql_info(__ICON).get('ylabel'), size=12)
        plt.xlabel(sql_info(__ICON).get('xlabel'), size=12)
        plt.title(sql_info(__ICON).get('des').format(year=self.year, level=self.level))
        # plt.show()
        plt.savefig(sql_info(__ICON).get('des').format(year=self.year, level=self.level), dpi=440, bbox_inches='tight')# )   # transparent=True,
        plt.close()
        gc.collect()

    def teamView(self):
        """
        折线图，输出球队，在某年的变化趋势图
        """
        __ICON = "teamv"
        plt.rcParams['font.sans-serif'] = ['SimHei']
        # plt.style.use('dark_background')                    # 设置绘图风格
        jround = [x for x in range(1,  35)]
        val = list()
        for x in jround:
            sql = sql_info(__ICON).get('sql').format(year=self.year, level=self.level, round=x, team=self.team)
            v = msq().search(sql)
            val.append(int(v[0][0]))

        val_ = listadd(val)
        for i, j in zip(jround, val_): plt.annotate(str(j), xy=(i, j), xytext=(-10, 5), textcoords='offset points')   # 相加
        # plt.figure(figsize=(20, 10), dpi=100)
        plt.plot(jround, val_, c='red')         #
        plt.scatter(jround, val_, c='red')      #
        plt.xticks(range(1, len(jround) + 1, 1))
        plt.yticks(range(1, max(val_)+1, 3))
        plt.grid(True, linestyle='--', alpha=0.2)   # 背景网格
        plt.xlabel(sql_info(__ICON).get('xlabel'), size=13)
        plt.ylabel(sql_info(__ICON).get('ylabel'), size=13)
        plt.title(sql_info(__ICON).get('des').format(year=self.year, level=self.level, team=self.team))
        # plt.show()
        plt.savefig(sql_info(__ICON).get('des').format(year=self.year, level=self.level, team=self.team), dpi=500, bbox_inches='tight')# )   # transparent=True,
        plt.close()
        gc.collect()

    def team_diff(self, teamA='札幌',teamB='名古屋'):
        """
        折线图，输出两支球队的总积分变化对比图，在某年的变化趋势图
        """
        __ICON = "teamd"
        plt.rcParams['font.sans-serif'] = ['SimHei']        # windows 下忽略字体错误
        # plt.style.use('dark_background')                    # 设置绘图风格
        plt.figure(figsize=(20, 8))
        plt.rcParams['axes.unicode_minus'] = False          # 用来正常显示负号
        jround = [x for x in range(1, 35)]

        def _Get_score(_team):
            val = list()
            for x in jround:
                sql = sql_info(__ICON).get('sql').format(year=self.year, level=self.level, round=x, team=_team)
                v = msq().search(sql)
                val.append(int(v[0][0]))
            return val

        team_a_data = listadd(_Get_score(teamA))
        team_b_data = listadd(_Get_score(teamB))

        for a, b in zip(jround, team_a_data):
            plt.text(a, b + 0.05, b, ha='center', va='bottom', fontsize=12, color='blue')
        for c, d in zip(jround, team_b_data):
            plt.text(c, d + 0.05, d, ha='center', va='bottom', fontsize=12, color='orange')

        plt.xlabel('比赛轮次')
        plt.ylabel('比赛总积分')
        plt.xticks(range(1, len(jround) + 1, 1))
        plt.yticks(range(0, max(team_b_data) + 2, 2))
        plt.plot(jround, team_a_data, label=f"{teamA}")      # 传入x和y1,通过plot绘制出折线图
        plt.plot(jround, team_b_data, label=f"{teamB}")
        plt.grid(True, linestyle='-', alpha=1)
        plt.legend()                                         # 图例
        plt.title(sql_info(__ICON).get('des').format(year=self.year, level=self.level, teamA=teamA, teamB=teamB))
        # plt.show()
        plt.savefig(sql_info(__ICON).get('des').format(year=self.year, level=self.level, teamA=teamA), dpi=440, bbox_inches='tight')# )   # transparent=True,
        plt.close()
        gc.collect()

    def team_diff_area(self,teamA='FC東京', teamB='広島'):
        """
        折线图，输出两支球队的在一段时间内积分变化对比图，在某年的变化趋势图
        """
        __ICON = "teamwl"
        plt.rcParams['font.sans-serif'] = ['SimHei']        # windows 下忽略字体错误
        # plt.style.use('dark_background')                    # 设置绘图风格
        plt.figure(figsize=(20, 8))
        plt.rcParams['axes.unicode_minus'] = False          # 用来正常显示负号
        jround = [x for x in range(1, 35)]

        def _Get_score(_team):
            val = list()
            for x in jround:
                sql = sql_info(__ICON).get('sql').format(year=self.year, level=self.level, round=x, team=_team)
                v = msq().search(sql)
                val.append(int(v[0][0]))
            return val

        team_a_data = _Get_score(teamA)
        team_b_data = _Get_score(teamB)

        # 添加图示
        for a, b in zip(jround, team_a_data):
            plt.text(a, b + 0.05, b, ha='center', va='bottom', fontsize=12, color='blue')
        for c, d in zip(jround, team_b_data):
            plt.text(c, d + 0.05, d, ha='center', va='bottom', fontsize=12, color='orange')

        plt.xlabel(sql_info(__ICON).get('xlabel'), size=12)
        plt.ylabel(sql_info(__ICON).get('ylabel'), size=12)
        plt.xticks(range(1, len(jround) + 2, 1))
        plt.yticks(range(0, max(team_b_data) + 1, 1))
        plt.plot(jround, team_a_data, label=f"{teamA}")      # 传入x和y1,通过plot绘制出折线图
        plt.plot(jround, team_b_data, label=f"{teamB}")
        plt.grid(True, linestyle='-', alpha=0.2)
        plt.legend()                                         # 图例
        plt.title(sql_info(__ICON).get('des').format(year=self.year, level=self.level, teamA=teamA, teamB=teamB))
        # plt.show()
        # plt.savefig("asdf", dpi=440, bbox_inches='tight')# )   # transparent=True,
        plt.savefig(sql_info(__ICON).get('des').format(year=self.year, level=self.level, teamA=teamA), dpi=440, bbox_inches='tight')# )   # transparent=True,
        plt.close()
        gc.collect()

    def over_big25(self):
        """某年某级别全场进球大于2.5的总数排名"""
        __ICON = "over2"
        def _autolabel(rects):
            """ 柱状图添加数值 """
            for rect in rects:
                height = rect.get_height()
                plt.text(rect.get_x() + rect.get_width() / 2. - 0.08, 1.03 * height, '%s' % int(height), size=10,
                         family="Times new roman")

        SQL = sql_info(__ICON).get('sql').format(level=self.level, year=self.year)
        s = msq().search(SQL)
        a = np.array(s)
        match_team = shu_pai(a[:, 0])
        match_data = [int(x) for x in a[:, 1]]
        plt.rcParams['font.sans-serif'] = ['SimHei']
        cm = plt.bar(match_team, match_data, align='center', alpha=1, color=['b', 'g', 'r', 'c', 'm', 'y', 'k', ])
        _autolabel(cm)
        plt.xticks(range(0, len(match_team) + 1, 1))
        plt.yticks(range(1, max(match_data) + 2, 1))
        plt.ylabel(sql_info(__ICON).get('ylabel'), size=12)
        plt.xlabel(sql_info(__ICON).get('xlabel'), size=12)
        plt.grid(True, linestyle='-', alpha=0.3)  # 背景网格
        # plt.legend(loc=0)
        plt.title(sql_info(__ICON).get('des').format(year=self.year, level=self.level))
        # plt.show()
        plt.savefig(sql_info(__ICON).get('des').format(year=self.year, level=self.level, team=self.team), dpi=440, bbox_inches='tight')# )   # transparent=True,
        plt.close()
        gc.collect()

    def small_big25(self):
        """某年某级别全场进球小于于2.5的总数排名"""
        __ICON = "small2"
        def _autolabel(rects):
            """ 柱状图添加数值 """
            for rect in rects:
                height = rect.get_height()
                plt.text(rect.get_x() + rect.get_width() / 2. - 0.08, 1.03 * height, '%s' % int(height), size=10,
                         family="Times new roman")

        SQL = sql_info(__ICON).get('sql').format(level=self.level, year=self.year)
        s = msq().search(SQL)
        a = np.array(s)
        match_team = shu_pai(a[:, 0])
        match_data = [int(x) for x in a[:, 1]]
        plt.rcParams['font.sans-serif'] = ['SimHei']
        cm = plt.bar(match_team, match_data, align='center', alpha=1, color=['b', 'g', 'r', 'c', 'm', 'y', 'k', ])
        _autolabel(cm)
        plt.xticks(range(0, len(match_team) + 1, 1))
        plt.yticks(range(1, max(match_data) + 2, 1))
        plt.ylabel(sql_info(__ICON).get('ylabel'), size=12)
        plt.xlabel(sql_info(__ICON).get('xlabel'), size=12)
        plt.grid(True, linestyle='-', alpha=0.3)  # 背景网格
        # plt.legend(loc=0)
        plt.title(sql_info(__ICON).get('des').format(year=self.year, level=self.level))
        plt.savefig(sql_info(__ICON).get('des').format(year=self.year, level=self.level, team=self.team), dpi=440, bbox_inches='tight')# )   # transparent=True,
        plt.close()
        gc.collect()

    def everyt_conner(self):
        '''获取某个队伍的角球趋势图'''
        __ICON = "ecd"
        SQL = sql_info(__ICON).get('sql').format(level=self.level, year=self.year, team=self.team)
        s = msq().search(SQL)
        a = np.array(s)
        team_round = a[:, 0]
        conner_count = [int(x) for x in a[:, 1]]
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.plot(team_round, conner_count, 's-', color='blue', label="角球趋势图")    # 示例
        plt.xlabel(sql_info(__ICON).get('xlabel'), size=12)                                        # 横坐标名字
        plt.ylabel(sql_info(__ICON).get('ylabel'), size=12)                         # 纵坐标名字
        plt.xticks(range(0, len(team_round) + 1, 1))                                          # (0,23) 范围0-23 ，单位 1
        plt.yticks(range(0, max(conner_count) + 2, 2))                                          # (0,23) 范围0-100 ，单位 4
        plt.grid(True, linestyle='--', alpha=0.5)   # 背景网格
        plt.title(sql_info(__ICON).get('des').format(year=self.year, level=self.level, team=self.team))
        plt.legend(loc=0)                                                                   # 图例
        # plt.show()
        plt.savefig(sql_info(__ICON).get('des').format(year=self.year, level=self.level, team=self.team), dpi=440, bbox_inches='tight')# )   # transparent=True,
        plt.close()
        gc.collect()

    def everyr_pingju(self):
        '''每轮的平局次数'''
        __ICON = "eco"
        SQL = sql_info(__ICON).get('sql').format(level=self.level, year=self.year)
        s = msq().search(SQL)
        a = np.array(s)
        match_round = a[:, 0]
        conner_count= a[:, 1]
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.plot(match_round, conner_count,
                 linewidth=2,
                 color='steelblue',
                 marker='o',
                 markersize=6,
                 markeredgecolor='black',
                 markerfacecolor='brown') # 示例
        plt.xticks(range(1, len(match_round) + 1, 1))                                          # (0,23) 范围0-23 ，单位 1
        plt.yticks(range(0, max(conner_count) + 2, 1))                                          # (0,23) 范围0-100 ，单位 4
        plt.xlabel(sql_info(__ICON).get('xlabel'), size=13)                                                 # 横坐标名字
        plt.ylabel(sql_info(__ICON).get('ylabel'), size=13)                                             # 纵坐标名字
        plt.grid(True, linestyle='--', alpha=0.5)   # 背景网格
        plt.title(sql_info(__ICON).get('des').format(year=self.year, level=self.level))
        # plt.show()
        # plt.legend(loc="best")                                             # 图例
        plt.savefig(sql_info(__ICON).get('des').format(year=self.year, level=self.level, team=self.team), dpi=440, bbox_inches='tight')# )   # transparent=True,
        plt.close()
        gc.collect()

    def everyr_conner_count(self):
        '''每轮的角球总数'''
        __ICON = "ecc"
        SQL = sql_info(__ICON).get('sql').format(level=self.level, year=self.year)
        s = msq().search(SQL)
        a = np.array(s)
        match_round = a[:, 0]
        conner_count = [int(x) for x in a[:, 1]]
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.plot(match_round, conner_count, 's-', color='b', label="角球变化趋势图")    # 示例
        plt.xlabel(sql_info(__ICON).get('xlabel'), size=13)                           # 横坐标名字
        plt.ylabel(sql_info(__ICON).get('ylabel'), size=13)                           # 纵坐标名字
        plt.xticks(range(1, len(match_round) + 1, 1))                                # (0,23) 范围0-23 ，单位 1
        plt.yticks(range(0, max(conner_count) + 2, 5))
        plt.grid(True, linestyle='--', alpha=.3)                                     # (0,23) 范围0-100 ，单位 4
        plt.legend(loc="best")                                                      # 图例
        plt.title(sql_info(__ICON).get('des').format(year=self.year, level=self.level))
        # plt.show()
        plt.savefig(sql_info(__ICON).get('des').format(year=self.year, level=self.level, team=self.team), dpi=440, bbox_inches='tight')# )   # transparent=True,
        plt.close()
        gc.collect()

    def halfmatchsmall15(self):
        '''每轮上半场进球小于1.5 的次数'''
        __ICON = "hms15"
        SQL = sql_info(__ICON).get('sql').format(level=self.level, year=self.year)
        s = msq().search(SQL)
        a = np.array(s)
        match_round = a[:, 0]
        conner_count = a[:, 1]
        plt.rcParams['font.sans-serif'] = ['SimHei']
        # plt.style.use('dark_background')
        plt.plot(match_round, conner_count, 's-', color='y', label='')
        plt.xticks(range(1, len(match_round) + 1, 1))
        plt.yticks(range(0, max(conner_count) + 2, 1))
        plt.xlabel(sql_info(__ICON).get('xlabel'), size=13)
        plt.ylabel(sql_info(__ICON).get('ylabel'), size=13)
        plt.grid(True, linestyle='--', alpha=0.3)
        plt.title(sql_info(__ICON).get('des').format(year=self.year, level=self.level))
        # plt.legend(loc="best")
        # plt.show()
        plt.savefig(sql_info(__ICON).get('des').format(year=self.year, level=self.level), dpi=440, bbox_inches='tight')  #  transparent=True,透明背景
        plt.close()
        gc.collect()

    def ke_coner_count(self):
        '''客场角球>=8个出现的次数排行'''

        def _autolabel(rects):
            """ 柱状图添加数值 """
            for rect in rects:
                height = rect.get_height()
                plt.text(rect.get_x() + rect.get_width() / 2. - 0.08, 1.03 * height, '%s' % int(height), size=10, family="Times new roman")

        __ICON = "kcc"
        SQL = sql_info(__ICON).get('sql').format(level=self.level, year=self.year)
        s = msq().search(SQL)
        a = np.array(s)
        match_round = a[:, 0]
        connr_count = [int(x) for x in a[:, 1]]
        plt.rcParams['font.sans-serif'] = ['SimHei']
        cm = plt.bar(match_round, connr_count, align='center', alpha=1, color=['b', 'g', 'r', 'c', 'm', 'y', 'k',])
        _autolabel(cm)
        plt.yticks(range(1, max(connr_count)+2, 1))                              # 为了美观，最大值+2
        plt.xlabel(sql_info(__ICON).get('xlabel'), size=13)
        plt.ylabel(sql_info(__ICON).get('ylabel'), size=13)
        plt.grid(True, linestyle='--', alpha=0.3)                               # 背景网格
        plt.title(sql_info(__ICON).get('des').format(year=self.year, level=self.level))
        # plt.show()
        plt.savefig(sql_info(__ICON).get('des').format(year=self.year, level=self.level, team=self.team),  dpi=440, bbox_inches='tight')# )   # transparent=True,透明背景
        plt.close()
        gc.collect()

    def onetbqc(self):
        '''某一个队伍半全场的一个分布图, 柱状图'''
        def _autolabel(rects):
            """ 柱状图添加数值 """
            for rect in rects:
                height = rect.get_height()
                plt.text(rect.get_x() + rect.get_width() / 2. - 0.08, 1.03 * height, '%s' % int(height), size=10, family="Times new roman")
        __ICON = 'onetbqc'
        SQL = sql_info(__ICON).get('sql').format(level=self.level, year=self.year, team=self.team)
        data = msq().search(SQL.format(level=self.level, year=self.year))
        a = np.array(data)
        banquan_x = a[:, 0]
        plt.rcParams['font.sans-serif'] = ['SimHei']
        loop_count_y = [int(x) for x in a[:, 1]]
        cm = plt.bar(banquan_x, loop_count_y, align='center', alpha=1, color=['b', 'g', 'r', 'c', 'm', 'y', 'k',])
        _autolabel(cm)
        plt.xlabel(sql_info(__ICON).get('xlabel'), size=13)
        plt.ylabel(sql_info(__ICON).get('ylabel'), size=13)
        plt.yticks(range(0, max(loop_count_y) + 2, 3))
        plt.grid(True, linestyle='-', alpha=0.1)
        plt.title(sql_info(__ICON).get('des').format(year=self.year, level=self.level, team=self.team))
        # plt.show()
        plt.savefig(sql_info(__ICON).get('des').format(year=self.year, level=self.level, team=self.team), dpi=440, bbox_inches='tight')# )   # 保存
        plt.close()
        gc.collect()
    def run(self):
        # self.cn_show()
        self.banquanchang()
        # self.soccor_detail()
        # self.check_sql()
        # self.wld_detail()
        # self.conner_detail()
        # self.bestzhu()
        # self.bestke()
        # self.teamView()
        # self.team_diff()
        # self.team_diff_area()
        # self.over_big25()
        # self.small_big25()
        # self.everyt_conner()
        # self.everyr_pingju()
        # self.everyr_conner_count()
        # self.halfmatchsmall15()
        # self.ke_coner_count()
        # self.onetbqc()


conerShow().run()