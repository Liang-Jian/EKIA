


'''

 抽象的实现

'''


class Adder:
    def __init__(self):
        self.sum = 0
    def ad(self,value):
        self.sum +=value


acc = Adder()
for i in range(99):
    acc.ad(i)
    print(id(acc))

print(acc.sum)