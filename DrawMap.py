import pygame
import os

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
                    pygame.draw.rect(self.win, (133, 151, 153), (j*self.tile_size, i*self.tile_size, self.tile_size, self.tile_size))
                else:
                    pygame.draw.rect(self.win, (252, 250, 245), (j*self.tile_size, i*self.tile_size, self.tile_size, self.tile_size))

        # for i in range(0, len(self.obstacles), 4):
        #     top = (self.obstacles[i] + 1) * self.tile_size
        #     left = (self.obstacles[i+1] + 1) * self.tile_size
        #     down = self.obstacles[i+2] * self.tile_size
        #     right = self.obstacles[i+3] * self.tile_size

        #     for y in range(top, down, self.tile_size):
        #         for x in range(left, right, self.tile_size):
        #             pygame.draw.rect(self.win, (255, 255, 0), (x, y, self.tile_size - 2, self.tile_size - 2))
                    
    

    
