import pygame
from DrawMap import MAP
from Character import Seeker, Hider
from setting import *
import random
from Obstacle import Obstacle
from Button import ImageButton

#Create button instance
start_button = ImageButton(start_img, 680, 250)
exit_button = ImageButton(exit_img, 680, 350)

def run_level3():
    # Initialize Pygame
    pygame.init()

    # Create the display window
    pygame.display.set_caption('Hide & Seek')
    
    game_started = False
    game_over = False
    
    # Create the map
    m = MAP('Map/map2.txt', win)
    
    num_hiders = 2
    
    # Create the characters
    seeker = Seeker(m, win)
    seeker.color = COLOR_SEEKER
    # Many hiders
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

    may_be_hider = [[-1, -1], [-1, -1]]
    
    tmp_num_hiders = num_hiders
    
    current_update = False

    def distance(p1, p2):
        len_p2 = len(seeker.find_path((seeker.row, seeker.col), (p2[0], p2[1])))
        len_p1 = len(seeker.find_path((seeker.row, seeker.col), (p1[0], p1[1])))
        return min(len_p1, len_p2)
    
    current = 0

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
                if current == 0:
                    if seeker.hider_location is None:
                        closest_distance = float('inf') 
                        closest_location = None  
                        for cell_list in may_be_hider:
                            if cell_list != [-1, -1]:
                                for cell in cell_list:
                                    dist = distance((seeker.row, seeker.col), cell)  
                                    if dist < closest_distance:  
                                        closest_distance = dist
                                        closest_location = cell  
                        if closest_location is not None:  
                            seeker.set_target_location(closest_location)
                else:
                    hider = hiders[current - 1]
                    if hider.target_location is None:
                        target = hider.find_farthest_location((hider.row, hider.col))
                        hider.set_target_location(target)
            
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

        if current == 0:
            seeker.check_target_location_is_walkable()
        else:
            hider = hiders[current - 1]
            hider.check_target_location_is_walkable()
        
        if game_started == True:
            if current == 0:
                if seeker.target_location is not None:
                    seeker.move_towards_target(announce)
                    current_update = True
                    pygame.time.wait(1000)
                else:
                    seeker.random_move()
                    pygame.time.wait(200)
            else:
                hider = hiders[current - 1]
                if hider.announce_location_position is not None:
                    if hider.target_location is not None:
                        hider.move_towards_target()
                        current_update = True
                        pygame.time.wait(200)
                            
        if current == 0:
            seeker.character_vision(3)
            if seeker.visible_cells is not None:
                for cell in seeker.visible_cells:
                    for hider in hiders:
                        if hider.row == cell[0] and hider.col == cell[1]:
                            seeker.target_location = None
                            seeker.set_target_location((hider.row, hider.col))
                            seeker.hider_location = (hider.row, hider.col)
                        else:
                            for cell_list in may_be_hider:
                                if cell in cell_list:
                                    cell_list.remove(cell)
        else:
            hider = hiders[current - 1]
            hider.character_vision(2)
            if hider.visible_cells is not None:
                for cell in hider.visible_cells:
                    if seeker.row == cell[0] and seeker.col == cell[1]:
                        hider.target_location = None
                        target = hider.find_farthest_location((seeker.row, seeker.col))
                        hider.set_target_location(target)
                        
        for hider in hiders:
            pygame.draw.rect(win, COLOR_HIDER, (hider.col * m.tile_size, hider.row * m.tile_size, m.tile_size, m.tile_size))
                        
        pygame.draw.rect(win, COLOR_SEEKER, (seeker.col * m.tile_size, seeker.row * m.tile_size, m.tile_size, m.tile_size))

        SCORE_TEXT = SCORE_FONT.render(f'Score: {seeker.score}', True, (0, 0, 0))  # Create a text surface with the score
        win.blit(SCORE_TEXT, [0,0])   
        
        # Update the display
        pygame.display.update()
        
        if current == 0:
            if seeker.found_hider(hiders, tmp_num_hiders, announce):
                seeker.hider_location = None
                for cell_list in may_be_hider:
                    for cell in cell_list:
                        if cell == (seeker.row, seeker.col):
                            may_be_hider.remove(cell_list)

                tmp_num_hiders -= 1
                win.fill(COLOR_FLOOR, pygame.Rect(0, 0, SCORE_TEXT.get_width(), SCORE_TEXT.get_height()))  # Fill the area with white color
                pygame.display.update()
                SCORE_TEXT = SCORE_FONT.render(f'Score: {seeker.score}', True, (0, 0, 0))  # Create a text surface with the score
                win.blit(SCORE_TEXT, [0,0])
                if tmp_num_hiders == 0:
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
                                run_level3()
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
            hider_check = 0
            random_move = random.choice(list)
            for hider in hiders:
                cell_list = []
                temp = hider.announce_location(3)
                for i in range(temp[0] - 3, temp[0] + 4):
                    for j in range(temp[1] - 3, temp[1] + 4):
                        if i >= 0 and i < len(seeker.map_data) and j >= 0 and j < len(seeker.map_data[0]) and seeker.map_data[i][j] != '1' and seeker.map_data[i][j] != '4':
                            cell_list.append((i, j))

                if may_be_hider[hider_check] == [-1, -1]:
                    may_be_hider[hider_check] = cell_list
                else:
                    may_be_hider[hider_check] = [cell for cell in may_be_hider[hider_check] if cell in cell_list]
                hider_check += 1
                announce.append(temp)
                hider.announce_location_position.append(temp)
            seeker.move_count = 0
        
        if current_update == True:
            if current == len(hiders):
                current = 0
            else:
                current += 1
            current_update = False

        SCORE_TEXT = SCORE_FONT.render(f'Score: {seeker.score}', True, (0, 0, 0))  # Create a text surface with the score
        win.blit(SCORE_TEXT, [0,0])   
        
        # Update the display
        pygame.display.update()
            
    return back_to_main_menu
