import pygame
from pygame.locals import DOUBLEBUF, OPENGL
import OpenGL.GL as gl
from OpenGL.GLU import gluOrtho2D

WIDTH, HEIGHT = 600, 600

# clip window
XMIN, XMAX = -100, 100
YMIN, YMAX = -100, 100

# region codes
INSIDE = 0   # 0000
LEFT = 1   # 0001
RIGHT = 2   # 0010
BOTTOM = 4   # 0100
TOP = 8   # 1000


def compute_code(x, y):
    code = INSIDE
    if x < XMIN:
        code |= LEFT
    elif x > XMAX:
        code |= RIGHT
    if y < YMIN:
        code |= BOTTOM
    elif y > YMAX:
        code |= TOP
    return code


def cohen_sutherland_clip(x1, y1, x2, y2):
    code1 = compute_code(x1, y1)
    code2 = compute_code(x2, y2)

    x = 0
    y = 0

    while True:
        if code1 == 0 and code2 == 0:
            return x1, y1, x2, y2

        if code1 & code2 != 0:
            return None

        code_out = code1 if code1 != 0 else code2

        if code_out & TOP:
            x = x1 + (x2 - x1) * (YMAX - y1) / (y2 - y1)
            y = YMAX
        elif code_out & BOTTOM:
            x = x1 + (x2 - x1) * (YMIN - y1) / (y2 - y1)
            y = YMIN
        elif code_out & RIGHT:
            y = y1 + (y2 - y1) * (XMAX - x1) / (x2 - x1)
            x = XMAX
        elif code_out & LEFT:
            y = y1 + (y2 - y1) * (XMIN - x1) / (x2 - x1)
            x = XMIN

        if code_out == code1:
            x1, y1 = x, y
            code1 = compute_code(x1, y1)
        else:
            x2, y2 = x, y
            code2 = compute_code(x2, y2)


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
    pygame.display.set_caption("Cohen-Sutherland Line Clipping")

    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity()
    gluOrtho2D(-200, 200, -200, 200)
    gl.glMatrixMode(gl.GL_MODELVIEW)

    x1, y1, x2, y2 = -50, 0, 50, 0
    clipped = cohen_sutherland_clip(x1, y1, x2, y2)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        draw_rect(XMIN, YMIN, XMAX, YMAX, (0.4, 0.4, 0.4))   # clip window
        draw_line(x1, y1, x2, y2, (1, 0, 0))                 # original line

        if clipped:
            cx1, cy1, cx2, cy2 = clipped
            draw_line(cx1, cy1, cx2, cy2, (1, 1, 1))         # clipped line

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
