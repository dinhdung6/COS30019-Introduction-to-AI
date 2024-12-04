def find_direction(from_node, to_node):
    x1, y1 = from_node[0], from_node[1]
    x2, y2 = to_node[0], to_node[1]

    dx = x2 - x1
    dy = y2 - y1

    if dx == 0 and dy == 1:
        return "down"
    elif dx == 0 and dy == -1:
        return "up"
    elif dx == 1 and dy == 0:
        return "right"
    elif dx == -1 and dy == 0:
        return "left"
    elif dx == 0 and dy > 1:
        return f"jump_down({dy})"
    elif dx == 0 and dy < -1:
        return f"jump_up({-dy})"
    elif dy == 0 and dx > 1:
        return f"jump_right({dx})"
    elif dy == 0 and dx < -1:
        return f"jump_left({-dx})"
    else:
        return "invalid"
