import pygame
from DrawMap import MAP
from Obstacle import Obstacle
import numpy as np
import random

class Character:
    def __init__(self, character_type, map, windows):
        self.character_type = character_type
        self.map_data = map.get_map_data()
        self.row = 0
        self.col = 0
        self.tile_size = map.tile_size
        self.win = windows
        self.move_delay = 1000
        self.last_move_time = 0
        self.visible_cells = None
        self.obstacle = None
        self.move_data = []
        self.has_append_move = False
        self.color = None
        
    def set_position(self):
        for i, row in enumerate(self.map_data):
            for j, col in enumerate(row):
                if col == str(self.character_type):
                    self.row = i
                    self.col = j
                    return
                
    def reset_map_data(self):
        for i, row in enumerate(self.map_data):
            for j, col in enumerate(row):
                if col == '4' or col == '3' or col == '2':
                    self.map_data[i][j] = '0'

        if self.obstacle is not None or self.can_pick_obstacle():
            for i in range(self.obstacle.top, self.obstacle.down + 1):
                for j in range(self.obstacle.left, self.obstacle.right + 1):
                    self.map_data[i][j] = '4'
                
    def move_left(self):
        current_time = pygame.time.get_ticks()
        if self.col > 0:
            if current_time - self.last_move_time > self.move_delay:
                if self.map_data[self.row][self.col - 1] == '0' or self.map_data[self.row][self.col - 1] == '3' or self.map_data[self.row][self.col - 1] == '2':
                    self.col -= 1

  
    def move_right(self):
        current_time = pygame.time.get_ticks()
        if self.col < len(self.map_data[0]) - 1:
            if current_time - self.last_move_time > self.move_delay:
                if self.map_data[self.row][self.col + 1] == '0' or self.map_data[self.row][self.col + 1] == '3' or self.map_data[self.row][self.col + 1] == '2':
                    self.col += 1

                
    def move_up(self):
        current_time = pygame.time.get_ticks()
        if self.row > 0:
            if current_time - self.last_move_time > self.move_delay:
                if self.map_data[self.row - 1][self.col] == '0' or self.map_data[self.row - 1][self.col] == '3' or self.map_data[self.row - 1][self.col] == '2':
                    self.row -= 1
    
    def move_down(self):
        current_time = pygame.time.get_ticks()
        if self.row < len(self.map_data) - 1:
            if current_time - self.last_move_time > self.move_delay:
                if self.map_data[self.row + 1][self.col] == '0' or self.map_data[self.row + 1][self.col]== '3' or self.map_data[self.row + 1][self.col] == '2':
                    self.row += 1

    def move_up_left(self):
        if self.row > 0 and self.col > 0:
            color = self.win.get_at(((self.col - 1) * self.tile_size, (self.row - 1) * self.tile_size))
            if color == (133, 151, 153, 255):
                self.row -= 1
                self.col -= 1
    
    def move_up_right(self):
        if self.row > 0 and self.col < len(self.map_data[0]) - 1:
            color = self.win.get_at(((self.col + 1) * self.tile_size, (self.row - 1) * self.tile_size))
            if color == (133, 151, 153, 255):
                self.row -= 1
                self.col += 1
                
    def move_down_left(self):
        if self.row < len(self.map_data) - 1 and self.col > 0:
            color = self.win.get_at(((self.col - 1) * self.tile_size, (self.row + 1) * self.tile_size))
            if color == (133, 151, 153, 255):
                self.row += 1
                self.col -= 1
                
    def move_down_right(self):
        if self.row < len(self.map_data) - 1 and self.col < len(self.map_data[0]) - 1:
            color = self.win.get_at(((self.col + 1) * self.tile_size, (self.row + 1) * self.tile_size))
            if color == (133, 151, 153, 255):
                self.row += 1
                self.col += 1
    
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
        elif key[pygame.K_e]:
            current_key = 'up_right'
        elif key[pygame.K_q]:
            current_key = 'up_left'
        elif key[pygame.K_z]:
            current_key = 'down_left'
        elif key[pygame.K_c]:
            current_key = 'down_right'
            
        if current_key is not None and (pygame.time.get_ticks() - self.last_move_time) > self.move_delay:
            if key[pygame.K_UP]:
                self.move_up()
            elif key[pygame.K_DOWN]:
                self.move_down()
            elif key[pygame.K_LEFT]:
                self.move_left()
            elif key[pygame.K_RIGHT]:
                self.move_right()
            elif key[pygame.K_e]:
                self.move_up_right()
            elif key[pygame.K_q]:
                self.move_up_left()
            elif key[pygame.K_z]:
                self.move_down_left()
            elif key[pygame.K_c]:
                self.move_down_right()
            self.last_move_time = pygame.time.get_ticks()

    def random_move(self):
        if len(self.move_data) != 0 and self.has_append_move == True:
            return self.move_data[0]
        list = ['Up', 'Down', 'Left', 'Right']
        for i in range(0, 20):
            self.move_data.append(random.choice(list))
        self.has_append_move = True
        return self.move_data[0]


    def can_pick_obstacle(self):
        for direction in [(0, -1), (-1, 0), (0, 1), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            row = self.row + direction[0]
            col = self.col + direction[1]
            if row >= 0 and row < len(self.map_data) and col >= 0 and col < len(self.map_data[0]):
                color = self.win.get_at((col * self.tile_size, row * self.tile_size))
                if color == (255, 255, 0, 255):
                    return True
        return False

    def set_obstacle(self, obstacle):
        if self.can_pick_obstacle():
            self.obstacle = obstacle
            obstacle.character_color = self.color

    def remove_obstacle(self):
        if self.obstacle is not None:
            self.obstacle.character_color = None
            self.obstacle = None

    def move_obstacle(self):
        if (pygame.time.get_ticks() - self.last_move_time) > self.move_delay / 2:
            key = pygame.key.get_pressed()
            if key[pygame.K_UP]:
                if self.row == 0 or self.map_data[self.row - 1][self.col] == '1':
                    return
                self.obstacle.move_up()
                self.reset_map_data()
                self.move_up()
            elif key[pygame.K_DOWN]:
                if self.row == len(self.map_data) - 1 or self.map_data[self.row + 1][self.col] == '1':
                    return
                self.obstacle.move_down()
                self.reset_map_data()
                self.move_down()
            elif key[pygame.K_LEFT]:
                if self.col == 0 or self.map_data[self.row][self.col - 1] == '1':
                    return
                self.obstacle.move_left()
                self.reset_map_data()
                self.move_left()
            elif key[pygame.K_RIGHT]:
                if self.col == len(self.map_data[0]) - 1 or self.map_data[self.row][self.col + 1] == '1':
                    return
                self.obstacle.move_right()
                self.reset_map_data()
                self.move_right()
            
            self.last_move_time = pygame.time.get_ticks()
    
    def character_vision(self, vision_range):
        grid_size = len(self.map_data)
        self.visible_cells = np.zeros((grid_size, grid_size), dtype=bool)

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
                        self.visible_cells[new_x, new_y] = True
                        pygame.draw.rect(self.win,(248, 145, 150), (new_y * self.tile_size, new_x * self.tile_size, self.tile_size, self.tile_size))

        self.visible_cells[x, y] = False

        return self.visible_cells
    
    def has_line_of_sight(self, start, end):
        points = self.bresenham(start, end)
        for point in points:
            x, y = point
            color = self.win.get_at((y * self.tile_size, x * self.tile_size))
            if color == (252, 250, 245, 255):  # If the point is a wall, return False
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
        for x in range(dx):
            result.append(np.array([x0 + x * xx + y * yx, y0 + x * xy + y * yy], dtype=np.uint8))

            if D >= 0:
                y += 1
                D -= 2*dx
            D += 2*dy 
        return np.array(result, dtype=np.uint8)

class Seeker(Character):
    def __init__(self, map, windows):
        super().__init__(3, map, windows)
        self.score = 0
        self.hider_position = []
        self.move_count = 0
    
    def found_hider(self, hider):
        if self.row == hider.row and self.col == hider.col:
            self.score += 20
            return True
        return False
    
    def move_up(self):
        super().move_up()
        self.score -= 1
        self.move_count += 1
        
    def move_down(self):
        super().move_down()
        self.score -= 1
        self.move_count += 1
    
    def move_left(self):
        super().move_left()
        self.score -= 1
        self.move_count += 1

    def move_right(self):
        super().move_right()
        self.score -= 1
        self.move_count += 1

    def move_up_left(self):
        super().move_up_left()
        self.score -= 1
        self.move_count += 1
   
    def move_up_right(self):
        super().move_up_right()
        self.score -= 1
        self.move_count += 1
    
    def move_down_left(self):
        super().move_down_left()
        self.score -= 1
        self.move_count += 1
    
    def move_down_right(self):
        super().move_down_right()
        self.score -= 1
        self.move_count += 1
     
    def get_hider_postion(self, hider_position):
        self.hider_position.clear()
        self.hider_position.append(hider_position)
        
class Hider(Character):
    def __init__(self, map, windows):
        super().__init__(2, map, windows)
    
    def move(self):
        pass
    
    def annouce_location(self, unit_range):
        grid_size = len(self.map_data)
        
        left_limit = max(0, self.row - unit_range)
        right_limit = min(grid_size, self.row + unit_range + 1)
        top_limit = max(0, self.col - unit_range)
        bottom_limit = min(grid_size, self.col + unit_range + 1)

        randomList = []
        
        for i in range (left_limit, right_limit):
            for j in range(top_limit, bottom_limit):
                randomList.append((i, j))
        
        return random.choice(randomList)
                
        
