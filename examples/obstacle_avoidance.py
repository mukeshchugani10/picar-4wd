import picar_4wd as fc
from random import randint

speed = 10

def main():
    while True:
        scan_list = fc.scan_step(35)
        if not scan_list:
            continue

        print(scan_list)
        tmp = scan_list[3:7]
        print(tmp)
        # if tmp != [2,2,2,2]:
        #     fc.turn_right(speed)
        # else:
        #     fc.forward(speed)

        if all([x == 2 for x in scan_list[3:7]]):
            fc.forward(speed)
        else:
            view_point = len(scan_list) // 2
            left_view = scan_list[: view_point]
            right_view = scan_list[view_point:]
            print(right_view, left_view, view_point)
            number_of_obstacles_left_view = view_point - left_view.count(2)
            number_of_obstacles_right_view = view_point - right_view.count(2)
            if number_of_obstacles_left_view > number_of_obstacles_right_view:
                fc.turn_right(speed)
                print("moving right")
            else:
                fc.turn_left(speed)
                print("moving left")

        # if tmp != [2, 2, 2, 2]:
        #     fc.stop()
        #     turnDirection = randint(0,1)
        #     fc.backward(speed)
        #     fc.time.sleep(1)
        #     if turnDirection == 1:
        #         fc.turn_left(speed)
        #     else:
        #         fc.turn_right(speed)

if __name__ == "__main__":
    try: 
        main()
    finally: 
        fc.stop()
