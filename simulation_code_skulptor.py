"""
Momentum Simulation

This program shows what happens when two objects of different 
masses and velocities collide on an angle

Directions
1. Click on the centre of the ball on the left side, and click anywhere
   outside the ball. A line will appear, which will represent the 
   direction the left ball moves. Do the same for the ball on the right.
   
2. Enter in your mass and velocity values for the corresponding balls.

3. Press the start button, and enjoy!


Additional Notes and issues:
- You can reset the arrows on the corresponding ball by clicking on
  the ball, and dragging it around.

- You can reset the state of the game by pressing the stop button.

- If no arrows are made, the balls will travel straight in the x
  direction.
  
- Some issues with draw handler:
    - Sometimes when drawing the directions for the point masses, lines will fail to appear from origin.
"""

#imports
import simplegui
import simplegui as gui
import math
import time

#Lists
objects = []
lines_1 = []
temp_line_1 = []
temp_line_2 = []
lines_2 = []
object_v =[]

#Variables
final_velocity1 = 0
final_velocity2 = 0
running = True
draw_line = False
draw_line_2 = False
counter = 0
counter2 = 0
collided = False
one_d = False
check_1 = False
check_2 = False

#Object Class
class Balls:
    """Class representing a ball in the simulation."""
    def __init__(self, position, velocity, angle, mass, ball_move, ball_number, col):
        """Initialize the ball with position, velocity, angle, mass, movement flag, ID, and color."""
        self.pos = list(position)
        self.velx = velocity
        self.vely = 0
        self.ang = angle
        self.mass = mass
        self.move = ball_move
        self.id = ball_number
        self.colour = col
        
    def draw(self, canvas):
        """Draw the ball on the given canvas."""
        canvas.draw_circle(self.pos, 10, 2, self.colour)
        
    def update(self):
        """Update the ball's position based on its velocity if simulation is not running."""
        if running == False:
            self.pos[0] += self.velx
            self.pos[1] += self.vely
                
    def velocity_function(self, text_input):
        """Set the ball's velocity based on user input and stored direction angle."""
        text_input = float(text_input)
        if running==True:
            if one_d == True:
                self.velx = text_input               
            else:
                # Use the stored angle to set velocity in the direction of the arrow
                self.velx = text_input * math.cos(self.ang)
                self.vely = text_input * math.sin(self.ang)
                
    def mass_function(self, text_input):
        """Set the ball's mass based on user input."""
        if running==True:
            self.mass = float(text_input)

def run():
    """Toggle simulation running state when the start/stop button is pressed."""
    global running
    if running == False: 
        button_run.set_text("START")
        reset()
        counter_reset()
        running = True        
    else:
        lines_1.clear()
        lines_2.clear()
        button_run.set_text('STOP')
        running = False
        check_1 = False
        check_2 = False
        
        if one_d == True:
            calculate(ball_1.mass, ball_2.mass, ball_1.velx, ball_2.velx)
    
def counter_reset():
    """Reset the counters used for drawing lines."""
    global counter, counter2
    counter = 0
    counter2 = 0
    return counter, counter2

def mouseclick(position):  
    """Handle mouse click events to draw direction lines and set ball directions."""
    global temp_line_1, temp_line_2, lines_1, lines_2, draw_line, draw_line_2, counter, counter2
    if running == True:
        if (ball_2.move == False):
            if(counter<=2):
                if (position[0] >= ball_1.pos[0] - 5 and position[0] <= ball_1.pos[0] + 5 and 
                    position[1] >= ball_1.pos[1] - 5 and position[1] <= ball_1.pos[1] + 5):
                    
                    if len(temp_line_1) == 0:
                        temp_line_1.append(position)
                        draw_line = True
                        counter+=1

                elif (draw_line == True):
                    temp_line_1.append(position)
                    lines_1.append(temp_line_1)
                    # Store direction for ball_1 after arrow is drawn
                    ball_1.ang = angle(1)
                    temp_line_1 = []
                    draw_line = False
                    counter+=1
        if(ball_2.move == True):
            counter_reset()

        if (ball_1.move == False):
            if(counter2<=2):
                if (position[0] >= ball_2.pos[0] - 5 and position[0] <= ball_2.pos[0] + 5 and 
                    position[1] >= ball_2.pos[1] - 5 and position[1] <= ball_2.pos[1] + 5):
                    if len(temp_line_2) == 0:
                        temp_line_2.append(position)
                        draw_line_2 = True  
                        counter2+=1

                elif (draw_line_2 == True):
                    temp_line_2.append(position)
                    lines_2.append(temp_line_2)
                    # Store direction for ball_2 after arrow is drawn
                    ball_2.ang = angle(2)
                    temp_line_2 = []
                    draw_line_2 = False
                    counter2+=1
        if(ball_1.move == True):
            counter_reset()

    ball_1.move = False
    ball_2.move = False

