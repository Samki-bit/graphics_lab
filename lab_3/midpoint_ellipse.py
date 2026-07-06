import OpenGL.GL as gl
import pygame

WIDTH = 1280
HEIGHT = 720


def main():
    pygame.init()
    pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF | pygame.OPENGL)

    running = True

    points = midpoint_ellipse(640, 360, 300, 200)
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


def midpoint_ellipse(cx, cy, rx, ry):
    points = []

    def plot_quadrants(cx, cy, x, y):
        offsets = [
            (x, y), (-x, y), (x, -y), (-x, -y),
        ]
        for ox, oy in offsets:
            points.append((cx + ox, cy + oy))

    rx2 = rx * rx
    ry2 = ry * ry

    # Region 1
    x = 0
    y = ry
    p1 = ry2 - (rx2 * ry) + (0.25 * rx2)
    plot_quadrants(cx, cy, x, y)

    dx = 2 * ry2 * x
    dy = 2 * rx2 * y

    while dx < dy:
        x += 1
        dx += 2 * ry2
        if p1 < 0:
            p1 += ry2 + dx
        else:
            y -= 1
            dy -= 2 * rx2
            p1 += ry2 + dx - dy
        plot_quadrants(cx, cy, x, y)

    # Region 2
    p2 = (ry2 * (x + 0.5) ** 2) + (rx2 * (y - 1) ** 2) - (rx2 * ry2)

    while y > 0:
        y -= 1
        dy -= 2 * rx2
        if p2 > 0:
            p2 += rx2 - dy
        else:
            x += 1
            dx += 2 * ry2
            p2 += rx2 - dy + dx
        plot_quadrants(cx, cy, x, y)

    return points


def to_ndc(x, y):
    x_ndc = (2 * x / WIDTH) - 1
    y_ndc = (2 * y / HEIGHT) - 1

    return x_ndc, y_ndc


if __name__ == "__main__":
    main()
