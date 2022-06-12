import pygame
import os
import math
from .tower import Tower
from menu import Menu

# load imgs for range and damage towers
range_imgs = [
    pygame.transform.scale(pygame.image.load(os.path.join("game_assets/support_towers","4.png")),(90,90)),
    pygame.transform.scale(pygame.image.load(os.path.join("game_assets/support_towers","5.png")),(90,90))
]


# range tower is to add extra range to each surrounding tower
class RangeTower(Tower):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.range = 150
        self.effect = [1.2,1.5]
        self.tower_imgs = range_imgs
        self.width=self.height=90
        self.name="range"

    def draw(self,win):
        super().draw_radius(win)
        super().draw(win)

    def support(self,towers):
        """
        increase the range of tower effected
        :param towers: list
        :return: None
        """
        effected = []
        for tower in towers:
            x=tower.x
            y=tower.y
            dis=math.sqrt((self.x-x)**2+(self.y-y)**2)
            if dis <= self.range:
                effected.append(tower)
        for tower in effected:
            tower.range=tower.original_range*self.effect[self.level-1]


damage_imgs = [
    pygame.transform.scale(pygame.image.load(os.path.join("game_assets/support_towers","8.png")),(90,90)),
    pygame.transform.scale(pygame.image.load(os.path.join("game_assets/support_towers","9.png")),(90,90))
]

# add damage effect to surrounding towers
class DamageTower(Tower):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.range=150
        self.tower_imgs=damage_imgs
        self.effect=[1.5,2]
        self.name="damage"
        self.width=self.height=90

    def draw(self,win):
        super().draw_radius(win)
        super().draw(win)

    def support(self,towers):
        """
        increase tower damage
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
            tower.damage = tower.original_damage*self.effect[self.level-1]