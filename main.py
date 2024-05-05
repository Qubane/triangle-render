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
    slope1 = (x2 - x1) / (y2 - y1)
    slope2 = (x3 - x1) / (y3 - y1)

    xo1 = xo2 = x1

    for yo in range(int(y1), int(y2)):
        xo1 += slope1
        xo2 += slope2
        draw_line(win, xo1, yo, xo2, yo, val)

    # fill bottom triangle
    slope1 = (x3 - x1) / (y3 - y1)
    slope2 = (x3 - x2) / (y3 - y2)

    xo1 = xo2 = x3

    for yo in range(int(y3), int(y1), -1):
        xo1 -= slope1
        xo2 -= slope2
        draw_line(win, xo1, yo, xo2, yo, val)


def main():
    win = tr.Window()
    win.initialize(tr.Mode.palette8)
    while True:
        win.update()
        draw_filled(
            win,
            random() * win.width, random() * win.height,
            random() * win.width, random() * win.height,
            random() * win.width, random() * win.height,
            int(random() * 256)
        )
        sleep(0.5)


if __name__ == '__main__':
    main()
