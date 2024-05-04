import TerminalRender as tr
from time import sleep
from random import random


def draw_line(win: tr.Window, x1, y1, x2, y2, val=1):
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


def draw_outline(win: tr.Window, x1, y1, x2, y2, x3, y3, val=1):
    draw_line(win, x1, y1, x2, y2, val)
    draw_line(win, x2, y2, x3, y3, val)
    draw_line(win, x3, y3, x1, y1, val)


def main():
    win = tr.Window()
    win.initialize(tr.Mode.palette8)
    while True:
        win.update()
        draw_outline(
            win,
            random() * win.width, random() * win.height,
            random() * win.width, random() * win.height,
            random() * win.width, random() * win.height,
            int(random() * 256)
        )
        sleep(0.5)


if __name__ == '__main__':
    main()
