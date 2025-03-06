# !/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = 'enzhao'
# Created by enzhao on 2025/3/6.
import pygame
import random
import sys

# 初始化参数
WIDTH, HEIGHT = 400, 500
GRID_SIZE = 90
GRID_PADDING = 10
TOP_PADDING = 100
COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46)
}
COLORS = {
    "background": (249, 224, 237),  # 浅粉背景
    "grid": (255, 243, 252),        # 网格线颜色
    0: (255, 255, 255, 0),          # 透明色
    2: (169, 222, 249),             # 浅蓝
    4: (255, 227, 174),             # 奶油黄
    8: (255, 192, 203),             # 粉红
    16: (221, 160, 221),            # 薰衣草紫
    32: (255, 182, 193),            # 桃红
    64: (152, 251, 152),            # 薄荷绿
    128: (240, 128, 128),           # 珊瑚色
    256: (147, 197, 114),           # 抹茶绿
    512: (255, 160, 122),           # 橙红
    1024: (216, 191, 216),          # 淡紫灰
    2048: (255, 215, 0)             # 金色
}


def init_board():
    """初始化4x4游戏板并添加初始数字块"""
    board = [[0]*4 for _ in range(4)]
    add_new_tile(board)
    add_new_tile(board)
    return board

def add_new_tile(board):
    """在空白位置随机添加新数字块（90%概率为2，10%概率为4）"""
    empty = [(i,j) for i in range(4) for j in range(4) if board[i][j]==0]
    if empty:
        i,j = random.choice(empty)
        board[i][j] = 2 if random.random() < 0.9 else 4

def move(board, direction):
    """处理移动逻辑（核心算法）"""
    def merge(row):
        new_row = []
        merged = False
        for num in row:
            if num == 0: continue
            if new_row and new_row[-1] == num and not merged:
                new_row[-1] *= 2
                merged = True
            else:
                new_row.append(num)
                merged = False
        return new_row + [0]*(4-len(new_row))

    rotated = list(zip(*board)) if direction in ['UP','DOWN'] else board
    if direction in ['DOWN','RIGHT']:
        rotated = [row[::-1] for row in rotated]

    new_board = []
    for row in rotated:
        merged_row = merge([x for x in row if x != 0])
        new_board.append(merged_row)

    if direction in ['DOWN','RIGHT']:
        new_board = [row[::-1] for row in new_board]
    if direction in ['UP','DOWN']:
        return [list(x) for x in list(zip(*new_board))]
    return new_board

def is_game_over(board):
    """检测游戏结束条件"""
    for i in range(4):
        for j in range(4):
            if board[i][j] == 0: return False
            if i<3 and board[i][j]==board[i+1][j]: return False
            if j<3 and board[i][j]==board[i][j+1]: return False
    return True

def draw_board(screen, board, font):
    """绘制游戏界面"""
    # screen.fill((187, 173, 160))  # 背景色
    screen.fill(COLORS.get("background"))  # 背景色
    for i in range(4):
        for j in range(4):
            x = j*(GRID_SIZE+GRID_PADDING)+10
            y = TOP_PADDING + i*(GRID_SIZE+GRID_PADDING)
            value = board[i][j]
            color = COLORS[value]
            pygame.draw.rect(screen, color, (x, y, GRID_SIZE, GRID_SIZE))
            if value != 0:
                text = font.render(str(value), True, (0,0,0) if value<8 else (255,255,255))
                text_rect = text.get_rect(center=(x+GRID_SIZE//2, y+GRID_SIZE//2))
                screen.blit(text, text_rect)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    score = 2048
    pygame.display.set_caption("2048")
    pygame.display.set_caption("马卡龙2048")
    font = pygame.font.Font(None, 56)
    score_font = pygame.font.Font(None, 28)
    score_text = score_font.render(f"Score: {score}", True, (255, 105, 180))
    screen.blit(score_text, (20, 70))
    clock = pygame.time.Clock()

    board = init_board()
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and not game_over:
                prev_board = [row[:] for row in board]
                if event.key == pygame.K_UP: board = move(board, 'UP')
                elif event.key == pygame.K_DOWN: board = move(board, 'DOWN')
                elif event.key == pygame.K_LEFT: board = move(board, 'LEFT')
                elif event.key == pygame.K_RIGHT: board = move(board, 'RIGHT')
                if board != prev_board: add_new_tile(board)
                game_over = is_game_over(board)

        draw_board(screen, board, font)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
