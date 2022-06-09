import pygame

if __name__=="__main__":
    # initialize all imported pygame modules
    pygame.init()
    win = pygame.display.set_mode((1350, 700))
    from main_menu import MainMenu
    # create a window
    mainMenu=MainMenu(win)
    mainMenu.run()


