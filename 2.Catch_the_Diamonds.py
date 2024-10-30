from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GLUT import GLUT_BITMAP_HELVETICA_18
import random

# Window dimensions
W_Width, W_Height = 800, 600

# Catcher attributes
catcherWidth = 50
catcherHeight = 20
catcherX = W_Width // 2

# Diamond attributes
diamondSize = 20
diamondX = random.randint(0, W_Width - diamondSize)
diamondY = W_Height

# Game state
score = 0
isGameOver = False
isPaused = True
fallingSpeed = 2

def to_zone_0(x, y, zone):
    if zone == 0:
        return int(x), int(y)
    elif zone == 1:
        return int(y), int(x)
    elif zone == 2:
        return int(y), int(-x)
    elif zone == 3:
        return int(-x), int(y)
    elif zone == 4:
        return int(-x), int(-y)
    elif zone == 5:
        return int(-y), int(-x)
    elif zone == 6:
        return int(-y), int(x)
    elif zone == 7:
        return int(x), int(-y)

def from_zone_0(x, y, zone):
    if zone == 0:
        return int(x), int(y)
    elif zone == 1:
        return int(y), int(x)
    elif zone == 2:
        return int(-y), int(x)
    elif zone == 3:
        return int(-x), int(y)
    elif zone == 4:
        return int(-x), int(-y)
    elif zone == 5:
        return int(-y), int(-x)
    elif zone == 6:
        return int(y), int(-x)
    elif zone == 7:
        return int(x), int(-y)

def determine_zone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    if abs(dx) >= abs(dy):
        if dx >= 0 and dy >= 0:
            return 0
        elif dx < 0 and dy >= 0:
            return 3
        elif dx < 0 and dy < 0:
            return 4
        elif dx >= 0 and dy < 0:
            return 7
    else:
        if dx >= 0 and dy >= 0:
            return 1
        elif dx < 0 and dy >= 0:
            return 2
        elif dx < 0 and dy < 0:
            return 5
        elif dx >= 0 and dy < 0:
            return 6


def draw_line(x1, y1, x2, y2):
    zone = determine_zone(x1, y1, x2, y2)
    x1, y1 = to_zone_0(int(x1), int(y1), zone)
    x2, y2 = to_zone_0(int(x2), int(y2), zone)

    dx = x2 - x1
    dy = y2 - y1
    d = 2 * dy - dx
    incE = 2 * dy
    incNE = 2 * (dy - dx)

    y = y1
    glBegin(GL_POINTS)
    for x in range(x1, x2 + 1):
        original_x, original_y = from_zone_0(x, y, zone)
        glVertex2i(int(original_x), int(original_y))
        if d > 0:
            d += incNE
            y += 1
        else:
            d += incE
    glEnd()

