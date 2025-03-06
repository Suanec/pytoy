# !/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = 'enzhao'
# Created by enzhao on 2025/3/6.

import pygame
import sys

# 初始化
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# 颜色定义
COLORS = {
    "background": (240, 240, 240),
    "target_zone": (200, 220, 255),
    "parking_zone": (220, 220, 220),
    "button": (180, 180, 180),
    "red": (255, 0, 0),
    "blue": (0, 0, 255),
    "green": (0, 255, 0),
    "yellow": (255, 255, 0)
}

# 游戏区域划分
TARGET_HEIGHT = HEIGHT // 3
GRID_SIZE = 60

# 车辆类定义
class Car(pygame.sprite.Sprite):
    def __init__(self, color, direction, col, row):
        super().__init__()
        self.image = pygame.Surface((GRID_SIZE-4, GRID_SIZE-4))
        self.image.fill(COLORS[color])
        # 绘制方向箭头
        font = pygame.font.SysFont(None, 36)
        text = font.render(direction, True, (0,0,0))
        self.image.blit(text, (15, 15))
        self.rect = self.image.get_rect(topleft=(col*GRID_SIZE+2, TARGET_HEIGHT + row*GRID_SIZE+2))

class Game:
    def __init__(self):
        self.screws = 312
        self.current_level = 234
        self.selected_car = None

        # 初始化示例车辆（根据关卡配置）
        self.cars = pygame.sprite.Group()
        self.cars.add(Car("red", "↑", 3, 2))
        self.cars.add(Car("blue", "←", 5, 4))

    def draw_interface(self):
        # 绘制目标区域
        screen.fill(COLORS["target_zone"], (0, 0, WIDTH, TARGET_HEIGHT))

        # 绘制停车场区域
        screen.fill(COLORS["parking_zone"], (0, TARGET_HEIGHT, WIDTH, HEIGHT-TARGET_HEIGHT))

        # 绘制网格线
        for x in range(0, WIDTH, GRID_SIZE):
            pygame.draw.line(screen, (0,0,0), (x, TARGET_HEIGHT), (x, HEIGHT))
        for y in range(TARGET_HEIGHT, HEIGHT, GRID_SIZE):
            pygame.draw.line(screen, (0,0,0), (0, y), (WIDTH, y))

        # 绘制按钮
        pygame.draw.rect(screen, COLORS["button"], (WIDTH-200, HEIGHT-60, 80, 40))
        pygame.draw.rect(screen, COLORS["button"], (WIDTH-100, HEIGHT-60, 80, 40))

    def handle_click(self, pos):
        # 车辆选择逻辑
        for car in self.cars:
            if car.rect.collidepoint(pos):
                self.selected_car = car
                break

game = Game()

# 游戏主循环
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            game.handle_click(event.pos)

    screen.fill(COLORS["background"])
    game.draw_interface()
    game.cars.draw(screen)

    pygame.display.flip()
    clock.tick(30)