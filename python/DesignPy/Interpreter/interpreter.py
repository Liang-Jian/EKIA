

class Boiler:
    def __init__(self):
        self.temperature = 83

    def __str__(self):
        return 'boiler temperature: {} degree'.format(self.temperature)

    def increase_temperature(self,amount):
        print("increasing the boiler's temperature by {} degrees".format(amount))
        self.temperature += amount
    def decrease_temperature(self,amount):
        print("decreasing the boiler's temperature by {} degrees".format(amount))
        self.temperature -=amount


