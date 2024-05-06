import math
import termrender as tr
from time import sleep
from random import random


def draw_line(win: tr.Window, x1, y1, x2, y2, val):
    """
    Function that draws a line.
    :param win: window
    :param x1: start x
    :param y1: start y
    :param x2: end x
    :param y2: end y
    :param val: what value to plot
    """

    # naive implementation makes me able to not turn my brain on
    # that's why we shall use that instead

    # calculate deltas
    dx = x2 - x1
    dy = y2 - y1

    # calculate biggest delta, and steps
    if abs(dx) > abs(dy):
        length = abs(dx)
        sx = 1 if dx > 0 else -1
        sy = dy / length
    else:
        length = abs(dy)
        sx = dx / length
        sy = 1 if dy > 0 else -1

    # plot the pixels
    for _ in range(int(length)):
        # plot pixel
        win.plot(int(x1), int(y1), val)

        # offset the coords
        x1 += sx
        y1 += sy


def draw_outline(win: tr.Window, x1, y1, x2, y2, x3, y3, val):
    """
    Draws triangle outline
    :param win: window
    :param x1: p1 x
    :param y1: p1 y
    :param x2: p2 x
    :param y2: p2 y
    :param x3: p3 x
    :param y3: p3 y
    :param val: value to plot
    """

    draw_line(win, x1, y1, x2, y2, val)
    draw_line(win, x2, y2, x3, y3, val)
    draw_line(win, x3, y3, x1, y1, val)


def draw_filled(win: tr.Window, x1, y1, x2, y2, x3, y3, val):
    """
    Draws filled triangle
    :param win: window
    :param x1: p1 x
    :param y1: p1 y
    :param x2: p2 x
    :param y2: p2 y
    :param x3: p3 x
    :param y3: p3 y
    :param val: value to plot
    """

    # sort the points from top to bottom
    if y2 < y1:
        x2, y2, x1, y1 = x1, y1, x2, y2
    if y3 < y1:
        x3, y3, x1, y1 = x1, y1, x3, y3
    if y3 < y2:
        x3, y3, x2, y2 = x2, y2, x3, y3

    # fill top triangle
    slope1 = (x2 - x1) / (y2 - y1) if y2 - y1 != 0 else 0
    slope2 = (x3 - x1) / (y3 - y1) if y3 - y1 != 0 else 0

    xo1 = xo2 = x1

    for yo in range(int(y1), int(y2)):
        xo1 += slope1
        xo2 += slope2
        draw_line(win, xo1, yo, xo2, yo, val)

    # fill bottom triangle
    slope1 = (x3 - x1) / (y3 - y1) if y3 - y1 != 0 else 0
    slope2 = (x3 - x2) / (y3 - y2) if y3 - y2 != 0 else 0

    xo1 = xo2 = x3

    for yo in range(int(y3), int(y1), -1):
        xo1 -= slope1
        xo2 -= slope2
        draw_line(win, xo1, yo, xo2, yo, val)


def project_xyz(x, y, z) -> tuple[float, float]:
    """
    Simple projection method
    :param x: point x
    :param y: point y
    :param z: point z
    :return: x, y coords
    """

    return x / z * 80, y / z * 80


def rotate_x(x, y, z, angle) -> tuple[float, float, float]:
    """
    Rotates a point around X axis
    :param x: point x
    :param y: point y
    :param z: point z
    :param angle: angles (radians)
    :return: tuple which contains rotated point
    """

    return x, y * math.cos(angle) - z * math.sin(angle), z * math.cos(angle) + y * math.sin(angle)


def rotate_y(x, y, z, angle) -> tuple[float, float, float]:
    """
    Rotates a point around Y axis
    :param x: point x
    :param y: point y
    :param z: point z
    :param angle: angles (radians)
    :return: tuple which contains rotated point
    """

    return x * math.cos(angle) - z * math.sin(angle), y, z * math.cos(angle) + x * math.sin(angle)


def rotate_z(x, y, z, angle) -> tuple[float, float, float]:
    """
    Rotates a point around Z axis
    :param x: point x
    :param y: point y
    :param z: point z
    :param angle: angles (radians)
    :return: tuple which contains rotated point
    """

    return x * math.cos(angle) - y * math.sin(angle), y * math.cos(angle) + x * math.sin(angle), z


def draw_cube(win: tr.Window, x, y, z, xo, yo, zo, rx, ry, rz, val):
    """
    Draws a cube
    :param win: window
    :param x: pos x
    :param y: pos y
    :param z: pos z
    :param xo: x offset
    :param yo: y offset
    :param zo: z offset
    :param rx: x rotation
    :param ry: y rotation
    :param rz: z rotation
    :param val: value
    """

    polys = [
        # front
        [(-x, y, -z), (x, y, -z), (x, -y, -z)],
        [(-x, y, -z), (x, -y, -z), (-x, -y, -z)],

        # back
        [(-x, y, z), (x, y, z), (x, -y, z)],
        [(-x, y, z), (x, -y, z), (-x, -y, z)],

        # left
        [(-x, y, -z), (-x, y, z), (-x, -y, z)],
        [(-x, y, -z), (-x, -y, z), (-x, -y, -z)],

        # right
        [(x, y, -z), (x, y, z), (x, -y, z)],
        [(x, y, -z), (x, -y, z), (x, -y, -z)],

        # top
        [(-x, y, z), (x, y, z), (x, y, -z)],
        [(-x, y, z), (x, y, -z), (-x, y, -z)],

        # bottom
        [(-x, -y, z), (x, -y, z), (x, -y, -z)],
        [(-x, -y, z), (x, -y, -z), (-x, -y, -z)],
    ]

    w, h = win.width // 2, win.height // 2
    for idx, poly in enumerate(polys):
        x, y, z = rotate_x(poly[0][0], poly[0][1], poly[0][2], rx)
        x, y, z = rotate_y(x, y, z, ry)
        x, y, z = rotate_y(x, y, z, rz)
        x1, y1 = project_xyz(x + xo, y + yo, z + zo)

        x, y, z = rotate_x(poly[1][0], poly[1][1], poly[1][2], rx)
        x, y, z = rotate_y(x, y, z, ry)
        x, y, z = rotate_y(x, y, z, rz)
        x2, y2 = project_xyz(x + xo, y + yo, z + zo)

        x, y, z = rotate_x(poly[2][0], poly[2][1], poly[2][2], rx)
        x, y, z = rotate_y(x, y, z, ry)
        x, y, z = rotate_y(x, y, z, rz)
        x3, y3 = project_xyz(x + xo, y + yo, z + zo)

        draw_outline(win, x1 + w, y1 + h, x2 + w, y2 + h, x3 + w, y3 + h, idx + 1)


def main():
    win = tr.Window()
    win.initialize(tr.Mode.palette8)
    count = 0
    while True:
        draw_cube(win, 10, 10, 10, 0, 0, 100, count/30, count/30, count/30, 1)
        win.update()
        win.clear()
        count += 1
        sleep(0.0333)


if __name__ == '__main__':
    main()
