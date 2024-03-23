import pygame
from DrawMap import MAP
from Character import Character

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 800, 800
FPS = 60

# Create the display window
win = pygame.display.set_mode((WIDTH, HEIGHT))

# Create the map
m = MAP('Map\\Map1.txt', win)

# Create the characters
seeker = Character(3, m)
hider = Character(2, m)

# Set the initial positions of the characters
seeker.set_position()
hider.set_position()

running = True
clock = pygame.time.Clock()
while running:
    clock.tick(FPS)

    # Move the seeker
    seeker.move()

    # Draw the map and the characters
    m.draw()
    pygame.draw.rect(win, (255, 0, 0), (seeker.col * m.tile_size, seeker.row * m.tile_size, m.tile_size, m.tile_size))
    pygame.draw.rect(win, (0, 0, 255), (hider.col * m.tile_size, hider.row * m.tile_size, m.tile_size, m.tile_size))

    # Update the display
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()