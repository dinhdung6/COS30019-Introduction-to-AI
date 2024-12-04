from search_utilities import AdventurerNode as SearchNode, explore_neighbors as get_neighbors

def depth_first_search(map_grid, start, goals):
    journey_stack = [(SearchNode(start[0], start[1]), [])]
    explored_territories = set()
    total_steps_taken = 0
    path_journey = []

    while journey_stack:
        current_node, current_path = journey_stack.pop()
        total_steps_taken += 1
        path_journey.append((current_node.x, current_node.y))

        if (current_node.x, current_node.y) in goals:
            print(f"Goal reached: {(current_node.x, current_node.y)}")
            return current_path + [current_node], total_steps_taken, path_journey, (current_node.x, current_node.y)

        explored_territories.add((current_node.x, current_node.y))
        neighbors = get_neighbors(current_node, map_grid)
        next_nodes = []
        for next_x, next_y, _ in neighbors:
            if map_grid.is_within_limits(next_x, next_y) and (next_x, next_y) not in explored_territories:
                next_node = SearchNode(next_x, next_y, current_node, current_node.travel_cost + 1)
                next_nodes.append((next_node, current_path + [current_node]))

        print(f"Current Node: {(current_node.x, current_node.y)}, Neighbors: {neighbors}")

        for node in reversed(next_nodes):
            journey_stack.append(node)

    return None, total_steps_taken, path_journey, None
