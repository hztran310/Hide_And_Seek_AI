import pygame
from DrawMap import MAP
from Character import Character, Seeker
from setting import *
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
hider = Character(2, m, win)

# Set the initial positions of the characters
seeker.set_position()
hider.set_position()

running = True
clock = pygame.time.Clock()
list_obstacles = m.get_obstacles()
obstacles = []
for i in range(0, len(list_obstacles), 4):
    obs = Obstacle(list_obstacles[i], list_obstacles[i+1], list_obstacles[i+2], list_obstacles[i+3], m, win)
    obstacles.append(obs)

while running:
    clock.tick(FPS)
    m.draw()
    
    for obs in obstacles:
        obs.draw()
        if seeker.can_pick_obstacle():
            key = pygame.key.get_pressed()
            if key[pygame.K_g]:
                seeker.set_obstacle(obs)
            elif key[pygame.K_h]:
                seeker.remove_obstacle()
        else:
            seeker.remove_obstacle()
    
    # Move the seeker
    if seeker.obstacle is None:
        seeker.move()
    else:
        seeker.move_obstacle()

    seeker.character_vision(3)

    pygame.draw.rect(win, (255, 0, 0), (seeker.col * m.tile_size, seeker.row * m.tile_size, m.tile_size, m.tile_size))
    pygame.draw.rect(win, (0, 0, 255), (hider.col * m.tile_size, hider.row * m.tile_size, m.tile_size, m.tile_size))
    

    
    SCORE_TEXT = SCORE_FONT.render(f'Score: {seeker.score}', True, (0, 0, 0))  # Create a text surface with the score
    win.blit(SCORE_TEXT, [0,0])    

    # Update the display
    pygame.display.update()
    
    if seeker.found_hider(hider):
        win.fill((133, 151, 153), pygame.Rect(0, 0, SCORE_TEXT.get_width(), SCORE_TEXT.get_height()))  # Fill the area with white color
        pygame.display.update()
        SCORE_TEXT = SCORE_FONT.render(f'Score: {seeker.score}', True, (0, 0, 0))  # Create a text surface with the score
        win.blit(SCORE_TEXT, [0,0])
        win.blit(TEXT_HIDER_FOUND, TEXT_REC.topleft)  # Draw the text at the calculated position
        pygame.display.update()
        pygame.time.wait(3000)  # Wait for 3 seconds
        break

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


pygame.quit()