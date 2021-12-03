import pygame
import os
from .enemy import Enemy

imgs=[]
for x in range(1,15):
    add_str = str(x)
    imgs.append(pygame.transform.scale(pygame.image.load(os.path.join(
        "game_assets/enemies/1",  add_str + ".png")),(54, 54)))

class Scorpion(Enemy):

    def __init__(self):
        super().__init__()
        self.name='scorpion'
        self.money=3
        self.imgs=[]
        self.max_health=10
        self.health=self.max_health
        self.imgs=imgs[:]
        self.animation = 5