import pygame
from DrawMap import MAP
from Obstacle import Obstacle
import numpy as np
import random
from queue import PriorityQueue
from setting import *
import math

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
        self.obstacles = []
        self.obstacle = None
        self.has_append_move = False
        self.color = None
        
    def set_position(self):
        for i, row in enumerate(self.map_data):
            for j, col in enumerate(row):
                if col == str(self.character_type):
                    self.row = i
                    self.col = j
                    # return
    
    def get_initial_position(self):
        for i, row in enumerate(self.map_data):
            for j, col in enumerate(row):
                if col == str(self.character_type):
                    self.row = i
                    self.col = j
                    break
                
    def reset_map_data(self):
        for i, row in enumerate(self.map_data):
            for j, col in enumerate(row):
                if col == '3' or col == '2' or col == '4':
                    self.map_data[i][j] = '0'

        if self.obstacles is not None:
            for obstacle in self.obstacles:
                for i in range(obstacle.top, obstacle.down + 1):
                    for j in range(obstacle.left, obstacle.right + 1):
                        self.map_data[i][j] = '4'
                

    def is_valid_move(self, position):
        row, col = position
        if row >= 0 and row < len(self.map_data) and col >= 0 and col < len(self.map_data[0]):
            return self.map_data[row][col] == '0' or self.map_data[row][col] == '3' or self.map_data[row][col] == '2'
        return False
                
    def move_left(self):
        if self.is_valid_move((self.row, self.col - 1)):
            self.col -= 1
            return True
        return False

    def move_right(self):
        if self.is_valid_move((self.row, self.col + 1)):
            self.col += 1
            return True
        return False
                
    def move_up(self):
        if self.is_valid_move((self.row - 1, self.col)):
            self.row -= 1
            return True
        return False
    
    def move_down(self):
        if self.is_valid_move((self.row + 1, self.col)):
            self.row += 1
            return True
        return False

    def move_up_left(self):
        if self.is_valid_move((self.row - 1, self.col - 1)):
            self.row -= 1
            self.col -= 1
            return True
        return False
    
    def move_up_right(self):
        if self.is_valid_move((self.row - 1, self.col + 1)):
            self.row -= 1
            self.col += 1
            return True
        return False
                
    def move_down_left(self):
        if self.is_valid_move((self.row + 1, self.col - 1)):
            self.row += 1
            self.col -= 1
            return True
        return False
                
    def move_down_right(self):
        if self.is_valid_move((self.row + 1, self.col + 1)):
            self.row += 1
            self.col += 1
            return True
        return False

    def random_move(self):
        random_list = ['Up', 'Down', 'Left', 'Right', 'Down_Left', 'Down_Right', 'Up_Left', 'Up_Right']
        move = random.choice(random_list)
        if move == 'Up':
            if self.is_valid_move((self.row - 1, self.col)):
                self.move_up()
        elif move == 'Down':
            if self.is_valid_move((self.row + 1, self.col)):
                self.move_down()
        elif move == 'Left':
            if self.is_valid_move((self.row, self.col - 1)):
                self.move_left()
        elif move == 'Right':
            if self.is_valid_move((self.row, self.col + 1)):
                self.move_right()
        elif move == 'Down_Left':
            if self.is_valid_move((self.row + 1, self.col - 1)):
                self.move_down_left()
        elif move == 'Down_Right':
            if self.is_valid_move((self.row + 1, self.col + 1)):
                self.move_down_right()
        elif move == 'Up_Left':
            if self.is_valid_move((self.row - 1, self.col - 1)):
                self.move_up_left()
        elif move == 'Up_Right':
            if self.is_valid_move((self.row - 1, self.col + 1)):
                self.move_up_right()

    def can_pick_obstacle(self):
        for direction in [(0, -1), (-1, 0), (0, 1), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            row = self.row + direction[0]
            col = self.col + direction[1]
            if row >= 0 and row < len(self.map_data) and col >= 0 and col < len(self.map_data[0]):
                color = self.win.get_at((col * self.tile_size, row * self.tile_size))
                if color == (COLOR_OBS[0], COLOR_OBS[1], COLOR_OBS[2], 255):
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
        if (pygame.time.get_ticks() - self.last_move_time) > self.move_delay:
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
        self.visible_cells = []

        x, y = self.row, self.col

        left_limit = max(0, x - vision_range)
        right_limit = min(grid_size, x + vision_range + 1)
        top_limit = max(0, y - vision_range)
        bottom_limit = min(grid_size, y + vision_range + 1)

        for new_x in range(left_limit, right_limit):
            for new_y in range(top_limit, bottom_limit):
                color = self.win.get_at((new_y * self.tile_size, new_x * self.tile_size))
                if not (new_x == x and new_y == y) and color != (COLOR_WALL[0], COLOR_WALL[1], COLOR_WALL[2], 255) and color != (COLOR_OBS[0], COLOR_OBS[1], COLOR_OBS[2], 255) and color != (COLOR_HIDER[0], COLOR_HIDER[1], COLOR_HIDER[2], 255) and color != (COLOR_SEEKER[0], COLOR_SEEKER[1], COLOR_SEEKER[2], 255):
                    if self.has_line_of_sight((x, y), (new_x, new_y)):
                        self.visible_cells.append((new_x, new_y))

        return self.visible_cells
    
    def draw_character_vision(self):
        if self.visible_cells is not None:
            for cell in self.visible_cells:
                pygame.draw.rect(self.win, COLOR_VIEW, (cell[1] * self.tile_size, cell[0] * self.tile_size, self.tile_size, self.tile_size))
    
    def has_line_of_sight(self, start, end):
        points = self.bresenham(start, end)
        for point in points:
            x, y = point
            color = self.win.get_at((y * self.tile_size, x * self.tile_size))
            if color == (COLOR_WALL[0], COLOR_WALL[1], COLOR_WALL[2], 255) or color == (COLOR_HIDER[0], COLOR_HIDER[1], COLOR_HIDER[2], 255) or color == (COLOR_SEEKER[0], COLOR_SEEKER[1], COLOR_SEEKER[2], 255) or color == (COLOR_OBS[0], COLOR_OBS[1], COLOR_OBS[2], 255):  # If the point is a wall, return False
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
    
    def set_target_location(self, positions):
        self.target_location = positions
        
    def neighbors(self, node):
        # This function returns the neighbors of a node in an 8-connected grid.
        dirs = [(0, -1), (-1, 0), (0, 1), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        result = []
        for dir in dirs:
            new_node = (node[0] + dir[0], node[1] + dir[1])
            if (new_node[0] >= 0 and new_node[0] < len(self.map_data) and
                new_node[1] >= 0 and new_node[1] < len(self.map_data[0]) and
                self.map_data[new_node[0]][new_node[1]] != '1' and self.map_data[new_node[0]][new_node[1]] != '4' and self.map_data[new_node[0]][new_node[1]] != '3'):  # Skip if the node is a wall
                result.append(new_node)
        return result
    
    def cost(self, current, next):
        return 1
    
    def move_to_neighbor(self, neighbor):
        if self.row - 1 == neighbor[0] and self.col == neighbor[1]:
            return 'Up'
        elif self.row + 1 == neighbor[0] and self.col == neighbor[1]:
            return 'Down'
        elif self.row == neighbor[0] and self.col - 1 == neighbor[1]:
            return 'Left'
        elif self.row == neighbor[0] and self.col + 1 == neighbor[1]:
            return 'Right'
        elif self.row - 1 == neighbor[0] and self.col - 1 == neighbor[1]:
            return 'Up_Left'
        elif self.row - 1 == neighbor[0] and self.col + 1 == neighbor[1]:
            return 'Up_Right'
        elif self.row + 1 == neighbor[0] and self.col + 1 == neighbor[1]:
            return 'Down_Right'
        elif self.row + 1 == neighbor[0] and self.col - 1 == neighbor[1]:
            return 'Down_Left'
    
    def heuristic(self, cell1, cell2):
        x1, y1 = cell1
        x2, y2 = cell2
        return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    
    def find_path(self, start, goal):
        open_set = set()
        closed_set = set()
        came_from = {}

        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}

        open_set.add(start)

        while open_set:
            current = min(open_set, key=lambda node: f_score[node])

            if current == goal:
                return self.reconstruct_path(came_from, goal)

            open_set.remove(current)
            closed_set.add(current)

            for neighbor in self.neighbors(current):
                tentative_g_score = g_score[current] + self.cost(current, neighbor)

                if neighbor in closed_set and tentative_g_score >= g_score.get(neighbor, float('inf')):
                    continue

                if neighbor not in open_set or tentative_g_score < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)

                    if neighbor not in open_set:
                        open_set.add(neighbor)

        return None
    
    def reconstruct_path(self, came_from, goal):
        current = goal
        path = []
        while current is not None:
            path.append(current)
            if current in came_from:
                current = came_from[current]
            else:
                break
        return path[::-1]
    
    def check_target_location_is_walkable(self):
        if self.target_location is not None:
            if (0 <= self.target_location[0] < len(self.map_data) and 
                0 <= self.target_location[1] < len(self.map_data[self.target_location[0]]) and 
                (self.map_data[self.target_location[0]][self.target_location[1]] == '1' or 
                 self.map_data[self.target_location[0]][self.target_location[1]] == '4')):
                self.target_location = None
    
