# src/lab1_part2/ultrasonic_detect.py

import picar_4wd as fc
import numpy as np
import math

def mark_obstacle(grid, grid_size, x, y, clearance = 1):
    x = int(x)
    y = int(y)
    for i in range(x - clearance, x + clearance + 1):
        for j in range(y - clearance, y + clearance + 1):
            if 0 <= i < grid_size and 0 <= j < grid_size:
                grid[j, i] = 1

def scan_surroundings(cur_pos = (19,39), cur_orientation = 'N', grid_size = 40):
    cur_x, cur_y = cur_pos
    # get angle offset from orientation
    if cur_orientation == 'E':
        angle_offset = -90
    elif cur_orientation == 'S':
        angle_offset = 180
    elif cur_orientation == 'W':
        angle_offset = 90
    else:
        angle_offset = 0
    obstacle_grid = np.zeros((grid_size, grid_size), dtype=int)
    for angle_deg in range(-60, 60, 5):
        abs_angle_deg = angle_offset + angle_deg
        # set servo angle
        fc.servo.set_angle(angle_deg)
        fc.time.sleep(0.03)
        # get distance in cm
        dist_cm = fc.us.get_distance()
        print(angle_deg, dist_cm)
        if dist_cm < 0 or dist_cm > 80:
            continue
        
        x = (dist_cm/10) * math.cos(math.radians(abs_angle_deg))
        y = (dist_cm/10) * math.sin(math.radians(abs_angle_deg))
        x = cur_x + round(x)
        y = cur_y + round(y)

        mark_obstacle(obstacle_grid, grid_size, x, y)
    return obstacle_grid

def main():
    grid_size=20
    obstacle_grid = scan_surroundings(cur_pos=(9, 9), cur_orientation='N', grid_size=grid_size)
    obstacle_grid[9, 9] = 2

    # Rotate the obstacle grid 90 degrees counterclockwise
    rotated_obstacle_grid = np.rot90(obstacle_grid)

    print(rotated_obstacle_grid)

if __name__ == "__main__":
    main()