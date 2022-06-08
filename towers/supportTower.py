import pygame
import os
import math
from tower import Tower

range_imgs = [
    pygame.transform.scale(pygame.image.load(os.path.join("game_assets/support_towers","4.png")),(90,90)),
    pygame.transform.scale(pygame.image.load(os.path.join("game_assets/support_towers","5.png")),(90,90))
]

# range tower is to add extra range to each surrounding tower
class RangeTower(Tower):
    def __init__(self):
        super().__init__()
        self.range = 75
        self.effect = [0.2,0.4]
        self.tower_imgs = range_imgs
        self.width=self.height=90
        self.name="range"
        self.price=[2000]

    def draw(self,win):
        super().draw_radius(win)
        super().draw(win)

    def support(self,towers):
        """
        modify towers according to ability
        :param towers: list
        :return: None
        """
        effected = []
        for tower in towers:
            x=tower.x
            y=tower.y
            dis=math.sqrt((self.x-x)**2+(self.y-y)**2)
            if dis <= self.range+tower.width/2:
                effected.append(tower)
        for tower in effected:
            tower.range=tower.original_range+round(tower.range*self.effect[self.level-1])

damage_imgs = [
    pygame.transform.scale(pygame.image.load(os.path.join("game_assets/support_towers","8.png")),(90,90)),
    pygame.transform.scale(pygame.image.load(os.path.join("game_assets/support_towers","9.png")),(90,90))
]

# add damage effect to surrounding towers
class DamageTower(Tower):
    def __init__(self):
        super().__init__()
        self.range=100
        self.tower_imgs=damage_imgs
        self.effect=[0.5,1]
        self.name="damage"
        self.price=[2000]

    def support(self,towers):
        """
        modify towers according to ability
        :param towers: list
        :return: None
        """
        effected = []
        for tower in towers:
            x=tower.x
            y=tower.y
            dis=math.sqrt((self.x-x)**2+(self.y-y)**2)
            if dis<=self.range+tower.width/2:
                effected.append(tower)
        for tower in effected:
            tower.damage = tower.original_damage+round(tower.original_damage*self.effect[self.level-1])