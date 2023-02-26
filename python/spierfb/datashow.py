

# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt

#
# plt.rcParams['font.sans-serif'] = ['Songti SC']
# plt.rcParams['axes.unicode_minus'] = False
#
#
# LEVEL = "A"
#
#
# _s = \
#       'select team, count(*) as total\n' \
#       'from\n' \
#       '(\n' \
#       '  select zhu as team\n' \
#       '  from j22 where level=\'A\' and zc+kc >= 9\n' \
#       '  union all\n' \
#       '  select ke as team\n' \
#       '  from j22 where level=\'A\' and zc+kc >= 9\n' \
#       ') d\n' \
#       'group by team\n' \
#       'order by total desc\n' \
#
# def addSpecial(x):
#     '''
#     list every element add '\n'
#     ['川崎Ｆ', '横浜FC', '浦和'] -> [['川\n崎Ｆ\n'], ['横\n浜FC\n'], ['浦\n和\n']]
#     '''
#     reafter = re.split('(?=[\u4e00-\u9fa5])', x)
#     splitafter = list()
#     while '' in reafter: reafter.remove('')
#     for i in reafter:
#         i += '\n'
#         splitafter.append(i)
#     str__ = ','.join(str(i) for i in splitafter).replace(',', '')
#     # print(str__)
#     ll = list()
#     ll.append(str__)
#     # print(ll)
#     return ll
#
#
# def splitlist(listdata):
#     '''
#     [['川\n崎Ｆ\n'], ['横\n浜FC\n'], ['浦\n和\n']] -> ['川\n崎Ｆ\n', '横\n浜FC\n', '浦\n和\n']
#     '''
#     return list(itertools.chain.from_iterable(listdata))
#
#
#
#
# def getJq(level='A'):
#     '''
#     # 每轮的角球总数
#     y = 轮数，round
#     allconner = 总数，total conner
#
#     '''
#
#     s = msq().search(f"select round,sum(zc+kc) from j21 where level='{level}' group by round")
#     a = np.array(s)
#     matchround = a[:, 0]
#     allconner  = a[:, 1]
#
#     # allconner = [0.8222,0.918,0.9344,0.9262,0.9371,0.9353]             # 总角球
#     # k2 = [0.8988,0.9334,0.9435,0.9407,0.9453,0.9453]#线2的纵坐标
#     plt.plot(matchround,allconner,'s-',color = 'g',label="ATT-RLSTM")    # 示例
#     # plt.plot(matchround,k2,'o-',color = 'g',label="CNN-RLSTM")#o-:圆形
#     plt.xlabel("比赛轮数")                                                # 横坐标名字
#     plt.xticks(range(0, 23, 1))                                          # (0,23) 范围0-23 ，单位 1
#     plt.yticks(range(0, 135, 5))                                         # (0,23) 范围0-100 ，单位 4
#     plt.ylabel("每轮的角球总数")                                           # 纵坐标名字
#     plt.legend(loc = "best")                                             # 图例
#     plt.show()
#
# def getbanchangjinqiu(level='A'):
#     '''
#     # 每轮上半场进球小于1.5 的
#     '''
#
#     s = MsqService().search(f"select round,count(*) from j21 where level='{level}' and left(bc,1) + right(bc,1) < 1.5 group by round")
#     a = np.array(s)
#     matchround = a[:, 0]
#     allconner  = a[:, 1]
#
#     plt.plot(matchround,allconner,'s-',color = 'g',label="ATT-RLSTM")    # 示例
#     plt.xlabel("比赛轮数")                                                # 横坐标名字
#     plt.xticks(range(0, 24, 1))                                          # (0,23) 范围0-23 ，单位 1
#     plt.yticks(range(0, 12, 1))                                          # (0,23) 范围0-100 ，单位 4
#     plt.ylabel(f" {level} 半场进球小于1.5的总次数")                                           # 纵坐标名字
#     plt.legend(loc = "best")                                             # 图例
#     plt.show()
#
# def bestzhu(level='A'):
#     '''
#     主场战绩最好的队伍
#     :return:
#     '''
#     data = MsqService().search(f"select zhu,count(*) as total  from j21 where level='{level}' and zj-kj >=0 group by zhu order by total desc")
#     a = np.array(data)
#
#     zhuteam = a[:, 0]
#     allcount  = a[:, 1]
#
#     # plt.plot(zhuteam,allconner,'s-',color = 'g',label="ATT-RLSTM")    # 示例
#     # plt.xlabel("比赛轮数")                                                # 横坐标名字
#     # plt.xticks(range(0, 24, 1))                                          # (0,23) 范围0-23 ，单位 1
#     # plt.yticks(range(0, 12, 1))                                          # (0,23) 范围0-100 ，单位 4
#     # plt.ylabel(f" {level} 半场进球小于1.5的次数")                           # 纵坐标名字
#     # plt.legend(loc = "best")                                             # 图例
#     # plt.show()
#     # zhuteam=['川崎Ｆ','横浜FM','浦和','神戸','鹿島','鳥栖','湘南']
#     # allcount=[13,11,10,9,9,8,8]
#     plt.bar(zhuteam,allcount,align='center',alpha=1)
#     plt.yticks(range(0, 15, 1))
#     plt.ylabel('次数')
#     plt.xlabel('队伍')
#     plt.title('主场战绩最好的队伍排列')
#     plt.show()
#
# def bestke(level='A'):
#     '''
#     客场战绩最好的队伍
#     :return:
#     '''
#     data = MsqService().search(f"select ke,count(*) as total  from j21 where level='{level}' and zj-kj <=0 group by ke order by total desc")
#     a = np.array(data)
#     zhuteam = a[:, 0]
#     allcount  = a[:, 1]
#
#     plt.bar(zhuteam,allcount,align='center',alpha=1)
#     plt.yticks(range(0, 15, 1))
#     plt.ylabel('次数')
#     plt.xlabel('队伍')
#     plt.title('客场战绩最好的队伍排列')
#     plt.show()
#
# def pingju(level='A'):
#     '''
#     每轮的平局次数
#     :return:
#     '''
#
#     s = MsqService().search(f"select round,count(*) from j21 where level='{level}' and zj = kj group by round;")
#     a = np.array(s)
#     matchround = a[:, 0]
#     allconner  = a[:, 1]
#
#     plt.plot(matchround,allconner,
#              linewidth=2,
#              color='steelblue',
#              marker='o',
#              markersize=6,
#              markeredgecolor='black',
#              markerfacecolor='brown') # 示例
#     plt.xlabel("比赛轮数")                                                # 横坐标名字
#     plt.xticks(range(0, 24, 1))                                          # (0,23) 范围0-23 ，单位 1
#     plt.yticks(range(0, 8, 1))                                          # (0,23) 范围0-100 ，单位 4
#     plt.ylabel(f" {level} 平局次数")                                           # 纵坐标名字
#     plt.legend(loc = "best")                                             # 图例
#
#
#
#     plt.show()
#
# def getjq8zhu(level='A'):
#     '''
#     主场 角球>=8 的 总次数
#     :return:
#     '''
#     s = msq().search(_s)
#
#
#     a = np.array(s)
#     team = a[:, 0]
#     conner_count  = a[:, 1]
#
#     print(team)
#     print(conner_count)
#     # plt.plot(matchround,allconner,'s-',color = 'g',label="主场角球最多的球队")    # 示例
#     # plt.xlabel("比赛轮数")                                                # 横坐标名字
#     # plt.xticks(range(0, 24, 1))                                          # (0,23) 范围0-23 ，单位 1
#     # plt.yticks(range(0, 12, 1))                                          # (0,23) 范围0-100 ，单位 4
#     # plt.ylabel(f" {level} 主场角球大于8 的总数")                                           # 纵坐标名字
#     # plt.legend(loc = "best")                                             # 图例
#     # plt.show()
#
#
#     # import matplotlib.pyplot as plt
#     #
#     # colums_x = ['aa','bc','ad','bd']
#
#     # colums_y = [12,14,10,15]
#
#     # 自定义 x轴 的取值：
#
#     # plt.xticks(range(len(conner_count)),team)
#
#     # 不要再写进 colums_x 了
#     # plt.plot(team)
#     # plt.show()
#     plt.bar(team,conner_count,color = 'g',label=u"主场角球最多的球队")
#     plt.show()
#
# def getjq8ke(level='A'):
#     '''
#     客场 角球>=8 的 总次数
#     :return:
#     '''
#     s = MsqService().search(
#     f"select ke,count(zhu) as total from j22 where level='{level}' and zc+kc >=8 group by ke order by total desc"
#     )
#     a = np.array(s)
#     matchround = a[:, 0]
#     allconner  = a[:, 1]
#     print(matchround)
#     matchTeam = list(map(addSpecial, matchround))
#     fix_matchTeam = splitlist(matchTeam)
#     print(fix_matchTeam)
#     plt.plot(fix_matchTeam,allconner,'s-',color = 'g',label="客场角球最多的球队")    # 示例
#     plt.xlabel("比赛轮数")                                                # 横坐标名字
#     plt.xticks(range(0, 24, 1))                                          # (0,23) 范围0-23 ，单位 1
#     plt.yticks(range(0, 12, 1))                                          # (0,23) 范围0-100 ，单位 4
#     plt.ylabel(f" {level} 客场角球大于8的总数")                                           # 纵坐标名字
#     plt.legend(loc = "best")                                             # 图例
#     plt.show()
#
# def getteamqj(level='A',team='川崎Ｆ'):
#     '''
#     获取某个队伍的角球趋势图
#     :param level:
#     :param team:
#     :return:
#     '''
#     s = MsqService().search(f"SELECT CONCAT(zhu,'-',ke) as bisai,round,zc+kc as total from j21 WHERE `level`='{level}' and (zhu= '{team}' or ke ='{team}') order  by round")
#     a = np.array(s)
#     matchteam  = a[:, 0]
#     matchround = a[:, 1]
#     allconner  = a[:, 2]
#     print(matchteam)
#     # matchTeam = list(map(addSpecial, matchround))
#     # fix_matchTeam = splitlist(matchTeam)
#     print(matchteam)
#     plt.plot(matchround,allconner,'s-',color = 'blue',label="角球趋势图")    # 示例
#     plt.xlabel("比赛轮数")                                                # 横坐标名字
#     plt.xticks(range(0, 24, 1))                                          # (0,23) 范围0-23 ，单位 1
#     plt.yticks(range(0, 17, 1))                                          # (0,23) 范围0-100 ，单位 4
#     plt.ylabel(f" {level} f{team} 的角球走势图")                           # 纵坐标名字
#     plt.legend(loc = 0)                                                  # 图例
#     plt.show()
#
#
# def getallxiao(level='B',team='大宫'):
#     s = MsqService().search(f"select * from j21 where  level='{level}' and zj+kj <=2 and (zhu='{team}' or ke='{team}')")
#     a = np.array(s)
#     matchteam  = a[:, 0]
#     matchround = a[:, 1]
#     allconner  = a[:, 2]
#     print(matchteam)
#     # matchTeam = list(map(addSpecial, matchround))
#     # fix_matchTeam = splitlist(matchTeam)
#     print(matchteam)
#     plt.plot(matchround,allconner,'s-',color = 'blue',label="角球趋势图")    # 示例
#     plt.xlabel("比赛轮数")                                                # 横坐标名字
#     plt.xticks(range(0, 24, 1))                                          # (0,23) 范围0-23 ，单位 1
#     plt.yticks(range(0, 17, 1))                                          # (0,23) 范围0-100 ，单位 4
#     plt.ylabel(f" {level} f{team} 的角球走势图")                           # 纵坐标名字
#     plt.legend(loc = 0)                                                  # 图例
#     plt.show()
#
#
# def train(level='B',team='大宫'):
#     s = MsqService().search(f"select * from j21 where  level='{level}' and zj+kj <=2 and (zhu='{team}' or ke='{team}')")
#     a = np.array(s)
#     matchteam  = a[:, 0]
#     matchround = a[:, 1]
#     allconner  = a[:, 2]
#     print(matchteam)
#     # matchTeam = list(map(addSpecial, matchround))
#     # fix_matchTeam = splitlist(matchTeam)
#     print(matchteam)
#     plt.scatter(x=10 ,y=5,
#                 color='steelblue')    # 示例
#     plt.xlabel("比赛轮数")                                                # 横坐标名字
#     plt.xticks(range(0, 24, 1))                                          # (0,23) 范围0-23 ，单位 1
#     plt.yticks(range(0, 17, 1))                                          # (0,23) 范围0-100 ，单位 4
#     plt.ylabel(f" {level} f{team} 的角球走势图")                           # 纵坐标名字
#     plt.legend(loc= 0)                                                  # 图例
#     plt.show()
import os,yaml
import mysql.connector


