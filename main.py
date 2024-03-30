import pygame
from DrawMap import MAP
from Character import Character, Seeker, Hider
from setting import *
import random

from Obstacle import Obstacle
    
# Initialize Pygame
pygame.init()

# Create the display window
win = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('Hide & Seek')

# Create the map
m = MAP('Map/Map1.txt', win)

# Create the characters
seeker = Seeker(m, win)
seeker.color = COLOR_SEEKER
hider = Hider(m, win)
num_hiders = 2
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
announce_len = -1

while running:
    clock.tick(FPS)
    win.fill(COLOR_WINDOW)
    
    m.draw()

    if announce is not None:
        for i in range(len(announce)):
            pygame.draw.rect(win, COLOR_ANNOUNCE, (announce[i][1] * m.tile_size, announce[i][0] * m.tile_size, m.tile_size, m.tile_size))
        if seeker.target_location is None:
            for i in range(len(announce)):
                if announce[i] in seeker.visited_announce:
                    announce.pop(i)
                    break
            seeker.set_target_location(announce)

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

    if seeker.target_location is not None:
        seeker.move_towards_target()
        pygame.time.wait(1000)
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
        pygame.time.wait(1000)

    seeker.character_vision(3)
    if seeker.visible_cells is not None:
        for cell in seeker.visible_cells:
            for hider in hiders:
                if hider.row == cell[0] and hider.col == cell[1]:
                    seeker.move_data.clear()
                    seeker.set_target_location((hider.row, hider.col))

    pygame.draw.rect(win, COLOR_SEEKER, (seeker.col * m.tile_size, seeker.row * m.tile_size, m.tile_size, m.tile_size))
    
    for hider in hiders:
        pygame.draw.rect(win, COLOR_HIDER, (hider.col * m.tile_size, hider.row * m.tile_size, m.tile_size, m.tile_size))

    if announce is not None:
        for i in range(len(announce)):
            pygame.draw.rect(win, COLOR_ANNOUNCE, (announce[i][1] * m.tile_size, announce[i][0] * m.tile_size, m.tile_size, m.tile_size))

    SCORE_TEXT = SCORE_FONT.render(f'Score: {seeker.score}', True, (0, 0, 0))  # Create a text surface with the score
    win.blit(SCORE_TEXT, [0,0])   
    
    # Update the display
    pygame.display.update()
    
    if seeker.found_hider(hiders, num_hiders):
        num_hiders -= 1
        win.fill(COLOR_FLOOR, pygame.Rect(0, 0, SCORE_TEXT.get_width(), SCORE_TEXT.get_height()))  # Fill the area with white color
        pygame.display.update()
        SCORE_TEXT = SCORE_FONT.render(f'Score: {seeker.score}', True, (0, 0, 0))  # Create a text surface with the score
        win.blit(SCORE_TEXT, [0,0])
        win.blit(TEXT_HIDER_FOUND, TEXT_REC.topleft)  # Draw the text at the calculated position
        pygame.display.update()
        pygame.time.wait(3000)  # Wait for 3 seconds
        if num_hiders == 0:
            break

    if seeker.move_count == random_move:
        random_move = random.choice(list)
        for hider in hiders:
            announce.append(random.choice(hider.announce_location(2)))
        seeker.move_count = 0

    SCORE_TEXT = SCORE_FONT.render(f'Score: {seeker.score}', True, (0, 0, 0))  # Create a text surface with the score
    win.blit(SCORE_TEXT, [0,0])   
    
    
    # Update the display
    pygame.display.update()
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    #pygame.time.delay(1000)  # Adjust the delay time as needed


pygame.quit()