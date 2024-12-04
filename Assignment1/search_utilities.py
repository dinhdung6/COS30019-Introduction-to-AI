class AdventurerNode:
    def __init__(self, x, y, mentor=None, travel_cost=0):
        self.x = x
        self.y = y
        self.mentor = mentor
        self.travel_cost = travel_cost
        self.depth = 0

    def __lt__(self, other):
        return self.x + self.y < other.x + other.y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    def __hash__(self):
        return hash((self.x, self.y))  # Hash based on x and y coordinates

class ExpeditionGrid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid_map = [[' ' for _ in range(cols)] for _ in range(rows)]

    def place_obstacle(self, start_x, start_y, width, height):
        for i in range(start_y, min(start_y + height, self.rows)):
            for j in range(start_x, min(start_x + width, self.cols)):
                self.grid_map[i][j] = 1
        print(f"Placed obstacle at ({start_x}, {start_y}) with width {width} and height {height}")

    def is_within_limits(self, x, y):
        return 0 <= x < self.cols and 0 <= y < self.rows and self.grid_map[y][x] != 1

    def is_permissible(self, x, y):
        return self.is_within_limits(x, y) and self.grid_map[y][x] != 1

def explore_neighbors(current_node, map_grid):
    paths = []
    for dx, dy in [(0, -1), (-1, 0), (0, 1), (1, 0)]:
        new_x, new_y = current_node.x + dx, current_node.y + dy
        if map_grid.is_within_limits(new_x, new_y):
            paths.append((new_x, new_y, 1))  # 1 is the cost to move to the neighbor
    return paths
def explore_neighbors_with_jumps(current_node, map_grid):
    paths = explore_neighbors(current_node, map_grid)  # existing neighbors
    jumps = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # right, left, down, up
    max_jump = 4  # maximum jump distance

    for dx, dy in jumps:
        for n in range(2, max_jump + 1):
            new_x, new_y = current_node.x + dx * n, current_node.y + dy * n
            if map_grid.is_within_limits(new_x, new_y):
                jump_cost = 2 ** (n - 1)
                paths.append((new_x, new_y, jump_cost))
    return paths