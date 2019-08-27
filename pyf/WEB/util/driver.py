
from initfunc.initfile import DriVer
from selenium import webdriver


class StartDriver(DriVer):
    def __init__(self):
        self.driver = webdriver.Ie()
        self.driver.maximize_window()