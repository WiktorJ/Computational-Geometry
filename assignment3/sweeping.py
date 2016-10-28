import math

from assignment3.generator import get_random_segments
from assignment3.sweep_elements import Segment, Point, Event, EventType, StateSegment
from custom_file_utils import read_file_to_tuples, write_tuple_to_file
from sortedcontainers import sortedset


def read_file_to_event_list(path):
    segments_as_tuples = read_file_to_tuples(path)
    return map(lambda points: Segment.from_tuple(points), segments_as_tuples)


def sweep(data_set):
    events = sortedset.SortedSet([e for segment in data_set for e in [Event(segment.start, [segment], EventType.start),
                                                                      Event(segment.end, [segment], EventType.end)]],
                                 key=lambda event: event.point.x)
    state = sortedset.SortedList()
    # TODO: check if there is more segments with the same starting point.x
    # first_event = events[0].segments[0]

    # sortedset.SortedList().add(StateSegment(first_event))
    while len(events):
        event = events.pop()
        if event.type == EventType.start:
            # TODO: Check if there is more segments
            segment = event.segments[0]
            state.add(StateSegment(segment))
            index = state.index(segment)


    return 'xD'


sweep(get_random_segments(0, 10, 100))
# write_tuple_to_file('test.csv', map(lambda segment: segment.to_tuple(), get_random_segments(0, 10, 100)))
