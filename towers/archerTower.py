import pygame
import os
import math
from .tower import Tower
from menu import Menu

menu_bg = pygame.transform.scale(pygame.image.load(os.path.join("game_assets","menu.png")),(120,70))
upgrade_btn = pygame.transform.scale(pygame.image.load(os.path.join("game_assets","upgrade.png")),(50,50))

tower_imgs1 = []
archer_imgs1 = []

# load archer tower and archer images
for x in range(7,10):
    tower_imgs1.append(pygame.transform.scale(pygame.image.load(os.path.join("game_assets/archer_towers/archer_1",str(x)+".png")),(90,90)))

for x in range(38,44):
    archer_imgs1.append(pygame.image.load(os.path.join("game_assets/archer_towers/archer_top",str(x)+".png")))

class ArcherTowerLong(Tower):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.tower_imgs = tower_imgs1
        # copy the list for animation
        self.archer_imgs = archer_imgs1[:]
        self.archer_count = 0
        self.range = 200
        self.original_range = self.range
        self.inRange = False
        self.left=True
        self.damage=1
        self.original_damage=self.damage
        self.width=self.height=90
        self.moving=False
        self.name="archer"
        self.menu=Menu(self,self.x,self.y,menu_bg,[2000,5000,"MAX"])
        self.menu.add_btn(upgrade_btn,"Upgrade")

    def get_upgrade_cost(self):
        """
        get the cost for upgrading a tower
        :return: int
        """
        return self.menu.get_item_cost()

    def draw(self,win):
        """
        draw arher tower and animated archer (archer_count)
        :param win: surface
        :return: None
        """
        super().draw_radius(win)
        super().draw(win)
        if self.inRange and not self.moving:
            self.archer_count += 1
            if self.archer_count>=len(self.archer_imgs)*10:
                self.archer_count=0
        else:
            self.archer_count = 0

        archer = self.archer_imgs[self.archer_count//10]
        if self.left == True:
            add = -25
        else:
            add=-archer.get_width()+10
        win.blit(archer,(self.x+add,self.y-archer.get_height()-25))


    def attack(self,enemies):
        """
        attack enemies in the list and modify the list
        :param enemies: list
        :return: int (money)
        """
        money = 0
        self.inRange=False
        enemy_closest=[]
        for enemy in enemies:
            x,y=enemy.x,enemy.y
            dis=math.sqrt((self.x-x-enemy.img.get_width()/2)**2+(self.y-enemy.img.get_width()/2-y)**2)
            if dis<self.range:
                self.inRange=True
                enemy_closest.append(enemy)

        enemy_closest.sort(key=lambda x:x.path_pos)
        enemy_closest=enemy_closest[::-1]

        if len(enemy_closest)>0:
            first_enemy = enemy_closest[0]
            # hits enemy when the archer shows in the last animation
            if self.archer_count == 50:
                if first_enemy.hit(self.damage):
                    money = first_enemy.money*2
                    enemies.remove(first_enemy)
            if first_enemy.x>self.x and not self.left:
                self.left = True
                for x,img in enumerate(self.archer_imgs):
                    self.archer_imgs[x]=pygame.transform.flip(img,True,False)
            elif self.left and first_enemy.x<self.x:
                self.left = False
                for x,img in enumerate(self.archer_imgs):
                    self.archer_imgs[x]=pygame.transform.flip(img,True,False)

        return money

tower_imgs2=[]
archer_imgs2=[]
# load archer tower and archer images
for x in range(10,13):
    tower_imgs2.append(pygame.transform.scale(pygame.image.load(os.path.join("game_assets/archer_towers/archer_2",str(x)+".png")),(90,90)))

for x in range(51,57):
    archer_imgs2.append(pygame.image.load(os.path.join("game_assets/archer_towers/archer_top_2",str(x)+".png")))

class ArcherTowerShort(ArcherTowerLong):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.tower_imgs2=tower_imgs2
        # copy the list for animation
        self.archer_imgs=archer_imgs2[:]
        self.archer_count = 0
        self.range = 120
        self.original_range=self.range
        self.inRange=False
        self.left=True
        self.damage=2
        self.original_damage=self.damage
        self.menu=Menu(self,self.x,self.y,menu_bg,[2500,5500,"MAX"])
        self.menu.add_btn(upgrade_btn,"Upgrade")
        self.name="archer2"
