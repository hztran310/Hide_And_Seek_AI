from Level1 import run_level1
from Level2 import run_level2
from Level3 import run_level3
from setting import *
from Button import Button

def main_menu():
    # Initialize Pygame
    pygame.init()
    pygame.display.set_caption('Hide & Seek')

    
    # Set up the clock
    clock = pygame.time.Clock()
    
    # Set up the font
    font = pygame.font.SysFont('comicsans', 60)
    
    # Set up the buttons
    level1_button = Button((241, 238, 220), 50, 150, 200, 80, 'Level 1')
    level2_button = Button((241, 238, 220), 50, 300, 200, 80, 'Level 2')
    level3_button = Button((241, 238, 220), 50, 450, 200, 80, 'Level 3')
    title = pygame.image.load('image/title.png')
    
    # Set up the loop
    run = True
    back_to_main_menu = False
    while run:
        clock.tick(FPS)
        win.fill(COLOR_WINDOW)
        level1_button.draw(win, index=0, total_buttons=3, gap=10)
        level2_button.draw(win, index=1, total_buttons=3, gap=10)
        level3_button.draw(win, index=2, total_buttons=3, gap=10)
        win.blit(title, (150, 5))
        pygame.display.update()
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if level1_button.isOver(pos):
                    back_to_main_menu = run_level1()
                    if back_to_main_menu == True:
                        continue
                if level2_button.isOver(pos):
                    back_to_main_menu = run_level2()
                    if back_to_main_menu == True:
                        continue
                if level3_button.isOver(pos):
                    back_to_main_menu = run_level3()
                    if back_to_main_menu == True:
                        continue


    pygame.quit()

main_menu()
