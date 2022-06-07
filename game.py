import pygame
import os
import time
from menu import PlayPauseButton, VerticalMenu

pygame.font.init()
pygame.init()

# path for enemies
path = [(-10, 224),(19, 224), (177, 235), (282, 283), (526, 277), (607, 217), (641, 105), (717, 57), (796, 83), (855, 222), (973, 284), (1046, 366), (1022, 458), (894, 492), (740, 504), (580, 542), (148, 541), (10, 442), (-20, 335), (-75, 305), (-100, 345)]

# load and scale images
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

# set up enemies in waves
# [scorpions, wizards, clubs, swords]
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

# load munis
pygame.mixer.music.load(os.path.join("game_assets","music.flac"))

attack_tower_names = ["archer","archer_2"]
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
        self.life_font = pygame.font.SysFont("comicsans",65)
        self.selected_tower = None
        self.menu = VerticalMenu(self.width - side_img.get_width()+70,250,side_img)
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


