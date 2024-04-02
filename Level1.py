import pygame
from DrawMap import MAP
from Character import Character, Seeker, Hider
from setting import *
import random
import math
from Obstacle import Obstacle
from Button import ImageButton

#Create button instance
start_button = ImageButton(start_img, 680, 250)
exit_button = ImageButton(exit_img, 680, 350)

def run_level1():
    # Initialize Pygame
    pygame.init()

    game_started = False
    game_over = False
    
    # Create the display window
    pygame.display.set_caption('Hide & Seek')

    # Create the map
    m = MAP('Map/Map2.txt', win)

    # Create the characters
    seeker = Seeker(m, win)
    seeker.color = COLOR_SEEKER
    hider = Hider(m, win)
    num_hiders = 1
    hiders = [Hider(m, win) for i in range(num_hiders)]
    for hider in hiders:
        hider.color = COLOR_HIDER
        
    # Set the initial positions of the characters
    seeker.set_position()
    initial_hider_position = []
    for hider in hiders:
        hider.set_position(initial_hider_position)
        initial_hider_position.append((hider.row, hider.col))
        
    running = True
    clock = pygame.time.Clock()

    list = [5, 6, 7, 8, 9, 10]
    random_move = random.choice(list)

    list_obstacles = m.get_obstacles()
    obstacles = []
    for i in range(0, len(list_obstacles), 4):
        obs = Obstacle(list_obstacles[i], list_obstacles[i+1], list_obstacles[i+2], list_obstacles[i+3], m, win)
        obstacles.append(obs)

    announce = []
    
    back_to_main_menu = False

    def distance(p1, p2):
        len_p2 = len(seeker.find_path((seeker.row, seeker.col), (p2[0], p2[1])))
        len_p1 = len(seeker.find_path((seeker.row, seeker.col), (p1[0], p1[1])))
        return min(len_p1, len_p2)
  
    while running:
        clock.tick(FPS)

        win.fill(COLOR_WINDOW)
        
        m.draw()
                        
        start_button.draw(win)
        exit_button.draw(win)

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                pygame.display.quit()
            if event.type == pygame.MOUSEBUTTONDOWN and game_started is False:
                if start_button.isOver(pos):
                    game_started = True
                if exit_button.isOver(pos):
                    running = False
                    back_to_main_menu = True
                
        if game_started == True:
            if announce is not None:
                if seeker.target_location is None:
                    res = None
                    min_distance = math.inf
                    for i in range(len(announce)):
                        if distance((seeker.row, seeker.col), (announce[i][0], announce[i][1])) < min_distance:
                            min_distance = distance((seeker.row, seeker.col), (announce[i][0], announce[i][1]))
                            res = announce[i]
                    if res is not None:
                        seeker.set_target_location(res)
            
        for obs in obstacles:
            obs.draw()
            if seeker.obstacle is None:
                seeker.set_obstacle(obs)
                seeker.reset_map_data()
                seeker.remove_obstacle()
            
            if seeker.can_pick_obstacle():
                key = pygame.key.get_pressed()
                if key[pygame.K_g]:
                    seeker.set_obstacle(obs)
                if key[pygame.K_h]:
                    seeker.remove_obstacle()
            else:
                seeker.remove_obstacle()

        seeker.check_target_location_is_walkable()
        
        if game_started == True:
            if seeker.target_location is not None:
                seeker.move_towards_target(announce)
                pygame.time.wait(200)
            else:
                random_list = ['Up', 'Down', 'Left', 'Right', 'Down_Left', 'Down_Right', 'Up_Left', 'Up_Right']
                seeker_move = random.choice(random_list)
                if seeker_move == 'Up':
                    if seeker.is_valid_move((seeker.row - 1, seeker.col)):
                        seeker.move_up()
                elif seeker_move == 'Down':
                    if seeker.is_valid_move((seeker.row + 1, seeker.col)):
                        seeker.move_down()
                elif seeker_move == 'Left':
                    if seeker.is_valid_move((seeker.row, seeker.col - 1)):
                        seeker.move_left()
                elif seeker_move == 'Right':
                    if seeker.is_valid_move((seeker.row, seeker.col + 1)):
                        seeker.move_right()
                elif seeker_move == 'Down_Left':
                    if seeker.is_valid_move((seeker.row + 1, seeker.col - 1)):
                        seeker.move_down_left()
                elif seeker_move == 'Down_Right':
                    if seeker.is_valid_move((seeker.row + 1, seeker.col + 1)):
                        seeker.move_down_right()
                elif seeker_move == 'Up_Left':
                    if seeker.is_valid_move((seeker.row - 1, seeker.col - 1)):
                        seeker.move_up_left()
                elif seeker_move == 'Up_Right':
                    if seeker.is_valid_move((seeker.row - 1, seeker.col + 1)):
                        seeker.move_up_right()
                pygame.time.wait(200)

        seeker.character_vision(3)
        if seeker.visible_cells is not None:
            for cell in seeker.visible_cells:
                for hider in hiders:
                    if hider.row == cell[0] and hider.col == cell[1]:
                        seeker.target_location = None
                        seeker.set_target_location((hider.row, hider.col))
        
        for hider in hiders:
            pygame.draw.rect(win, COLOR_HIDER, (hider.col * m.tile_size, hider.row * m.tile_size, m.tile_size, m.tile_size))
                        
        pygame.draw.rect(win, COLOR_SEEKER, (seeker.col * m.tile_size, seeker.row * m.tile_size, m.tile_size, m.tile_size))

        SCORE_TEXT = SCORE_FONT.render(f'Score: {seeker.score}', True, (0, 0, 0))  # Create a text surface with the score
        win.blit(SCORE_TEXT, [0,0])   
        
        # Update the display
        pygame.display.update()
        
        if seeker.found_hider(hiders, num_hiders, announce):
            num_hiders -= 1
            win.fill(COLOR_FLOOR, pygame.Rect(0, 0, SCORE_TEXT.get_width(), SCORE_TEXT.get_height()))  # Fill the area with white color
            pygame.display.update()
            SCORE_TEXT = SCORE_FONT.render(f'Score: {seeker.score}', True, (0, 0, 0))  # Create a text surface with the score
            win.blit(SCORE_TEXT, [0,0])
            if num_hiders == 0:
                game_over = True
                win.fill(COLOR_FLOOR, pygame.Rect(0, 0, TEXT_HIDER_FOUND.get_width(), TEXT_HIDER_FOUND.get_height()))  # Fill the area with white color
                pygame.display.update()
                win.blit(GAME_OVER_TEXT, GAME_OVER_REC.topleft)    
                win.blit(RESTART_TEXT, RESTART_REC.topleft)
                pygame.display.update()        
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                            pygame.quit()
                            pygame.display.quit()
                        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and game_over:
                            running = False
                            game_started = False
                            game_over = False
                            run_level1()
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            pos = pygame.mouse.get_pos()
                            if exit_button.isOver(pos):
                                running = False
                                back_to_main_menu = True
                                return back_to_main_menu
                    pygame.display.update()
            else:
                win.blit(TEXT_HIDER_FOUND, TEXT_HIDER_FOUND_REC.topleft)  # Draw the text at the calculated position
                pygame.display.update()
                pygame.time.wait(2000)  # Wait for 3 seconds
            
        if seeker.move_count == random_move:
            random_move = random.choice(list)
            for hider in hiders:
                tmp = hider.announce_location(2)
                announce.append(tmp)
                hider.announce_location_position.append(tmp)
            seeker.move_count = 0


        SCORE_TEXT = SCORE_FONT.render(f'Score: {seeker.score}', True, (0, 0, 0))  # Create a text surface with the score
        win.blit(SCORE_TEXT, [0,0])   
    

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                                
        # Update the display
        pygame.display.update()
        
    return back_to_main_menu


        
    