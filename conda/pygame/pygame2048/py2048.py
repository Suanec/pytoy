# !/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = 'enzhao'

import random

# Created by enzhao on 2025/3/6.
import pygame

# 初始化Pygame
pygame.init()
pygame.display.set_caption("马卡龙2048")
clock = pygame.time.Clock()

# 马卡龙色系配色方案
COLORS = {
    "background": (249, 224, 237),  # 浅粉背景
    "grid": (255, 243, 252),  # 网格线颜色
    "text": (60, 60, 60), # 文字颜色
    "title": (255, 105, 180),
    0: (255, 255, 255, 0),  # 透明色
    2: (169, 222, 249),  # 浅蓝
    4: (255, 227, 174),  # 奶油黄
    8: (255, 192, 203),  # 粉红
    16: (221, 160, 221),  # 薰衣草紫
    32: (255, 182, 193),  # 桃红
    64: (152, 251, 152),  # 薄荷绿
    128: (240, 128, 128),  # 珊瑚色
    256: (147, 197, 114),  # 抹茶绿
    512: (255, 160, 122),  # 橙红
    1024: (216, 191, 216),  # 淡紫灰
    2048: (255, 215, 0),  # 金色
    "default" : (221, 160, 221)
}


class Grid:
    def __init__(self, _row_size = 4):
        self.row_size = _row_size
        self.c_size_cell = 80
        self.c_size_padding = 10
        self.c_size_header = 80
        self.c_boarder_radius = 8
        self.c_size_font = 36
        self.dft_row_size = (
                2 * self.c_size_padding + # 左侧隔离大小，方块左侧没有，加一个
                1 * self.c_size_padding + # 右侧隔离大小，方块自带一个
                (self.c_size_padding + self.c_size_cell) * self.row_size # 单个方块带隔离大小
        )
        self.c_size_screen_width = self.dft_row_size
        self.c_size_screen_height = self.dft_row_size + self.c_size_header + self.c_size_padding * 2
        self.screen = pygame.display.set_mode((self.c_size_screen_width, self.c_size_screen_height))
        self.grid = [[0] * self.row_size for _ in range(self.row_size)]
        # self.grid = [[2 ** (i + 3)] * self.row_size for i in range(self.row_size)]
        self.pre_grid = [row[:] for row in self.grid]
        self.score = 0
        self.max = 2
        self.candidates = [2]
        self.opd = False
        self.add_new_tile()
        self.add_new_tile()

    def add_new_tile(self):
        empty_cells = [(i, j) for i in range(self.row_size) for j in range(self.row_size) if self.grid[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            t = random.choice(self.candidates)
            self.grid[i][j] = 2 if random.random() < 0.5 else t

    def merge(self, row):
        new_row = []
        merged = False
        for num in row:
            if num == 0: continue
            if new_row and new_row[-1] == num and not merged:
                new_row[-1] *= 2
                self.score += new_row[-1] * 2
                if(new_row[-1] > self.max):
                    self.max = new_row[-1]
                    self.candidates.append(self.max)
                merged = True
            else:
                new_row.append(num)
                merged = False
        return new_row + [0] * (self.row_size - len(new_row))

    def move(self, direction):
        """处理移动逻辑（核心算法）"""
        # self.pre_grid = self.grid
        self.pre_grid = [row[:] for row in self.grid]
        self.opd = False

        rotated = list(zip(*self.grid)) if direction in ['UP', 'DOWN'] else self.grid
        if direction in ['DOWN', 'RIGHT']:
            rotated = [row[::-1] for row in rotated]

        new_board = []
        for row in rotated:
            merged_row = self.merge([x for x in row if x != 0])
            new_board.append(merged_row)

        if direction in ['DOWN', 'RIGHT']:
            new_board = [row[::-1] for row in new_board]
        if direction in ['UP', 'DOWN']:
            new_board = [list(x) for x in list(zip(*new_board))]
        self.grid = new_board
        i_pre_grid = [row[:] for row in self.grid]
        if(not (i_pre_grid == self.pre_grid)):
            self.opd = True

    def draw(self):
        self.screen.fill(COLORS["background"])

        # 绘制标题
        title_font = pygame.font.Font(None, 48)
        title_text = title_font.render("2048", True, COLORS["title"])
        self.screen.blit(title_text, (20, 20))

        # 绘制分数
        score_font = pygame.font.Font(None, 28)
        score_text = score_font.render(f"Score: {self.score}", True, COLORS["title"] )
        self.screen.blit(score_text, (20, 70))

        for i in range(self.row_size):
            for j in range(self.row_size):
                val = self.grid[i][j]
                # 绘制色块
                rect = pygame.Rect(
                    j * (self.c_size_cell + self.c_size_padding) + self.c_size_padding * 2,
                    i * (self.c_size_cell + self.c_size_padding) + self.c_size_padding * 2 + self.c_size_header,
                    self.c_size_cell, self.c_size_cell
                )
                pygame.draw.rect(self.screen, COLORS.get(val, COLORS["default"]), rect, border_radius=self.c_boarder_radius)
                # 绘制数字
                if val > 0:
                    font = pygame.font.Font(None, self.c_size_font)
                    text = font.render(str(val), True, COLORS["text"])
                    text_rect = text.get_rect(center=rect.center)
                    self.screen.blit(text, text_rect)

        if(self.is_game_over()):
            # 游戏结束，显示最终分数
            game_over_font = pygame.font.Font(None, 28)
            game_over_text = game_over_font.render(f"Game Over! \nYour score is {self.score}", True, COLORS["title"])
            self.screen.blit(game_over_text, (20, 200))

    def is_game_over(self):
        """检测游戏结束条件"""
        for i in range(self.row_size):
            for j in range(self.row_size):
                if self.grid[i][j] == 0: return False
                if i < self.row_size - 1 and self.grid[i][j] == self.grid[i + 1][j]: return False
                if j < self.row_size - 1 and self.grid[i][j] == self.grid[i][j + 1]: return False
        return True


def main():
    grid = Grid()
    # grid = Grid(_row_size=10)
    # grid = Grid(_row_size=2)
    running = True

    while running:
        # 绘制游戏区域
        grid.draw()

        game_over = False
        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and not game_over:
                if event.key == pygame.K_UP: grid.move('UP')
                elif event.key == pygame.K_DOWN: grid.move('DOWN')
                elif event.key == pygame.K_LEFT: grid.move('LEFT')
                elif event.key == pygame.K_RIGHT: grid.move('RIGHT')
                if grid.opd: grid.add_new_tile()
                game_over = grid.is_game_over()
            if event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_RETURN:
                    running = False

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
