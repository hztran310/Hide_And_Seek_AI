import pygame
from DrawMap import MAP

class Character:
    def __init__(self, character_type, map, windows):
        self.character_type = character_type
        self.map_data = map.get_map_data()
        self.row = 0
        self.col = 0
        self.tile_size = map.tile_size
        self.win = windows

    def set_position(self):
        for i, row in enumerate(self.map_data):
            for j, col in enumerate(row):
                if col == str(self.character_type):
                    self.row = i
                    self.col = j
                    return
    

    def move(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_UP]:
            if self.row > 0:
                color = self.win.get_at((self.col * self.tile_size, (self.row - 1) * self.tile_size))
                if color == (133, 151, 153, 255):
                    self.row -= 1
        elif key[pygame.K_DOWN]:
            if self.row < len(self.map_data) - 1:
                color = self.win.get_at((self.col * self.tile_size, (self.row + 1) * self.tile_size))
                if color == (133, 151, 153, 255):
                    self.row += 1
        elif key[pygame.K_LEFT]:
            if self.col > 0:
                color = self.win.get_at(((self.col - 1) * self.tile_size, self.row * self.tile_size))
                if color == (133, 151, 153, 255):
                    self.col -= 1
        elif key[pygame.K_RIGHT]:
            if self.col < len(self.map_data[0]) - 1:
                color = self.win.get_at(((self.col + 1) * self.tile_size, self.row * self.tile_size))
                if color == (133, 151, 153, 255):
                    self.col += 1