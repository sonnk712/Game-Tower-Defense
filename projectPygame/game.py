from math import e, inf
import pygame
import os
from pygame.mixer import pause
from towers.archerTower import ArcherTower, ArcherTowerShort
from enemies.wizard import Sword
from enemies.scorpion import Scorpion
from enemies.knife import Knife
from enemies.boss import Boss
import time, random
from menu.menu import VerticalMenu, PlayPauseButton
# pygame.init()

lives_img = pygame.image.load(os.path.join("game_assets","live.png"))
star_img = pygame.image.load(os.path.join("game_assets","coin.png"))
side_img = pygame.transform.scale(pygame.image.load(os.path.join("game_assets","side2.png")), (500, 130))
buy_archer = pygame.transform.scale(pygame.image.load(os.path.join("game_assets","arc.png")), (75, 70))
buy_archer_2 = pygame.transform.scale(pygame.image.load(os.path.join("game_assets","49.png")), (75, 70))
wave_bg = pygame.transform.scale(pygame.image.load(os.path.join("game_assets","wave.png")), (225, 75))
play_btn = pygame.transform.scale(pygame.image.load(os.path.join("game_assets","button_start.png")), (75, 75))
pause_btn = pygame.transform.scale(pygame.image.load(os.path.join("game_assets","button_pause.png")), (75, 75))

attack_tower_names = ["archer", "archer2"]

waves = [[8, 0,0 ,0],[10, 5, 0],[15, 5, 5],[20, 20, 0],[10, 10, 10, 1],[0, 100, 0],
        [20, 100, 0],[50, 100, 0],[100, 100, 0],[0, 0, 50, 3],[20, 0, 100],
        [20, 0, 150],[200, 100, 200],
]




