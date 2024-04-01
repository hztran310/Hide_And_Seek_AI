import math
import random
import numpy as np

from Character import Character, Seeker, Hider

# new_pos is in the center of its range, while old_pos is the top left of the previous finding range
# new_pos = (row, col, limit to the right, limit to down) (Sau khi nhận được annouce, điểm được annouce cần được xác định limit phải, down => Cần có width, length của map)
# old_pos = (row, col, limit to the right, limit to down)
def update_finding_range(old_pos, new_pos):
    if new_pos[0] < old_pos[0] and old_pos[0] + old_pos[3] >= new_pos[0]:
        old_pos[0] = new_pos[0]
        old_pos[3] = old_pos[0] + old_pos[3] - new_pos[0]
    if new_pos[0] > old_pos[0] and new_pos[3] + new_pos[0] >= old_pos[0]:
        old_pos[3] = new_pos[0] + new_pos[3] - old_pos[0]
    
    if new_pos[1] > old_pos[1] and old_pos[1] + old_pos[2] >= new_pos[1]:
        old_pos[1] = new_pos[1]
        old_pos[2] = old_pos[1] + old_pos[2] - new_pos[1]
    if new_pos[1] < old_pos[1] and new_pos[2] + new_pos[1] >= old_pos[1]:
        old_pos[2] = new_pos[1] + new_pos[2] - old_pos[1]

    #return lại vùng finding_range mới
    return old_pos 

# finding top left of new_pos range
def find_top_left_range(pos):
    if pos[0] - 3 < 0:
        pos[3] = pos[3] + pos[0]
        pos[0] = 0
    else:
        pos[0] = pos[0] - 3
        pos[3] = pos[3] + 3

    if pos[1] - 3 < 0:
        pos[2] = pos[2] + pos[1]
        pos[1] = 0
    else:
        pos[1] = pos[1] - 3
        pos[2] = pos[2] + 3
    
    return pos

def cal_distance(pos1, pos2):
    return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

# Có thể đề xuất thêm chức năng kiểm tra hoặc đánh dấu lại ô có hider thay vì chỉ để True/False
# Cần kiểm tra lại xem visible_cells có phải là nguyên cái map nhưng đánh các ô nhìn thấy được là True, còn lại là False hay ko?
# Tự hỏi là map_data của con seeker có đánh dấu vị trí của con hider như cách để truy xuất map bth không? Nếu ko thì cần đổi seeker.map_data thành vị trí của hider. Nếu có thì về mặt logic có đúng theo đề yêu cầu ko ta?
def check_for_hider(seeker):
    for row in range(len(seeker.visible_cells)):
        for col in range(len(seeker.visible_cells[row])):
            # Truy cập ô trong visible_cells ở hàng row và cột col
            if seeker.visible_cells[row, col] == True and seeker.map_data[row][col] == 2:
                return True, row, col
    return False, row, col

# Chạy hết hàm = 1 move
# Hàm go khi xác định được vị trí cần đến
def go(seeker, row, col):
    if seeker.row == row:
        if cal_distance((seeker.row, seeker.col + 1), (row, col)) > cal_distance((seeker.row, seeker.col - 1), (row, col)):
            if seeker.map_data[seeker.row][seeker.col - 1] == 0 or seeker.map_data[seeker.row][seeker.col - 1] == 2:
                seeker.move_left()
                pass
        else:
            if seeker.map_data[seeker.row][seeker.col + 1] == 0 or seeker.map_data[seeker.row][seeker.col + 1] == 2:
                seeker.move_right()
                pass
    if seeker.col == col:
        if cal_distance((seeker.row + 1, seeker.col), (row, col)) > cal_distance((seeker.row - 1, seeker.col), (row, col)):
            if seeker.map_data[seeker.row - 1][seeker.col] == 0 or seeker.map_data[seeker.row - 1][seeker.col] == 2:
                seeker.move_up()
                pass
        else:
            if seeker.map_data[seeker.row + 1][seeker.col] == 0 or seeker.map_data[seeker.row + 1][seeker.col] == 2:
                seeker.move_down()
                pass
        
    up_left = (seeker.row - 1, seeker.col - 1)
    up_right = (seeker.row - 1, seeker.col + 1)
    down_left = (seeker.row + 1, seeker.col - 1)
    down_right = (seeker.row + 1, seeker.col + 1)

    dis = min(cal_distance(up_left, (row, col)), cal_distance(up_right, (row, col)), cal_distance(down_left, (row, col)), cal_distance(down_right, (row, col)))

    if dis == cal_distance(up_left, (row, col)):
        if seeker.map_data[seeker.row - 1][seeker.col - 1] == 0 or seeker.map_data[seeker.row - 1][seeker.col - 1] == 2:
            seeker.move_up_left()
            pass
    elif dis == cal_distance(up_right, (row, col)):
        if seeker.map_data[seeker.row - 1][seeker.col + 1] == 0 or seeker.map_data[seeker.row - 1][seeker.col + 1] == 2:
            seeker.move_up_right()
            pass
    elif dis == cal_distance(down_left, (row, col)):
        if seeker.map_data[seeker.row + 1][seeker.col - 1] == 0 or seeker.map_data[seeker.row + 1][seeker.col - 1] == 2:
            seeker.move_down_left()
            pass
    elif dis == cal_distance(down_right, (row, col)):
        if seeker.map_data[seeker.row + 1][seeker.col + 1] == 0 or seeker.map_data[seeker.row + 1][seeker.col + 1] == 2:
            seeker.move_down_right()
            pass
    
    up = (seeker.row - 1, seeker.col)
    down = (seeker.row + 1, seeker.col)
    left = (seeker.row, seeker.col - 1)
    right = (seeker.row, seeker.col + 1
                )
    dis = min(cal_distance(up, (row, col)), cal_distance(down, (row, col)), cal_distance(left, (row, col)), cal_distance(right, (row, col)))

    if dis == cal_distance(up, (row, col)):
        if seeker.map_data[seeker.row - 1][seeker.col] == 0 or seeker.map_data[seeker.row - 1][seeker.col] == 2:
            seeker.move_up()
    elif dis == cal_distance(down, (row, col)):
        if seeker.map_data[seeker.row + 1][seeker.col] == 0 or seeker.map_data[seeker.row + 1][seeker.col] == 2:
            seeker.move_down()
    elif dis == cal_distance(left, (row, col)):
        if seeker.map_data[seeker.row][seeker.col - 1] == 0 or seeker.map_data[seeker.row][seeker.col - 1] == 2:
            seeker.move_left()
    elif dis == cal_distance(right, (row, col)):
        if seeker.map_data[seeker.row][seeker.col + 1] == 0 or seeker.map_data[seeker.row][seeker.col + 1] == 2:
            seeker.move_right()