def collision(position1, position2, radius):
    """Check if two positions collide within a given radius."""
    if math.sqrt(((position1[0]-position2[0])**2) + (position1[1]-position2[1])**2) <= radius + 10:
        return True

def mousedrag(position):
    """Allow repositioning of balls before simulation starts."""
    if running == True:
        if (ball_1.move == False):            
            if (position[0] >= ball_1.pos[0] - 30 and position[0] <= ball_1.pos[0] + 30 and 
                position[1] >= ball_1.pos[1] - 30 and position[1] <= ball_1.pos[1] + 30):                    
                ball_1.pos = list(position)        
                ball_2.move = True
                lines_1.clear()
                counter_reset()

        if (ball_2.move == False):
            if (position[0] >= ball_2.pos[0] - 30 and position[0] <= ball_2.pos[0] + 30 and 
                position[1] >= ball_2.pos[1] - 30 and position[1] <= ball_2.pos[1] + 30):
                ball_2.pos = list(position)
                ball_1.move = True
                lines_2.clear()
                counter_reset()

def angle(ball_num):
    """Calculate the angle from the ball's position to the end of its last drawn line."""
    global ball_1, ball_2, lines_1, lines_2
    if ball_num == 1 and lines_1:
        dx = lines_1[-1][1][0] - ball_1.pos[0]
        dy = lines_1[-1][1][1] - ball_1.pos[1]
        return math.atan2(dy, dx)
    if ball_num == 2 and lines_2:
        dx = lines_2[-1][1][0] - ball_2.pos[0]
        dy = lines_2[-1][1][1] - ball_2.pos[1]
        return math.atan2(dy, dx)
    return 0

def calculate(m1, m2, v1, v2):
    """Perform standard 1D elastic collision calculations."""
    global final_velocity1, final_velocity2
    final_velocity1 = (m1 - m2) / (m1 + m2) * v1 + (2 * m2) / (m1 + m2) * v2
    final_velocity2 = (2 * m1) / (m1 + m2) * v1 + (m2 - m1) / (m1 + m2) * v2

def resolve_collision(ball1, ball2):
    """Resolve collision between two balls using elastic collision formulas."""
    dx = ball2.pos[0] - ball1.pos[0]
    dy = ball2.pos[1] - ball1.pos[1]
    distance = math.sqrt(dx*dx + dy*dy)
    if distance == 0:
        return

    nx = dx / distance
    ny = dy / distance

    tx = -ny
    ty = nx

    v1n = ball1.velx * nx + ball1.vely * ny
    v1t = ball1.velx * tx + ball1.vely * ty
    v2n = ball2.velx * nx + ball2.vely * ny
    v2t = ball2.velx * tx + ball2.vely * ty

    m1 = ball1.mass
    m2 = ball2.mass

    v1n_after = (m1 - m2) / (m1 + m2) * v1n + (2 * m2) / (m1 + m2) * v2n
    v2n_after = (2 * m1) / (m1 + m2) * v1n + (m2 - m1) / (m1 + m2) * v2n

    v1t_after = v1t
    v2t_after = v2t

    ball1.velx = v1n_after * nx + v1t_after * tx
    ball1.vely = v1n_after * ny + v1t_after * ty
    ball2.velx = v2n_after * nx + v2t_after * tx
    ball2.vely = v2n_after * ny + v2t_after * ty

