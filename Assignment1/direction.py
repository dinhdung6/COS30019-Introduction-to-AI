def find_direction(from_node, to_node):
    x1, y1 = from_node.x, from_node.y
    x2, y2 = to_node.x, to_node.y
    
    if x2 == x1 and y2 == y1 + 1:
        return "down"
    elif x2 == x1 and y2 == y1 - 1:
        return "up"
    elif x2 == x1 + 1 and y2 == y1:
        return "right"
    elif x2 == x1 - 1 and y2 == y1:
        return "left"
