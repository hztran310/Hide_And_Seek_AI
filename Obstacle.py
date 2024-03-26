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
        self.max_row = len(map.get_map_data())
        self.max_col = len(map.get_map_data()[0])

    
    def draw(self):
        top = (self.top + 1) * self.tile_size
        left = (self.left + 1) * self.tile_size
        down = self.down * self.tile_size
        right = self.right * self.tile_size

        for y in range(top, down, self.tile_size):
            for x in range(left, right, self.tile_size):
                pygame.draw.rect(self.win, (255, 255, 0), (x, y, self.tile_size, self.tile_size))

    def move_up(self):
        top = (self.top + 1) * self.tile_size
        left = (self.left + 1) * self.tile_size
        right = self.right * self.tile_size
        for x in range(left, right, self.tile_size):
            if self.top > 0:
                color = self.win.get_at((x, top))
                if color != (133, 151, 153, 255):
                    return
                else:
                    self.top -= 1
                    self.down -= 1
                    return

    def move_down(self):
        down = self.down * self.tile_size
        left = (self.left + 1) * self.tile_size
        right = self.right * self.tile_size
        for x in range(left, right, self.tile_size):
            if self.down < self.max_row:
                color = self.win.get_at((x, down))
                if color != (133, 151, 153, 255):
                    return
                else:
                    self.top += 1
                    self.down += 1
                    return

    def move_left(self):
        top = (self.top + 1) * self.tile_size
        left = (self.left + 1) * self.tile_size
        down = self.down * self.tile_size
        for y in range(top, down, self.tile_size):
            if self.left > 0:
                color = self.win.get_at((left, y))
                if color != (133, 151, 153, 255):
                    return
                else:
                    self.left -= 1
                    self.right -= 1
                    return
        
        

    def move_right(self):
        top = (self.top + 1) * self.tile_size
        down = self.down * self.tile_size
        right = self.right * self.tile_size
        for y in range(top, down, self.tile_size):
            if self.right < self.max_col:
                color = self.win.get_at((right, y))
                if color != (133, 151, 153, 255):
                    return
                else:
                    self.left += 1
                    self.right += 1
                    return


    

        