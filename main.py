import pygame
from DrawMap import MAP
from Character import Character, Seeker
from setting import *
    
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

while running:
    clock.tick(FPS)
    
    m.draw()
    # Move the seeker
    seeker.move()
    seeker.character_vision(3)
    
    SCORE_TEXT = SCORE_FONT.render(f'Score: {seeker.score}', True, (0, 0, 0))  # Create a text surface with the score
    win.blit(SCORE_TEXT, [0,0])
    
    # Draw the map and the characters
    pygame.draw.rect(win, (255, 0, 0), (seeker.col * m.tile_size, seeker.row * m.tile_size, m.tile_size, m.tile_size))
    pygame.draw.rect(win, (0, 0, 255), (hider.col * m.tile_size, hider.row * m.tile_size, m.tile_size, m.tile_size))

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