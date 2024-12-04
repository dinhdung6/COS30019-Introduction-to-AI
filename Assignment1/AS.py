from search_utilities import AdventurerNode as SearchNode, explore_neighbors_with_jumps as get_neighbors_with_jumps, explore_neighbors as get_neighbors
from heuristics import manhattan_journey as heuristic_function

def a_star_search(map_grid, start, goals, heuristic_function, use_jumps=False):
    priority_queue = [(0, heuristic_function(start, goal), SearchNode(start[0], start[1])) for goal in goals]
    visited_nodes = set()
    total_expanded_nodes = 0
    traversed_nodes = []

    while priority_queue:
        priority_queue.sort(key=lambda x: x[0])
        min_index = 0
        for i in range(len(priority_queue)):
            if priority_queue[i][0] < priority_queue[min_index][0]:
                min_index = i
        _, _, current_node = priority_queue.pop(min_index)

        total_expanded_nodes += 1
        traversed_nodes.append((current_node.x, current_node.y))
        if (current_node.x, current_node.y) in goals:
            return trace_path(current_node), total_expanded_nodes, traversed_nodes, (current_node.x, current_node.y)

        visited_nodes.add((current_node.x, current_node.y))
        neighbors = get_neighbors_with_jumps(current_node, map_grid) if use_jumps else get_neighbors(current_node, map_grid)
        for next_x, next_y, cost in neighbors:
            if (next_x, next_y) not in visited_nodes and map_grid.is_within_limits(next_x, next_y):
                for goal in goals:
                    priority_queue.append((current_node.travel_cost + heuristic_function((next_x, next_y), goal), heuristic_function((next_x, next_y), goal), SearchNode(next_x, next_y, current_node)))
                visited_nodes.add((next_x, next_y))

    return [], total_expanded_nodes, traversed_nodes, None

def trace_path(node):
    path = []
    while node:
        path.append(node)
        node = node.mentor
    return list(reversed(path))
