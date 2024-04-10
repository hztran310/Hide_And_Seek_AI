import pygame
from DrawMap import MAP
from setting import *

class Obstacle:
    def __init__(self, top, left, down, right, map, windows):
        self.top = top
        self.left = left
        self.down = down
        self.right = right
        self.tile_size = map.tile_size
        self.win = windows
        self.map_data = map.get_map_data()
        self.move_delay = 200
        self.last_move_time = 0
        self.character_color = None

    def draw(self):
        top = self.top * self.tile_size
        left = self.left * self.tile_size
        down = (self.down + 1) * self.tile_size
        right = (self.right + 1) * self.tile_size

        for y in range(top, down, self.tile_size):
            for x in range(left, right, self.tile_size):
                pygame.draw.rect(self.win, COLOR_OBS, (x, y, self.tile_size, self.tile_size))

    def get_obstacle(self, position):
        row, col = position
        if row >= self.top and row <= self.down and col >= self.left and col <= self.right:
            return self
        else:
            return None
    
    def remove_draw(self):
        top = self.top * self.tile_size
        left = self.left * self.tile_size
        down = (self.down + 1) * self.tile_size
        right = (self.right + 1) * self.tile_size

        for y in range(top, down, self.tile_size):
            for x in range(left, right, self.tile_size):
                pygame.draw.rect(self.win, COLOR_FLOOR, (x, y, self.tile_size, self.tile_size))

    def is_legal_move(self, x, y):
        color = self.win.get_at((x,y))
        if color == (COLOR_WALL[0], COLOR_WALL[1], COLOR_WALL[2], 255):
            return False
        elif color == (COLOR_FLOOR[0], COLOR_FLOOR[1], COLOR_FLOOR[2], 255) or color == (COLOR_VIEW[0], COLOR_VIEW[1], COLOR_VIEW[2], 255) or color == (COLOR_ANNOUNCE[0], COLOR_ANNOUNCE[1], COLOR_ANNOUNCE[2], 255):
            return True
        elif color != (self.character_color[0], self.character_color[1], self.character_color[2], 255):
            return False
        return True
                
    def move_up(self):
        up = (self.top - 1) * self.tile_size
        left = self.left * self.tile_size
        right = (self.right + 1) * self.tile_size
        if self.top - 1 >= 0:
            for x in range(left, right, self.tile_size):
                if self.is_legal_move(x, up):
                    continue
                else:
                    return
            self.top -= 1
            self.down -= 1


    def move_down(self):
        down = (self.down + 1) * self.tile_size
        left = self.left * self.tile_size
        right = (self.right + 1) * self.tile_size
        if self.down < len(self.map_data) - 1:
            for x in range(left, right, self.tile_size):
                if self.is_legal_move(x, down):
                    continue
                else:
                    return
            self.top += 1
            self.down += 1

    def move_left(self):
        top = self.top * self.tile_size
        left = (self.left - 1) * self.tile_size
        if self.left - 1>= 0:
            for y in range(top, (self.down + 1) * self.tile_size, self.tile_size):
                if self.is_legal_move(left, y):
                    continue
                else:
                    return
            self.left -= 1
            self.right -= 1

    def move_right(self):
        top = self.top * self.tile_size
        right = (self.right + 1) * self.tile_size
        if self.right < len(self.map_data[0]) - 1:
            for y in range(top, (self.down + 1) * self.tile_size, self.tile_size):
                if self.is_legal_move(right, y):
                    continue
                else:
                    return
            self.left += 1
            self.right += 1
    
    