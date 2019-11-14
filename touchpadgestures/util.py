import math


def dist_sqr(x1: float, y1: float, x2: float, y2: float):
    return (x1 - x2) ** 2 + (y1 - y2) ** 2


def rad2deg(x: float):
    return x * 180 / math.pi


def angle(x: float, y: float):
    deg = rad2deg(math.atan2(-y, x))
    return deg if deg >= 0 else 360 + deg


def angle_diff(a: float, b: float):
    d = math.fmod(a - b + 360, 360)
    return 360 - d if d > 180 else d
