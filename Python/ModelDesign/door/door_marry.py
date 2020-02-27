

'''

    page57
    门面模式的应用

'''

#
# class EventManager(object):
#     def __init__(self):
#         print("Event Manager :: Let me talk to the folks \n")
#     def arrange(self):
#         self.hotelier = Hotelier()
#         self.hotelier.bookHotel()
#
#         self.florist = Florist()
#         self.florist.setFlowerRequirements()
#
#         self.caterer = Caterer()
#         self.caterer.setCuisine()
#
#         self.musician = Musician()
#         self.musician.setMusicType()
#
# class Hotelier(object):
#     def __init__(self):
#         print("Arranging the hotel for Marriage?--")
#
#     def __isAvailable(self):
#         print("Is the hotel free for the event on given day")
#         return True
#     def bookHotel(self):
#         if self.__isAvailable():
#             print("Registered the booking \n")
# class Florist(object):
#     def __init__(self):
#         print("Flower Decorations for the Event ?--")
#     def setFlowerRequirements(self):
#         print("Carnations,roses and lilies would be used for Decorations \n\n")
# class Caterer(object):
#     def __init__(self):
#         print("Food Arrangements for the Event ---")
#     def setCuisine(self):
#         print("Chinese & Continental Cuisine to be served \n\n")
# class Musician(object):
#     def __init__(self):
#         print("Musical Arrangements for the Marriage --")
#     def setMusicType(self):
#         print("Jazz and  Classical will be played \n\n")
#
# class You(object):
#     def __init__(self):
#         print("YOU:: Whoa! Marriage Arrangements??!!")
#     def askEventManager(self):
#         print("You:: Let's Contact the Event Manager \n\n")
#         em = EventManager()
#         em.arrange()
#     def __del__(self):
#         print("YOU:: Thanks to Event Manager,All preparations done! Phew!")
#
# you = You()
# you.askEventManager()






import os,sys,time,subprocess,pickle,platform,logging
import tempfile,shutil,pymysql,multiprocessing,threading
# import win32api,win32com,win32gui,win32con
from selenium.webdriver.support.select import Select

caseID = "11"

from decimal import Decimal
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import  pymysql
# from PIL import ImageGrab,Image
sep = os.path.sep  # \

AGENT_PATH = os.path.abspath(os.path.join(os.getcwd(),"./"))                # agent home python ac/sel/pro/exe.py
PIC_PATH = AGENT_PATH + "\\result\\images\\"+caseID                         # pic home
LOG_PATH = AGENT_PATH + "\\result\\log\\"+caseID            # log home

from selenium import webdriver
if not os.path.exists(LOG_PATH) : os.makedirs(LOG_PATH)

timeout = TIME_OUT = 30
kEys ='0x2c'
global logger,path

BasePath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
Flie_Path = os.path.join(BasePath,"porjtect")
path = Flie_Path if platform.system() ==  "Windows" else "/home/jettech/Agent/execute"

infoTable = model = ifInstallMonkey = ifRunMonkey = None

open(LOG_PATH + "\\processLog.txt", 'w')                      # open log file
logger = logging.getLogger("jettech")                       # create logger
logger.setLevel(logging.INFO)
fh = logging.FileHandler(LOG_PATH+ "\\processLog.txt")        # create handle ,write2file
formatter = logging.Formatter('%(message)s')                # define handle 's formatter
fh.setFormatter(formatter)
logger.addHandler(fh)                                       # add logger to handle
# driver = webdriver.Ie()
driver = webdriver.Ie()
driver.get("http://221.226.73.174:10580/jettechHomePage/")
driver.maximize_window()
driver.implicitly_wait(10)
logger.info("get url success")

driver.find_element_by_id("username").send_keys("370303199011026610")
driver.implicitly_wait(5)
driver.find_element_by_id("password").send_keys("798513")
driver.implicitly_wait(5)
driver.find_element_by_id("btn_login").click()
driver.implicitly_wait(5)
pngPATH=os.path.abspath('.') + "\\result\\image"



