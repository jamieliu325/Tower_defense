import pygame

if __name__=="__main__":
    # initialize all imported pygame modules
    pygame.init()
    # create a window
    win = pygame.display.set_mode((1350, 700))
    # import and run MainMenu
    from main_menu import MainMenu
    mainMenu=MainMenu(win)
    mainMenu.run()