def draw_handler(canvas):
    """Draw the balls, lines, and display mass/velocity info on the canvas."""
    global ball_2, ball_1, collided, final_velocity1, final_velocity2
    
    m = ("Mass is " + str(ball_1.mass))
    m2 = ("Mass 2 is " + str(ball_2.mass))
    v = ("X Speed is " + str(ball_1.velx))
    vy = ("Y Speed is " + str(ball_1.vely))
    v2 = ("X Speed is " + str(ball_2.velx))
    vy2 = ("Y Speed is " + str(ball_2.vely))

    canvas.draw_text(m, (100, 500), 24, 'Red')
    canvas.draw_text(v, (100, 550), 24, 'Red')
    canvas.draw_text(vy, (100, 600), 24, 'Red')
    
    canvas.draw_text(m2, (450, 500), 24, 'Blue') 
    canvas.draw_text(v2, (450, 550), 24, 'Blue')
    canvas.draw_text(vy2, (450, 600), 24, 'Blue')

    canvas.draw_line((ball_1.pos), (ball_2.pos), 2, 'White')    
    ball_1.draw(canvas)
    for line in lines_1:
        canvas.draw_line(line[0], line[1], 3, 'Red')
    ball_2.draw(canvas)
    for line_2 in lines_2:
        canvas.draw_line(line_2[0], line_2[1], 3, 'Blue')
        
    if ball_1.mass==0:
        canvas.draw_text("YOU CAN'T USE 0", (200, 150), 12, 'Red')
    if ball_1.mass<0:
        canvas.draw_text("YOU CAN'T HAVE NEGATIVE MASS", (50, 150), 18, 'Red')
    if ball_2.mass==0:
        canvas.draw_text("YOU CAN'T USE 0", (600, 150), 12, 'Red')
    if ball_2.mass<0:
        canvas.draw_text("YOU CAN'T HAVE NEGATIVE MASS", (450, 150), 18, 'Blue')
    
    if running == True:
        if inp_m.get_text() != '':
            ball_1.mass_function(inp_m.get_text())
        if inp_m_2.get_text() != '':
            ball_2.mass_function(inp_m_2.get_text())
        if inp_v.get_text() != '':
            ball_1.velocity_function(inp_v.get_text())
        if inp_v_2.get_text() != '':    
            ball_2.velocity_function(inp_v_2.get_text())

    if running == False:
        if collision(ball_1.pos, ball_2.pos, 20) == True:
            if one_d == True:
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

def mass_handler_1(m1):
    """Handler for mass input of ball 1."""
    objects[0].mass_function(m1)
    
def mass_handler_2(m2):
    """Handler for mass input of ball 2."""
    objects[1].mass_function(m2)
    
def velocity_handler_1(v1):
    """Handler for velocity input of ball 1."""
    objects[0].velocity_function(v1)    
    
def velocity_handler_2(v2):
    """Handler for velocity input of ball 2."""
    objects[1].velocity_function(v2)  
    
def reset():
    """Reset the simulation state and ball positions/velocities."""
    global ball_1, ball_2, collided
    ball_1.pos = [200,250]
    ball_2.pos = [600,250]
    ball_1.velx = 0
    ball_2.velx = 0
    ball_1.vely = 0
    ball_2.vely = 0
    lines_1.clear()
    lines_2.clear()
    counter_reset()
    collided = False

#ball generation
ball_1 = Balls([200,250],0,0,1,False,1, "Red")
ball_2 = Balls([600,250],0,0,1,False,2, "Blue")
objects.append(ball_1)
objects.append(ball_2)

#Frame generation
if one_d == True:
    frame = gui.create_frame('Frame',1000,300)
else:
    frame = gui.create_frame('Frame',800,800) 

inp_m = frame.add_input('Insert mass 1', mass_handler_1, 50)
inp_m_2 = frame.add_input('Insert mass 2', mass_handler_2, 50)
inp_v = frame.add_input('Insert velocity 1', velocity_handler_1, 50)
inp_v_2 = frame.add_input('Insert velocity 2', velocity_handler_2, 50)
button_run = frame.add_button('START', run, 100)

frame.set_canvas_background('White')
frame.set_draw_handler(draw_handler)
frame.set_mouseclick_handler(mouseclick)
frame.set_mousedrag_handler(mousedrag)
frame.start()
