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

        if all([x == 2  for x in scan_list]):
            fc.forward(speed)
        else:
            fc.turn_right(speed)
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
