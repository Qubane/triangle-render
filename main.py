import math
import termrender as tr
from time import sleep


# 3d rendering
MESH = []
NEAR_CLIP = 10

# window
WIN = tr.Window()
WIN.initialize(tr.Mode.palette8)


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

    # if deltas are both 0, then return
    if dx == dy == 0:
        return

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
    for _ in range(int(length+0.99)):
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

    minx = min(x1, x2, x3)
    maxx = max(x1, x2, x3)

    # triangle has no height
    if y1 - y3 == 0:
        return

    # calculate second slope
    slope2 = (x3 - x1) / (y3 - y1)

    # check for top-flat triangle
    if y1 - y2 != 0:
        # fill top triangle
        slope1 = (x2 - x1) / (y2 - y1)

        xo1 = xo2 = x1
        for yo in range(int(y1), int(y2)+1):
            draw_line(win, xo1, yo, xo2, yo, val)
            xo1 += slope1
            xo2 += slope2
            if minx > xo1 or xo1 > maxx:
                xo1 = minx if xo1 < minx else maxx
            if minx > xo2 or xo2 > maxx:
                xo2 = minx if xo2 < minx else maxx

    # check for bottom-flat triangle
    if y2 - y3 != 0:
        # fill bottom triangle
        slope1 = (x3 - x2) / (y3 - y2)

        xo1 = xo2 = x3
        for yo in range(int(y3), int(y2)-1, -1):
            draw_line(win, xo1, yo, xo2, yo, val)
            xo1 -= slope1
            xo2 -= slope2
            if xo1 < minx or xo1 > maxx:
                xo1 = minx if xo1 < minx else maxx
            if xo1 < minx or xo2 > maxx:
                xo2 = minx if xo2 < minx else maxx


def project_xyz(x, y, z) -> tuple[float, float]:
    """
    Simple projection method
    :param x: point x
    :param y: point y
    :param z: point z
    :return: x, y coords
    """

    return x / z * 100, y / z * 100


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


def append_transformed_poly(poly, xo, yo, zo, rx, ry, rz):
    """
    Appends polygons to MESH
    :param poly:
    :param xo:
    :param yo:
    :param zo:
    :param rx:
    :param ry:
    :param rz:
    """

    transformed_poly = []

    x, y, z = rotate_x(poly[0][0], poly[0][1], poly[0][2], rx)
    x, y, z = rotate_y(x, y, z, ry)
    x, y, z = rotate_y(x, y, z, rz)
    vertex = (x + xo, y + yo, z + zo)
    transformed_poly.append(vertex)

    x, y, z = rotate_x(poly[1][0], poly[1][1], poly[1][2], rx)
    x, y, z = rotate_y(x, y, z, ry)
    x, y, z = rotate_y(x, y, z, rz)
    vertex = (x + xo, y + yo, z + zo)
    if z + zo > transformed_poly[0][2]:
        transformed_poly.insert(0, vertex)
    else:
        transformed_poly.append(vertex)

    x, y, z = rotate_x(poly[2][0], poly[2][1], poly[2][2], rx)
    x, y, z = rotate_y(x, y, z, ry)
    x, y, z = rotate_y(x, y, z, rz)
    vertex = (x + xo, y + yo, z + zo)
    if z + zo > transformed_poly[0][2]:
        transformed_poly.insert(0, vertex)
    elif z + zo > transformed_poly[1][2]:
        transformed_poly.insert(1, vertex)
    else:
        transformed_poly.append(vertex)

    MESH.append(transformed_poly)


def make_plane(x, y, xo, yo, zo, rx, ry, rz):
    """
    Generates a plane mesh
    :param x: pos x
    :param y: pos y
    :param xo: x offset
    :param yo: y offset
    :param zo: z offset
    :param rx: x rotation
    :param ry: y rotation
    :param rz: z rotation
    """

    polys = [
        [(-x, 0, y), (x, 0, y), (x, 0, -y)],
        [(-x, 0, y), (x, 0, -y), (-x, 0, -y)]
    ]
    for poly in polys:
        append_transformed_poly(poly, xo, yo, zo, rx, ry, rz)


def make_cube(x, y, z, xo, yo, zo, rx, ry, rz):
    """
    Generates a cube mesh
    :param x: pos x
    :param y: pos y
    :param z: pos z
    :param xo: x offset
    :param yo: y offset
    :param zo: z offset
    :param rx: x rotation
    :param ry: y rotation
    :param rz: z rotation
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
    for poly in polys:
        append_transformed_poly(poly, xo, yo, zo, rx, ry, rz)


def render_mesh():
    """
    Renders scene mesh
    """

    # sort everything
    MESH.sort(key=lambda x: (x[0][2]+x[1][2]+x[2][2])/3, reverse=True)

    # clipping
    idx = 0
    while idx < len(MESH):
        # fetch poly
        poly = MESH[idx]

        # ignore mesh that is fully behind the camera
        if poly[0][2] < NEAR_CLIP and poly[1][2] < NEAR_CLIP and poly[2][2] < NEAR_CLIP:
            idx += 1
            continue

        # ignore mesh that is fully in front of camera
        if poly[0][2] >= NEAR_CLIP and poly[1][2] >= NEAR_CLIP and poly[2][2] >= NEAR_CLIP:
            idx += 1
            continue

        # 2 vertices in front
        if poly[0][2] >= NEAR_CLIP and poly[1][2] >= NEAR_CLIP and poly[2][2] < NEAR_CLIP:
            pass

        # 1 vertex in front
        if poly[0][2] >= NEAR_CLIP and poly[1][2] < NEAR_CLIP and poly[2][2] < NEAR_CLIP:
            pass

        idx += 1

    # screen centering (to make 0, 0 in the middle)
    hw, hh = WIN.width // 2, WIN.height // 2

    # render
    for idx, poly in enumerate(MESH):
        # ignore mesh that is fully behind the camera
        if poly[0][2] < NEAR_CLIP and poly[1][2] < NEAR_CLIP and poly[2][2] < NEAR_CLIP:
            continue

        # calculate projected points
        x1, y1 = project_xyz(poly[0][0], poly[0][1], poly[0][2])
        x2, y2 = project_xyz(poly[1][0], poly[1][1], poly[1][2])
        x3, y3 = project_xyz(poly[2][0], poly[2][1], poly[2][2])

        # plot the triangle
        draw_filled(WIN, x1 + hw, y1 + hh, x2 + hw, y2 + hh, x3 + hw, y3 + hh, (idx + 1) % len(WIN.palette))

    # clear mesh
    MESH.clear()


def main():
    count = 0
    while True:
        # make_plane(40, 40, 0, 40, 100, 3.2, count / 50, 0)
        make_cube(10, 10, 10, 0, 0, 40, count/50, count/50, count/50)
        render_mesh()
        WIN.update()
        WIN.clear()
        count += 1
        sleep(0.0333)


if __name__ == '__main__':
    main()
