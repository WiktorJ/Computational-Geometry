def filter_inline_points(points, min_point):
    filtered_points = []
    first = min_point
    second = points.pop(0)
    while len(points) > 0:
        current = points.pop(0)
        if first[0] == second[0] == current[0] \
                or first[1] == second[1] == current[1]:
            second = current
        else:
            filtered_points.append(first)
            first = second
            second = current
    filtered_points.append(first)
    filtered_points.append(second)
    return filtered_points
