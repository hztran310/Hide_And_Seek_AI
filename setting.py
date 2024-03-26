import pygame

pygame.init()

WIDTH, HEIGHT = 800, 800
FPS = 60

FONT = pygame.font.Font(None, 36)  # Create a font object
TEXT_HIDER_FOUND = FONT.render('Hider found!', True, (0, 0, 0))  # Create a text surface
TEXT_REC = TEXT_HIDER_FOUND.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # Get the rectangle around the text and center it

SCORE_FONT = pygame.font.SysFont("commicsansms", 25)  # Create a font object for the score
