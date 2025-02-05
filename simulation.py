"""
Momentum Simulation (Tkinter version)

Instructions:
1. In configuration mode (when the button says START), click on the center of a ball and then click outside it to draw a line to set the direction the ball will move.
2. Use the text boxes to set the mass and speed for each ball.
3. Click START to begin the simulation (the button will then say STOP). You can stop the simulation and reset by clicking STOP.
4. You may drag a ball (by clicking and dragging near its circle) to reposition it within the sandbox.

Note:
- Ported simulation from CodeSkulptor SimpleGUI code to Tkinter.
- Displayed numbers are limited to 3 decimal places.
- A solid guide circle is drawn inside each ball to show where to click.
    - You can reset the arrows on the corresponding ball by clicking on
      the ball, and dragging it around.
"""

import tkinter as tk
import math

# -------------------------
# Global Variables & Lists
# -------------------------
config_mode = True      # True = configuration mode; False = simulation running
collided = False
one_d = False           # if True, perform 1D collision calculations; otherwise use 2D resolution

counter = 0
counter2 = 0
draw_line = False
draw_line_2 = False
lines_1 = []            # stores arrow lines for ball_1 (each is a list: [start_point, end_point])
lines_2 = []            # stores arrow lines for ball_2
temp_line_1 = []        # temporary list for ball_1 arrow points
temp_line_2 = []        # temporary list for ball_2 arrow points

final_velocity1 = 0
final_velocity2 = 0

# -------------------------
# Ball Class Definition
# -------------------------
class Balls:
    def __init__(self, position, velocity, angle, mass, ball_move, ball_number, col):
        self.pos = list(position)
        self.velx = velocity
        self.vely = 0
        self.ang = angle
        self.mass = mass
        self.move = ball_move
        self.id = ball_number
        self.colour = col

    def draw(self, canvas):
        # Draw the main circle (radius = 10)
        x, y = self.pos
        r = 10
        canvas.create_oval(x - r, y - r, x + r, y + r,
                           outline=self.colour, width=2)
        # Draw a solid inner guide circle (radius = 5)
        inner_r = 5
        canvas.create_oval(x - inner_r, y - inner_r, x + inner_r, y + inner_r,
                           fill="gray", outline="gray")

    def update(self):
        # Only update the ball’s position when simulation is active (i.e. not in config mode)
        if not config_mode:
            self.pos[0] += self.velx
            self.pos[1] += self.vely

    def velocity_function(self, text_input):
        try:
            text_input = float(text_input)
        except:
            return
        if config_mode:
            if one_d:
                self.velx = text_input               
            else:
                # Set velocity components based on stored angle
                self.velx = text_input * math.cos(self.ang)
                self.vely = text_input * math.sin(self.ang)

    def mass_function(self, text_input):
        try:
            if config_mode:
                self.mass = float(text_input)
        except:
            pass

# -------------------------
# Physics Functions
# -------------------------
def calculate(m1, m2, v1, v2):
    global final_velocity1, final_velocity2
    final_velocity1 = ((m1 - m2) / (m1 + m2)) * v1 + ((2 * m2) / (m1 + m2)) * v2
    final_velocity2 = ((2 * m1) / (m1 + m2)) * v1 + ((m2 - m1) / (m1 + m2)) * v2

