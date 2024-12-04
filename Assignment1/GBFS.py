from search_utilities import AdventurerNode as SearchNode, explore_neighbors as get_neighbors
from heuristics import manhattan_journey as manhattan_distance

def greedy_best_first_search(map_grid, start, goals, manhattan_distance):
    priority_queue = [(min(manhattan_distance(start, goal) for goal in goals), SearchNode(start[0], start[1]))]
    visited_nodes = set()
    total_expanded_nodes = 0
    traversed_nodes = []

    while priority_queue:
        priority_queue.sort(key=lambda x: x[0])
        min_heuristic, current_node = priority_queue.pop(0)
        total_expanded_nodes += 1
        traversed_nodes.append((current_node.x, current_node.y))

        if (current_node.x, current_node.y) in goals:
            return trace_path(current_node), total_expanded_nodes, traversed_nodes, (current_node.x, current_node.y)

        visited_nodes.add((current_node.x, current_node.y))
        neighbors = get_neighbors(current_node, map_grid)
        for next_x, next_y, _ in neighbors:
            if (next_x, next_y) not in visited_nodes and map_grid.is_within_limits(next_x, next_y):
                heuristic_value = min(manhattan_distance((next_x, next_y), goal) for goal in goals)
                priority_queue.append((heuristic_value, SearchNode(next_x, next_y, current_node)))
                visited_nodes.add((next_x, next_y))

    return [], total_expanded_nodes, traversed_nodes, None

def trace_path(node):
    path = []
    while node:
        path.append(node)
        node = node.mentor
    return list(reversed(path))
