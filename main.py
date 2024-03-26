import pygame
from DrawMap import MAP
from Character import Character, Seeker
from multiprocessing import Process
from tkinter import Tk, messagebox

def show_message():
    root = Tk()
    root.withdraw()
    messagebox.showinfo("Game Notification", "Hider found!")
    root.destroy()
    
# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 800, 800
FPS = 60

# Create the display window
win = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('Hide & Seek')

# Create the map
m = MAP('Map/Map1.txt', win)

# Create the characters
# seeker = Character(3, m, win)
seeker = Seeker(m, win)
hider = Character(2, m, win)

# Set the initial positions of the characters
seeker.set_position()
hider.set_position()

running = True
clock = pygame.time.Clock()

font = pygame.font.Font(None, 36)  # Create a font object
text = font.render('Hider found!', True, (0, 0, 0))  # Create a text surface
text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # Get the rectangle around the text and center it

while running:
    clock.tick(FPS)
    
    m.draw()
    # Move the seeker
    seeker.move()
    seeker.character_vision(3)
    
    # Draw the map and the characters
    pygame.draw.rect(win, (255, 0, 0), (seeker.col * m.tile_size, seeker.row * m.tile_size, m.tile_size, m.tile_size))
    pygame.draw.rect(win, (0, 0, 255), (hider.col * m.tile_size, hider.row * m.tile_size, m.tile_size, m.tile_size))

    # Update the display
    pygame.display.update()
    
    if seeker.found_hider(hider):
        win.blit(text, text_rect.topleft)  # Draw the text at the calculated position
        pygame.display.update()
        pygame.time.wait(3000)  # Wait for 3 seconds
        break

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()