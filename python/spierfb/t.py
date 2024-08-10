#
# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# import mysql.connector
# import yaml
# import sys
# import os


# np.random.seed(0)#使得每次生成的随机数相同
# ts = pd.Series(np.random.randn(1000), index=pd.date_range("1/1/2000", periods=1000))
# ts1 = ts.cumsum()#累加
# ts1.plot(kind="line")#默认绘制折线图

from sanic import Sanic
from sanic.response import json

app = Sanic("my-hello-world-app")

@app.route('/')
async def test(request):
    return json({'hello': 'world'})

if __name__ == '__main__':
    app.run()