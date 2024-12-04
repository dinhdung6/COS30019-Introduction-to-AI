import sys
import re
import time
import psutil
from AS import a_star_search
from DFS import depth_first_search
from BFS import breadth_first_search
from GBFS import greedy_best_first_search
from CUS1 import cus1
from CUS2 import cus2, custom_heuristic
from heuristics import manhattan_journey as manhattan_distance
from gui import run_gui
from search_utilities import ExpeditionGrid
from direction import find_direction

def main(file_path, search_method, use_jumps):
    with open(file_path, 'r') as f:
        data = f.read()

    lines = data.splitlines()

    # Parse dimensions
    dimensions = re.findall(r'\d+', lines[0])
    rows, cols = int(dimensions[0]), int(dimensions[1])
    map_grid = ExpeditionGrid(rows, cols)

    # Parse start position
    start = tuple(map(int, re.findall(r'\d+', lines[1])))

    # Parse goals
    goals_line = lines[2]
    goals = [tuple(map(int, re.findall(r'\d+', goal))) for goal in goals_line.split('|')]

    # Parse obstacles
    for i in range(3, len(lines)):
        obstacle = list(map(int, re.findall(r'\d+', lines[i])))
        map_grid.place_obstacle(obstacle[0], obstacle[1], obstacle[2], obstacle[3])

    # Debug prints
    print(f"Parsed dimensions: {rows} x {cols}")
    print(f"Parsed start: {start}")
    print(f"Parsed goals: {goals}")
    print("Grid after placing obstacles:")
    for row in map_grid.grid_map:
        print(row)

    process = psutil.Process()

    def execute_search():
        if search_method == "DFS":
            return depth_first_search(map_grid, start, goals, use_jumps)
        elif search_method == "BFS":
            return breadth_first_search(map_grid, start, goals, use_jumps)
        elif search_method == "GBFS":
            return greedy_best_first_search(map_grid, start, goals, use_jumps)
        elif search_method == "AS":
            return a_star_search(map_grid, start, goals, manhattan_distance, use_jumps)
        elif search_method == "CUS1":
            return cus1(map_grid, start, goals, use_jumps)
        elif search_method == "CUS2":
            return cus2(map_grid, start, goals, custom_heuristic, use_jumps)
        else:
            print("Invalid input. Type only: DFS, BFS, GBFS, AS, CUS1, CUS2.")
            sys.exit(1)

    start_time = time.time()
    path, total_nodes, journey_log, goal_reached = execute_search()

    if path:
        print(f"{file_path} {search_method}")
        print(f"< Node ({goal_reached[0]}, {goal_reached[1]})> {total_nodes}")
        directions = [find_direction((path[i].x, path[i].y), (path[i+1].x, path[i+1].y)) for i in range(len(path)-1)]
        print(directions)
    else:
        print(f"{file_path} {search_method}")
        print(f"No goal is reachable; {total_nodes}")

    memory_use = process.memory_info().rss / (1024 ** 2)
    print(f"Memory usage: {memory_use:.2f} MB")

    try:
        if path:
            run_gui(map_grid, start, goals, [(node.x, node.y) for node in path], journey_log, start_time)
        else:
            print("Can't get to destination.")
    except Exception as e:
        print(f"Can't show the navigation: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python search.py <file_path> <search_method> <use_jumps>")
        sys.exit(1)

    file_path = sys.argv[1]
    search_method = sys.argv[2].upper()
    use_jumps = sys.argv[3].lower() == 'true'
    main(file_path, search_method, use_jumps)
