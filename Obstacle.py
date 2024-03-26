import pygame
from DrawMap import MAP

class Obstacle:
    def __init__(self, top, left, down, right, map, windows):
        self.top = top
        self.left = left
        self.down = down
        self.right = right
        self.tile_size = map.tile_size
        self.win = windows
        self.map_data = map.get_map_data()

    def reset_map_data(self):
        for i, row in enumerate(self.map_data):
            for j, col in enumerate(row):
                if col == '4' or col == '3' or col == '2':
                    self.map_data[i][j] = '0'

        if self.obstacle is not None:
            for i in range(self.obstacle.top, self.obstacle.down + 1):
                for j in range(self.obstacle.left, self.obstacle.right + 1):
                    self.map_data[i][j] = '4'

    def draw(self):
        top = self.top * self.tile_size
        left = self.left * self.tile_size
        down = (self.down + 1) * self.tile_size
        right = (self.right + 1) * self.tile_size

        for y in range(top, down, self.tile_size):
            for x in range(left, right, self.tile_size):
                pygame.draw.rect(self.win, (255, 255, 0), (x, y, self.tile_size, self.tile_size))


    def move_up(self):
        up = (self.top - 1) * self.tile_size
        left = self.left * self.tile_size
        right = (self.right + 1) * self.tile_size
        if self.top - 1>= 0:
            for x in range(left, right, self.tile_size):
                color = self.win.get_at((x, up))
                if color == (252, 250, 245, 255) or color == (255, 0, 0, 255) or color == (0, 0, 255, 255):  
                    return
            self.top -= 1
            self.down -= 1

    def move_down(self):
        down = (self.down + 1) * self.tile_size
        left = self.left * self.tile_size
        right = (self.right + 1) * self.tile_size
        if self.down < len(self.map_data) - 1:
            for x in range(left, right, self.tile_size):
                color = self.win.get_at((x, down))
                if color == (252, 250, 245, 255) or color == (255, 0, 0, 255) or color == (0, 0, 255, 255):  
                    return
            self.top += 1
            self.down += 1

    def move_left(self):
        top = self.top * self.tile_size
        left = (self.left - 1) * self.tile_size
        right = self.right * self.tile_size
        if self.left - 1>= 0:
            for y in range(top, (self.down + 1) * self.tile_size, self.tile_size):
                color = self.win.get_at((left, y))
                if color == (252, 250, 245, 255) or color == (255, 0, 0, 255) or color == (0, 0, 255, 255):
                    return
            self.left -= 1
            self.right -= 1

    def move_right(self):
        top = self.top * self.tile_size
        right = (self.right) * self.tile_size
        down = (self.down) * self.tile_size
        if self.right < len(self.map_data[0]) - 1:
            for y in range(top, down, self.tile_size):
                color = self.win.get_at((right, y))
                if color == (252, 250, 245, 255) or color == (255, 0, 0, 255) or color == (0, 0, 255, 255):  
                    return
            self.left += 1
            self.right += 1