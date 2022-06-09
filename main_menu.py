import pygame
import os
from game import Game

# load start button and logo
start_btn = pygame.image.load(os.path.join("game_assets","button_play.png"))
logo = pygame.image.load(os.path.join("game_assets","logo.png"))

class MainMenu:

    def __init__(self,win):
        self.width = 1350
        self.height = 700
        self.bg = pygame.image.load(os.path.join("game_assets","bg.png"))
        self.bg = pygame.transform.scale(self.bg,(self.width,self.height))
        self.win=win
        self.btn = (self.width/2 - start_btn.get_width()/2, 350, start_btn.get_width(),start_btn.get_height())

    def run(self):
        run = True

        while run:
            for event in pygame.event.get():
                # check if game is quit
                if event.type == pygame.QUIT:
                    run = False
                # check if mouse hits play button when mouse is released
                if event.type == pygame.MOUSEBUTTONUP:
                    # the position where mouse hits
                    x,y=pygame.mouse.get_pos()
                    if self.btn[0]<=x<=self.btn[0]+self.btn[2]:
                        if self.btn[1]<=y<=self.btn[1]+self.btn[3]:
                            game = Game(self.win)
                            game.run()
                            del game
            self.draw()

        pygame.quit()

    # draw background map, logo, and start button on the window
    def draw(self):
        self.win.blit(self.bg,(0,0))
        self.win.blit(logo,(self.width/2-logo.get_width(),0))
        self.win.blit(start_btn,(self.btn[0],self.btn[1]))
        pygame.display.update()

