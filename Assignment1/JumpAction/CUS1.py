from search_utilities import AdventurerNode as Node, explore_neighbors_with_jumps as get_neighbors_with_jumps, explore_neighbors as get_neighbors

def cus1(map_grid, start, goals, use_jumps=False):
    for goal in goals:
        result, total_nodes, traversed, reached_goal = bidirectional_search(map_grid, start, goal, use_jumps)
        if result:
            return result, total_nodes, traversed, reached_goal
    return None, 0, [], None

def bidirectional_search(map_grid, start, goal, use_jumps):
    start_frontier = [(Node(start[0], start[1]), [])]
    goal_frontier = [(Node(goal[0], goal[1]), [])]
    start_visited = {}
    goal_visited = {}

    total_nodes_expanded = 0
    nodes_traversed = []

    while start_frontier and goal_frontier:
        total_nodes_expanded += 1

        # Expand the start frontier
        start_node, start_path = start_frontier.pop(0)
        nodes_traversed.append((start_node.x, start_node.y))
        if (start_node.x, start_node.y) in goal_visited:
            goal_path = goal_visited[(start_node.x, start_node.y)]
            return start_path + [start_node] + goal_path[::-1], total_nodes_expanded, nodes_traversed, (start_node.x, start_node.y)
        start_visited[(start_node.x, start_node.y)] = start_path + [start_node]

        neighbors = get_neighbors_with_jumps(start_node, map_grid) if use_jumps else get_neighbors(start_node, map_grid)
        for next_x, next_y, cost in neighbors:
            if map_grid.is_within_limits(next_x, next_y) and (next_x, next_y) not in start_visited:
                start_frontier.append((Node(next_x, next_y), start_path + [start_node]))

        # Expand the goal frontier
        goal_node, goal_path = goal_frontier.pop(0)
        nodes_traversed.append((goal_node.x, goal_node.y))
        if (goal_node.x, goal_node.y) in start_visited:
            start_path = start_visited[(goal_node.x, goal_node.y)]
            return start_path + goal_path[::-1], total_nodes_expanded, nodes_traversed, (goal_node.x, goal_node.y)
        goal_visited[(goal_node.x, goal_node.y)] = goal_path + [goal_node]

        neighbors = get_neighbors_with_jumps(goal_node, map_grid) if use_jumps else get_neighbors(goal_node, map_grid)
        for next_x, next_y, cost in neighbors:
            if map_grid.is_within_limits(next_x, next_y) and (next_x, next_y) not in goal_visited:
                goal_frontier.append((Node(next_x, next_y), goal_path + [goal_node]))

    return None, total_nodes_expanded, nodes_traversed, None
