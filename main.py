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
num_hiders = 1
hider.color = COLOR_HIDER

# Set the initial positions of the characters
seeker.set_position()
hider.set_position()

running = True
clock = pygame.time.Clock()

list = [5, 6, 7, 8, 9, 10]
random_move = random.choice(list)
list_obstacles = m.get_obstacles()
obstacles = []
for i in range(0, len(list_obstacles), 4):
    obs = Obstacle(list_obstacles[i], list_obstacles[i+1], list_obstacles[i+2], list_obstacles[i+3], m, win)
    obstacles.append(obs)

annouce = None


while running:
    clock.tick(FPS)
    win.fill(COLOR_WINDOW)
    
    m.draw()

    seeker.character_vision(3)
    pygame.draw.rect(win, COLOR_SEEKER, (seeker.col * m.tile_size, seeker.row * m.tile_size, m.tile_size, m.tile_size))
    pygame.draw.rect(win, COLOR_HIDER, (hider.col * m.tile_size, hider.row * m.tile_size, m.tile_size, m.tile_size))
    if annouce is not None:
        pygame.draw.rect(win, COLOR_ANNOUNCE, (annouce[1] * m.tile_size, annouce[0] * m.tile_size, m.tile_size, m.tile_size))
        if seeker.move_data is None:
            seeker.move_data = seeker.find_path(annouce)


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

    # if seeker.obstacle is not None:
    #     if len(seeker.move_data) == 0 and seeker.has_append_move == True:
    #         break
    #     if seeker.move_data[0] == seeker.row and seeker.move_data[1] == seeker.col:
    #         seeker.move_data.pop(0)
    #     seeker_move = seeker.move_to_neighbor(seeker.move_data[0])
    #     print(seeker.move_data[0])
    #     if seeker_move == 'Up':
    #         seeker.move_up()
    #     elif seeker_move == 'Down':
    #         seeker.move_down()
    #     elif seeker_move == 'Left':
    #         seeker.move_left()
    #     elif seeker_move == 'Right':
    #         seeker.move_right()
    #     elif seeker_move == 'Down_Left':
    #         seeker.move_down_left
    #     elif seeker_move == 'Down_Right':
    #         seeker.move_down_right
    #     elif seeker_move == 'Up_Left':
    #         seeker.move_up_left
    #     elif seeker_move == 'Up_Right':
    #         seeker.move_up_right
    #     seeker.character_vision(3)
    #     seeker.move_data.pop(0)
    #     seeker.move()
    # else:
    #     seeker.obstacle.remove_draw()
        # seeker.move_obstacle()
        #seeker.obstacle.draw()
    # else:
    #     seeker.move()


    if seeker.move_data is not None:
        if len(seeker.move_data) == 0 and seeker.has_append_move == True:
            break
        if seeker.move_data[0] == seeker.row and seeker.move_data[1] == seeker.col:
            seeker.move_data.pop(0)
        seeker_move = seeker.move_to_neighbor(seeker.move_data[0])
        if seeker_move == 'Up':
            seeker.move_up()
        elif seeker_move == 'Down':
            seeker.move_down()
        elif seeker_move == 'Left':
            seeker.move_left()
        elif seeker_move == 'Right':
            seeker.move_right()
        elif seeker_move == 'Down_Left':
            seeker.move_down_left()
        elif seeker_move == 'Down_Right':
            seeker.move_down_right()
        elif seeker_move == 'Up_Left':
            seeker.move_up_left()
        elif seeker_move == 'Up_Right':
            seeker.move_up_right()
        #seeker.character_vision(3)
        seeker.move_data.pop(0)
    else:
        random_list = ['Up', 'Down', 'Left', 'Right', 'Down_Left', 'Down_Right', 'Up_Left', 'Up_Right']
        move = random.choice(random_list)
        if move == 'Up':
            seeker.move_up()
        elif move == 'Down':
            seeker.move_down()
        elif move == 'Left':
            seeker.move_left()
        elif move == 'Right':
            seeker.move_right()
        elif move == 'Down_Left':
            seeker.move_down_left()
        elif move == 'Down_Right':
            seeker.move_down_right()
        elif move == 'Up_Left':
            seeker.move_up_left()
        elif move == 'Up_Right':
            seeker.move_up_right()
        #seeker.character_vision(3)



    SCORE_TEXT = SCORE_FONT.render(f'Score: {seeker.score}', True, (0, 0, 0))  # Create a text surface with the score
    win.blit(SCORE_TEXT, [0,0])   

    
    # Update the display
    pygame.display.update()
    
    if seeker.found_hider(hider):
        win.fill(COLOR_FLOOR, pygame.Rect(0, 0, SCORE_TEXT.get_width(), SCORE_TEXT.get_height()))  # Fill the area with white color
        pygame.display.update()
        SCORE_TEXT = SCORE_FONT.render(f'Score: {seeker.score}', True, (0, 0, 0))  # Create a text surface with the score
        win.blit(SCORE_TEXT, [0,0])
        win.blit(TEXT_HIDER_FOUND, TEXT_REC.topleft)  # Draw the text at the calculated position
        pygame.display.update()
        pygame.time.wait(3000)  # Wait for 3 seconds
        break
    
    # if seeker.move_count == random_move:
    #     random_move = random.choice(list)
    #     hider_location = []
    #     for i in range(0, num_hiders):
    #         tmp = hider.annouce_location(2)
    #         hider_location.append(tmp)
    #         ANNOUNCE_LOCATION_TEXT = SCORE_FONT.render(f'Hider {i + 1} is at {tmp}', True, (0, 0, 0))
    #         ANNOUNCE_LOCATION_REC = ANNOUNCE_LOCATION_TEXT.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50 * i))
    #         win.blit(ANNOUNCE_LOCATION_TEXT, ANNOUNCE_LOCATION_REC.topleft)
    #         pygame.display.update()
    #         pygame.time.wait(1000)
    #     seeker.move_count = 0
    #     seeker.get_hider_postion(hider_location)
    #     print(seeker.find_path(hider_location))

    if seeker.move_count == random_move:
        random_move = random.choice(list)
        for i in range(0, num_hiders):
            annouce = hider.annouce_location(2)
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