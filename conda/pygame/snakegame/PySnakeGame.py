# !/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = 'enzhao'
# Created by enzhao on 2025/3/6.
import pygame
import random
import sys

# 初始化Pygame
pygame.init()

# 游戏窗口设置
WIDTH, HEIGHT = 640, 480
GRID_SIZE = 20
FPS = 10

# 马卡龙色系配色方案
COLORS = {
    "背景": (255, 246, 238),    # 浅米色
    "文字": (149, 145, 183),    # 淡紫色
    "食物": (255, 173, 197),    # 樱花粉
    "蛇头": (162, 210, 202),    # 薄荷绿
    "蛇身": [
        (253, 223, 223),        # 浅粉色
        (222, 235, 247),        # 淡蓝色
        (220, 215, 247),        # 薰衣草紫
        (255, 239, 209)         # 奶油黄
    ]
}

# 方向向量
DIRECTIONS = {
    "UP": (0, -1),
    "DOWN": (0, 1),
    "LEFT": (-1, 0),
    "RIGHT": (1, 0)
}

class SnakeGame:
    def __init__(self):
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("马卡龙贪吃蛇")
        self.clock = pygame.time.Clock()

        # 游戏初始化
        self.snake = [(WIDTH//2, HEIGHT//2)]
        self.direction = DIRECTIONS["RIGHT"]
        self.food = self.generate_food()
        self.score = 0
        self.game_over = False

    def generate_food(self):
        while True:
            x = random.randint(0, (WIDTH-GRID_SIZE)//GRID_SIZE) * GRID_SIZE
            y = random.randint(0, (HEIGHT-GRID_SIZE)//GRID_SIZE) * GRID_SIZE
            if (x, y) not in self.snake:
                return (x, y)

    def draw_snake(self):
        for i, (x, y) in enumerate(self.snake):
            # 头部使用不同颜色
            if i == 0:
                pygame.draw.rect(self.window, COLORS["蛇头"], (x, y, GRID_SIZE-1, GRID_SIZE-1))
            else:
                # 身体渐变色循环
                color = COLORS["蛇身"][i % len(COLORS["蛇身"])]
                pygame.draw.rect(self.window, color, (x, y, GRID_SIZE-1, GRID_SIZE-1))

    def draw_food(self):
        pygame.draw.circle(self.window, COLORS["食物"],
                           (self.food[0]+GRID_SIZE//2, self.food[1]+GRID_SIZE//2),
                           GRID_SIZE//2 - 1)

    def show_game_over(self):
        font = pygame.font.Font(None, 48)
        text = font.render(f"游戏结束 得分: {self.score}", True, COLORS["文字"])
        self.window.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 30))
        pygame.display.update()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if self.game_over:
                        if event.key == pygame.K_r:
                            self.__init__()
                    else:
                        if event.key == pygame.K_UP and self.direction != DIRECTIONS["DOWN"]:
                            self.direction = DIRECTIONS["UP"]
                        elif event.key == pygame.K_DOWN and self.direction != DIRECTIONS["UP"]:
                            self.direction = DIRECTIONS["DOWN"]
                        elif event.key == pygame.K_LEFT and self.direction != DIRECTIONS["RIGHT"]:
                            self.direction = DIRECTIONS["LEFT"]
                        elif event.key == pygame.K_RIGHT and self.direction != DIRECTIONS["LEFT"]:
                            self.direction = DIRECTIONS["RIGHT"]

            if not self.game_over:
                # 移动蛇
                new_head = (self.snake[0][0] + self.direction[0]*GRID_SIZE,
                            self.snake[0][1] + self.direction[1]*GRID_SIZE)

                # 碰撞检测
                if (new_head[0] < 0 or new_head[0] >= WIDTH or
                        new_head[1] < 0 or new_head[1] >= HEIGHT or
                        new_head in self.snake):
                    self.game_over = True
                else:
                    self.snake.insert(0, new_head)
                    if new_head == self.food:
                        self.score += 1
                        self.food = self.generate_food()
                    else:
                        self.snake.pop()

            # 绘制界面
            self.window.fill(COLORS["背景"])
            self.draw_snake()
            self.draw_food()

            if self.game_over:
                self.show_game_over()

            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = SnakeGame()
    game.run()