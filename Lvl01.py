import math
import random

from Character import Character, Seeker, Hider

# new_pos is in the center of its range, while old_pos is the top left of the previous finding range
# new_pos = (row, col, limit to the right, limit to down) (Sau khi nhận được annouce, điểm được annouce cần được xác định limit phải, down => Cần có width, length của map)
# old_pos = (row, col, limit to the right, limit to down)
def update_fiding_range(old_pos, new_pos):
    # finding top left of new_pos range
    if new_pos[0] - 3 < 0:
        new_pos[3] = new_pos[3] + new_pos[0]
        new_pos[0] = 0
    else:
        new_pos[0] = new_pos[0] - 3
        new_pos[3] = new_pos[3] + 3

    if new_pos[1] - 3 < 0:
        new_pos[4] = new_pos[4] + new_pos[1]
        new_pos[1] = 0
    else:
        new_pos[1] = new_pos[1] - 3
        new_pos[4] = new_pos[4] + 3
    
    if new_pos[0] < old_pos[0] and old_pos[0] + old_pos[3] >= new_pos[0]:
        old_pos[0] = new_pos[0]
        old_pos[3] = old_pos[0] + old_pos[3] - new_pos[0]
    if new_pos[0] > old_pos[0] and new_pos[3] + new_pos[0] >= old_pos[0]:
        old_pos[3] = new_pos[0] + new_pos[3] - old_pos[0]
    
    if new_pos[1] > old_pos[1] and old_pos[1] + old_pos[4] >= new_pos[1]:
        old_pos[1] = new_pos[1]
        old_pos[4] = old_pos[1] + old_pos[4] - new_pos[1]
    if new_pos[1] < old_pos[1] and new_pos[4] + new_pos[1] >= old_pos[1]:
        old_pos[4] = new_pos[1] + new_pos[4] - old_pos[1]

    #return lại vùng fiding_range mới
    return old_pos 

def cal_distance(pos1, pos2):
    return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)


