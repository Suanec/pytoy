# !/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = 'enzhao'
# Created by enzhao on 2025/3/7.
import pygame
import random
from math import sin, cos, radians

# 马卡龙配色方案
class MacaronColors:
    BACKGROUND = (245, 213, 228)    # 浅粉
    SCREW_BODY = (163, 216, 232)     # 淡蓝
    SCREW_HEAD = (244, 233, 155)     # 鹅黄
    TEXT = (217, 122, 166)           # 玫红
    BUTTON = (158, 217, 200)         # 薄荷绿

class Screw(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.original_image = self._create_screw_image()
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(center=(x, y))
        self.angle = 0
        self.rotation_speed = random.choice([-5, 5])
        self.life = 100
        self.hit = False

    def _create_screw_image(self):
        surf = pygame.Surface((60, 60), pygame.SRCALPHA)
        # 绘制螺丝身体
        pygame.draw.rect(surf, MacaronColors.SCREW_BODY, (20, 10, 20, 40), border_radius=5)
        # 绘制螺丝头部
        pygame.draw.circle(surf, MacaronColors.SCREW_HEAD, (30, 15), 12)
        return surf

    def update(self):
        if not self.hit:
            # 自然旋转
            self.angle = (self.angle + self.rotation_speed) % 360
            self.image = pygame.transform.rotate(self.original_image, self.angle)
            self.rect = self.image.get_rect(center=self.rect.center)
        else:
            # 被击中后的动画
            self.life -= 4
            self.image = pygame.transform.smoothscale(self.original_image,
                                                      (self.life, self.life))
            self.rect = self.image.get_rect(center=self.rect.center)

    def check_click(self, pos):
        if self.rect.collidepoint(pos) and not self.hit:
            self.hit = True
            return True
        return False

class ScrewGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("马卡龙打螺丝")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 40)

        self.screws = pygame.sprite.Group()
        self.score = 0
        self.game_time = 30
        self.last_spawn = pygame.time.get_ticks()
        self.running = True
        self.game_active = True

    def spawn_screw(self):
        x = random.randint(100, 700)
        y = random.randint(100, 500)
        self.screws.add(Screw(x, y))

    def draw_score(self):
        score_surf = self.font.render(f"分数: {self.score}", True, MacaronColors.TEXT)
        self.screen.blit(score_surf, (20, 20))

        time_surf = self.font.render(f"时间: {int(self.game_time)}", True, MacaronColors.TEXT)
        self.screen.blit(time_surf, (20, 60))

    def draw_game_over(self):
        overlay = pygame.Surface((800, 600), pygame.SRCALPHA)
        overlay.fill((255, 255, 255, 128))
        self.screen.blit(overlay, (0, 0))

        text = self.font.render(f"游戏结束！最终得分: {self.score}", True, MacaronColors.TEXT)
        self.screen.blit(text, (200, 250))

        # 重新开始按钮
        pygame.draw.rect(self.screen, MacaronColors.BUTTON, (300, 350, 200, 50))
        text = self.font.render("重玩", True, MacaronColors.TEXT)
        self.screen.blit(text, (365, 360))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_active:
                    for screw in self.screws:
                        if screw.check_click(event.pos):
                            self.score += 10
                else:
                    # 检查重新开始按钮
                    if 300 < event.pos[0] < 500 and 350 < event.pos[1] < 400:
                        self.game_active = True
                        self.game_time = 30
                        self.score = 0
                        self.screws.empty()

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.handle_events()

            if self.game_active:
                # 更新游戏逻辑
                now = pygame.time.get_ticks()
                if now - self.last_spawn > 1500 and len(self.screws) < 8:
                    self.spawn_screw()
                    self.last_spawn = now

                self.game_time -= 1/60
                if self.game_time <= 0:
                    self.game_active = False

                self.screws.update()
                # 移除生命周期结束的螺丝
                self.screws = pygame.sprite.Group(
                    [s for s in self.screws if s.life > 0])

            # 绘制界面
            self.screen.fill(MacaronColors.BACKGROUND)
            self.screws.draw(self.screen)
            self.draw_score()

            if not self.game_active:
                self.draw_game_over()

            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    game = ScrewGame()
    game.run()