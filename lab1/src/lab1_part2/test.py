import picar_4wd as fc
import time

def main():
    # return the distance at 0 degree in cm
    # dist = fc.get_distance_at(0)
    # print(dist)

    #turn left 90 degree
    # fc.turn_left(20)
    # time.sleep(1.1) 

    # go forward for 20 cm
    fc.forward(5)
    time.sleep(1)

    fc.stop()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Stopped by ^C")
    finally:
        fc.stop()