class Game:
    def __init__(self,win):
        self.width = 1000
        self.height = 700
        self.win = win
        self.enemys = []
        self.attack_towers = [ArcherTower(300,370),ArcherTowerShort(800,350),ArcherTowerShort(400,200)]
        self.support_towers = []
        self.lives = 10
        self.money = 20000
        self.bg = pygame.image.load(os.path.join("game_assets", "bg2.png"))
        self.bg = pygame.transform.scale(self.bg, (self.width, self.height))
        self.timer = time.time()
        self.life_font = pygame.font.SysFont("comicsans", 65)
        self.selected_tower=None
        self.clicks=[]
        self.menu = VerticalMenu(self.width - side_img.get_width() + 70, 250, side_img)
        self.menu.add_btn(buy_archer, "buy_archer", 500)
        self.menu.add_btn(buy_archer_2, "buy_archer_2", 750)
        self.moving_object=None
        self.wave=0
        self.current_wave = waves[self.wave][:]
        self.pause =True
        self.playpausebutton=PlayPauseButton(play_btn,pause_btn,10,self.height-700)

    def gen_enemies(self):
        if sum(self.current_wave)==0:
            if len(self.enemys)==0:
                self.wave+=1
                self.current_wave=waves[self.wave]
                #self.pause=True
                #self.playpausebutton.paused=self.pause
        else:
            wave_enemies = [Scorpion(), Sword(), Knife(),Boss()]
            for x in range(len(self.current_wave)):
                if self.current_wave[x]!=0:
                    self.enemys.append(wave_enemies[x])
                    self.current_wave[x]=self.current_wave[x]-1
                    break

    def run(self):
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(100)

            if self.pause==False:            
                #gen monster
                if time.time() - self.timer > random.randrange(1,5)/2:
                    self.timer= time.time()
                    self.gen_enemies()
                    # self.enemys.append(random.choice([Scorpion(), Wizard(), Knife()]))
            pygame.time.delay(0)

            pos = pygame.mouse.get_pos()
            # check for moving object
            if self.moving_object:
                self.moving_object.move(pos[0],pos[1])
                tower_list = self.attack_towers[:]
                collide = False
                for tw in tower_list:
                    if tw.collide(self.moving_object):
                        collide = True
                        tw.place_color = (255,0,0,100)
                    else:
                        tw.place_color = (0,0,255,100)
                        if not collide:
                            self.moving_object.place_color = (0,0,255,100)

            # main event loop
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    run=False
                # pos = pygame.mouse.get_pos()
                if event.type==pygame.MOUSEBUTTONUP:
                    # if u re moving an object and click
                    if self.moving_object:
                        not_allowed = False
                        tower_list = self.attack_towers[:]
                        for tw in tower_list:
                            if tw.collide(self.moving_object):
                                not_allowed=True
                        if not not_allowed:
                            if self.moving_object.name in attack_tower_names:
                                self.attack_towers.append(self.moving_object)

                            self.moving_object.moving=False
                            self.moving_object=None
                    else:

                        #check for play or pause
                        if self.playpausebutton.click(pos[0],pos[1]):
                            self.pause=not (self.pause)
                            self.playpausebutton.paused=self.pause

                        #look if u click on side menu
                        side_menu_button = self.menu.get_clicked(pos[0], pos[1])
                        if side_menu_button:
                            cost = self.menu.get_item_cost(side_menu_button)
                            if self.money >= cost:
                                self.money -= cost
                                self.add_tower(side_menu_button)
                        
                        btn_clicked=None
                        if self.selected_tower:
                            btn_clicked=self.selected_tower.menu.get_clicked(pos[0],pos[1])
                            if btn_clicked:
                                if btn_clicked == "Upgrade":
                                    cost = self.selected_tower.get_upgrade_cost()
                                    if cost=="MAX":
                                        cost=999999999
                                    if self.money >= cost:
                                        self.money -= cost
                                        self.selected_tower.upgrade()
                                elif btn_clicked =="Sell":
                                    s=self.selected_tower
                                    s.move(1200,800)
                                    cost = self.selected_tower.get_upgrade_cost()
                                    if cost=="MAX":
                                        cost=999999999                                    
                                    self.money+=int(cost)
                                    try:
                                        self.attack_towers.remove(s)
                                    except Exception as e:
                                        print(e)
                                    
                        if not(btn_clicked):
                            for tw in self.attack_towers:
                                if tw.click(pos[0], pos[1]):     
                                    tw.selected=True
                                    self.selected_tower=tw
                                else:
                                    tw.selected=False

            
            #loop through enemies
            if not self.pause:
                to_del=[]
                for en in self.enemys:
                    en.move()
                    if en.x> 1000:
                        to_del.append(en)
                #delete all enemies off the screen
                for d in to_del:
                    self.lives-=1
                    self.enemys.remove(d)
                
                #loop through towers
                for tw in self.attack_towers:
                    self.money+=tw.attack(self.enemys)

                if self.lives <=0:
                    print("You lose!!")
                    run = False

            self.draw()


    def draw(self):
        self.win.blit(self.bg, (0,0))
        #draw placement circle
        if self.moving_object:
            for tower in self.attack_towers:
                tower.draw_placement(self.win)
        #draw enemies
        for en in self.enemys:
            en.draw(self.win)
            
        #draw towers
        for tw in self.attack_towers:
            tw.draw(self.win)
            
        #draw menu
        self.menu.draw(self.win)

        #draw play,pause button
        self.playpausebutton.draw(self.win)
        
        #redraw selected tower
        if self.selected_tower:
            self.selected_tower.draw(self.win)
            
        #draw moving object
        if self.moving_object:
            self.moving_object.draw(self.win)
            
        #draw lives
        text = self.life_font.render(str(self.lives), 1, (255,255,255))
        life = pygame.transform.scale(lives_img,(50,50))
        start_x=self.width-life.get_width()-10

        self.win.blit(text, (start_x - text.get_width()-10 , 12))
        self.win.blit(life, (start_x, 10))

        #draw coins
        text = self.life_font.render(str(self.money), 1, (255,255,255))
        money = pygame.transform.scale(star_img,(50,50))
        start_x=self.width-life.get_width()+30

        self.win.blit(text, (start_x - text.get_width()-50 , 70))
        self.win.blit(money, (start_x-30, 65))

        # draw wave
        self.win.blit(wave_bg, (400,10))
        text = self.life_font.render("Wave #" + str(self.wave), 1, (255,255,255))
        self.win.blit(text, (wave_bg.get_width()+200 , 25))
    
        pygame.display.update()

    def add_tower(self, name):
        x, y = pygame.mouse.get_pos()
        name_list = ["buy_archer", "buy_archer_2",]
        object_list = [ArcherTower(x,y), ArcherTowerShort(x,y),]

        try:
            obj = object_list[name_list.index(name)]
            self.moving_object = obj
            obj.moving = True
        except Exception as e:
            print(str(e) + "NOT VALID NAME")

if __name__ == "__main__":
    pygame.init()
    win = pygame.display.set_mode((1000, 700))
    from main_menu.main_menu import MainMenu
    mainMenu = MainMenu(win)
    mainMenu.run()


# win=pygame.display.set_mode((1000,700))
# g=Game(win)
# g.run()
