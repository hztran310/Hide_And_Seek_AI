import pygame
from DrawMap import MAP
from Character import Seeker, Hider
from setting import *
import random
from Obstacle import Obstacle
from Button import ImageButton
import os
import copy

#Create button instance
start_button = ImageButton(start_img, 680, 250)
exit_button = ImageButton(exit_img, 680, 350)

def run_level4():
    # Initialize Pygame
    pygame.init()

    # Create the display window
    pygame.display.set_caption('Hide & Seek')
    
    game_started = False
    game_over = False
    
    # Create the map
    m = MAP('Map/Map0.txt', win)
    seeker_map_data = copy.deepcopy(m.map_data)
    hider_map_data = copy.deepcopy(m.map_data)
    
    num_hiders = 0
    
    with open(os.path.normpath('Map/Map0.txt'), 'r') as file:
        rows, cols = map(int, file.readline().split()) 
        for i in range(rows):
            line = file.readline().strip()
            for j in range(cols):
                if line[j] == '2':
                    num_hiders += 1
    
    # Create the characters
    seeker = Seeker(m, win)
    seeker.color = COLOR_SEEKER
    seeker.map_data = seeker_map_data
    # Many hiders
    hiders = [Hider(m, win) for i in range(num_hiders)]
    for hider in hiders:
        hider.map_data = hider_map_data
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
    
    tmp_num_hiders = num_hiders
    
    current_update = False

    def distance(cell1, cell2):
        return abs(cell1[0] - cell2[0]) + abs(cell1[1] - cell2[1])
    
    current = 0
    
    new_announcement = False
    
    has_announce = False

    pre_start = True

    for hider in hiders:
        hider.time_limit = 100

    seeker.reset_map_data()
    
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
            # Handle button click event throughout the game loop
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if exit_button.isOver(pos):
                    running = False
                    back_to_main_menu = True
        
        for obs in obstacles:
            obs.draw()
            
            for hider in hiders:
                hider.obstacles.append(obs)

        for hider in hiders:
            hider.reset_map_data()

        if seeker.can_pick_obstacle() and seeker.obstacle is None:
            for obs in obstacles:
                for direction in [(0, -1), (-1, 0), (0, 1), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                    row = seeker.row + direction[0]
                    col = seeker.col + direction[1]
                    if obs.get_obstacle((row, col)) is not None:
                        seeker.obstacles.append(obs)
                        seeker.set_obstacle(obs)
                        seeker.reset_map_data()
                        break

        if announce is not None and not pre_start:
            if current == 0:
                if seeker.obstacle is not None:
                    if seeker.previous_move is not None:
                        if seeker.previous_move == 'Up':
                            seeker.move_obstacle('Down')
                        elif seeker.previous_move == 'Down':
                            seeker.move_obstacle('Up')
                        elif seeker.previous_move == 'Left':
                            seeker.move_obstacle('Right')
                        elif seeker.previous_move == 'Right':
                            seeker.move_obstacle('Left')
                        seeker.previous_move = None
                        seeker.remove_obstacle()
                else:
                    if (seeker.target_location is not None and new_announcement == True) or seeker.hider_location is None or seeker.target_location is None:
                        closest_distance = float('inf') 
                        closest_location = None  
                        for cell in announce:
                            if distance((seeker.row, seeker.col), cell) < closest_distance:
                                closest_distance = distance((seeker.row, seeker.col), cell)
                                closest_location = cell
                        if closest_location is not None:
                            seeker.set_target_location(closest_location)
                        new_announcement = False                    
            else:
                hider = hiders[current - 1]
                if hider.target_location is None:
                    target = hider.find_farthest_location((hider.row, hider.col))
                    hider.set_target_location(target)
        

        if game_started == True:
            if pre_start:
                hider = hiders[current]
                if not hider.can_pick_obstacle() and hider.obstacle is None:
                    hider.go_to_obstacle()
                    hider.move_towards_target()
                elif hider.can_pick_obstacle():
                    for direction in [(0, -1), (-1, 0), (0, 1), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                        row = hider.row + direction[0]
                        col = hider.col + direction[1]
                        for obs in obstacles:
                            if obs.get_obstacle((row, col)) is not None:
                                hider.set_obstacle(obs)
                                break
                    
                    hider.move_obstacle_to_entrance()
                else:
                    hider.remove_obstacle()
                    hider.time_limit = 0

                hider.reset_map_data()

                current += 1
                if current == len(hiders):
                    current = 0
                if all(hider.time_limit == 0 for hider in hiders):
                    pre_start = False
                

            else:
                # Normal game phase: both the hider and seeker can move
                if current == 0:
                    if seeker.target_location is not None:
                        seeker.move_towards_target(announce)
                        current_update = True
                        pygame.time.wait(100)
                    else:
                        seeker.random_move()
                        if has_announce == True:
                            current_update = True
                        pygame.time.wait(100)
                else:
                    hider = hiders[current - 1]
                    if hider.announce_location_position is not None:
                        if hider.target_location is not None:
                            hider.move_towards_target()
                            current_update = True
                            pygame.time.wait(100)
                            
        
        seeker.character_vision(3)            
        seeker.draw_character_vision()
        
        for hider in hiders:
            hider.character_vision(2)
            hider.draw_character_vision()
                                
        for hider in hiders:
            pygame.draw.rect(win, COLOR_HIDER, (hider.col * m.tile_size, hider.row * m.tile_size, m.tile_size, m.tile_size))
            
        pygame.draw.rect(win, COLOR_SEEKER, (seeker.col * m.tile_size, seeker.row * m.tile_size, m.tile_size, m.tile_size))
        
        # Update the display
        pygame.display.update()
        
        if current == 0:
            if seeker.found_hider(hiders, tmp_num_hiders, announce):
                seeker.hider_location = None
                seeker.target_location = None
                tmp_num_hiders -= 1
                win.fill(COLOR_WINDOW, pygame.Rect(680, 0, SCORE_TEXT.get_width(), SCORE_TEXT.get_height()))  # Fill the area with white color
                pygame.display.update()
                SCORE_TEXT = SCORE_FONT.render(f'Score: {seeker.score}', True, (0, 0, 0))  # Create a text surface with the score
                win.blit(SCORE_TEXT, [680,0])
                if tmp_num_hiders == 0:
                    game_over = True
                    win.fill(COLOR_FLOOR, pygame.Rect(0, 0, TEXT_HIDER_FOUND.get_width(), TEXT_HIDER_FOUND.get_height()))  # Fill the area with white color
                    pygame.display.update()
                    SCORE_TEXT = SCORE_FONT.render(f'Score: {seeker.score}', True, (0, 0, 0))  # Create a text surface with the score
                    win.blit(SCORE_TEXT, [680,0])
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
                                run_level4()
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
            has_announce = True
            random_move = random.choice(list)
            announce.clear()
            for hider in hiders:
                temp = hider.announce_location(3)
                announce.append(temp)
                hider.announce_location_position.append(temp)
            new_announcement = True
            seeker.move_count = 0
                    
        if current_update == True:
            if current == len(hiders):
                current = 0
            else:
                current += 1
            current_update = False

        SCORE_TEXT = SCORE_FONT.render(f'Score: {seeker.score}', True, (0, 0, 0))  # Create a text surface with the score
        win.blit(SCORE_TEXT, [680,0])   
        
        # Update the display
        pygame.display.update()
            
    return back_to_main_menu

