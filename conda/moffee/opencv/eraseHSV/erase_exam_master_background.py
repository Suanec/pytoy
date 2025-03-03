# !/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = 'enzhao'
# Created by enzhao on 2025/3/3.

import cv2
import numpy as np
import sys

def erase_exam_master(_file_name):
    # 1. 加载图像
    image = cv2.imread(_file_name)

    # 检查是否成功加载图像
    if image is None:
        print("Error: Could not load the input image.")
    else:
        # 2. 定义蓝色的HSV阈值范围
        lower_blue = np.array([22,2,210])   # HSV空间下的最低蓝色阈值
        upper_blue = np.array([255, 255, 255]) # HSV空间下的最高蓝色阈值
        
        # 将BGR格式转换为HSV格式以便于颜色分割
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # 创建掩膜，只保留落在蓝色范围内的像素
        mask = cv2.inRange(hsv_image, lower_blue, upper_blue)
        
        # 对原始图像应用掩膜，提取出蓝色部分
        blue_part = cv2.bitwise_and(image, image, mask=mask)
        
        # 设置目标颜色（例如绿色）
        target_color_bgr = (255, 255, 255)  # BGR格式的绿色
        
        # 在掩膜位置填充目标颜色
        result_image = image.copy()
        result_image[mask > 0] = target_color_bgr

        # 或者选择保存结果图像至本地
        output_filename = _file_name + 'output_replaced_exam_master_background.jpg'
        cv2.imwrite(output_filename, result_image)
        print(f"The modified image has been saved to {output_filename}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_image_path>")
        sys.exit(1)
    else:
        erase_exam_master(sys.argv[1])