def ryaml(key, peer="control"):
    # read yaml file
    homept = os.path.expanduser('~')
    _f = open(f"{homept}/EKIA/python/spierfb/run.yml", "r", encoding="utf8")
    config = yaml.load(_f.read(), Loader=yaml.Loader)
    conf = config[peer]
    _f.close()
    return conf[key]
class msq:

    def __init__(self):
        self.conn = mysql.connector.connect(host=ryaml("host", "db"), user=ryaml("user", "db"),
                                            password=ryaml("password", "db"),
                                            database=ryaml("dbname", "db"), use_unicode=True)
        self.cursor = self.conn.cursor()

    def search(self, sql):
        self.cursor.execute(sql)
        select_data = self.cursor.fetchall()
        # Logi("sql result:={}".format(select_data))
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
    def __init__(self, level='A', year='j22'):
        self.level= level
        self.year = year
        self.s1 = f"select round,sum(zc+kc),sum(zj+kj) from {year} where level='{level}' group by round"

    def show(self):
        s = msq().search(self.s1)
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

        round_ = np.array(round_list)
        cn_data = np.array(cn_list)
        jinqiu = np.array(goals_list)
        N = len(round_)
        x = np.arange(N)

        fig = plt.figure()
        sub = fig.add_subplot(111)

        wid = 0.4
        x1 = x - wid / 2
        x2 = x + wid / 2
        sub.bar(x1, cn_data, label='jiaoqiu', width=wid, alpha=0.75, edgecolor='k', hatch='*')
        sub.bar(x2, jinqiu, label='jinqiu', width=wid, alpha=0.75, edgecolor='k', hatch='/')

        for i in range(N):
            sub.text(x1[i], cn_data[i], '{:.1f}'.format(cn_data[i]), verticalalignment='bottom',
                     horizontalalignment='center')
            sub.text(x2[i], jinqiu[i], '{:.1f}'.format(jinqiu[i]), verticalalignment='bottom',
                     horizontalalignment='center')
        sub.tick_params(axis='x', length=0)
        sub.set_xticks(x)
        sub.set_xticklabels(x)
        sub.set_xlabel(f'{self.year[1::]} year {self.level} match round', fontsize=15)
        sub.set_ylabel(f'{self.year[1::]} year total coner', fontsize=15)

        plt.show()
        """
        cn_data = data.iloc[:, 1].to_numpy()
        jinqiu = data.iloc[:, 2].to_numpy()
        print(year)
        print(cn_data)

        """
    def run(self):
        self.show()


ms = msq()


def every_team(team='清水'):
    sql_ = ms.search(f"select '{team}',count(*) from j22 where level='A' and ('{team}' = zhu or '{team}' = ke) and zj+kj=0")
    for i in sql_:
        print(i)


if __name__ == '__main__':
    # conerShow().run()
    every_team()