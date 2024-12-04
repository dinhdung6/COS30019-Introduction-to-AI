from search_utilities import AdventurerNode as SearchNode, explore_neighbors_with_jumps as get_neighbors_with_jumps, explore_neighbors as get_neighbors

def breadth_first_search(map_grid, start, goals, use_jumps=False):
    queue = [(SearchNode(start[0], start[1]), [])]
    explored_territories = set()
    total_steps_taken = 0
    path_journey = []

    while queue:
        current_node, current_path = queue.pop(0)
        if (current_node.x, current_node.y) in explored_territories:
            continue
        explored_territories.add((current_node.x, current_node.y))
        total_steps_taken += 1
        path_journey.append((current_node.x, current_node.y))

        if (current_node.x, current_node.y) in goals:
            return current_path + [current_node], total_steps_taken, path_journey, (current_node.x, current_node.y)

        neighbors = get_neighbors_with_jumps(current_node, map_grid) if use_jumps else get_neighbors(current_node, map_grid)
        for next_x, next_y, cost in neighbors:
            if map_grid.is_within_limits(next_x, next_y) and (next_x, next_y) not in explored_territories:
                new_node = SearchNode(next_x, next_y, current_node, current_node.travel_cost + cost)
                queue.append((new_node, current_path + [current_node]))

    return None, total_steps_taken, path_journey, None
