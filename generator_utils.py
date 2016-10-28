import random
import math
import csv


def get_random(min, max):
    return random.uniform(min, max)


def generate_in_range(min, max, amount):
    points = []
    for _ in range(0, amount):
        points.append((get_random(min, max), get_random(min, max)))
    return points


def generate_on_circle(center_x, center_y, radius, amount):
    points = []
    for _ in range(0, amount):
        angle = get_random(0, 2 * math.pi)
        points.append((center_x + radius * math.cos(angle), center_y + radius * math.sin(angle)))
    return points


def generate_on_line(min, max, amount):
    points = []
    for _ in range(0, amount):
        x = get_random(min, max)
        points.append((x, 0.05 * x + 0.05))
    return points


def generate_on_quadrangle(left_up, left_down, right_down, right_up, amount):
    points = []
    for _ in range(0, amount):
        side = random.randint(0, 3)
        if side == 0:
            points.append((left_up[0], get_random(left_down[1], left_up[1])))
        elif side == 1:
            points.append((get_random(left_down[0], right_down[0]), left_down[1]))
        elif side == 2:
            points.append((right_down[0], get_random(right_down[1], right_up[1])))
        else:
            points.append((get_random(left_up[0], right_up[0]), left_up[1]))
    return points


def generate_on_square(left_up, left_down, right_down, right_up, amount_axis, amount_diameter):
    points = []
    points.append(left_up)
    points.append(left_down)
    points.append(right_down)
    points.append(right_up)
    for _ in range(0, amount_diameter):
        x = get_random(left_down[0], right_up[0])
        points.append((x, x))

    for _ in range(0, amount_diameter):
        x = get_random(left_up[0], right_down[0])
        points.append((x, left_up[1] - x))

    for _ in range(0, amount_axis):
        points.append((left_up[0], get_random(left_down[1], left_up[1])))

    for _ in range(0, amount_axis):
        points.append((get_random(left_down[0], right_down[0]), left_down[1]))

    return points



