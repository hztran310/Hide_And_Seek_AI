import pygame
from DrawMap import MAP
from Character import Character, Seeker, Hider
from setting import *
import random
from Obstacle import Obstacle
from Button import ImageButton
from Movement import movement

#Create button instance
start_button = ImageButton(start_img, 680, 250)
exit_button = ImageButton(exit_img, 680, 350)

def run_level1():
    filename = 'Map/Map3.txt'
    num_hiders = 1
    back_to_main_menu = movement(num_hiders, filename)
    return back_to_main_menu
