

from initfunc.initflow import Flow
from flow.chexianFlow import CheXian



_baodanhao = ("62201001360201900000000002")
_baoanhao  = ("070151021360201900010109")


class CheXianFlow(Flow):

    def run(self):
        CheXian(_baodanhao).baodan()

if __name__ == '__main__':
    CheXianFlow().run()
