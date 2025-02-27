# src/lab1_part2/plan_path.py

import heapq
import numpy as np

class DStarPlanner:
    def __init__(self, grid: np.ndarray):
        self.grid = grid.copy()
        self.height, self.width = self.grid.shape
        self.cost_g = np.full((self.height, self.width), np.inf)
        self.visited = np.zeros((self.height, self.width), dtype=bool)
        self.parent = {}
    
    def in_bounds(self, x, y):
        # check if coordinate is inside map
        return 0 <= x < self.width and 0 <= y < self.height

    def is_free(self, x, y):
        # check if (x, y) is obstacle
        return self.grid[y, x] == 0

    def get_neighbors(self, x, y):
        # get free neighbors of (x, y)
        directions = [(1,0), (-1,0), (0,1), (0,-1)]
        neighbors = []
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if self.in_bounds(nx, ny) and self.is_free(nx, ny):
                neighbors.append((nx, ny))
        return neighbors

    def heuristic(self, x1, y1, x2, y2):
        # manhattan distance
        return abs(x1 - x2) + abs(y1 - y2)

    def compute_path(self, start, dest):
        (sx, sy) = start
        (dx, dy) = dest
        self.cost_g.fill(np.inf)
        self.visited.fill(False)
        self.parent.clear()
        open_list = []

        # Initialize
        self.cost_g[sy, sx] = 0.0
        heapq.heappush(open_list, (self.heuristic(sx, sy, dx, dy), sx, sy))

        while open_list:
            f_cost, x, y = heapq.heappop(open_list)

            if self.visited[y, x]:
                continue
            self.visited[y, x] = True

            # check if reached destination
            if (x, y) == (dx, dy):
                return self.reconstruct_path(start, dest)

            g_cost = self.cost_g[y, x]

            # explore neighbors
            for (nx, ny) in self.get_neighbors(x, y):
                new_cost = g_cost + 1.0
                if new_cost < self.cost_g[ny, nx]:
                    self.cost_g[ny, nx] = new_cost
                    self.parent[(nx, ny)] = (x, y)
                    h = self.heuristic(nx, ny, dx, dy)
                    heapq.heappush(open_list, (new_cost + h, nx, ny))

        return None

    def reconstruct_path(self, start, dest):
        # backtract
        path = []
        current = dest
        while current != start:
            path.append(current)
            if current not in self.parent:
                return None
            current = self.parent[current]
        path.append(start)
        path.reverse()
        return path


def plan_path(grid: np.ndarray, start: tuple, dest: tuple) -> list:
    planner = DStarPlanner(grid)
    path = planner.compute_path(start, dest)
    return path


if __name__ == "__main__":
    import numpy as np

    test_grid = np.array([
        [0, 0, 1, 0, 0],
        [0, 1, 0, 1, 1],
        [0, 0, 0, 0, 0],
        [1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0]
    ])
    start_coord = (4, 2)
    dest_coord = (0, 0)

    result_path = plan_path(test_grid, start_coord, dest_coord)
    if result_path is None:
        print("No path found.")
    else:
        print("Path found:", result_path)
