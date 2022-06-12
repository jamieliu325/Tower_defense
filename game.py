import pygame
import os
import time
from menu import PlayPauseButton, VerticalMenu
from enemies.scorpion import Scorpion
from enemies.club import Club
from enemies.sword import Sword
from enemies.wizard import Wizard
from towers.archerTower import ArcherTowerLong,ArcherTowerShort
from towers.supportTower import DamageTower,RangeTower
import random

# pygame initiation
pygame.font.init()
pygame.init()

# path for enemies
path = [(-10, 224),(19, 224), (177, 235), (282, 283), (526, 277), (607, 217), (641, 105), (717, 57), (796, 83), (855, 222), (973, 284), (1046, 366), (1022, 458), (894, 492), (740, 504), (580, 542), (148, 541), (10, 442), (-20, 335), (-75, 305), (-100, 345)]

# load and scale images for the game
lives_img = pygame.image.load(os.path.join("game_assets","heart.png"))
star_img = pygame.image.load(os.path.join("game_assets","star.png"))
side_img = pygame.transform.scale(pygame.image.load(os.path.join("game_assets","side.png")),(120,500))
buy_archer = pygame.transform.scale(pygame.image.load(os.path.join("game_assets","buy_archer.png")),(75,75))
buy_archer_2 = pygame.transform.scale(pygame.image.load(os.path.join("game_assets","buy_archer_2.png")),(75,75))
buy_damage = pygame.transform.scale(pygame.image.load(os.path.join("game_assets","buy_damage.png")),(75,75))
buy_range = pygame.transform.scale(pygame.image.load(os.path.join("game_assets","buy_range.png")),(75,75))
play_btn = pygame.transform.scale(pygame.image.load(os.path.join("game_assets","button_start.png")),(75,75))
pause_btn = pygame.transform.scale(pygame.image.load(os.path.join("game_assets","button_pause.png")),(75,75))
sound_btn = pygame.transform.scale(pygame.image.load(os.path.join("game_assets","button_sound.png")),(75,75))
sound_btn_off = pygame.transform.scale(pygame.image.load(os.path.join("game_assets","button_sound_off.png")),(75,75))
wave_bg = pygame.transform.scale(pygame.image.load(os.path.join("game_assets","wave.png")),(225,75))

# set up enemy waves
# number of enemies for [scorpions, wizards, clubs, swords]
waves = [
    [20, 0, 0],
    [50, 0, 0],
    [100, 0, 0],
    [0, 20, 0],
    [0, 50, 0, 1],
    [0, 100, 0],
    [20, 100, 0],
    [50, 100, 0],
    [100, 100, 0],
    [0, 0, 50, 3],
    [20, 0, 100],
    [20, 0, 150],
    [200, 100, 200]
]

# load music
pygame.mixer.music.load(os.path.join("game_assets","music.flac"))

# tower names
attack_tower_names = ["archer","archer2"]
support_tower_names = ["range","damage"]

