
import csv
import os




d = dict()


def get_scfromcsv(fp=r"storedb03_hs_esl_goods_tesl.csv"):
    # 获取指定门店号的信息
    if not fp.endswith(".csv"):
        return
        # raise TypeError("only support csv file !")
    _fp = rf"/Users/shi/Desktop/{fp}"
    # _fp = rf"D:\120w\{fp}"
    data = []
    with open(_fp, encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            print(row)
            if row[2] not in d:
                d[row[2]] = [f"{row[0]},{row[1]}"]
            else:
                pass
    f.close()
    # print(d)
    return data


def getallfile():
    files = [f for f in os.listdir(rf"/Users/shi/Desktop/")]
    # files = [f for f in os.listdir(rf"./perf_data/perf_data_100w_60osd/")]
    return files


csv_list = getallfile()
# print(csv_list)


for f in csv_list:
    s = get_scfromcsv(f)
    print(s)
print(d)