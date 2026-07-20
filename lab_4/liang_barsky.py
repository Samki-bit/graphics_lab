import pygame
from pygame.locals import DOUBLEBUF, OPENGL
import OpenGL.GL as gl
from OpenGL.GLU import gluOrtho2D

WIDTH, HEIGHT = 600, 600

# clip window
XMIN, XMAX = -100, 100
YMIN, YMAX = -100, 100


def liang_barsky_clip(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    p = [-dx, dx, -dy, dy]
    q = [x1 - XMIN, XMAX - x1, y1 - YMIN, YMAX - y1]

    t0, t1 = 0.0, 1.0

    for i in range(4):
        if p[i] == 0:
            if q[i] < 0:
                return None
        else:
            t = q[i] / p[i]
            if p[i] < 0:
                t0 = max(t0, t)
            else:
                t1 = min(t1, t)

    if t0 > t1:
        return None

    cx1 = x1 + t0 * dx
    cy1 = y1 + t0 * dy
    cx2 = x1 + t1 * dx
    cy2 = y1 + t1 * dy
    return cx1, cy1, cx2, cy2


def draw_rect(xmin, ymin, xmax, ymax, color):
    gl.glColor3f(*color)
    gl.glBegin(gl.GL_LINE_LOOP)
    gl.glVertex2f(xmin, ymin)
    gl.glVertex2f(xmax, ymin)
    gl.glVertex2f(xmax, ymax)
    gl.glVertex2f(xmin, ymax)
    gl.glEnd()


def draw_line(x1, y1, x2, y2, color):
    gl.glColor3f(*color)
    gl.glBegin(gl.GL_LINES)
    gl.glVertex2f(x1, y1)
    gl.glVertex2f(x2, y2)
    gl.glEnd()


def main():
    pygame.init()
    pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Liang-Barsky Line Clipping")

    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity()
    gluOrtho2D(-200, 200, -200, 200)
    gl.glMatrixMode(gl.GL_MODELVIEW)

    x1, y1, x2, y2 = -150, -50, 150, 80
    clipped = liang_barsky_clip(x1, y1, x2, y2)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        draw_rect(XMIN, YMIN, XMAX, YMAX, (0.4, 0.4, 0.4))   # clip window
        draw_line(x1, y1, x2, y2, (1, 0, 0))                 # original

        if clipped:
            cx1, cy1, cx2, cy2 = clipped
            draw_line(cx1, cy1, cx2, cy2, (1, 1, 1))         # clipped

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
