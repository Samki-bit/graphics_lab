import pygame
import OpenGL.GL as gl

WIDTH = 1280
HEIGHT = 720


def main():
    pygame.init()
    pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF | pygame.OPENGL)

    running = True

    points = dda_line(640, 360, 300, 300)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        gl.glBegin(gl.GL_POINTS)
        for x, y in points:
            gl.glVertex2f(*to_ndc(x, y))
        gl.glEnd()
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


if __name__ == "__main__":
    main()
