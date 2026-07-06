import pygame
import OpenGL.GL as gl

WIDTH = 1280
HEIGHT = 720


def main():
    pygame.init()
    pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF | pygame.OPENGL)

    running = True

    points = bla_line(640, 360, 300, 300)
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


def bla_line(x1, y1, x2, y2):
    points = []
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    sx = 1 if x2 > x1 else -1
    sy = 1 if y2 > y1 else -1

    if dx >= dy:
        p = 2 * dy - dx
        x, y = x1, y1
        for _ in range(dx + 1):
            points.append((x, y))
            if p < 0:
                p += 2 * dy
            else:
                y += sy
                p += 2 * dy - 2 * dx
            x += sx
    else:
        p = 2 * dx - dy
        x, y = x1, y1
        for _ in range(dy + 1):
            points.append((x, y))
            if p < 0:
                p += 2 * dx
            else:
                x += sx
                p += 2 * dx - 2 * dy
            y += sy

    return points


def to_ndc(x, y):
    x_ndc = (2 * x / WIDTH) - 1
    y_ndc = (2 * y / HEIGHT) - 1

    return x_ndc, y_ndc


if __name__ == "__main__":
    main()
