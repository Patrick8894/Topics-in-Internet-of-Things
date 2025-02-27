import picar_4wd as fc
import time
import random

speed = 20
min_dist = 35

def main():
    while True:
        # scan with ultrasonic sensor
        scan_list = fc.scan_step(min_dist)

        # if scan_list returns None, continue
        if not scan_list:
            continue

        if scan_list[3:7] != [2, 2, 2, 2]:
            # handle obstacle
            fc.stop() # stop the car
            fc.backward(speed) # back up for a bit
            time.sleep(0.3)
            # choose a random direction
            direction = random.choice([1, 2]) # 1 = left, 2 = right
            turn_time = random.uniform(0.6, 1.5)
            # turn to that direction
            if direction == 1:
                fc.turn_left(speed)
            else:
                fc.turn_right(speed)
            time.sleep(turn_time)
            # finally stop, and the car should continue moving forward if there is no obstacle in front
            fc.stop()
        else:
            fc.forward(speed)
        time.sleep(0.1)



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Stopped by ^C")
    finally:
        fc.stop()