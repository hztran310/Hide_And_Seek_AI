import pygame
from Character import Player

class MAP:
    def __init__(self,filename, windows):
        self.player = None
        self.map_data = []
        self.obstacles = list()
        with open(filename, 'r') as file:
            rows, cols = map(int, file.readline().split()) 
            for _ in range(rows):
                self.map_data.append(list(file.readline().strip()))
            for line in file:
                for number in line.split():
                    self.obstacles.append(int(number))
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

        top = self.obstacles[0] * self.tile_size
        left = self.obstacles[1] * self.tile_size
        down = self.obstacles[2] * self.tile_size
        right = self.obstacles[3] * self.tile_size  
        for top in range (down):
            pygame.draw.rect(self.win, (255, 255, 0), (left, top, self.tile_size, self.tile_size))
        for left in range (right):
            pygame.draw.rect(self.win, (255, 255, 0), (left, top, self.tile_size, self.tile_size))          