def resolve_collision(ball1, ball2):
    dx = ball2.pos[0] - ball1.pos[0]
    dy = ball2.pos[1] - ball1.pos[1]
    distance = math.sqrt(dx*dx + dy*dy)
    if distance == 0:
        return

    # normal and tangent vectors
    nx = dx / distance
    ny = dy / distance
    tx = -ny
    ty = nx

    # velocities in normal and tangential directions
    v1n = ball1.velx * nx + ball1.vely * ny
    v1t = ball1.velx * tx + ball1.vely * ty
    v2n = ball2.velx * nx + ball2.vely * ny
    v2t = ball2.velx * tx + ball2.vely * ty

    m1 = ball1.mass
    m2 = ball2.mass

    # new normal velocities after elastic collision
    v1n_after = ((m1 - m2) / (m1 + m2)) * v1n + ((2 * m2) / (m1 + m2)) * v2n
    v2n_after = ((2 * m1) / (m1 + m2)) * v1n + ((m2 - m1) / (m1 + m2)) * v2n

    # Tangential components remain unchanged.
    ball1.velx = v1n_after * nx + v1t * tx
    ball1.vely = v1n_after * ny + v1t * ty
    ball2.velx = v2n_after * nx + v2t * tx
    ball2.vely = v2n_after * ny + v2t * ty

def collision(position1, position2, radius):
    # Returns True if the circles (radius 10 each) are colliding given an extra margin.
    if math.sqrt((position1[0]-position2[0])**2 + (position1[1]-position2[1])**2) <= radius + 10:
        return True
    return False

def angle(ball_num):
    # Compute the angle from the ball’s current position to the endpoint of its last drawn arrow.
    if ball_num == 1 and lines_1:
        dx = lines_1[-1][1][0] - ball_1.pos[0]
        dy = lines_1[-1][1][1] - ball_1.pos[1]
        return math.atan2(dy, dx)
    if ball_num == 2 and lines_2:
        dx = lines_2[-1][1][0] - ball_2.pos[0]
        dy = lines_2[-1][1][1] - ball_2.pos[1]
        return math.atan2(dy, dx)
    return 0

def counter_reset():
    global counter, counter2
    counter = 0
    counter2 = 0

def reset():
    global collided
    ball_1.pos = [200, 250]
    ball_2.pos = [600, 250]
    ball_1.velx = 0
    ball_1.vely = 0
    ball_2.velx = 0
    ball_2.vely = 0
    lines_1.clear()
    lines_2.clear()
    counter_reset()
    collided = False

# -------------------------
# Event Handlers
# -------------------------
def on_mouse_click(event):
    global temp_line_1, temp_line_2, lines_1, lines_2, draw_line, draw_line_2, counter, counter2
    pos = (event.x, event.y)
    if config_mode:
        # For ball_1 arrow drawing:
        if not ball_2.move:
            if counter <= 2:
                # When clicking on the ball center, record the ball's current position.
                if (ball_1.pos[0] - 5 <= pos[0] <= ball_1.pos[0] + 5 and
                    ball_1.pos[1] - 5 <= pos[1] <= ball_1.pos[1] + 5):
                    if len(temp_line_1) == 0:
                        temp_line_1.append(tuple(ball_1.pos))
                        draw_line = True
                        counter += 1
                elif draw_line:
                    temp_line_1.append(pos)
                    lines_1.append(temp_line_1.copy())
                    ball_1.ang = angle(1)
                    temp_line_1.clear()
                    draw_line = False
                    counter += 1
        if ball_2.move:
            counter_reset()

        # For ball_2 arrow drawing:
        if not ball_1.move:
            if counter2 <= 2:
                if (ball_2.pos[0] - 5 <= pos[0] <= ball_2.pos[0] + 5 and
                    ball_2.pos[1] - 5 <= pos[1] <= ball_2.pos[1] + 5):
                    if len(temp_line_2) == 0:
                        temp_line_2.append(tuple(ball_2.pos))
                        draw_line_2 = True  
                        counter2 += 1
                elif draw_line_2:
                    temp_line_2.append(pos)
                    lines_2.append(temp_line_2.copy())
                    ball_2.ang = angle(2)
                    temp_line_2.clear()
                    draw_line_2 = False
                    counter2 += 1
        if ball_1.move:
            counter_reset()

    # Reset the "move" flags after a click.
    ball_1.move = False
    ball_2.move = False

