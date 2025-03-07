# !/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = 'enzhao'
# Created by enzhao on 2025/3/7.
import pygame
import sys
from math import sin, cos, radians

class MacaronColors:
    BACKGROUND = (242, 220, 236)    # 浅紫
    SCREW_NORMAL = (163, 216, 232)   # 淡蓝
    SCREW_SOLVED = (158, 217, 200)   # 薄荷绿
    GRID = (244, 233, 155)          # 鹅黄
    TEXT = (217, 122, 166)           # 玫红

class PuzzleScrew(pygame.sprite.Sprite):
    def __init__(self, x, y, target_angle, is_master=False):
        super().__init__()
        self.original_image = self.create_screw_image()
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(center=(x, y))
        self.current_angle = 0
        self.target_angle = target_angle
        self.is_master = is_master  # 主螺丝控制其他螺丝
        self.is_solved = False

    def create_screw_image(self):
        surf = pygame.Surface((60, 60), pygame.SRCALPHA)
        # 绘制螺丝主体
        pygame.draw.circle(surf, MacaronColors.SCREW_NORMAL, (30, 30), 25)
        # 绘制凹槽
        for angle in range(0, 360, 90):
            start = (30 + 15*cos(radians(angle)), 30 + 15*sin(radians(angle)))
            end = (30 + 20*cos(radians(angle)), 30 + 20*sin(radians(angle)))
            pygame.draw.line(surf, (255,255,255), start, end, 3)
        return surf

    def rotate(self, clockwise=True):
        if not self.is_solved:
            self.current_angle += 90 if clockwise else -90
            self.current_angle %= 360
            self.image = pygame.transform.rotate(self.original_image, self.current_angle)
            self.rect = self.image.get_rect(center=self.rect.center)
            self.check_solved()

    def check_solved(self):
        tolerance = 5  # 允许的角度误差
        self.is_solved = abs(self.current_angle - self.target_angle) <= tolerance
        return self.is_solved

    def update(self):
        if self.is_solved:
            pygame.draw.circle(self.image, MacaronColors.SCREW_SOLVED, (30,30), 25)

class PuzzleSystem:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((600, 600))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 40)

        # 3x3谜题布局
        self.screws = pygame.sprite.Group()
        self.create_puzzle()

        self.running = True

    def create_puzzle(self):
        puzzle = [
            [0, 270, 180],
            [90, 0, 90],
            [180, 270, 0]
        ]
        for row in range(3):
            for col in range(3):
                x = 150 + col * 150
                y = 150 + row * 150
                target = puzzle[row][col]
                screw = PuzzleScrew(x, y, target, is_master=(row==1 and col==1))
                self.screws.add(screw)

    def draw_grid(self):
        # 绘制解谜网格线
        for i in range(1,3):
            pygame.draw.line(self.screen, MacaronColors.GRID,
                             (150*i, 50), (150*i, 550), 3)
            pygame.draw.line(self.screen, MacaronColors.GRID,
                             (50, 150*i), (550, 150*i), 3)

    def check_victory(self):
        return all(screw.is_solved for screw in self.screws)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for screw in self.screws:
                    if screw.rect.collidepoint(pos):
                        if screw.is_master:
                            # 主螺丝旋转会影响周围螺丝
                            for other in self.screws:
                                if abs(other.rect.centerx - screw.rect.centerx) <= 150 and \
                                        abs(other.rect.centery - screw.rect.centery) <= 150:
                                    other.rotate(clockwise=(event.button==1))
                        else:
                            screw.rotate(clockwise=(event.button==1))

    def run(self):
        while self.running:
            self.screen.fill(MacaronColors.BACKGROUND)
            self.draw_grid()

            self.handle_events()
            self.screws.update()
            self.screws.draw(self.screen)

            if self.check_victory():
                text = self.font.render("谜题破解成功！", True, MacaronColors.TEXT)
                self.screen.blit(text, (200, 550))

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    game = PuzzleSystem()
    game.run()