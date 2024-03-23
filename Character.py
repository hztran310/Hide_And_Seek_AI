import pygame
from DrawMap import MAP

class Character:
    def __init__(self, character_type, map):
        self.character_type = character_type
        self.map_data = map.get_map_data()
        self.row = 0
        self.col = 0
        self.tile_size = map.tile_size
        self.last_key = None
        self.last_move_time = 0
        self.move_delay = 200

    def set_position(self):
        for i, row in enumerate(self.map_data):
            for j, col in enumerate(row):
                if col == str(self.character_type):
                    self.row = i
                    self.col = j
                    return
    

    def move(self, map_data):
        key = pygame.key.get_pressed()
        current_key = None

        if key[pygame.K_UP]:
            current_key = pygame.K_UP
        elif key[pygame.K_DOWN]:
            current_key = pygame.K_DOWN
        elif key[pygame.K_LEFT]:
            current_key = pygame.K_LEFT
        elif key[pygame.K_RIGHT]:
            current_key = pygame.K_RIGHT
        
        # if current_key != self.last_key and current_key is not None:
        if current_key is not None and (pygame.time.get_ticks() - self.last_move_time) > self.move_delay:
            if key[pygame.K_UP]:
                if self.row > 0 and self.map_data[self.row - 1][self.col] != '1':
                    self.row -= 1
                    map_data[self.row + 1][self.col] = '0'
            elif key[pygame.K_DOWN]:
                if self.row < len(self.map_data) - 1 and self.map_data[self.row + 1][self.col] != '1':
                    self.row += 1
                    map_data[self.row - 1][self.col] = '0'
            elif key[pygame.K_LEFT]:
                if self.col > 0 and self.map_data[self.row][self.col - 1] != '1':
                    self.col -= 1
                    map_data[self.row][self.col + 1] = '0'
            elif key[pygame.K_RIGHT]:
                if self.col < len(self.map_data[0]) - 1 and self.map_data[self.row][self.col + 1] != '1':
                    self.col += 1
                    map_data[self.row][self.col - 1] = '0'
            self.last_move_time = pygame.time.get_ticks()
        return map_data