class Game:
    def __init__(self,win):
        self.width = 1350
        self.height = 700
        self.win = win
        self.enemies = []
        self.attack_towers = []
        self.support_towers = []
        self.lives = 50
        self.money = 10000
        self.bg = pygame.transform.scale(pygame.image.load(os.path.join("game_assets","bg.png")),(self.width,self.height))
        self.timer = time.time()
        self.life_font = pygame.font.SysFont("comicsans",45)
        self.selected_tower = None
        self.menu = VerticalMenu(self.width - side_img.get_width(),130,side_img)
        self.menu.add_btn(buy_archer,"buy_archer",500)
        self.menu.add_btn(buy_archer_2,"buy_archer_2",750)
        self.menu.add_btn(buy_damage,"buy_damage",1000)
        self.menu.add_btn(buy_range,"buy_range",1000)
        self.moving_object = None
        self.wave = 1
        self.current_wave = waves[self.wave-1][:]
        self.pause = True
        self.music_on = True
        self.playPauseButton = PlayPauseButton(play_btn,pause_btn,10,self.height-85)
        self.soundButton = PlayPauseButton(sound_btn,sound_btn_off,90,self.height-85)

    def gen_enemies(self):
        """
        generate the next wave of enemies if all enemies are generated and removed from the game
        generate enemies from the current wave
        :return: None
        """
        if sum(self.current_wave) == 0:
            if len(self.enemies)==0:
                self.wave += 1
                self.current_wave=waves[self.wave-1]
                self.pause=True
                self.playPauseButton.paused=self.pause
        else:
            wave_enemies = [Scorpion(),Wizard(),Club(),Sword()]
            for x in range(len(self.current_wave)):
                if self.current_wave[x] != 0:
                    self.enemies.append(wave_enemies[x])
                    self.current_wave[x] -= 1

    def run(self):
        # play music
        pygame.mixer.music.play(loops=-1)
        run = True
        clock = pygame.time.Clock()
        while run:
            # set up runtime speed of the game
            clock.tick(500)
            if self.pause == False:
            # generate enemies by setting up the frequency of generation
                if time.time() - self.timer >= random.randrange(1,6)/2:
                    self.timer = time.time()
                    self.gen_enemies()

            pos = pygame.mouse.get_pos()
            # check for moving object
            if self.moving_object:
                self.moving_object.move(pos[0],pos[1])
                tower_list=self.attack_towers+self.support_towers
                collide=False
                for tower in tower_list:
                    if tower.collide(self.moving_object):
                        # if towers collide, placement color turns to red
                        collide = True
                        tower.place_color=(255,0,0,100)
                        self.moving_object.place_color=(255,0,0,100)
                    else:
                        tower.place_color=(0,0,255,100)
                        if not collide:
                            self.moving_object.place_color=(0,0,255,100)

            # main event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    # if you are moving an object
                    if self.moving_object:
                        not_allowewd = False
                        tower_list=self.attack_towers[:]+self.support_towers[:]
                        for tower in tower_list:
                            if tower.collide(self.moving_object):
                                not_allowewd=True
                        if not not_allowewd:
                            if self.moving_object.name in attack_tower_names:
                                self.attack_towers.append(self.moving_object)
                            elif self.moving_object.name in support_tower_names:
                                self.support_towers.append(self.moving_object)
                            self.moving_object.moving=False
                            self.moving_object=None
                    else:
                        # check for play or pause
                        if self.playPauseButton.click(pos[0],pos[1]):
                            self.pause = not self.pause
                            self.playPauseButton.paused=self.pause
                        elif self.soundButton.click(pos[0],pos[1]):
                            self.music_on = not self.music_on
                            self.soundButton.paused = self.music_on
                            if self.music_on:
                                pygame.mixer.music.unpause()
                            else:
                                pygame.mixer.music.pause()
                        # check if click on side menu
                        side_menu_button = self.menu.get_clicked(pos[0],pos[1])
                        if side_menu_button:
                            cost = self.menu.get_item_cost(side_menu_button)
                            if self.money>=cost:
                                self.money-=cost
                                self.add_tower(side_menu_button)

                        # to check if click on tower
                        btn_clicked = None
                        if self.selected_tower:
                            btn_clicked = self.selected_tower.menu.get_clicked(pos[0],pos[1])
                            # upgrade tower
                            if btn_clicked == "Upgrade":
                                cost = self.selected_tower.get_upgrade_cost()
                                if cost != "MAX" and self.money>=cost:
                                    self.money-=cost
                                    self.selected_tower.upgrade()
                        if not btn_clicked:
                            for tw in self.attack_towers:
                                if tw.click(pos[0],pos[1]):
                                    tw.selected=True
                                    self.selected_tower=tw
                                else:
                                    tw.selected=False
                            for tw in self.support_towers:
                                if tw.click(pos[0],pos[1]):
                                    tw.selected=True
                                    self.selected_tower=tw
                                else:
                                    tw.selected=False
            # add effects to attack tower
            for tw in self.support_towers:
                tw.support(self.attack_towers)
            # loop through enemies
            if not self.pause:
                # check if enemies off screen
                to_del = []
                for en in self.enemies:
                    en.move()
                    if en.x<-15:
                        to_del.append(en)
                # delete enemies off the screen
                for d in to_del:
                    self.lives-=1
                    self.enemies.remove(d)
                # loop through towers
                for tw in self.attack_towers:
                    self.money += tw.attack(self.enemies)


                # if lose
                if self.lives<=0:
                    print("You Lose")
                    run=False
            self.draw()


    def draw(self):
        self.win.blit(self.bg,(0,0))
        # drawing placement circles:
        if self.moving_object:
            for tower in self.attack_towers:
                tower.draw_placement(self.win)
            for tower in self.support_towers:
                tower.draw_placement(self.win)
            self.moving_object.draw_placement(self.win)

        # draw attack and support towers
        for tw in self.attack_towers:
            tw.draw(self.win)

        for tw in self.support_towers:
            tw.draw(self.win)

        # draw enemies
        for en in self.enemies:
            en.draw(self.win)

        # draw selected tower
        if self.selected_tower:
            self.selected_tower.draw(self.win)

        # draw moving object
        if self.moving_object:
            self.moving_object.draw(self.win)


        # draw menu
        self.menu.draw(self.win)

        # draw play and pause button
        self.playPauseButton.draw(self.win)

        # draw music button
        self.soundButton.draw(self.win)

        # draw lives
        text = self.life_font.render(str(self.lives),1,(255,255,255))
        life = pygame.transform.scale(lives_img,(50,50))
        start_x = self.width - life.get_width() -10
        self.win.blit(text,(start_x-text.get_width()-10,0))
        self.win.blit(life,(start_x,10))

        # draw money
        text = self.life_font.render(str(self.money),1,(255,255,255))
        money = pygame.transform.scale(star_img,(50,50))
        money_x = self.width - money.get_width()-10
        self.win.blit(text,(money_x-text.get_width()-10,60))
        self.win.blit(money,(start_x,65))

        # draw wave
        self.win.blit(wave_bg,(10,10))
        text=self.life_font.render("Wave #"+str(self.wave),1,(255,255,255))
        self.win.blit(text,(10+wave_bg.get_width()/2-text.get_width()/2,15))

        pygame.display.update()

    def add_tower(self,name):
        x,y=pygame.mouse.get_pos()
        name_list=["buy_archer","buy_archer_2","buy_damage","buy_range"]
        object_list=[ArcherTowerLong(x,y),ArcherTowerShort(x,y),DamageTower(x,y),RangeTower(x,y)]
        try:
            obj = object_list[name_list.index(name)]
            self.moving_object = obj
            obj.moving=True
        except Exception as e:
            print(str(e)+"NOT VALID NAME")



