import pygame
import heapq

pygame.init()

WIDTH, HEIGHT = 800, 640
FPS = 60

win = pygame.display.set_mode((WIDTH, HEIGHT))


COLOR_HIDER = (0, 0, 255)
COLOR_SEEKER = (255, 0, 0)
COLOR_WALL = (252, 250, 245)
COLOR_VIEW = (248, 145, 150)
COLOR_FLOOR = (133, 151, 153)
COLOR_OBS = (255, 255, 0)
COLOR_WINDOW = (50, 133, 168)
COLOR_ANNOUNCE = (157, 194, 242)
COLOR_BUTTON = (152, 66, 245)

FONT = pygame.font.Font(None, 36)  # Create a font object
TEXT_HIDER_FOUND = FONT.render('Hider found!', True, (0, 0, 0))  # Create a text surface
TEXT_HIDER_FOUND_REC = TEXT_HIDER_FOUND.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # Get the rectangle around the text and center it

SCORE_FONT = pygame.font.SysFont("commicsansms", 25)  # Create a font object for the score

GAME_OVER_TEXT = FONT.render('Last Hider Found! Game Over!', True, (0, 0, 0))  # Create a text surface
GAME_OVER_REC = GAME_OVER_TEXT.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # Get the rectangle around the text and center it


