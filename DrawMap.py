import pygame
import os
from setting import *

class MAP:
    def __init__(self,filename, windows):
        self.player = None
        self.map_data = []
        self.obstacles = list()
        # with open(filename, 'r') as file:
        with open(os.path.normpath(filename), 'r') as file: # Windows: open(filename, 'r'), to work on macOS
            rows, cols = map(int, file.readline().split()) 
            for _ in range(rows):
                self.map_data.append(list(file.readline().strip()))
            for line in file:
                for number in line.split():
                    self.obstacles.append(int(number))
        self.win = windows
        self.tile_size = min(self.win.get_width() // cols, self.win.get_height() // rows)

    def get_map_data(self):
        return self.map_data
    
    def get_obstacles(self):
        return self.obstacles

    def draw(self):
        for i, row in enumerate(self.map_data):
            for j, col in enumerate(row):
                if col == '0' or col == '2' or col == '3':
                    pygame.draw.rect(self.win, COLOR_FLOOR, (j*self.tile_size, i*self.tile_size, self.tile_size, self.tile_size))
                else:
                    pygame.draw.rect(self.win, COLOR_WALL, (j*self.tile_size, i*self.tile_size, self.tile_size, self.tile_size))

                    
    

    
