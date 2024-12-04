import math

def manhattan_journey(current, destination):
    return abs(current[0] - destination[0]) + abs(current[1] - destination[1])

def euclidean_journey(current, destination):
    return math.sqrt((current[0] - destination[0]) ** 2 + (current[1] - destination[1]) ** 2)
