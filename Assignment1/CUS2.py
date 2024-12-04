import heapq
from search_utilities import AdventurerNode as Node, explore_neighbors as get_neighbors

def cus2(map_grid, start, goals, heuristic_func, weight=2, secondary_weight=1):
    open_set = []
    for goal in goals:
        f_score = weight * heuristic_func(start, goal) + secondary_weight * manhattan_distance(start, goal)
        heapq.heappush(open_set, (f_score, 0, Node(start[0], start[1])))

    visited = set()
    total_nodes_expanded = 0
    nodes_traversed = []

    while open_set:
        _, _, current_node = heapq.heappop(open_set)
        total_nodes_expanded += 1
        nodes_traversed.append((current_node.x, current_node.y))

        if (current_node.x, current_node.y) in goals:
            return retrace_path(current_node), total_nodes_expanded, nodes_traversed, (current_node.x, current_node.y)

        visited.add((current_node.x, current_node.y))
        neighbors = get_neighbors(current_node, map_grid)
        for next_x, next_y, _ in neighbors:
            if (next_x, next_y) not in visited and map_grid.is_within_limits(next_x, next_y):
                tentative_g_score = current_node.travel_cost + 1
                for goal in goals:
                    f_score = tentative_g_score + weight * heuristic_func((next_x, next_y), goal) + secondary_weight * manhattan_distance((next_x, next_y), goal)
                    heapq.heappush(open_set, (f_score, tentative_g_score, Node(next_x, next_y, current_node, tentative_g_score)))

    return [], total_nodes_expanded, nodes_traversed, None

def retrace_path(node):
    path = []
    while node:
        path.append(node)
        node = node.mentor
    return list(reversed(path))

# Custom heuristic function combining Euclidean and Manhattan distances
def custom_heuristic(node, goal, weight=2, secondary_weight=1):
    euclidean = euclidean_distance(node, goal)
    manhattan = manhattan_distance(node, goal)
    return weight * euclidean + secondary_weight * manhattan

# Example heuristic function (Manhattan Distance)
def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Example heuristic function (Euclidean Distance)
def euclidean_distance(a, b):
    return ((a[0] - b[0])**2 + (a[1] - b[1])**2) ** 0.5
