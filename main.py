from Level1 import run_level1
from Level2 import run_level2
from setting import *
from Button import Button

def main_menu():
    # Initialize Pygame
    pygame.init()
    # Set up the display    
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    # Set up the clock
    clock = pygame.time.Clock()
    # Set up the font
    font = pygame.font.SysFont('comicsans', 60)
    # Set up the buttons
    level1_button = Button((255, 0, 0), 50, 50, 200, 100, 'Level 1')
    level2_button = Button((0, 255, 0), 50, 200, 200, 100, 'Level 2')
    # Set up the loop
    run = True
    while run:
        clock.tick(FPS)
        win.fill(COLOR_WINDOW)
        level1_button.draw(win)
        level2_button.draw(win)
        pygame.display.update()
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if level1_button.isOver(pos):
                    run_level1()
                if level2_button.isOver(pos):
                    run_level2()

    pygame.quit()


main_menu()
