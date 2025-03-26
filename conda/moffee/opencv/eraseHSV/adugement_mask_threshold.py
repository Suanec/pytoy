# !/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = 'enzhao'
# Created by enzhao on 2025/3/3.

import cv2
import numpy as np

# 1. 读取图像
image = cv2.imread('temp.jpg')

# 可选预处理：高斯模糊去噪
blur = cv2.GaussianBlur(image, (5,5), 0)

# 2. 转换为HSV颜色空间
hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

def nothing(x): pass

cv2.namedWindow("Trackbars")
cv2.createTrackbar("Lower H", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("Upper H", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("Lower S", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("Upper S", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("Lower V", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("Upper V", "Trackbars", 0, 255, nothing)

while True:
    l_h = cv2.getTrackbarPos("Lower H", "Trackbars")
    u_h = cv2.getTrackbarPos("Upper H", "Trackbars")
    l_s = cv2.getTrackbarPos("Lower S", "Trackbars")
    u_s = cv2.getTrackbarPos("Upper S", "Trackbars")
    l_v = cv2.getTrackbarPos("Lower V", "Trackbars")
    u_v = cv2.getTrackbarPos("Upper V", "Trackbars")
    lower = np.array([l_h, l_s, l_v])
    upper = np.array([u_h, u_s, u_v])
    mask = cv2.inRange(hsv, lower, upper)
    # cv2.imshow("Adjustment", mask)
    inverted_mask = cv2.bitwise_not(mask)
    whites_only_array = np.full_like(image, (255, 255, 255))
    result_without_blues = cv2.bitwise_and(image, whites_only_array, mask=inverted_mask)
    cv2.imshow("Adjustment", result_without_blues)
    if cv2.waitKey(1) == 27:  # 按ESC退出
        break
# [22,2,210],[255,255,255]
