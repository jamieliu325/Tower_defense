import pygame
import os
import math

class Enemy:
    def __init__(self):
        self.width = 64
        self.height = 64
        self.animation_count = 0
        self.health = 1
        self.vel = 3
        self.path = [(-10, 224), (19, 224), (177, 235), (282, 283), (526, 277), (607, 217), (641, 105), (717, 57),
                     (796, 83), (855, 222), (973, 284), (1046, 366), (1022, 458), (894, 492), (740, 504), (580, 542),
                     (148, 541), (10, 442), (-20, 335), (-75, 305), (-100, 345)]
        self.x = self.path[0][0]
        self.y = self.path[0][1]
        self.img = pygame.image.load(os.path.join("game_assets/enemies/1","1_enemies_1_run_000.png"))
        self.dis = 0
        self.path_pos = 0
        self.move_count = 0
        self.move_dis = 0
        self.flipped = False
        self.max_health = 0
        self.speed_increase = 1

    def draw(self,win):
        """
        draw enemy with given images
        :param win: surface
        :return: None
        """
        self.img = self.imgs[self.animation_count]
        win.blit(self.img,(self.x-self.img.get_width()/2,self.y-self.img.get_height()/2-35))
        self.draw_health_bar(win)

    def draw_health_bar(self,win):
        """
        draw heath bar above enemy
        :param win: surface
        :return: None
        """
        length = 50
        health_bar = length*self.health/self.max_health
        pygame.draw.rect(win,(255,0,0),(self.x-30,self.y-75,length,10),0)
        pygame.draw.rect(win,(0,255,0),(self.x-30,self.y-75,health_bar,10),0)

    def move(self):
        """
        move enemy
        :return: None
        """
        self.animation_count += 1
        if self.animation_count >= len(self.imgs):
            self.animation_count = 0

        x1,y1 = self.path[self.path_pos]
        x1 = x1+80
        if self.path_pos + 1 >= len(self.path):
            x2,y2 = (-10,355)
        else:
            x2,y2 = self.path[self.path_pos+1]
        x2 = x2 +80

        dirn = ((x2-x1), (y2-y1))
        length = math.sqrt(dirn[0]**2+dirn[1]**2)
        dirn = (dirn[0]/length*self.speed_increase,dirn[1]/length*self.speed_increase)

        # flip enemy  when they are moving toward left
        if dirn[0]<0 and not self.flipped:
            self.flipped = True
            for x,img in enumerate(self.imgs):
                self.imgs[x] = pygame.transform.flip(img,True,False)

        move_x,move_y = (self.x+dirn[0],self.y+dirn[1])
        self.x,self.y=move_x,move_y

        # go to next point, dirn[0]>=0: moving right, else: moving left; dirn[1]>=0: moving down, else:moving up
        if dirn[0]>=0:
            if dirn[1]>=0:
                if self.x>=x2 and self.y>=y2:
                    self.path_pos +=1
            else:
                if self.x>=x2 and self.y<=y2:
                    self.path_pos +=1
        else:
            if dirn[1]>=0:
                if self.x<=x2 and self.y>=y2:
                    self.path_pos+=1
            else:
                if self.x<=x2 and self.y>=y2:
                    self.path_pos += 1

    def hit(self,damage):
        """
        remove one health after each hit and check if enemy has died
        :param damage: int
        :return: bool
        """
        self.health -= damage
        if self.health<=0:
            return True
        return False
