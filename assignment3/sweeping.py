from assignment3.generator import get_random_segments, save_segments_to_file, get_segments_from_file
from assignment3.sweep_elements import Segment, Point, Event, EventType, StateSegment, \
    get_point_orientation_relative_to_line, ABOVE, BELOW, Intersection
from custom_file_utils import read_file_to_tuples, write_tuple_to_file, copy_file
from sortedcontainers import sortedset

intersections = set()
points = []


def read_file_to_event_list(path):
    segments_as_tuples = read_file_to_tuples(path)
    return map(lambda points: Segment.from_tuple(points), segments_as_tuples)


def get_above_neighbour(segment, state):
    index = state.index(segment)
    if index > 0:
        return state[index - 1].segment
    return None


def get_below_neighbour(segment, state):
    index = state.index(segment)
    if index < len(state) - 1:
        return state[index + 1].segment
    return None


def line(p1, p2):
    A = (p1.y - p2.y)
    B = (p2.x - p1.x)
    C = (p1.x * p2.y - p2.x * p1.y)
    return A, B, -C


def intersection(L1, L2, range_1, range_2):
    D = L1[0] * L2[1] - L1[1] * L2[0]
    Dx = L1[2] * L2[1] - L1[1] * L2[2]
    Dy = L1[0] * L2[2] - L1[2] * L2[0]
    if D != 0:
        x = Dx / D
        y = Dy / D
        if range_1[0] <= x <= range_1[1] and range_2[0] <= x <= range_2[1]:
            return x, y
        else:
            return None
    else:
        return None


def get_intersection_point(segment1, segment2, starting_orientation):
    orientation = get_point_orientation_relative_to_line(segment1.end, segment2)
    if orientation != starting_orientation:
        line1 = line(segment1.start, segment1.end)
        line2 = line(segment2.start, segment2.end)
        intersect = intersection(line1, line2, (segment1.start.x, segment1.end.x), (segment2.start.x, segment2.end.x))
        if intersect:
            return Point(intersect[0], intersect[1])
        return None
    return None


def add_intersection_if_exists(segment, neighbour, orientation, events):
    if neighbour and segment:
        point = get_intersection_point(segment, neighbour, orientation)
        if point:
            inter = Intersection(point, segment, neighbour)
            if inter not in intersections:
                intersections.add(inter)
                points.append(point)
                events.add(Event(point, [segment, neighbour], EventType.intersection))


def add_state_and_intersections(state, state_segment, events):
    state.add(state_segment)
    above_neighbour = get_above_neighbour(state_segment, state)
    below_neighbour = get_below_neighbour(state_segment, state)
    add_intersection_if_exists(state_segment.segment, above_neighbour, BELOW, events)
    add_intersection_if_exists(state_segment.segment, below_neighbour, ABOVE, events)


def make_snapshot(point, set_name, snapshot_count):
    write_tuple_to_file('results/' + set_name + '/snapshot' + str(snapshot_count) + '/intersections.csv',
                        map(lambda e: e.to_tuple(), intersections))
    write_tuple_to_file('results/' + set_name + '/snapshot' + str(snapshot_count) + '/point.csv', [point.to_tuple()])
    write_tuple_to_file('results/' + set_name + '/snapshot' + str(snapshot_count) + '/points.csv',
                        map(lambda e: e.to_tuple(), points))
    pass


def sweep(set_name):
    data_set_file_name = 'data_sets/' + set_name + '.csv'
    data_set = get_segments_from_file(data_set_file_name)
    copy_file(data_set_file_name, 'results/' + set_name + '/segments.csv')
    events_list = [e for segment in data_set for e in [Event(segment.start, [segment], EventType.start),
                                                       Event(segment.end, [segment], EventType.end)]]
    events = sortedset.SortedSet()
    for e in events_list:
        if e in events:
            print("Two segments intersecting at end or start")
            index = events.index(e)
            first_event = events[index]
            points.append(e.point)
            intersections.add(Intersection(e.point, e.segments[0], first_event.segments[0]))
        else:
            events.add(e)

    snapshot_count = 0
    state = sortedset.SortedList()
    # TODO: check if there is more segments with the same starting point.x
    # first_event = events[0].segments[0]

    # sortedset.SortedList().add(StateSegment(first_event))
    while len(events):
        event = events.pop(0)
        if event.type == EventType.start:
            # TODO: Check if there is more segments
            segment = event.segments[0]
            state_segment = StateSegment(segment)
            add_state_and_intersections(state, state_segment, events)
        elif event.type == EventType.end:
            segment = event.segments[0]
            state_segment = StateSegment(segment)
            above_neighbour = get_above_neighbour(state_segment, state)
            below_neighbour = get_below_neighbour(state_segment, state)
            if below_neighbour and below_neighbour.end == segment.end:
                state.remove(StateSegment(below_neighbour))
                below_neighbour = get_below_neighbour(state_segment, state)
            if above_neighbour and above_neighbour.end == segment.end:
                state.remove(StateSegment(above_neighbour))
                above_neighbour = get_below_neighbour(state_segment, state)
            state.remove(state_segment)
            add_intersection_if_exists(above_neighbour, below_neighbour, ABOVE, events)
        else:
            above_segment = StateSegment(event.segments[0])
            below_segment = StateSegment(event.segments[1])

            state.remove(above_segment)
            state.remove(below_segment)

            above_segment.orientation_point = event.point
            below_segment.orientation_point = event.point

            add_state_and_intersections(state, above_segment, events)

            add_state_and_intersections(state, below_segment, events)
        snapshot_count += 1
        make_snapshot(event.point, set_name, snapshot_count)

    print("Number of intersections: ", len(intersections))


# save_segments_to_file('data_sets/set5.csv', get_random_segments(0, 6, 15))
sweep("set6")
# sweep(get_random_segments(0, 10, 10))
# write_tuple_to_file('test.csv', map(lambda segment: segment.to_tuple(), get_random_segments(0, 10, 100)))
