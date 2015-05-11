"""Arranges rectangles such that their bounding box approximates a particular
aspect ratio.

Example usage:

from aspackt import arrangement, AspectRatio

# some collection of items with width and height attributes
rectangles = [...]

# get a map of items -> top-left-coordinate
arranged = arrangement(rectangles, AspectRatio(4, 3))
"""

from collections import namedtuple

AspectRatio = namedtuple('AspectRatio', ['width', 'height'])
Box = namedtuple('Box', ['width', 'height'])
Coordinate = namedtuple('Coordinate', ['x', 'y'])

def area(i):
    return i.width * i.height

def next_item(items, smallest_wh_sum=True):
    largest_area = area(items[0])
    largest_items = [i for i in items if area(i) == largest_area]

    if len(largest_items) > 1:
        largest_items.sort(
            key=lambda i: i.width + i.height,
            reverse=smallest_wh_sum
        )
    return largest_items.pop()

def aspect_ratio_boxes(aspect_ratio):
    w_step, h_step = aspect_ratio
    width = height = 0
    while True:
        width += w_step
        height += h_step
        yield Box(width, height)

def smallest_fit_for(item, boxes):
    d = next(boxes)
    while d.width < item.width or d.height < item.height:
        d = next(boxes)
    return [
        [0 for x in range(d.width)]
        for y in range(d.height)
    ]

def insert_item_into_box_at(item, box, at):
    for y in range(item.height):
        for x in range(item.width):
            box[y+at.y][x+at.x] = 1

def find_fit(item, box):
    available_rows = [i for i, row in enumerate(box) if 0 in row]
    for ridx in available_rows:
        end_y = ridx + item.height
        if end_y >= len(box):
            break
        available_columns = [i for i, x in enumerate(box[ridx]) if x == 0]
        for cidx in available_columns:
            end_x = cidx + item.width
            if end_x >= len(box[ridx]):
                break
            test_row = [0 for x in range(item.width)]
            for i in range(item.height):
                if box[ridx + i][cidx:end_x] != test_row:
                    break
            else:
                return Coordinate(cidx, ridx)
    return None

class ItemArrangement(dict):
    def set_bounds(self, width, height):
        self.width = width
        self.height = height

def arrangement(coll, aspect_ratio=AspectRatio(4, 3)):
    """Given a collection of items return a map of item -> position.

    The positions returned will be such that the bounding box of the arrangement
    will approximate the given aspect ratio.

    Items are expected to have width and height attributes, the aspect ratio is
    expected to have x and y attributes. A named tuple, aspackt.AspectRatio
    exists for convenience.
    """
    items = coll.copy()
    items.sort(key=area, reverse=True)
    first_item = next_item(items, smallest_wh_sum=False)
    items.remove(first_item)

    final_coordinates = ItemArrangement()
    final_coordinates[first_item] =  Coordinate(0, 0)
    boxes = aspect_ratio_boxes(aspect_ratio)
    bounding_box = smallest_fit_for(first_item, boxes)
    final_coordinates.set_bounds(len(bounding_box[0]), len(bounding_box))
    insert_item_into_box_at(first_item, bounding_box, Coordinate(0, 0))

    while items:
        arrangee = next_item(items)
        items.remove(arrangee)

        coords = find_fit(arrangee, bounding_box)
        while coords is None:
            ratio_box = next(boxes)
            final_coordinates.set_bounds(ratio_box.width, ratio_box.height)
            line_additions = [
                0 for x in range(ratio_box.width - len(bounding_box[0]))
            ]
            for i, x in enumerate(bounding_box):
                bounding_box[i].extend(line_additions)
            for i in range(ratio_box.height - len(bounding_box)):
                bounding_box.append([0 for x in range(ratio_box.width)])
            coords = find_fit(arrangee, bounding_box)
        insert_item_into_box_at(arrangee, bounding_box, coords)
        final_coordinates[arrangee] = coords

    return final_coordinates
