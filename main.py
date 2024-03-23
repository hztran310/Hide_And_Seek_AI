import pygame
from DrawMap import MAP
from Character import Player 

# Initialize Pygame
pygame.init()

# Set up some constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Create the window
win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Create the map
m = MAP('Map\Map1.txt', win)

running = True
clock = pygame.time.Clock()
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw the map
    m.draw()

    # Update the display
    pygame.display.flip()

pygame.quit()
