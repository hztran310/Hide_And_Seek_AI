import pygame
from Character import Player

class MAP:
    def __init__(self,filename, windows):
        self.player = None
        self.map_data = []
        with open(filename, 'r') as file:
            rows, cols = map(int, file.readline().split()) 
            for line in file:
                self.map_data.append(list(line.strip()))
        self.win = windows
        self.tile_size = min(self.win.get_width() // cols, self.win.get_height() // rows)

    def draw(self):
        for i, row in enumerate(self.map_data):
            for j, col in enumerate(row):
                if col == '0':
                    pygame.draw.rect(self.win, (133, 151, 153), (j*self.tile_size, i*self.tile_size, self.tile_size, self.tile_size))
                elif col == '1':
                    pygame.draw.rect(self.win, (252, 250, 245), (j*self.tile_size, i*self.tile_size, self.tile_size, self.tile_size))
                elif col == '2':
                    pygame.draw.rect(self.win, (0, 0, 255), (j*self.tile_size, i*self.tile_size, self.tile_size, self.tile_size))
                elif col == '3':
                    pygame.draw.rect(self.win, (255, 0, 0), (j*self.tile_size, i*self.tile_size, self.tile_size, self.tile_size))