class Seeker(Character):
    def __init__(self, map, windows):
        super().__init__(3, map, windows)
        self.score = 0
        self.hider_position = []
        self.move_count = 0
        self.target_location = None
        self.hider_location = None
    
    def found_hider(self, hiders, num_hiders, announces):
        for i in range(num_hiders):
            if self.row == hiders[i].row and self.col == hiders[i].col:
                self.score += 20
                for hider_announce in hiders[i].announce_location_position:
                    if hider_announce in announces:
                        announces.remove(hider_announce)
                hiders.pop(i)
                return True
        return False
    
    def move_up(self):
        if super().move_up():
            self.score -= 1
            self.move_count += 1
        
    def move_down(self):
        if super().move_down():
            self.score -= 1
            self.move_count += 1
    
    def move_left(self):
        if super().move_left():
            self.score -= 1
            self.move_count += 1

    def move_right(self):
        if super().move_right():
            self.score -= 1
            self.move_count += 1

    def move_up_left(self):
        if super().move_up_left():
            self.score -= 1
            self.move_count += 1
   
    def move_up_right(self):
        if super().move_up_right():
            self.score -= 1
            self.move_count += 1
    
    def move_down_left(self):
        if super().move_down_left():
            self.score -= 1
            self.move_count += 1
    
    def move_down_right(self):
        if super().move_down_right():
            self.score -= 1
            self.move_count += 1
     
    def move_towards_target(self, announce):
        if self.target_location is not None:
            # Use the A* algorithm to find the shortest path to the target
            path = self.find_path((self.row, self.col), self.target_location)
            # If a path was found, move to the next cell in the path
            if path:
                next_cell = path[0]
                if (next_cell[0] == self.row and next_cell[1] == self.col):
                    path.pop(0)
                    if path:
                        next_cell = path[0]
                direction = self.move_to_neighbor(next_cell)

                # Call the appropriate movement method based on the direction
                if direction == 'Up':
                    self.move_up()
                elif direction == 'Down':
                    self.move_down()
                elif direction == 'Left':
                    self.move_left()
                elif direction == 'Right':
                    self.move_right()
                elif direction == 'Up_Left':
                    self.move_up_left()
                elif direction == 'Up_Right':
                    self.move_up_right()
                elif direction == 'Down_Left':
                    self.move_down_left()
                elif direction == 'Down_Right':
                    self.move_down_right()
            
            if self.row == self.target_location[0] and self.col == self.target_location[1]:
                if self.target_location in announce:
                    announce.remove(self.target_location)
                self.target_location = None

        