def on_mouse_drag(event):
    pos = (event.x, event.y)
    if config_mode:
        # Drag ball_1 if the click is near its center:
        if not ball_1.move:
            if (ball_1.pos[0] - 30 <= pos[0] <= ball_1.pos[0] + 30 and
                ball_1.pos[1] - 30 <= pos[1] <= ball_1.pos[1] + 30):
                ball_1.pos = [pos[0], pos[1]]
                ball_2.move = True
                lines_1.clear()
                counter_reset()
        # Drag ball_2 similarly:
        if not ball_2.move:
            if (ball_2.pos[0] - 30 <= pos[0] <= ball_2.pos[0] + 30 and
                ball_2.pos[1] - 30 <= pos[1] <= ball_2.pos[1] + 30):
                ball_2.pos = [pos[0], pos[1]]
                ball_1.move = True
                lines_2.clear()
                counter_reset()

def toggle_simulation():
    """Toggle between configuration mode and simulation mode."""
    global config_mode, collided
    if config_mode:
        # Start simulation: clear any drawn arrows and change button text.
        config_mode = False
        toggle_button.config(text="STOP")
        lines_1.clear()
        lines_2.clear()
        counter_reset()
        collided = False
    else:
        # Stop simulation and reset.
        config_mode = True
        toggle_button.config(text="START")
        reset()
        counter_reset()

# -------------------------
# Drawing / Update Function
# -------------------------
def update():
    global collided, final_velocity1, final_velocity2
    # Clear canvas:
    canvas.delete("all")

    # Display information text for ball 1 (limit to 3 decimal places):
    m_text = f"Mass is {ball_1.mass:.3f}"
    v_text = f"X Speed is {ball_1.velx:.3f}"
    vy_text = f"Y Speed is {ball_1.vely:.3f}"
    canvas.create_text(100, 500, text=m_text, fill="red", font=("Arial", 16))
    canvas.create_text(100, 550, text=v_text, fill="red", font=("Arial", 16))
    canvas.create_text(100, 600, text=vy_text, fill="red", font=("Arial", 16))
    
    # Display information text for ball 2 (limit to 3 decimal places):
    m2_text = f"Mass 2 is {ball_2.mass:.3f}"
    v2_text = f"X Speed is {ball_2.velx:.3f}"
    vy2_text = f"Y Speed is {ball_2.vely:.3f}"
    canvas.create_text(450, 500, text=m2_text, fill="blue", font=("Arial", 16))
    canvas.create_text(450, 550, text=v2_text, fill="blue", font=("Arial", 16))
    canvas.create_text(450, 600, text=vy2_text, fill="blue", font=("Arial", 16))
    
    # Draw a line between the centers of the two balls.
    canvas.create_line(ball_1.pos[0], ball_1.pos[1], ball_2.pos[0], ball_2.pos[1], fill="white", width=2)
    
    # Draw the balls.
    ball_1.draw(canvas)
    ball_2.draw(canvas)
    
    # Draw the arrows for ball 1 and ball 2.
    # Use the current ball position as the starting point.
    for line in lines_1:
        canvas.create_line(ball_1.pos[0], ball_1.pos[1], line[1][0], line[1][1], fill="red", width=5)
    for line in lines_2:
        canvas.create_line(ball_2.pos[0], ball_2.pos[1], line[1][0], line[1][1], fill="blue", width=5)
    
    # Error messages for bad mass values.
    if ball_1.mass == 0:
        canvas.create_text(200, 150, text="YOU CAN'T USE 0", fill="red", font=("Arial", 12))
    if ball_1.mass < 0:
        canvas.create_text(50, 150, text="YOU CAN'T HAVE NEGATIVE MASS", fill="red", font=("Arial", 18))
    if ball_2.mass == 0:
        canvas.create_text(600, 150, text="YOU CAN'T USE 0", fill="red", font=("Arial", 12))
    if ball_2.mass < 0:
        canvas.create_text(450, 150, text="YOU CAN'T HAVE NEGATIVE MASS", fill="blue", font=("Arial", 18))
    
    # In configuration mode, update ball parameters from the entry fields.
    if config_mode:
        m_val = mass1_entry.get()
        if m_val != "":
            try:
                ball_1.mass = float(m_val)
            except:
                pass
        m2_val = mass2_entry.get()
        if m2_val != "":
            try:
                ball_2.mass = float(m2_val)
            except:
                pass
        v_val = velocity1_entry.get()
        if v_val != "":
            try:
                v_val = float(v_val)
                if one_d:
                    ball_1.velx = v_val
                else:
                    ball_1.velx = v_val * math.cos(ball_1.ang)
                    ball_1.vely = v_val * math.sin(ball_1.ang)
            except:
                pass
        v2_val = velocity2_entry.get()
        if v2_val != "":
            try:
                v2_val = float(v2_val)
                if one_d:
                    ball_2.velx = v2_val
                else:
                    ball_2.velx = v2_val * math.cos(ball_2.ang)
                    ball_2.vely = v2_val * math.sin(ball_2.ang)
            except:
                pass
    else:
        # When simulation is running, update positions and resolve collisions.
        if collision(ball_1.pos, ball_2.pos, 20):
            if one_d:
                calculate(ball_1.mass, ball_2.mass, ball_1.velx, ball_2.velx)
                ball_1.velx = final_velocity1
                ball_2.velx = final_velocity2
            else:
                if not collided:
                    resolve_collision(ball_1, ball_2)
                    collided = True
        else:
            collided = False

        ball_1.update()
        ball_2.update()
    
    # Schedule the next update (20 ms ~ 50 frames per second)
    root.after(20, update)

