import pygame
import OpenGL.GL as gl

WIDTH = 1280
HEIGHT = 720


def main():
    pygame.init()
    pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF | pygame.OPENGL)

    running = True

    points = midpoint_circle(640, 360, 300)
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


def midpoint_circle(cx, cy, r):
    points = []

    def plot_octants(cx, cy, x, y):
        offsets = [
            (x, y), (-x, y), (x, -y), (-x, -y),
            (y, x), (-y, x), (y, -x), (-y, -x),
        ]
        for ox, oy in offsets:
            points.append((cx + ox, cy + oy))

    x = 0
    y = r
    p = 1 - r
    plot_octants(cx, cy, x, y)

    while x < y:
        x += 1
        if p < 0:
            p += 2 * x + 1
        else:
            y -= 1
            p += 2 * x - 2 * y + 1
        plot_octants(cx, cy, x, y)

    return points


def to_ndc(x, y):
    x_ndc = (2 * x / WIDTH) - 1
    y_ndc = (2 * y / HEIGHT) - 1

    return x_ndc, y_ndc


if __name__ == "__main__":
    main()
