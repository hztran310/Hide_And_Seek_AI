import pygame
from DrawMap import MAP

class Character:
    def __init__(self, character_type, map):
        self.character_type = character_type
        self.map_data = map.get_map_data()
        self.row = 0
        self.col = 0
        self.tile_size = map.tile_size

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
            if self.row > 0 and self.map_data[self.row - 1][self.col] != '1':
                self.row -= 1
        elif key[pygame.K_DOWN]:
            if self.row < len(self.map_data) - 1 and self.map_data[self.row + 1][self.col] != '1':
                self.row += 1
        elif key[pygame.K_LEFT]:
            if self.col > 0 and self.map_data[self.row][self.col - 1] != '1':
                self.col -= 1
        elif key[pygame.K_RIGHT]:
            if self.col < len(self.map_data[0]) - 1 and self.map_data[self.row][self.col + 1] != '1':
                self.col += 1