# -------------------------
# Create Ball Objects
# -------------------------
ball_1 = Balls([200, 250], 0, 0, 1, False, 1, "red")
ball_2 = Balls([600, 250], 0, 0, 1, False, 2, "blue")

# -------------------------
# Build the Tkinter GUI
# -------------------------
root = tk.Tk()
root.title("Momentum Simulation")

# Create the canvas.
canvas = tk.Canvas(root, width=800, height=800, bg="white")
canvas.pack()

# Create a control frame for input fields and button.
control_frame = tk.Frame(root)
control_frame.pack(pady=10)

# Mass and velocity entries for ball 1 and ball 2.
tk.Label(control_frame, text="Mass 1:").grid(row=0, column=0, padx=5, pady=2)
mass1_entry = tk.Entry(control_frame, width=10)
mass1_entry.grid(row=0, column=1, padx=5, pady=2)
mass1_entry.insert(0, "1")

tk.Label(control_frame, text="Mass 2:").grid(row=0, column=2, padx=5, pady=2)
mass2_entry = tk.Entry(control_frame, width=10)
mass2_entry.grid(row=0, column=3, padx=5, pady=2)
mass2_entry.insert(0, "1")

tk.Label(control_frame, text="Velocity 1:").grid(row=1, column=0, padx=5, pady=2)
velocity1_entry = tk.Entry(control_frame, width=10)
velocity1_entry.grid(row=1, column=1, padx=5, pady=2)
velocity1_entry.insert(0, "0")

tk.Label(control_frame, text="Velocity 2:").grid(row=1, column=2, padx=5, pady=2)
velocity2_entry = tk.Entry(control_frame, width=10)
velocity2_entry.grid(row=1, column=3, padx=5, pady=2)
velocity2_entry.insert(0, "0")

# Button to start/stop simulation.
toggle_button = tk.Button(control_frame, text="START", width=12, command=toggle_simulation)
toggle_button.grid(row=2, column=1, columnspan=2, pady=5)

# Bind mouse events on the canvas.
canvas.bind("<Button-1>", on_mouse_click)
canvas.bind("<B1-Motion>", on_mouse_drag)

# -------------------------
# Start the Update Loop
# -------------------------
update()  # kick off the periodic update
root.mainloop()
