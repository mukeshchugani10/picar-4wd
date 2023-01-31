import numpy as np

import picar_4wd as fc


def adv_mapping():
    grid = np.zeros((100, 100))  # 100*100 bounding box in front of the picar
    for i in range(121):
        curr = i - 60  # get the current angle
        reading = fc.get_distance_at(curr)
        if reading > 120:
            continue
        a = 50 + round(reading * np.sin(np.radians(curr)), 0) # x
        b = round(reading * np.cos(np.radians(curr)), 0)  # y
        if a > 99 or b > 99:
            continue
        grid[int(a) ,int(b)] =  1# set the point to 1 if there is a
    # print("finish ", j, " scan") # print(curr, reading, np.radians(curr), a)

    return grid


if __name__ == '__main__':
    matrix = adv_mapping()

    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in matrix]))