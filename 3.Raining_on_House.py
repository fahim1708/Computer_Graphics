import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import random

# Initialize Pygame and OpenGL
pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
gluOrtho2D(0, 800, 0, 600)

# Variables for rain and background
raindrops = [(random.randint(0, 800), random.randint(600, 1200)) for _ in range(100)]
direction = 0
bg_color = [0.0, 0.0, 0.0]
bg_target = [0.0, 0.0, 0.0]

def draw_house():
    glColor3f(1 - bg_color[0], 1 - bg_color[1], 1 - bg_color[2])
    glBegin(GL_LINES)
    # Draw the house (base rectangle)
    glVertex2f(300, 200)
    glVertex2f(500, 200)
    glVertex2f(500, 200)
    glVertex2f(500, 400)
    glVertex2f(500, 400)
    glVertex2f(300, 400)
    glVertex2f(300, 400)
    glVertex2f(300, 200)
    
    # Draw the roof (triangle)
    glVertex2f(300, 400)
    glVertex2f(400, 500)
    glVertex2f(400, 500)
    glVertex2f(500, 400)
    
    # Draw the door (small rectangle)
    glVertex2f(350, 200)
    glVertex2f(350, 300)
    glVertex2f(350, 300)
    glVertex2f(400, 300)
    glVertex2f(400, 300)
    glVertex2f(400, 200)
    
    # Draw the window (small square)
    glVertex2f(450, 300)
    glVertex2f(450, 350)
    glVertex2f(450, 350)
    glVertex2f(500, 350)
    glVertex2f(500, 350)
    glVertex2f(500, 300)
    glVertex2f(500, 300)
    glVertex2f(450, 300)
    glEnd()

def draw_rain():
    global raindrops
    glColor3f(1 - bg_color[0], 1 - bg_color[1], 1 - bg_color[2])
    glBegin(GL_LINES)
    for i in range(len(raindrops)):
        x, y = raindrops[i]
        glVertex2f(x, y)
        glVertex2f(x + direction, y - 20)
        raindrops[i] = (x + direction, y - 20)
        if y - 20 < 0:
            raindrops[i] = (random.randint(0, 800), 600)
    glEnd()

def update_bg_color():
    for i in range(3):
        if bg_color[i] < bg_target[i]:
            bg_color[i] += 0.01
        elif bg_color[i] > bg_target[i]:
            bg_color[i] -= 0.01
    glClearColor(bg_color[0], bg_color[1], bg_color[2], 1.0)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                direction -= 1
            if event.key == pygame.K_RIGHT:
                direction += 1
            if event.key == pygame.K_UP:  # Simulate night to day
                bg_target = [1.0, 1.0, 1.0]
            if event.key == pygame.K_DOWN:  # Simulate day to night
                bg_target = [0.0, 0.0, 0.0]

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    update_bg_color()
    draw_house()
    draw_rain()
    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()
