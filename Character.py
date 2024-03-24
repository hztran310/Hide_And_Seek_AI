import pygame
from DrawMap import MAP
import numpy as np

class Character:
    def __init__(self, character_type, map, windows):
        self.character_type = character_type
        self.map_data = map.get_map_data()
        self.row = 0
        self.col = 0
        self.tile_size = map.tile_size
        self.win = windows
        self.move_delay = 90
        self.last_move_time = 0
        
    def set_position(self):
        for i, row in enumerate(self.map_data):
            for j, col in enumerate(row):
                if col == str(self.character_type):
                    self.row = i
                    self.col = j
                    return
    
    def move(self):
        key = pygame.key.get_pressed()
        current_key = None
        
        if key[pygame.K_UP]:
            current_key = 'up'
        elif key[pygame.K_DOWN]:
            current_key = 'down'
        elif key[pygame.K_LEFT]:
            current_key = 'left'
        elif key[pygame.K_RIGHT]:
            current_key = 'right'
            
        if current_key is not None and (pygame.time.get_ticks() - self.last_move_time) > self.move_delay:
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
            self.last_move_time = pygame.time.get_ticks()
    
    def character_vision(self, vision_range):
        grid_size = len(self.map_data)
        visible_cells = np.zeros((grid_size, grid_size), dtype=bool)

        x, y = self.row, self.col

        left_limit = max(0, x - vision_range)
        right_limit = min(grid_size, x + vision_range + 1)
        top_limit = max(0, y - vision_range)
        bottom_limit = min(grid_size, y + vision_range + 1)

        for new_x in range(left_limit, right_limit):
            for new_y in range(top_limit, bottom_limit):
                color = self.win.get_at((new_y * self.tile_size, new_x * self.tile_size))
                if not (new_x == x and new_y == y) and color != (252, 250, 245, 255) and color != (255, 255, 0, 255):
                    if self.has_line_of_sight((x, y), (new_x, new_y)):
                        visible_cells[new_x, new_y] = True
                        pygame.draw.rect(self.win,(248, 145, 150), (new_y * self.tile_size, new_x * self.tile_size, self.tile_size, self.tile_size))

        visible_cells[x, y] = False

        return visible_cells
    
    def has_line_of_sight(self, start, end):
        points = self.bresenham(start, end)
        for point in points:
            x, y = point
            color = self.win.get_at((y * self.tile_size, x * self.tile_size))
            if color == (252, 250, 245, 255) or color == (255, 255, 0,255):  # If the point is a wall, return False
                return False
        return True
    
    def bresenham(self, p1, p2):
        x0, y0 = p1
        x1, y1 = p2
        dx = x1 - x0
        dy = y1 - y0

        xsign = 1 if dx > 0 else -1
        ysign = 1 if dy > 0 else -1

        dx = abs(dx)
        dy = abs(dy)

        if dx > dy:
            xx, xy, yx, yy = xsign, 0, 0, ysign
        else:
            dx, dy = dy, dx
            xx, xy, yx, yy = 0, ysign, xsign, 0

        D = 2*dy - dx
        y = 0
        result = []
        for x in range(dx + 1):
            
            result.append(np.array([x0 + x * xx + y * yx, y0 + x * xy + y * yy], dtype=np.uint8))

            if D >= 0:
                y += 1
                D -= 2*dx
            D += 2*dy 
        return np.array(result, dtype=np.uint8)


        
                            
                    

        


        
        
                    
                
