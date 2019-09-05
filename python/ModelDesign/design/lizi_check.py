
'''

page38

'''


class HealthCheck:
    _instance = None
    def __new__(cls, *args, **kwargs):

        if not HealthCheck._instance:
            HealthCheck._instance = super(HealthCheck,cls).__new__(cls,*args,**kwargs)
        return HealthCheck._instance
    def __init__(self):
        self._service = []
    def addService(self):

        self._service.append("Service 1")
        self._service.append("Service 2")
        self._service.append("Service 3")
        self._service.append("Service 4")

    def changeService(self):
        self._service.pop()
        self._service.append("Service 5")

hc1 = HealthCheck()
hc2 = HealthCheck()


hc1.addService()
print("Schedule health check for service (1)...")

for i in range(4):
    print("Checking",hc1._service[i])

hc2.changeService()
print("Schedule health check for service (2)...")

for i in range(4):
    print("Checking",hc2._service[i])