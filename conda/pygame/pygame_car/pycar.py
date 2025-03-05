# !/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = 'enzhao'
# Created by enzhao on 2025/3/5.
import pygame
pygame.init()
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
CAR_WIDTH = 50
CAR_HEIGHT = 30
CENTER_LEFT = WINDOW_WIDTH / 2 - CAR_WIDTH / 2
CENTER_TOP = WINDOW_HEIGHT / 2 - CAR_HEIGHT / 2
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))  # 设置窗口尺寸[1](@ref)
class Car:
    def __init__(self, x, y):
        self.x = x  # 坐标初始化[1](@ref)
        self.y = y
        self.image = pygame.Surface((CAR_WIDTH, CAR_HEIGHT))  # 车身尺寸50x30像素
        self.image.fill((255, 0, 0))  # 填充红色[1](@ref)

    def add_x(self, _delta = 0):
        self.x += _delta
        if(self.x > WINDOW_WIDTH): # 超出屏幕后重置位置
            self.x = -CAR_WIDTH
        if(self.x < -CAR_WIDTH): # 超出屏幕后重置位置
            self.x = WINDOW_WIDTH

    def add_y(self, _delta = 0):
        self.y += _delta
        if(self.y > WINDOW_HEIGHT): # 超出屏幕后重置位置
            self.y = -CAR_HEIGHT
        if(self.y < -CAR_HEIGHT): # 超出屏幕后重置位置
            self.y = WINDOW_HEIGHT
    def draw(self):
        screen.blit(self.image, (self.x, self.y))  # 绘制到屏幕[1](@ref)
car = Car(CENTER_LEFT, CENTER_TOP)  # 初始位置居中
# car = Car(0, 300)  # 初始位置居中
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 0))  # 清屏为黑色背景
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]: car.add_x(-2)  # 左移
    elif keys[pygame.K_RIGHT]: car.add_x(2)  # 右移
    elif keys[pygame.K_UP]: car.add_y(-2)  # 左移
    elif keys[pygame.K_DOWN]: car.add_y(2)  # 右移
    font = pygame.font.Font(None, 36)
    text = font.render("Use ARROWS to move", True, (255, 255, 255))
    screen.blit(text, (100, 50))  # 在指定位置渲染文本[1](@ref)
    car.draw()
    pygame.display.flip()  # 更新显示[1](@ref)

