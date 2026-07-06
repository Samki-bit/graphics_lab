import pygame
import OpenGL.GL as gl

WIDTH = 1280
HEIGHT = 720

ORIGIN_X = 80
ORIGIN_Y = 100
BAR_WIDTH = 80
GAP = 20
MAX_BAR_HEIGHT = 380

COLORS = [
    (1.0, 0.2, 0.2),
    (0.2, 0.8, 0.2),
    (0.2, 0.4, 1.0),
    (1.0, 0.8, 0.0),
    (0.8, 0.2, 0.8),
    (0.0, 0.8, 0.8),
]

DATA = [40, 90, 60, 120, 75, 30]


def main():
    pygame.init()
    pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF | pygame.OPENGL)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        draw_histogram(DATA)
        pygame.display.flip()
    pygame.quit()


def dda_line(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    steps = int(max(abs(dx), abs(dy)))
    if steps == 0:
        return [(x1, y1)]
    x_inc = dx / steps
    y_inc = dy / steps
    points = []
    x, y = float(x1), float(y1)
    for _ in range(steps + 1):
        points.append((round(x), round(y)))
        x += x_inc
        y += y_inc
    return points


def to_ndc(x, y):
    x_ndc = (2 * x / WIDTH) - 1
    y_ndc = (2 * y / HEIGHT) - 1
    return x_ndc, y_ndc


def draw_line(x1, y1, x2, y2):
    gl.glBegin(gl.GL_POINTS)
    for x, y in dda_line(x1, y1, x2, y2):
        gl.glVertex2f(*to_ndc(x, y))
    gl.glEnd()


def draw_histogram(data):
    d_max = max(data)
    for i, value in enumerate(data):
        bar_h = int((value / d_max) * MAX_BAR_HEIGHT)
        x1 = ORIGIN_X + i * (BAR_WIDTH + GAP)
        x2 = x1 + BAR_WIDTH
        y1 = ORIGIN_Y
        y2 = ORIGIN_Y + bar_h
        color = COLORS[i % len(COLORS)]

        gl.glColor3f(*color)
        for scan_y in range(y1, y2):
            draw_line(x1, scan_y, x2, scan_y)

        gl.glColor3f(1.0, 1.0, 1.0)
        draw_line(x1, y1, x1, y2)
        draw_line(x2, y1, x2, y2)
        draw_line(x1, y2, x2, y2)

    total_width = len(data) * (BAR_WIDTH + GAP) - GAP
    gl.glColor3f(1.0, 1.0, 1.0)
    draw_line(ORIGIN_X - 5, ORIGIN_Y, ORIGIN_X + total_width + 5, ORIGIN_Y)


if __name__ == "__main__":
    main()