# Chạy hết hàm = 1 lần move
def seeker_lv01(seeker, hider_location):
    directions = ['left', 'right', 'up', 'down', 'down_left', 'down_right', 'up_left', 'up_right']
    finding_range = (-1, -1, 0, 0)
    # random move when the unit hiding range = 0 and the hider hasn't annouced yet
    # hider_location: Pos that the hider annouced
    if hider_location == None and finding_range == (-1, -1, 0, 0):
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
        pass

    # Biến hider_location bên ngoài khi chưa nhận được annouce mới thì khi truyền vào phải bằng NONE
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

        hider_location += (limit_right, limit_down, )

        hider_location = find_top_left_range(hider_location)

        if finding_range == (-1, -1, 0, 0):
            finding_range = hider_location
        else:
            finding_range = update_finding_range(finding_range, hider_location)

    if check_for_hider(seeker)[0] == True: # Khi thấy hider, use hàm "go" để tới chỗ hider (Nếu là lvl03, hider di chuyển được thì tiến hành đặt hàm "go" trong hàm chính để luôn cập nhật vị trí mới nhất của hider sau 1 lượt di chuyển)
        return False, True, (check_for_hider(seeker)[1], check_for_hider(seeker)[2]) # return chưa tới chỗ annouce, đã nhìn thấy hider, (vị trí của hider) -> Sử dụng vị trí đã tìm thấy trong vision của seeker vì trong lvl02 có nhiều hiders 
    # TH: Nếu đã ở top left của finding range (Chưa nhận được annouce mới tức finding range vẫn như cũ) thì tiến hành tìm kiếm trong finding range.
    # TH này có thể đề xuất thử lưu lại các ô trong đã kiểm tra trong lúc tìm kiếm trong khu vực finding range.
    # (nếu được thì sẽ thu hẹp lại các ô cần tìm kiếm vì các finding range giao nhau, tuy nhiên khó và mất nhiều bộ nhớ để lưu trữ)
    elif finding_range[0] == seeker.row and finding_range[1] == seeker.col:
        return True, False, (finding_range[0], finding_range[1]) 
        # Xử lý tìm kiếm trong vùng finding range (cách đi sẽ sử dụng hàm "go", đích đến lần lượt là các ô trong vùng finding range) ở bên ngoài cho đến khi:
            # 1. Thấy được hider (use "check_for_hider") và tiếp tục use hàm "go" để chạy tới hider.
            # 2. Khi nhận được annouce mới thì gọi lại hàm "seeker_lvl01" (tránh cho seeker move được một bước rồi lại quay lại top_left của finding range)
    elif finding_range != (-1, -1, 0, 0):
        go(seeker, finding_range[0], finding_range[1])
        return False, False, (finding_range[0], finding_range[1]) 

# Mô phỏng code khi tìm kiếm trong vùng finding range, dùng để tham khảo cho zui thoi :))
# Check lại xem có cần + 1 vào không?
def check_in_finding_range(seeker, finding_range):
    for row in range(finding_range[0], finding_range[0] + finding_range[3] + 1):
        for col in range(finding_range[1], finding_range[1] + finding_range[2] + 1):
            go(seeker, row, col)
            if check_for_hider(seeker)[0] == True:
                return True, check_for_hider(seeker)[1], check_for_hider(seeker)[2]  # Dí hider khi đã biết được vị trí (Cần return vị trí trong trường hợp có nhiều hiders như lvl02)
    return False, seeker.row, seeker.col
    
