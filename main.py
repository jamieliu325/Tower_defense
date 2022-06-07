import pygame

if __name__=="__main__":
    # initialize all imported pygame modules
    pygame.init()
    from main_menu import MainMenu
    # create a window
    mainMenu=MainMenu()
    mainMenu.run()


