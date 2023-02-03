import numpy as np

import picar_4wd as fc
import time
from utils import Utils


def print_matrix(matrix):
    for row in matrix:
        for val in row:
            print(val, end=" ")
        print()

def move_dir(dir):
    if dir == 'forward':
        fc.forward(10)
        time.sleep(0.19)
    elif dir == 'backward':
        fc.backward(10)
        time.sleep(0.19)
    elif dir == 'right':
        fc.turn_right(10)
        time.sleep(1.0)
    else:
        fc.turn_left(10)
        time.sleep(1.0)


def downsize(map, new_map_size, org_map_size):

    new_map = np.zeros((new_map_size, new_map_size))
    r = org_map_size//new_map_size

    for x in range(new_map_size):
        for y in range(new_map_size):
            grid = map[r*x:r*x + r, r*y:r*y + r]
            # print("the grid is ", grid)
            if sum([sum(row) for row in grid]) > 1:
                new_map[x][y] = 1

    return new_map

def generate_map(map_size, angle_of_view, threshold):
    fc.servo.set_angle(0)
    time.sleep(1)
    map = np.zeros((map_size, map_size))

    #Assuming car is at (0, map/2) coordinates.

    for i in range(angle_of_view + 1):
        angle = i - angle_of_view//2 #Initial value is -60 the sensor starts scanning from the right
        distance = fc.get_distance_at(angle)
        print("The distance and angle is", distance, angle)

        #Based on our analysis distance returned in calibrated in cms, a safe reading assuming no obstacle can
        # be 100, with -2  or -1 implying value to be inf

        if distance < threshold and distance > 0:
            row = int(distance*np.cos(np.radians(angle)))
            col = int(map_size/2 + distance*np.sin(np.radians(angle)))

            # print("Thr row and column are", row, col)
            map[row][col] = 1

    fc.servo.set_angle(0)
    return map


def traverse(map_size, reduced_map_size, stopping_threshold, angle_of_view, start_pos_x, start_pos_y):
    org_map = generate_map(map_size, angle_of_view, stopping_threshold)
    car_map = downsize(org_map, reduced_map_size, map_size)
    car_map = list(map(lambda row: list(map(lambda x: int(x), row)), car_map))
    print_matrix(car_map)

    path = Utils().shortestPath(car_map, (start_pos_x, start_pos_y, 0, []))
    print(path)
    print("The length of path is", len(path))

    final_path = []
    dir = 0
    for i in range(0, len(path) - 1):
        start_point = path[i]
        next_point = path[i + 1]
        # print(start_point, next_point, dir)
        if start_point[0] > next_point[0]:
            if dir == 0:
                final_path.append('backward')
            # left
            elif dir == 1:
                final_path.append('left')
                final_path.append('forward')
                dir = 3
            # right
            elif dir == 2:
                final_path.append('left')
                final_path.append('forward')
                dir = 3
            # back
            else:
                final_path.append('forward')
        # x+1
        elif start_point[0] < next_point[0]:
            if dir == 0:
                final_path.append('forward')
            # left
            elif dir == 1:
                final_path.append('right')
                final_path.append('forward')
                dir = 0
            # right
            elif dir == 2:
                final_path.append('left')
                final_path.append('forward')
                dir = 0
            # back
            else:
                final_path.append('backward')

        elif start_point[1] > next_point[1]:
            if dir == 0:
                final_path.append('right')
                final_path.append('forward')
                dir = 2
            # left
            elif dir == 1:
                final_path.append('backward')
            # right
            elif dir == 2:
                final_path.append('forward')
            # back
            else:
                final_path.append('left')
                final_path.append('forward')
                dir = 1

        elif start_point[1] < next_point[1]:
            if dir == 0:
                final_path.append('left')
                final_path.append('forward')
                dir = 1
            # left
            elif dir == 1:
                final_path.append('forward')
            # right
            elif dir == 2:
                final_path.append('backward')
            # back
            else:
                final_path.append('right')
                final_path.append('forward')
                dir = 2

    print(path)
    print(final_path)

    for dir in final_path:
        move_dir(dir)
    fc.stop()

if __name__ == '__main__':
    steps = 2
    map_size = 100
    reduced_map_size = 20
    stopping_threshold = 70
    angle_of_view = 120
    start_pos_x = 0
    start_pos_y = 10

    for _ in range(steps):
        traverse(map_size, reduced_map_size, stopping_threshold, angle_of_view, start_pos_x, start_pos_y)


