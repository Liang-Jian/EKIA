
from interface.interfaceDriver import DriVer
from selenium import webdriver


class StartDriver(DriVer):
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()