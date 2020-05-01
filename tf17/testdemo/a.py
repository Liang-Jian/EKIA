# -*- coding: utf-8 -*-
# 将RGB彩色图像转为灰度图像

import cv2
import numpy

lena = cv2.imread(r'C:\win-back\pic\_158763463416.jpeg')
img = lena
height = img.shape[0]
width = img.shape[1]
channels = img.shape[2]

value = [0] * 3
gray_img = numpy.zeros([height, width], numpy.uint8)

for row in range(height):
    for column in range(width):
        for chan in range(channels):
            value[chan] = img[row, column, chan]
        R = value[2]
        G = value[1]
        B = value[0]
        # new_value = 0.2989 * R + 0.5870 * G + 0.1140 * B
        new_value = 0.2989 * R + 0.5870 * G + 0.1140 * B  # 转为灰度像素
        gray_img[row, column] = new_value

cv2.imshow('original image', img)
cv2.waitKey(0)
cv2.imshow('gray image', gray_img)
cv2.waitKey(0)
