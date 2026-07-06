import pygame
import OpenGL.GL as gl
import OpenGL.GLU as glu
import numpy as np


WIDTH = 1280
HEIGHT = 720

# Homogenous line Matrix
line = np.array([[-150, 100],
                [-150, 100],
                [1, 1]])


def x_shear(points, shx):
    # X Shearing Matrix
    Sh_x = np.array([[1, shx, 0],
                    [0, 1, 0],
                    [0, 0, 1]])
    return Sh_x @ points


def y_shear(points, shy):
    # Y Shearing Matrix
    Sh_y = np.array([[1, 0, 0],
                    [shy, 1, 0],
                    [0, 0, 1]])
    return Sh_y @ points


def main():
    pygame.init()
    pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF | pygame.OPENGL)

    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity()
    glu.gluOrtho2D(-640, 640, -360, 360)
    gl.glMatrixMode(gl.GL_MODELVIEW)

    sheared_x_line = x_shear(line, 2)
    sheared_y_line = y_shear(line, 1)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        draw_line(line, (1, 1, 1))
        draw_line(sheared_x_line, (1, 1, 0))
        draw_line(sheared_y_line, (0, 1, 1))
        pygame.display.flip()
    pygame.quit()


def draw_line(line, color):
    gl.glColor3f(*color)
    gl.glBegin(gl.GL_LINES)
    for i in range(line.shape[1]):
        x, y, w = line[:, i]
        gl.glVertex2f(x / w, y / w)
    gl.glEnd()


if __name__ == "__main__":
    main()