def seeker_lv01(seeker, hider_location):
    directions = ['left', 'right', 'up', 'down', 'down_left', 'down_right', 'up_left', 'up_right']
    fiding_range = (-1, -1, 0, 0)
    # random move when the unit hiding range = 0 and the hider hasn't annouced yet
    # hider_location: Pos that the hider annouced
    while hider_location == None and fiding_range == (-1, -1, 0, 0):
        previous_position = (seeker.row, seeker.col)  # Store the previous position
        random_direction = random.choice(directions)
        if random_direction == 'left':
            seeker.move_left()
        elif random_direction == 'right':
            seeker.move_right()
        elif random_direction == 'up':
            seeker.move_up()
        elif random_direction == 'down':
            seeker.move_down()
        elif random_direction == 'down_left':
            seeker.move_down_left()
        elif random_direction == 'down_right':
            seeker.move_down_right()
        elif random_direction == 'up_left':
            seeker.move_up_left()
        elif random_direction == 'up_right':
            seeker.move_up_right()
        if (seeker.row, seeker.col) != previous_position:  # Check if the position changed
            seeker.score -= 1
            seeker.move_count += 1

    if hider_location != None:
        # w: width of map; l: length of map
        if len(seeker.map_data) - hider_location[0] - 1 < 3:
            limit_right = len(seeker.map_data) - hider_location[0] - 1
        else:
            limit_right = 3

        if len(seeker.map_data[0]) - hider_location[1] - 1 < 3:
            limit_down = len(seeker.map_data[0]) - hider_location[1] - 1
        else:
            limit_down = 3

        hider_location += (limit_right, limit_down, ) # cần có width và length của map

        if finding_range == (-1, -1, 0, 0):
            finding_range = hider_location
        else:
            finding_range = update_fiding_range(finding_range, hider_location)

        hider_location = None

    # Cần ktra thêm obstacles,wall
    if finding_range != (-1, -1, 0, 0):
        if seeker.row == finding_range[0]:
            if cal_distance((seeker.row, seeker.col + 1), finding_range) > cal_distance((seeker.row, seeker.col - 1), finding_range):
                while seeker.map_data[seeker.row][seeker.col - 1] == 0 or seeker.map_data[seeker.row][seeker.col - 1] == 2:
                    seeker.move_left()
            else:
                while seeker.map_data[seeker.row][seeker.col + 1] == 0 or seeker.map_data[seeker.row][seeker.col + 1] == 2:
                    seeker.move_right()
        if seeker.col == finding_range[1]:
            if cal_distance((seeker.row + 1, seeker.col), finding_range) > cal_distance((seeker.row - 1, seeker.col), finding_range):
                while seeker.map_data[seeker.row - 1][seeker.col] == 0 or seeker.map_data[seeker.row - 1][seeker.col] == 2:
                    seeker.move_up()
            else:
                while seeker.map_data[seeker.row + 1][seeker.col] == 0 or seeker.map_data[seeker.row + 1][seeker.col] == 2:
                    seeker.move_down()
        up_left = (seeker.row - 1, seeker.col - 1)
        up_right = (seeker.row - 1, seeker.col + 1)
        down_left = (seeker.row + 1, seeker.col - 1)
        down_right = (seeker.row + 1, seeker.col + 1)

        dis = min(cal_distance(up_left, hider_location), cal_distance(up_right, hider_location), cal_distance(down_left, hider_location), cal_distance(down_right, hider_location))

        if dis == cal_distance(up_left, hider_location):
            while seeker.map_data[seeker.row - 1][seeker.col - 1] == 0 or seeker.map_data[seeker.row - 1][seeker.col - 1] == 2:
                seeker.move_up_left()
        elif dis == cal_distance(up_right, hider_location):
            while seeker.map_data[seeker.row - 1][seeker.col + 1] == 0 or seeker.map_data[seeker.row - 1][seeker.col + 1] == 2:
                seeker.move_up_right()
        elif dis == cal_distance(down_left, hider_location):
            while seeker.map_data[seeker.row + 1][seeker.col - 1] == 0 or seeker.map_data[seeker.row + 1][seeker.col - 1] == 2:
                seeker.move_down_left()
        elif dis == cal_distance(down_right, hider_location):
            while seeker.map_data[seeker.row + 1][seeker.col + 1] == 0 or seeker.map_data[seeker.row + 1][seeker.col + 1] == 2:
                seeker.move_down_right()
        
        up = (seeker.row - 1, seeker.col)
        down = (seeker.row + 1, seeker.col)
        left = (seeker.row, seeker.col - 1)
        right = (seeker.row, seeker.col + 1
                 )
        dis = min(cal_distance(up, hider_location), cal_distance(down, hider_location), cal_distance(left, hider_location), cal_distance(right, hider_location))

        if dis == cal_distance(up, hider_location):
            if seeker.map_data[seeker.row - 1][seeker.col] == 0 or seeker.map_data[seeker.row - 1][seeker.col] == 2:
                seeker.move_up()
                pass
            else:
                pass
        elif dis == cal_distance(down, hider_location):
            if seeker.map_data[seeker.row + 1][seeker.col] == 0 or seeker.map_data[seeker.row + 1][seeker.col] == 2:
                seeker.move_down()
                pass
            else:
                pass
        elif dis == cal_distance(left, hider_location):
            if seeker.map_data[seeker.row][seeker.col - 1] == 0 or seeker.map_data[seeker.row][seeker.col - 1] == 2:
                seeker.move_left()
                pass
            else:
                pass
        elif dis == cal_distance(right, hider_location):
            if seeker.map_data[seeker.row][seeker.col + 1] == 0 or seeker.map_data[seeker.row][seeker.col + 1] == 2:
                seeker.move_right()
                pass
            else:
                pass


    