class Hider(Character):
    def __init__(self, map, windows):
        super().__init__(2, map, windows)
        self.initial_hider_position = []
        self.announce_location_position = []
        self.is_announcing = False
        self.target_location = None
        self.new_announce = False
        self.previous_path = []
        self.seeker_location = None
    
    def set_position(self, initial_hider_position):
        for i, row in enumerate(self.map_data):
            for j, col in enumerate(row):
                if col == str(self.character_type):
                    if (i, j) not in initial_hider_position:
                        self.row = i
                        self.col = j
                        return

    def announce_location(self, unit_range):
        grid_size = len(self.map_data)
        
        left_limit = max(0, self.row - unit_range)
        right_limit = min(grid_size, self.row + unit_range + 1)
        top_limit = max(0, self.col - unit_range)
        bottom_limit = min(grid_size, self.col + unit_range + 1)

        randomList = []
        
        for i in range (left_limit, right_limit):
            for j in range(top_limit, bottom_limit):
                if (i == self.row and j == self.col) or (self.map_data[i][j] == '1' or self.map_data[i][j] == '4'):
                    continue
                randomList.append((i, j))
        announce_pos = random.choice(randomList)
        pygame.draw.rect(self.win, COLOR_ANNOUNCE, (announce_pos[1] * self.tile_size, announce_pos[0] * self.tile_size, self.tile_size, self.tile_size))        
        return announce_pos
    
    def distance(self, p1, p2):
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
    
    def find_farthest_location(self):
        max_distance = float('-inf')
        farthest_location = None

        # Define the search area
        start_row = max(0, self.row - 10)
        end_row = min(len(self.map_data), self.row + 10)
        start_col = max(0, self.col - 10)
        end_col = min(len(self.map_data[0]), self.col + 10)

        for i in range(start_row, end_row):
            for j in range(start_col, end_col):
                if self.map_data[i][j] == '1' or self.map_data[i][j] == '4':
                    continue
                distance = self.distance((i, j), self.announce_location_position)
                if distance > max_distance:
                    max_distance = distance
                    farthest_location = (i, j)

        # If no farthest location was found within the search area, wrap around the map
        if farthest_location is None:
            for i in range(start_row, end_row):
                for j in range(start_col, end_col):
                    # Calculate the new positions by wrapping around the map
                    new_i = (i + len(self.map_data)) % len(self.map_data)
                    new_j = (j + len(self.map_data[0])) % len(self.map_data[0])
                    if self.map_data[new_i][new_j] == '1' or self.map_data[new_i][new_j] == '4':
                        continue
                    distance = self.distance((new_i, new_j), self.announce_location_position)
                    if distance > max_distance:
                        max_distance = distance
                        farthest_location = (new_i, new_j)

        return farthest_location


    def heuristic(self, current, goal, seeker_position):
        return self.distance(current, goal) - self.distance(current, seeker_position)
                
    def find_path(self, start, goal):
        row, col = goal
        if self.map_data[row][col] == '1' or self.map_data[row][col] == '4':
            start_row = max(0, row - 3)
            end_row = min(len(self.map_data), row + 3)
            start_col = max(0, col - 3)
            end_col = min(len(self.map_data[0]), col + 3)
            for i in range(start_row, end_row):
                for j in range(start_col, end_col):
                    if self.map_data[i][j] == '0':
                        goal = (i, j)
                        break
                
        open_set = set()
        closed_set = set()
        came_from = {}

        g_score = {start: 0}
        if self.seeker_location is not None:
            f_score = {start: self.heuristic(start, goal, self.seeker_location)}
        else:
            f_score = {start: self.heuristic(start, goal, (self.row, self.col))}

        open_set.add(start)

        while open_set:
            current = min(open_set, key=lambda node: f_score[node])

            if current == goal:
                return self.reconstruct_path(came_from, goal)

            open_set.remove(current)
            closed_set.add(current)

            for neighbor in self.neighbors(current):
                tentative_g_score = g_score[current] + self.cost(current, neighbor)

                if neighbor in self.previous_path:
                    tentative_g_score += 1000  # Adjust the penalty value as needed

                if neighbor in closed_set and tentative_g_score >= g_score.get(neighbor, float('inf')):
                    continue

                if neighbor not in open_set or tentative_g_score < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    if self.seeker_location is not None:
                        f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal, self.seeker_location)
                    else:
                        f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal, (self.row, self.col))

                    if neighbor not in open_set:
                        open_set.add(neighbor)

        return None
    
    def move_towards_target(self):
        if self.target_location is not None:
            # Use the A* algorithm to find the shortest path to the target
            path = self.find_path((self.row, self.col), self.target_location)
            
            full_path = path.copy()

            # If a path was found, move to the next cell in the path
            if path:
                next_cell = path[0]
                if (next_cell[0] == self.row and next_cell[1] == self.col):
                    path.pop(0)
                    if path:
                        next_cell = path[0]
                direction = self.move_to_neighbor(next_cell)

                # Call the appropriate movement method based on the direction
                if direction == 'Up':
                    self.move_up()
                elif direction == 'Down':
                    self.move_down()
                elif direction == 'Left':
                    self.move_left()
                elif direction == 'Right':
                    self.move_right()
                elif direction == 'Up_Left':
                    self.move_up_left()
                elif direction == 'Up_Right':
                    self.move_up_right()
                elif direction == 'Down_Left':
                    self.move_down_left()
                elif direction == 'Down_Right':
                    self.move_down_right()
            
            if self.row == self.target_location[0] and self.col == self.target_location[1]:
                self.previous_path = full_path
                self.target_location = None
    
    def minimax(self, depth, alpha, beta, maximizingPlayer, seeker_row, seeker_col):
        if depth == 0 or self.is_terminal_state():
            return self.utility(seeker_row, seeker_col), (self.row, self.col)

        if maximizingPlayer:
            maxEval = float('-inf')
            best_move = None
            for child in self.get_children():
                eval, move = self.minimax(depth - 1, alpha, beta, False, child[0], child[1])
                if eval > maxEval:
                    maxEval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return maxEval, best_move
        else:
            minEval = float('inf')
            best_move = None
            for child in self.get_children():
                eval, move = self.minimax(depth - 1, alpha, beta, True, child[0], child[1])
                if eval < minEval:
                    minEval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return minEval, best_move
    
    def is_terminal_state(self):
        return self.target_location is None or self.target_location == (self.row, self.col)
    
    def utility(self, seeker_row, seeker_col):
        return self.heuristic((self.row, self.col), (seeker_row, seeker_col), (seeker_row, seeker_col))
    
    def get_children(self):
        children = []
        for neighbor in self.neighbors((self.row, self.col)):
            children.append(neighbor)
        return children
     
    def move_when_saw_seeker(self, seeker_row, seeker_col):
        _, best_move = self.minimax(5, float('-inf'), float('inf'), True, seeker_row, seeker_col)
        if best_move == (self.row, self.col):
            possible_moves = self.get_children()
            if (self.row, self.col) in possible_moves:  # check if the current position is in the list
                possible_moves.remove((self.row, self.col))  # remove the current position
            if possible_moves:  # check if there are other moves available
                # Choose the move that is farthest from the seeker
                best_move = max(possible_moves, key=lambda move: self.distance(move, (seeker_row, seeker_col)))
        return best_move