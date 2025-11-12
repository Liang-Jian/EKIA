


MINI4 = '1.4GHz Mac mini'

class AppleFactory:

    class MacMini4:
        def __init__(self):
            self.memory = 4
            self.hdd = 500
            self.gpu = 'intel HD Graphics 5000'
        def __str__(self):
            info = ('model:{}'.format(MINI4),
                    'memory:{}'.format(self.memory),
                    'Hard Disk: {}'.format(self.hdd),
                    'Graphics Card: {}'.format(self.gpu))
            return '\n'.join(info)

    def build_computer(self,model):
        if (model == MINI4):
            return self.MacMini4()
        else:
            print("I don't know how to build {}".format(model))
if __name__ == '__main__':
    afac  =AppleFactory()
    mac_min = afac.build_computer(MINI4)
    print(mac_min)