import pygame
import os
from .enemy import Enemy
import math

imgs=[]
for x in range(1,15):
    if x<10:
        add_str='0'+str(x)
    else: 
        add_str = str(x)
    imgs.append(pygame.transform.scale(pygame.image.load(os.path.join("game_assets/enemies/boss","9_enemies_1_walk_0" + add_str + ".png")),(70, 70)))

class Boss(Enemy):

    def __init__(self):
        super().__init__()
        self.name='boss'
        self.money=5
        self.imgs=[]
        self.max_health=15
        self.health=self.max_health
        self.imgs=imgs[:]
        self.speed=0.8

    def draw_health_bar(self,win):
        length=70
        move_by= round(length/self.max_health)
        health_bar=move_by * self.health

        pygame.draw.rect(win, (255,0,0),(self.x-70, self.y-30, length, 5), 0)
        pygame.draw.rect(win, (0,255,0),(self.x-70, self.y-30, health_bar, 5), 0)

    def draw(self, win):
  
        self.img=self.imgs[self.animation_count//5]
        # self.animation_count+=1
        # if self.animation_count >=len(self.imgs)*20:
        #     self.animation_count=0

        win.blit(self.img, (self.x-self.img.get_width(),self.y-self.img.get_height()//2))
        self.draw_health_bar(win)
        # self.move()
    
    def move(self):
         
        self.animation_count+=3
        if self.animation_count >=len(self.imgs)*5:
            self.animation_count=0

        x1, y1 = self.path[self.path_pos]
        if self.path_pos + 1 >= len(self.path):
            x2, y2 = (1000, 700)
        else:
            x2, y2 = self.path[self.path_pos+1]

        dirn = ((x2-x1)*2, (y2-y1)*2)
        length = math.sqrt((dirn[0])**2 + (dirn[1])**2)
        dirn = (dirn[0]/length*self.speed, dirn[1]/length*self.speed)

        if dirn[0] < 0 and not(self.flipped):
            self.flipped = True
            for x, img in enumerate(self.imgs):
                self.imgs[x] = pygame.transform.flip(img, True, False)

        move_x, move_y = ((self.x + dirn[0]), (self.y + dirn[1]))

        self.x = move_x
        self.y = move_y

        # Go to next point
        if dirn[0] >= 0: # moving right
            if dirn[1] >= 0: # moving down
                if self.x >= x2 and self.y >= y2:
                    self.path_pos += 1
            else:
                if self.x >= x2 and self.y <= y2:
                    self.path_pos += 1
        else: # moving left
            if dirn[1] >= 0:  # moving down
                if self.x <= x2 and self.y >= y2:
                    self.path_pos += 1
            else:
                if self.x <= x2 and self.y >= y2:
                    self.path_pos += 1  