import pygame
from menu import Menu
import os
import math

menu_bg = pygame.transform.scale(pygame.image.load(os.path.join("game_assets","menu.png")),(120,70))
upgrade_btn = pygame.transform.scale(pygame.image.load(os.path.join("game_assets","upgrade.png")),(50,50))

class Tower:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.width = 0
        self.height = 0
        self.sell_price = [0,0,0]
        self.price = [0,0,0]
        self.level = 1
        self.selected = False
        self.menu = Menu(self,self.x,self.y,menu_bg,[2000,"MAX"])
        self.menu.add_btn(upgrade_btn,"Upgrade")
        self.tower_imgs=[]
        self.damage=1
        self.place_color=(0,0,255,100)

    def draw(self,win):
        """
        draw towers
        :param win: surface
        :return: None
        """
        img = self.tower_imgs[self.level-1]
        win.blit(img,(self.x-img.get_width()/2,self.y-img.get_height()/2))
        # draw tower's menu
        if self.selected:
            self.menu.draw(win)

    def draw_radius(self,win):
        if self.selected:
            # draw a circle of tower's range
            surface=pygame.Surface((self.range*4,self.range*4),pygame.SRCALPHA,32)
            pygame.draw.circle(surface,(128,128,128,100),(self.range,self.range),self.range,0)
            win.blit(surface,(self.x-self.range,self.y-self.range))

    def draw_placement(self,win):
        # draw range circle
        surface=pygame.Surface((self.range*4,self.range*4),pygame.SRCALPHA,32)
        pygame.draw.circle(surface,(0,0,255,100),(50,50),50,0)
        win.blit(surface,(self.x-50,self.y-50))

    def click(self,X,Y):
        """
        to check if tower has been clicked on and selects tower if it is clicked
        :param X: int
        :param Y: int
        :return: bool
        """
        img = self.tower_imgs[self.level-1]
        if self.x - img.get_width()/2<=X<=self.x-img.get_width()/2+self.width:
            if self.y-img.get_height()/2<=Y<=self.y+self.height-img.get_height()/2:
                return True
        return False

    def upgrade(self):
        """
        upgrade the tower
        :return: None
        """
        if self.level<len(self.tower_imgs):
            self.level+=1
            self.damage+=1

    def get_upgrade_cost(self):
        """
        upgrade cost
        :return: int
        """
        return self.price[self.level-1]

    def move(self,x,y):
        """
        move tower to x,y
        :param x: int
        :param y: int
        :return: None
        """
        self.x=x
        self.y=y
        self.menu.x=x
        self.menu.y=y
        self.menu.update()

    def collide(self,otherTower):
        """
        to check if a new tower will collide with an existing tower
        :param otherTower: tower
        :return: bool
        """
        x2,y2=otherTower.x,otherTower.y
        dis = math.sqrt((x2-self.x)**2+(y2-self.y)**2)
        if dis>=100:
            return False
        else:
            return True