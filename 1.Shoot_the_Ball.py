from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

# Global Variables
window_width, window_height = 800, 600
shooter_x = 0
shooter_radius = 25
bullet_radius = 5
bullets = []
falling_circles = []
score = 0
game_over = False
misses = 0
misfires = 0
max_misses = 3
max_misfires = 3
paused = False
initial_speed = 1  # Slow initial speed for falling circles
speed_increase_factor = 0.02  # Speed increases slowly over time
spawn_interval = 3000  # Initial interval (ms) to spawn new falling circles
last_spawn_time = 0  # Timer to control when to spawn new circles
circle_spawn_rate = 1  # Start with 1 ball falling
difficulty_time = 0  # Timer to control when to increase difficulty

# Circle Drawing Function using GL_POINTS
def draw_circle(x_center, y_center, radius):
    glBegin(GL_POINTS)

    # Start drawing from the top of the circle (zone 0)
    x = 0
    y = radius
    d = 1 - radius

    # Draw initial point (0, radius) in all zones
    for zone in range(8):
        x_sym, y_sym = from_zone_0(x, y, zone)
        glVertex2f(x_center + x_sym, y_center + y_sym)

    # Loop through the circle points using the midpoint algorithm
    while x < y:
        if d < 0:
            d += 2 * x + 3
        else:
            d += 2 * (x - y) + 5
            y -= 1
        x += 1

        # Draw points in all 8 zones using symmetry
        for zone in range(8):
            x_sym, y_sym = from_zone_0(x, y, zone)
            glVertex2f(x_center + x_sym, y_center + y_sym)

            # Draw the symmetric point for each zone
            x_sym, y_sym = from_zone_0(y, x, zone)
            glVertex2f(x_center + x_sym, y_center + y_sym)

    glEnd()

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

def draw_left_arrow(x, y, width, color):
    glColor3f(*color)
    draw_line(x, y, x + width, y)
    draw_line(x, y, x + 15, y-15)
    draw_line(x, y, x + 15, y + 15)

def draw_crossX(x, y, color):
    glColor3f(*color)
    draw_line(x, y, x+15, y+15)
    draw_line(x, y, x-15, y+15)
    draw_line(x, y, x-15, y-15)
    draw_line(x, y, x+15, y-15)

def draw_resume(x, y, color):
    glColor3f(*color)
    draw_line(x, y, x, y + 15)
    draw_line(x, y, x, y - 15)
    draw_line(x, y-15, x-15, y)
    draw_line(x, y+15, x-15, y)

def draw_pause(x, y, color):
    glColor3f(*color)
    draw_line(x, y, x, y + 15)
    draw_line(x, y, x, y - 15)
    draw_line(x-10, y, x - 10, y + 15)
    draw_line(x-10, y, x - 10, y - 15)

