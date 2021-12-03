import pygame
from .tower import Tower
import os
import math
import time
from menu.menu import Menu
from menu import *

menu_bg = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "menu1.png")), (220, 70))
upgrade_btn = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "upgrade_button.png")), (50, 50))
sell_btn= pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "sell.png")), (45, 45))

class ArcherTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.tower_imgs=[]
        self.archer_imgs=[]
        self.archer_count=0
        self.range=200
        self.inRange=False
        self.left=True
        self.damage=1
        self.width=self.height=54
        self.menu=Menu(self,self.x,self.y,menu_bg, [2000,5000,"MAX"])
        self.menu.add_btn(upgrade_btn, "Upgrade")
        self.menu.add_sell_btn(sell_btn,"Sell")
        self.moving=False
        self.name="archer"

        #load archer tower imgs
        for x in range(12,15):
            add_str = str(x)
            self.tower_imgs.append(pygame.transform.scale
                (pygame.image.load(os.path.join("game_assets/archer_tower/archer_1",  add_str + ".png")),(74, 54)))
        for x in range(35,40):
            add_str = str(x)
            self.archer_imgs.append(pygame.transform.scale
              (pygame.image.load(os.path.join("game_assets/archer_tower/archer_top",  add_str + ".png")),(200, 100)))

    def get_upgrade_cost(self):
        """
        gets the upgrade cost
        :return: int
        """
        return self.menu.get_item_cost()



    def draw(self,win):
        #draw range circle
        super().draw_radius(win)
        super().draw(win)
        
        if self.inRange and not (self.moving):    
            self.archer_count+=1
            if self.archer_count>=len(self.archer_imgs)*8:
                self.archer_count=0
        else:
            self.archer_count=0

        archer=self.archer_imgs[self.archer_count//8]
        # if self.left==True:
        #     add=-25
        # else:
        #     add=archer.get_width()/2
        win.blit(archer,  ((self.x+self.width)-(archer.get_width()/2)-45,
                           (self.y-archer.get_height()/2)-20))


    def change_range(self,r):
        self.range=r

    def attack(self,enemies):
        #attacks an enemy in the enemy list
        money=0
        self.inRange=False
        enemy_closet=[]
        for enemy in enemies:
            x=enemy.x
            y=enemy.y
            dis = math.sqrt((self.x-x)**2 + (self.y-y)**2)
            if dis < self.range:
                self.inRange=True
                enemy_closet.append(enemy)

        enemy_closet.sort(key=lambda x: x.path_pos)
        enemy_closet=enemy_closet[::-1]
        if len(enemy_closet)>0:
            first_enemy=enemy_closet[0]
            if self.archer_count==4:
                self.timer=time.time()
                if first_enemy.hit(self.damage)==True:
                    money= first_enemy.money
                    enemies.remove(first_enemy)

            if first_enemy.x > self.x and not(self.left):
                self.left = True
                for x, img in enumerate(self.archer_imgs):
                    self.archer_imgs[x] = pygame.transform.flip(img, True, False)
            elif self.left and first_enemy.x < self.x:
                self.left = False
                for x, img in enumerate(self.archer_imgs):
                    self.archer_imgs[x] = pygame.transform.flip(img, True, False)
        return money

tower_imgs1 = []
archer_imgs1 = []
# load archer tower images
for x in range(1,4):
    add_str = str(x)
    tower_imgs1.append(pygame.transform.scale(pygame.image.load(os.path.join("game_assets/archer_tower/stone",  add_str + ".png")),(54, 54)))
for x in range(49,56):
    add_str = str(x)
    archer_imgs1.append(pygame.transform.scale(pygame.image.load(os.path.join("game_assets/archer_tower/stone-top",  add_str + ".png")),(30, 30)))

class ArcherTowerShort(ArcherTower):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.tower_imgs=tower_imgs1[:]
        self.archer_imgs=archer_imgs1[:]
        self.archer_count=0
        self.range=100
        self.inRange=False
        self.left=True
        self.damage=2
        self.width=self.height=54
        self.menu=Menu(self,self.x,self.y,menu_bg, [2000,5000,"MAX"])
        self.menu.add_btn(upgrade_btn, "Upgrade")
        self.name="archer2"
    def upgrade(self):
        if self.level<len(self.tower_imgs):
            self.level +=1
            self.damage+=3
            self.range+=50