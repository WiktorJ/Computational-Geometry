from sortedcontainers import sortedset

from assignment4.vertex import VertexType, Vertex, get_point_orientation_relative_to_line, LEFT, RIGHT
from custom_file_utils import remove_characters, read_file_to_tuples, write_tuple_to_file

result = []

def is_monotonic(points):
    events = sortedset.SortedSet(points)
    while len(events) > 0:
        event = events.pop(0)
        index = points.index(event)

        if index == 0:
            before_index = len(points) - 1
        else:
            before_index = index - 1

        if index == len(points) - 1:
            after_index = 0
        else:
            after_index = index + 1
        before = points[before_index]
        after = points[after_index]
        vertex_type = VertexType.get_vertex_type(before, event, after)
        if vertex_type == VertexType.SPLIT or vertex_type == VertexType.MERGE:
            print('Polygon is not monotonic')
            return False
    return True
    pass


def load_to_vertexes(points):
    return [Vertex(point[0], point[1]) for point in points]


def left_chain_next(current_index, vs):
    return current_index - 1 if current_index > 0 else len(vs) - 1


def right_chain_next(current_index, vs):
    return current_index + 1 if current_index < len(vs) - 1 else 0


def generate_chain(current_v, current_index, get_next_index, vertexes, max_v):
    chain = []
    while current_v != max_v:
        current_index = get_next_index(current_index, vertexes)
        current_v = vertexes[current_index]
        chain.append(current_v)

    return chain


def same_chain_join(stack, stack_top, current_v, comparison_site):
    stack.pop()
    finish = False
    prev = None
    while len(stack) > 0 and not finish:
        prev = stack.pop()
        if get_point_orientation_relative_to_line(stack_top, [current_v, prev]) == comparison_site:
            result.append((prev, current_v))
            print("S Joining: ", prev, current_v)
            stack_top = prev
        else:
            finish = True
    stack.append(prev)
    stack.append(stack_top)


def triangulation(vertexes):
    max_v = max(vertexes)
    min_v = min(vertexes)
    min_index = vertexes.index(min_v)
    current_index = min_index
    current_v = min_v
    left_chain = generate_chain(current_v,
                                current_index,
                                left_chain_next,
                                vertexes,
                                max_v)
    right_chain = generate_chain(current_v,
                                 current_index,
                                 right_chain_next,
                                 vertexes,
                                 max_v)

    vertexes = sorted(vertexes)
    stack = [vertexes[0], vertexes[1]]
    vertexes = list(reversed(vertexes[2:]))
    current_v = vertexes.pop()
    while current_v != max_v:
        stack_top = stack[len(stack) - 1]
        if stack_top in left_chain and current_v in left_chain:  # or stack_top in right_chain and current_v in right_chain:
            same_chain_join(stack, stack_top, current_v, LEFT)
        elif stack_top in right_chain and current_v in right_chain:
            same_chain_join(stack, stack_top, current_v, RIGHT)
        else:
            for e in stack:
                result.append((e, current_v))
                print("D Joining: ", e, current_v)
            stack = [stack_top, current_v]
        current_v = vertexes.pop()


points_tuples = read_file_to_tuples(remove_characters('data2.csv', ['(', ',', ')']))

vertexes = load_to_vertexes(points_tuples)

triangulation(vertexes)

write_tuple_to_file('result.csv', result)
remove_characters('result.csv', ['\"', '(', ')', ','])

# print(is_monotonic(sorted(vertexes)))
