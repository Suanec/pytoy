# !/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = 'enzhao'
# Created by enzhao on 2025/3/7.
import pygame,sys
from pygame.locals import *

class MacaronColors:
    BACKGROUND = (242, 220, 236)    # 浅紫色
    CAR = (163, 216, 232)           # 淡蓝色
    TARGET_CAR = (217, 122, 166)    # 玫红色
    GRID = (244, 233, 155)          # 鹅黄色
    BLOCK = (158, 217, 200)         # 薄荷绿
    TEXT = (255, 183, 197)          # 粉红色

class Vehicle(pygame.sprite.Sprite):
    def __init__(self, x, y, length, orientation, is_target=False):
        super().__init__()
        self.is_target = is_target
        self.orientation = orientation  # 'H' 水平 / 'V' 垂直
        self.length = length
        self.color = MacaronColors.TARGET_CAR if is_target else MacaronColors.CAR

        # 创建车辆表面
        if orientation == 'H':
            self.image = pygame.Surface((60*length, 60), SRCALPHA)
            pygame.draw.rect(self.image, self.color, (0, 20, 60*length, 40), border_radius=10)
        else:
            self.image = pygame.Surface((60, 60*length), SRCALPHA)
            pygame.draw.rect(self.image, self.color, (20, 0, 40, 60*length), border_radius=10)

        self.rect = self.image.get_rect(topleft=(x*60, y*60))
        self.selected = False

    def can_move(self, direction, obstacles):
        test_rect = self.rect.copy()
        step = 60 if direction in ['right', 'down'] else -60

        if self.orientation == 'H':
            if direction in ['left', 'right']:
                test_rect.x += step
            else:
                return False
        else:
            if direction in ['up', 'down']:
                test_rect.y += step
            else:
                return False

        # 边界检测
        if test_rect.left < 0 or test_rect.right > 360 or test_rect.top < 0 or test_rect.bottom > 360:
            return False

        # 碰撞检测
        for obstacle in obstacles:
            if obstacle != self and test_rect.colliderect(obstacle.rect):
                return False
        return True

class ParkingPuzzle:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((600, 480))
        pygame.display.set_caption("马卡龙挪车")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

        # 初始化关卡（6x6网格）
        self.vehicles = pygame.sprite.Group()
        self.init_level()
        self.selected_vehicle = None
        self.moves = 0
        self.game_won = False

    def init_level(self):
        # 目标车辆（红色）
        self.vehicles.add(Vehicle(0, 2, 2, 'H', is_target=True))
        # 其他障碍车辆
        self.vehicles.add(Vehicle(2, 0, 2, 'V'))
        self.vehicles.add(Vehicle(4, 0, 3, 'V'))
        self.vehicles.add(Vehicle(0, 4, 3, 'H'))
        self.vehicles.add(Vehicle(3, 3, 2, 'H'))

    def draw_grid(self):
        # 绘制停车网格
        for x in range(0, 361, 60):
            pygame.draw.line(self.screen, MacaronColors.GRID, (x, 0), (x, 360), 2)
        for y in range(0, 361, 60):
            pygame.draw.line(self.screen, MacaronColors.GRID, (0, y), (360, y), 2)

    def check_win(self):
        target = next(v for v in self.vehicles if v.is_target)
        return target.rect.right > 360

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for vehicle in self.vehicles:
                    if vehicle.rect.collidepoint(pos):
                        self.selected_vehicle = vehicle
                        break

            if event.type == KEYDOWN and self.selected_vehicle:
                direction_map = {
                    K_LEFT: 'left',
                    K_RIGHT: 'right',
                    K_UP: 'up',
                    K_DOWN: 'down'
                }
                if event.key in direction_map:
                    if self.selected_vehicle.can_move(direction_map[event.key], self.vehicles):
                        step = 60 if direction_map[event.key] in ['right', 'down'] else -60
                        if self.selected_vehicle.orientation == 'H':
                            self.selected_vehicle.rect.x += step
                        else:
                            self.selected_vehicle.rect.y += step
                        self.moves += 1
                        self.game_won = self.check_win()

    def run(self):
        while True:
            self.screen.fill(MacaronColors.BACKGROUND)
            self.handle_events()

            # 绘制游戏区域
            pygame.draw.rect(self.screen, MacaronColors.BLOCK, (360, 140, 120, 60))  # 出口
            self.draw_grid()
            self.vehicles.draw(self.screen)

            # 显示移动次数
            moves_text = self.font.render(f"move step 移动次数: {self.moves}", True, MacaronColors.TEXT)
            self.screen.blit(moves_text, (400, 360))

            if self.game_won:
                win_text = self.font.render("成功逃脱！success ", True, MacaronColors.TEXT)
                self.screen.blit(win_text, (400, 200))

            pygame.display.flip()
            self.clock.tick(30)

if __name__ == "__main__":
    game = ParkingPuzzle()
    game.run()