import pygame
from pygame.locals import DOUBLEBUF, OPENGL
import OpenGL.GL as gl
from OpenGL.GLU import gluOrtho2D

WIDTH, HEIGHT = 600, 600

# Clip window
XMIN, XMAX = -100, 100
YMIN, YMAX = -100, 100

CLIP_EDGES = ["LEFT", "RIGHT", "BOTTOM", "TOP"]


def inside(p, edge):
    x, y = p
    if edge == "LEFT":
        return x >= XMIN
    if edge == "RIGHT":
        return x <= XMAX
    if edge == "BOTTOM":
        return y >= YMIN
    if edge == "TOP":
        return y <= YMAX


def intersect(p1, p2, edge):
    x1, y1 = p1
    x2, y2 = p2

    if edge in ("LEFT", "RIGHT"):
        x = XMIN if edge == "LEFT" else XMAX
        t = (x - x1) / (x2 - x1)
        y = y1 + t * (y2 - y1)
        return (x, y)
    else:
        y = YMIN if edge == "BOTTOM" else YMAX
        t = (y - y1) / (y2 - y1)
        x = x1 + t * (x2 - x1)
        return (x, y)


def clip_polygon(polygon):
    output = polygon

    for edge in CLIP_EDGES:
        input_list = output
        output = []
        if not input_list:
            break

        n = len(input_list)
        for i in range(n):
            current = input_list[i]
            previous = input_list[i - 1]

            current_in = inside(current, edge)
            previous_in = inside(previous, edge)

            if current_in:
                if not previous_in:
                    output.append(intersect(previous, current, edge))
                output.append(current)
            elif previous_in:
                output.append(intersect(previous, current, edge))

    return output


def draw_rect(xmin, ymin, xmax, ymax, color):
    gl.glColor3f(*color)
    gl.glBegin(gl.GL_LINE_LOOP)
    gl.glVertex2f(xmin, ymin)
    gl.glVertex2f(xmax, ymin)
    gl.glVertex2f(xmax, ymax)
    gl.glVertex2f(xmin, ymax)
    gl.glEnd()


def draw_polygon(points, color):
    if not points:
        return
    gl.glColor3f(*color)
    gl.glBegin(gl.GL_LINE_LOOP)
    for x, y in points:
        gl.glVertex2f(x, y)
    gl.glEnd()


def main():
    pygame.init()
    pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Sutherland-Hodgeman Polygon Clipping")

    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity()
    gluOrtho2D(-200, 200, -200, 200)
    gl.glMatrixMode(gl.GL_MODELVIEW)

    subject_polygon = [(-120, -60), (0, 150), (120, 150), (120, -60),]
    clipped_polygon = clip_polygon(subject_polygon)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        draw_rect(XMIN, YMIN, XMAX, YMAX, (0.4, 0.4, 0.4))     # clip window
        draw_polygon(subject_polygon, (1, 0, 0))               # original
        draw_polygon(clipped_polygon, (1, 1, 1))             # clipped

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
