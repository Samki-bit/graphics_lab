import pygame
import OpenGL.GL as gl
import OpenGL.GLU as glu
import numpy as np
import math


WIDTH = 1280
HEIGHT = 720

# Homogenous line Matrix
line = np.array([[-150, 0],
                [0, 0],
                [1, 1]])


def rotate(angle):
    angle_radian = math.radians(angle)
    # Rotation Matrix
    R = np.array([[math.cos(angle_radian), -math.sin(angle_radian), 0],
                  [math.sin(angle_radian), math.cos(angle_radian), 0],
                  [0, 0, 1]])
    return R


def scale(sx, sy):
    # Scaling Matrix
    S = np.array([[sx, 0, 0],
                  [0, sy, 0],
                  [0, 0, 1]])
    return S


def x_shear(shx):
    # X Shearing Matrix
    Sh_x = np.array([[1, shx, 0],
                    [0, 1, 0],
                    [0, 0, 1]])
    return Sh_x


def translate(tx, ty):
    # Traslation Matrix
    T = np.array([[1, 0, tx],
                  [0, 1, ty],
                  [0, 0, 1]])
    return T


def composite_transformation(line):
    T1 = translate(100, 100)
    R = rotate(45)
    S = scale(2, 2)
    Sh_x = x_shear(1)

    # Transformed from right to left
    transformation = Sh_x @ S @ R @ T1 @ line

    return transformation


def main():
    pygame.init()
    pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF | pygame.OPENGL)

    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity()
    glu.gluOrtho2D(-640, 640, -360, 360)
    gl.glMatrixMode(gl.GL_MODELVIEW)

    transformed_line = composite_transformation(line)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        draw_line(line, (1, 1, 1))
        draw_line(transformed_line, (1, 1, 0))
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