def display():
    global game_over, paused
    glClear(GL_COLOR_BUFFER_BIT)

    # Draw Control Buttons at the top of the screen
    glColor3f(0, 1, 1)  # Cyan color for buttons
    draw_left_arrow(-window_width // 2 + 40, window_height // 2 - 40, 30, (0, 0.5, 1))  # Left Arrow Button for Restart
    draw_crossX(window_width // 2 - 45, window_height // 2 - 45, (1, 0, 0))  # Cross Button for Closing the game

    # Pause/Resume Button
    if paused:
        draw_resume(0, window_height // 2 - 40, (1, 1, 0))  # Resume Button in Yellow
    else:
        draw_pause(0, window_height // 2 - 40, (1, 1, 0))  # Pause Button in Yellow

    if not game_over and not paused:
        # Draw Shooter Circle
        glColor3f(1, 1, 0)  # Yellow
        draw_circle(shooter_x, -window_height // 2 + shooter_radius, shooter_radius)

        # Draw Bullets
        glColor3f(1, 0, 0)  # Red
        for bullet in bullets:
            draw_circle(bullet['x'], bullet['y'], bullet_radius)

        # Draw Falling Circles
        glColor3f(0, 1, 0)  # Green
        for circle in falling_circles:
            draw_circle(circle['x'], circle['y'], circle['radius'])

    glutSwapBuffers()

def update(value):
    global bullets, falling_circles, score, game_over, misses, misfires, paused
    global initial_speed, difficulty_time, circle_spawn_rate, last_spawn_time, spawn_interval

    if not game_over and not paused:
        # Update Bullet Positions
        for bullet in bullets:
            bullet['y'] += 5

        # Update Falling Circles
        for circle in falling_circles:
            circle['y'] -= circle['speed']  # Use variable speed

        # Check for collisions between bullets and falling circles
        new_bullets = []
        for bullet in bullets:
            hit_any_circle = False
            for circle in falling_circles:
                if (bullet['x'] - circle['x']) ** 2 + (bullet['y'] - circle['y']) ** 2 <= (bullet_radius + circle['radius']) ** 2:
                    falling_circles.remove(circle)
                    score += 1
                    hit_any_circle = True
                    break  # Stop checking this bullet since it hit a circle

            # If the bullet hit a circle, remove it, otherwise check if it's off-screen
            if hit_any_circle:
                continue
            elif bullet['y'] <= window_height // 2:
                new_bullets.append(bullet)  # Bullet still on screen
            else:
                misfires += 1  # Bullet missed all circles and left screen
                if misfires >= max_misfires:
                    game_over = True
                    print("Game Over: Misfired too many times!")
                    print(f"Final Score: {score}")

        bullets = new_bullets

        # Remove off-screen falling circles and count misses
        new_falling_circles = []
        for circle in falling_circles:
            if circle['y'] - circle['radius'] < -window_height // 2:
                misses += 1
                if misses >= max_misses:
                    game_over = True
                    print("Game Over: Missed too many circles!")
                    print(f"Final Score: {score}")
                else:
                    new_falling_circles.append(circle)
            else:
                new_falling_circles.append(circle)
        falling_circles = new_falling_circles

        # Check if it's time to spawn a new circle
        current_time = glutGet(GLUT_ELAPSED_TIME)
        if current_time - last_spawn_time > spawn_interval:
            last_spawn_time = current_time
            falling_circles.append({
                'x': random.randint(-window_width // 2 + 50, window_width // 2 - 50),
                'y': window_height // 2,
                'radius': random.randint(20, 30),
                'speed': initial_speed  # Start with initial speed
            })

        # Difficulty progression: increase speed and decrease spawn interval over time
        difficulty_time += 1
        if difficulty_time % 500 == 0:  # Every few seconds, increase difficulty
            for circle in falling_circles:
                circle['speed'] += speed_increase_factor  # Increase speed over time
            spawn_interval = max(500, spawn_interval - 100)  # Reduce spawn interval, but not lower than 500 ms

    glutPostRedisplay()
    glutTimerFunc(16, update, 0)

# Keyboard Input for controlling shooter and shooting bullets
def keyboard(key, x, y):
    global shooter_x, bullets, misfires, game_over

    if game_over:
        return

    if key == b'a':  # Move shooter left
        shooter_x = max(shooter_x - 15, -window_width // 2 + shooter_radius)
    elif key == b'd':  # Move shooter right
        shooter_x = min(shooter_x + 15, window_width // 2 - shooter_radius)
    elif key == b' ':  # Shoot bullet
        bullets.append({'x': shooter_x, 'y': -window_height // 2 + shooter_radius + bullet_radius})
        # misfires += 1
        # if misfires >= max_misfires:
        #     game_over = True
        #     print("Game Over: Misfired too many times!")
        #     print(f"Final Score: {score}")

# Special Keys for Play/Pause and Restart
def special_keys(key, x, y):
    global paused, game_over, score, misses, misfires, falling_circles, bullets
    global initial_speed, circle_spawn_rate, difficulty_time, spawn_interval, last_spawn_time  # Add spawn_interval here

    if key == GLUT_KEY_LEFT:  # Restart the game
        score = 0
        misses = 0
        misfires = 0
        falling_circles = []
        bullets = []
        game_over = False
        initial_speed = 1  # Reset speed
        spawn_interval = 3000  # Reset spawn rate
        last_spawn_time = 0  # Reset last spawn time
        difficulty_time = 0  # Reset difficulty timer
        print("Starting Over")

    elif key == GLUT_KEY_UP:  # Play/Pause
        paused = not paused
        if paused:
            print("Game Paused")
        else:
            print("Game Resumed")

# Mouse Function to detect button clicks
def mouse(button, state, x, y):
    global paused, game_over, score, misses, misfires, falling_circles, bullets
    global initial_speed, circle_spawn_rate, difficulty_time, spawn_interval, last_spawn_time

    # Convert GLUT window coordinates to OpenGL coordinates
    opengl_x = x - window_width // 2
    opengl_y = window_height // 2 - y

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        # Check if left arrow button (restart) is clicked
        if -window_width // 2 + 40 <= opengl_x <= -window_width // 2 + 70 and window_height // 2 - 55 <= opengl_y <= window_height // 2 - 25:
            # Restart the game
            score = 0
            misses = 0
            misfires = 0
            falling_circles = []
            bullets = []
            game_over = False
            initial_speed = 1  # Reset speed
            spawn_interval = 3000  # Reset spawn rate
            last_spawn_time = 0  # Reset last spawn time
            difficulty_time = 0  # Reset difficulty timer
            print("Game Restarted")

        # Check if cross button (exit) is clicked
        if window_width // 2 - 60 <= opengl_x <= window_width // 2 - 30 and window_height // 2 - 60 <= opengl_y <= window_height // 2 - 30:
            on_exit()  # Exit game

        # Check if pause/resume button is clicked
        if -15 <= opengl_x <= 15 and window_height // 2 - 60 <= opengl_y <= window_height // 2 - 25:
            paused = not paused
            if paused:
                print("Game Paused")
            else:
                print("Game Resumed")

# Exit game on close button
def on_exit():
    global score
    print("Goodbye")
    print(f"Final Score: {score}")
    glutLeaveMainLoop()  # This properly exits the GLUT main loop and avoids sys.exit()

# Initialize OpenGL
def init():
    glClearColor(0, 0, 0, 1)
    gluOrtho2D(-window_width // 2, window_width // 2, -window_height // 2, window_height // 2)

# Main function
def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE)
    glutInitWindowSize(window_width, window_height)
    glutCreateWindow(b"Circle Shooter Game")

    glutDisplayFunc(display)
    glutTimerFunc(16, update, 0)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(special_keys)
    glutMouseFunc(mouse)  # Register the mouse function
    glutCloseFunc(on_exit)

    init()
    glutMainLoop()

if __name__ == "__main__":
    main()
