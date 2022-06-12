import pygame
import os

pygame.init()

star = pygame.transform.scale(pygame.image.load(os.path.join("game_assets","star.png")),(50,50))
star2 = pygame.transform.scale(pygame.image.load(os.path.join("game_assets","star.png")),(20,20))

class Button:
    """
    button on the top of tower for update
    menu.x and menu.y is the center of the selected tower
    """
    def __init__(self,menu,img,name):
        self.name = name
        self.img = img
        self.menu = menu
        self.x = menu.x - 50
        self.y = menu.y - 110
        self.width = self.img.get_width()
        self.height = self.img.get_height()

    def click(self,X,Y):
        """
        if clicks on the button
        :param X: int
        :param Y: int
        :return: bool
        """
        if self.x<=X<=self.x+self.width:
            if self.y<=Y<=self.y+self.height:
                return True
        return False

    def draw(self,win):
        """
        draw the buttons
        :param win: surface
        :return: None
        """
        win.blit(self.img,(self.x,self.y))

    def update(self):
        """
        update the button position
        :return: None
        """
        self.x = self.menu.x - 50
        self.y = self.menu.y - 110


class PlayPauseButton(Button):

    def __init__(self,play_img,pause_img,x,y):
        self.img = play_img
        self.play = play_img
        self.pause = pause_img
        self.x = x
        self.y = y
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.paused = True

    def draw(self,win):
        """
        draw play and music button
        :param win: surface
        :return: None
        """
        if self.paused:
            win.blit(self.play,(self.x,self.y))
        else:
            win.blit(self.pause,(self.x,self.y))

class VerticalButton(Button):

    def __init__(self, x, y, img, name, cost):
        self.name = name
        self.img = img
        self.x = x
        self.y = y
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.cost = cost


class Menu:
    """
    menu on the top of the tower
    x and y s the center of the tower
    """
    def __init__(self, tower, x, y, img, item_cost):
        self.x = x
        self.y = y
        self.width = img.get_width()
        self.height = img.get_height()
        self.item_cost = item_cost
        self.buttons = []
        self.items = 0
        self.bg = img
        self.tower = tower
        self.font = pygame.font.SysFont("comiscans", 25)

    def add_btn(self, img, name):
        """
        add buttons to menu
        :param img: surface
        :param name: str
        :return: None
        """
        self.items += 1
        self.buttons.append(Button(self, img, name))

    def get_item_cost(self):
        """
        get costs for upgrading tower
        :return: int
        """
        return self.item_cost[self.tower.level - 1]

    def draw(self, win):
        """
        draw buttons and menu bg
        :param win: surface
        :return: None
        """
        win.blit(self.bg, (self.x - self.bg.get_width() / 2, self.y - 120))
        for item in self.buttons:
            item.draw(win)
            win.blit(star, (item.x + item.width + 5, item.y - 9))
            text = self.font.render(str(self.item_cost[self.tower.level - 1]), 1, (255, 255, 255))
            win.blit(text, (item.x + item.width + 30 - text.get_width() / 2, item.y + star.get_height() - 8))

    def get_clicked(self, X, Y):
        """
        return the name of clicked button from the menu
        :param X: int
        :param Y: int
        :return: str
        """
        for btn in self.buttons:
            if btn.click(X, Y):
                return btn.name
        return None

    def update(self):
        """
        update menu and button position
        :return: None
        """
        for btn in self.buttons:
            btn.update()


class VerticalMenu(Menu):
    """
    vertical menu on the side
    """

    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.width = img.get_width()
        self.height = img.get_height()
        self.buttons = []
        self.items = 0
        self.bg = img
        self.font = pygame.font.SysFont("comiscans", 25)

    def add_btn(self, img, name, cost):
        """
        add buttons to the side menu
        :param img: surface
        :param name: str
        :param cost: int
        :return: None
        """
        self.items += 1
        btn_x = self.x + 25
        btn_y = self.y + 25 + (self.items - 1) * 120
        self.buttons.append(VerticalButton(btn_x, btn_y, img, name, cost))

    def get_item_cost(self, name):
        """
        get cost of item
        :param name: str
        :return: int
        """
        for btn in self.buttons:
            if btn.name == name:
                return btn.cost


    def draw(self, win):
        """
        draw buttons and menu bg
        :param win: surface
        :return: None
        """
        win.blit(self.bg, (self.x, self.y))
        for item in self.buttons:
            item.draw(win)
            win.blit(star2, (item.x + 2, item.y + item.height))
            text = self.font.render(str(item.cost), 1, (255, 255, 255))
            win.blit(text, (item.x + item.width / 2 - text.get_width() / 2 + 7, item.y + item.height + 5))