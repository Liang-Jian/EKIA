import time
from enum import Enum

PizzaProgress = Enum('PizzaProgress','queued preparation baking ready')
PizzaDough = Enum('PizzaDough','thin thick')
PizzaSauce = Enum('PizzaSauce','tomato creme_fraiche')
PizzaTopping = Enum('PizzaTopping','mozzarella double_mozzarella bacon ham mushrooms red_opion oregano')
STEP_DELAY = 3




class Pizza:
    def __init__(self,name):
        self.name = name
        self.dough = None
        self.sauce = None
        self.topping = []


    def __str__(self):
        return self.name

    def prepare_dough(self,dough):
        self.dough = dough
        print('preparing the {} dough of your {}...'.format(self.dough.name,self))
        time.sleep(STEP_DELAY)
        print('done with the {} dough'.format(self.dough.name))


class MargaritaBuilder:
    def __init__(self):
        self.pizza = Pizza('margarite')
        self.progress = PizzaProgress.queued
        self.baking_time = 5

    def prepare_dough(self):
        self.progress = PizzaProgress.preparation
        self.pizza.prepare_dough(PizzaDough.thin)

    def add_sauce(self):
        print('adding the tomato sauce to your margarita ...')
        self.pizza.sauce = PizzaSauce.tomato
        time.sleep(STEP_DELAY)
        print('done with the tomato sauce')

    def add_topping(self):
        print('adding the topping (double mozzarella,oregano) to your margarite')
        self.pizza.topping.append([i for i in (PizzaTopping.double_mozzarella,PizzaTopping.oregano)])
        time.sleep(STEP_DELAY)
        print('Done with the topping (double mozzarella,oregano)')

    def bake(self):
        self.progress = PizzaProgress.baking
        print('baking you margarita for {} second'.format(self.baking_time))
        time.sleep(self.baking_time)
        self.progress = PizzaProgress.ready
        print('your margarita is ready')


class CreamyBaconBuild:
    def __init__(self):
        self.pizza = Pizza('creampy bacon')
        self.progress = PizzaProgress.queued
        self.baking_time =7

    def prepare_dough(self):
        self.progress = PizzaProgress.preparation
        self.pizza.prepare_dough(PizzaDough.thick)
    def add_sauce(self):
        print('adding the creme fraiche sauce to you creamy bacon ...')
        self.pizza.sauce = PizzaSauce.creme_fraiche
        time.sleep(STEP_DELAY)
        print('done with the creme fraiche sauce')

    def add_topping(self):
        print('adding the topping (mozzarella,bacon,ham,mushrooms,redonion,oregano) to your creamy bacon')
        self.pizza.topping.append([t for t in (PizzaTopping.mozzarella,PizzaTopping.bacon,PizzaTopping.ham,PizzaTopping.mushrooms,PizzaTopping.red_onion,PizzaTopping.oregano)])
        time.sleep(STEP_DELAY)
        print('Done with the topping (mozzarella,bacon,ham,mushrooms,red onion,oregano')


    def bake(self):
        self.progress = PizzaProgress.baking
        print('baking you creamy bacon for {} senconds'.format(self.baking_time))
        time.sleep(self.baking_time)
        self.progress = PizzaProgress.ready
        print('your creamy bacon is ready')

class Waiter:
    def __init__(self):
        self.builder = None
    def construct_pizza(self,builder):
        self.builder = builder
        [step() for step in (builder.prepare_dough,builder.add_sauce,builder.add_topping,builder.bake)]

    @property
    def pizze(self):
        return self.builder.pizza

def validate_style(builders):
    try:
        pizza_style = input('what pizza would you like ,[m] argarita or [c] readmy bacon?')
        builder = builders[pizza_style]()
        valid_input = True
    except KeyError as err:
        print('sorry,only margarita(key m) and creamy bacon (key c) are available')
        return (False,None)
    return (True,builder)



def main():
    builders = dict(m =MargaritaBuilder,c=CreamyBaconBuild)
    valid_input = False
    while not valid_input:
        valid_input,builder = validate_style(builders)
    print()
    waiter = Waiter()
    waiter.construct_pizza(builder)
    pizza = waiter.pizze
    print()
    print('Enjoy you {}'.format(pizza))

if __name__ == '__main__':
    main()