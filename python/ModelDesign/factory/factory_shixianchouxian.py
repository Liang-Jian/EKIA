


'''

page 49
抽象工厂模式
'''


from abc import ABCMeta,abstractclassmethod


class PizzaFactory(metaclass=ABCMeta):
    @abstractclassmethod
    def createVegPizza(self):
        pass
    @abstractclassmethod
    def createNonVegPizza(self):
        pass
class IndianPizzaFactory(PizzaFactory):
    def createVegPizza(self):
        return DeluxVeggiePizza()
    def createNonVegPizza(self):
        return ChickenPizza()
class USPizzaFactory(PizzaFactory):
    def createVegPizza(self):
        return MexicanVegPizza()
    def createNonVegPizza(self):
        return HamPizza()
class VegPizza(metaclass=ABCMeta):
    @abstractclassmethod
    def prepare(self,VegPizza):
        pass
class NonVegPizza(metaclass=ABCMeta):
    @abstractclassmethod
    def serve(self,VegPizza):
        pass
class DeluxVeggiePizza(VegPizza):
    def prepare(self):
        print("Prepare ",type(self).__name__)
class ChickenPizza(NonVegPizza):
    def serve(self,VegPizza):
        print(type(self).__name__,"is served with chicken on",type(VegPizza).__name__)
class MexicanVegPizza(VegPizza):
    def prepare(self):
        print("Prepare ",type(self).__name__)
class HamPizza(NonVegPizza):
    def serve(self,VegPizza):
        print(type(self).__name__,"is served with Ham on",type(VegPizza).__name__)
class PizzaStore:
    def __init__(self):
        pass
    def makePizzas(self):
        for factory in [IndianPizzaFactory(),USPizzaFactory()]:
            self.facotry = factory
            self.NonVegPizza = self.facotry.createNonVegPizza()
            self.VegPizza  = self.facotry.createVegPizza()
            self.VegPizza.prepare()
            self.NonVegPizza.serve(self.VegPizza)
pizza = PizzaStore()
pizza.makePizzas()