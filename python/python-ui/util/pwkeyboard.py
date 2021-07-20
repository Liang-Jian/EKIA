
####
#
# Mi Ma Jian Pan
#
####

import pytesseract
from PIL import ImageGrab
from PIL import Image
import time
import queue
import win32api,win32com,win32gui,win32con
import cv2

import rabird.winio
from ctypes import *
res_path ="C:\\User\\res\\"   # res file pic in this


# mi ma keyword , OK #

def grab(): # get screen picture
    im= ImageGrab.grab()
    im.save(res_path + "screen.jpg")
def match(char):
    keyboard = cv2.imread(res_path+ "screen.jpg",0)
    num0 = cv2.imread(res_path+ char + ".png",0)
    res = cv2.matchTemplate(keyboard,num0,cv2.TM_CCOEFF_NORMED)
    min_val,max_val,min_loc,max_loc = cv2.minMaxLoc(res)
    print(max_loc)
    return max_loc
def mouse_move(x,y):
    windll.user32.SetCursorPos(x,y)  # use windows hook move
def mouse_click(x,y): # move and click
    mouse_move(x,y)
    time.sleep(0.5)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)
def sendPw():
    time.sleep(2)
    mouse_click(1350,427) # click password icon
    time.sleep(1)
    grab()
    pwd = "123456c"
    for c in pwd:
        x,y = match(c)
        print(x,y)
        mouse_click(x+10,y+10)




##################
#
# yan zheng ma shi bie
#
##################

def cut_noise(image,pixel_node):
    rows,cols = image.size  #picture wight and height
    change_pos = []
    for i in range(1,rows-1):
        for j in range(1,cols -1):
            pixel_set = 0
            for m in range(i-1,i+2):
                for n in range(j-1,j+2):
                    if image.getpixel((m,n)) != 1:
                        pixel_set +=1
            if pixel_set <= pixel_node:
                change_pos.append((i,j))
    for pos in change_pos:
        image.putpixel(pos,1)
    return image
def getCode():
    scrshot = ImageGrab.grab()
    # img = scrshot.crop((1095,446,1162,471))
    img = scrshot.crop((1264,446,1331,472))

    img.save(r"C:\Users\zengp\Desktop\a\a.jpg")
    img = img.convert("RGB")
    img = img.convert("L")
    thredshold = 175
    table = []
    for i in range(256):
        if i < thredshold:
            table.append(0)
        else:
            table.append(1)
    img = img.point(table,'1')
    cutnoised = cut_noise(img,3)
    cutnoised1 = cut_noise(cutnoised,2)
    cutnoised2 = cutnoised1.crop((2,2,65,23))
    rustr  = pytesseract.image_to_string(cutnoised2)
    # rustr  = pytesseract.image_to_string(cutnoised2,config='-psm 7 digits')
    rustr = rustr.replace(" ","")
    print(rustr)

# if __name__ == '__main__':
#     getCode()
sendPw()