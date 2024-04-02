import pygame
from DrawMap import MAP
from Character import Character, Seeker, Hider
from setting import *
from Button import ImageButton
import os
from Movement import movement

#Create button instance
start_button = ImageButton(start_img, 680, 250)
exit_button = ImageButton(exit_img, 680, 350)

def run_level2():
    filename = 'Map/Map2.txt'
    num_hiders = 0
    with open(os.path.normpath(filename), 'r') as file:
        rows, cols = map(int, file.readline().split()) 
        for i in range(rows):
            line = file.readline().strip()
            for j in range(cols):
                if line[j] == '2':
                    num_hiders += 1
    back_to_main_menu = movement(num_hiders, filename)
    return back_to_main_menu
    