def draw_catcher(x, y):
    glColor3f(1.0, 1.0, 1.0)
    draw_line(x+10 - catcherWidth // 2, y, x-10 + catcherWidth // 2, y)
    draw_line(x+10 - catcherWidth // 2, y, x - catcherWidth // 2, y + catcherHeight)
    draw_line(x-10 + catcherWidth // 2, y, x + catcherWidth // 2, y + catcherHeight)
    draw_line(x - catcherWidth // 2, y + catcherHeight, x + catcherWidth // 2, y + catcherHeight)

def draw_diamond(x, y):
    glColor3f(random.random(), random.random(), random.random())
    draw_line(x, y, x - diamondSize // 2, y - diamondSize // 2)
    draw_line(x, y, x + diamondSize // 2, y - diamondSize // 2)
    draw_line(x - diamondSize // 2, y - diamondSize // 2, x, y - diamondSize)
    draw_line(x + diamondSize // 2, y - diamondSize // 2, x, y - diamondSize)

def draw_text(x, y, text):
    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

def draw_left_arrow(x, y, width, height, color):
    glColor3f(*color)
    draw_line(x, y, x + width, y)
    draw_line(x, y, x+15, y-15 + height)
    draw_line(x, y, x+15, y+15 - height)
    
def draw_crossX(x, y, width, height, color):
    glColor3f(*color)
    draw_line(x, y, x + width, y+30)
    draw_line(x, y+30, x + width, y)

def draw_resume(x, y, width, height, color):
    glColor3f(*color)
    draw_line(x, y, x, y-40)
    draw_line(x-10+width, y, x-10+width, y-40)

def draw_pause(x, y, width, height, color):
    glColor3f(*color)
    draw_line(x, y, x-10+width, y+20)
    draw_line(x, y, x-10+width, y-20)
    draw_line(x-10+width, y+20, x-10+width, y-20)

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    global isGameOver, isPaused

    # Draw catcher
    if isGameOver:
        glColor3f(1.0, 0.0, 0.0)
    else:
        glColor3f(1.0, 1.0, 1.0)
    draw_catcher(catcherX, 50)

    # Draw diamond
    if not isGameOver and not isPaused:
        draw_diamond(diamondX, diamondY)

    # Draw buttons
    draw_left_arrow(10, W_Height - 30, 30, 30, (0.0, 1.0, 1.0))
    
    draw_crossX(W_Width - 40, W_Height - 40, 30, 30, (1.0, 0.0, 0.0))
    

    if not isGameOver and not isPaused:
        draw_resume(W_Width // 2 - 15, W_Height - 10, 30, 30, (1.0, 0.0, 0.0))
        
    else:
        draw_pause(W_Width // 2 - 15, W_Height - 30, 30, 30, (1.0, 0.65, 0.0))
        

    # Draw score
    glColor3f(1.0, 1.0, 1.0)
    draw_text(10, 10, f"Score: {score}")

    glutSwapBuffers()

def reshape(w, h):
    global W_Width, W_Height
    W_Width, W_Height = w, h
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, w, 0, h)
    glMatrixMode(GL_MODELVIEW)

def timer(value):
    global diamondY, isGameOver, diamondX, score, fallingSpeed

    if not isGameOver and not isPaused:
        diamondY -= fallingSpeed
        if diamondY <= 0:
            isGameOver = True
            print(f"Game Over. Score: {score}")
        elif catcherX - catcherWidth // 2 <= diamondX <= catcherX + catcherWidth // 2 and diamondY <= 50 + catcherHeight:
            score += 1
            print(f"Score: {score}")
            diamondY = W_Height
            diamondX = random.randint(0, W_Width - diamondSize)
            fallingSpeed += 0.1

    glutPostRedisplay()
    glutTimerFunc(16, timer, 0)

def keyboard(key, x, y):
    global catcherX, W_Width, catcherWidth, isPaused
    if key == GLUT_KEY_LEFT and catcherX > catcherWidth // 2:
        catcherX -= 10
    elif key == GLUT_KEY_RIGHT and catcherX < W_Width - catcherWidth // 2:
        catcherX += 10
    elif key == GLUT_KEY_UP:
        isPaused = not isPaused
    glutPostRedisplay()

def mouse(button, state, x, y):
    global isGameOver, score, fallingSpeed, diamondY, diamondX, isPaused, catcherX
    if state == GLUT_DOWN:
        if button == GLUT_LEFT_BUTTON:
            # Convert mouse coordinates
            y = W_Height - y
            if 10 <= x <= 40 and W_Height - 40 <= y <= W_Height - 10:
                isGameOver = False
                isPaused = False
                score = 0
                diamondY = W_Height
                diamondX = random.randint(0, W_Width - diamondSize)
                fallingSpeed = 2.0
                print("Starting Over")
            elif W_Width // 2 - 15 <= x <= W_Width // 2 + 15 and W_Height - 40 <= y <= W_Height - 10:
                isPaused = not isPaused
            elif W_Width - 40 <= x <= W_Width - 10 and W_Height - 40 <= y <= W_Height - 10:
                print(f"Goodbye. Score: {score}")
                glutLeaveMainLoop()

    glutPostRedisplay()

def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    gluOrtho2D(0, W_Width, 0, W_Height)

def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE)
    glutInitWindowSize(W_Width, W_Height)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Catch the Diamonds!")
    init()
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    # glutKeyboardFunc(keyboard)
    glutSpecialFunc(keyboard)
    glutMouseFunc(mouse)
    glutTimerFunc(0, timer, 0)
    glutMainLoop()

if __name__ == "__main__":
    main()
