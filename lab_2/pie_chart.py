import pygame
import math
import OpenGL.GL as gl
data = [30, 20, 25, 25]
colors = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0)]

pygame.init()
pygame.display.set_mode((800, 600), pygame.DOUBLEBUF | pygame.OPENGL)

total = sum(data)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    gl.glClear(gl.GL_COLOR_BUFFER_BIT)

    start = 0
    for value, color in zip(data, colors):
        end = start + (value/total)*360

        gl.glColor3f(*color)
        gl.glBegin(gl.GL_TRIANGLE_FAN)
        gl.glVertex2f(0, 0)

        angle = start
        while angle <= end:
            rad = math.radians(angle)
            gl.glVertex2f(0.6*math.cos(rad), 0.6*math.sin(rad))
            angle += 1

        gl.glEnd()
        start = end

    pygame.display.flip()

pygame.quit()
