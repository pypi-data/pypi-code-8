'''
Collection of general calculation functions.
'''


def intersect(x, y1, y2):
    if y1[0] == y2[0]:
        return x[0]
    start = y1[0] > y2[0]
    left = x[0]
    for xp, c1, c2 in zip(x[1:], y1[1:], y2[1:]):
        if (c1 == c2):
            return xp
        if (start or c1 > c2) and not (start and c1 > c2):
            break
        left = xp
    else:
        return None
