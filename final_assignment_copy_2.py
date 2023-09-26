# Import necessary libraries
from numpy import *
from vpython import *

def setting():
    """
    Initializes and sets up the scene, objects, and labels for the projectile game.
    
    This function creates a 3D scene with various elements including a ground, target box, launching platform,
    egg, arrow, buildings, and labels for these visual elements. It also sets global parameters for the game.
    
    Parameters:
    None
    
    Returns:
    Various objects and labels required for the game.
    """
    
    # Create a 3D scene
    scene = canvas(width=640, height=480, center=vector(8,5,0), background=vector(0.8,1,0.9), range=8)
    
    # Create the ground
    ground = curve(pos=[(0,0,0),(16,0,0)], radius=0.15, color=vector(0,0.7,0))

    # Set random values for target and platform
    T = float(10*random()+5)
    target = box(pos=vector(T,1,0), width=0.5, height=2, length=0.5, color=color.cyan)
    p = 0.7*random()
    platform = curve(pos=[(0,p,0),(1,p,0)], color=color.magenta)
    
    # Create the egg and arrow
    egg = sphere(pos=vector(0,p+0.3,0), radius=0.3, make_trail=True, trail_type="points")
    ar = arrow(pos=vector(0,p+0.3,0), axis=vector(0,0,0), length=0.3, color=vector(0,0,0), shaftwidth=0.05)

    # Create background elements
    far_ground = box(pos=vector(-0,-30,-130), width=100, heigth=0.01, length=190)
    building1 = box(pos=vector(-10,-4,-40), width=2, height=10, length=4)
    building2 = box(pos=vector(-15,-7,-40),width=2,height=5,length=5,color=color.black)
    building3 = box(pos=vector(-1,-8,-40),width=2,height=4,length=15,color=color.magenta)
    building4 = box(pos=vector(5,-9,-49),width=2,height=7,length=20,color=color.purple)
    building5 = box(pos=vector(-8,-3,-49),width=2,height=15,length=5,color=color.yellow)
    building6 = box(pos=vector(30,-6,-54),width=2,height=14,length=30,color=vector(0.3,0.3,0.5))
    building7 = box(pos=vector(-30,-6,-54),width=2,height=14,length=30,color=vector(0.3,0.3,0.5))

    # Create the sun
    sun = sphere(pos=vector(-2.3,13,0), radius=4, color=color.yellow)

    # Create labels for visual elements
    ground_label = label(pos=vector(8,0,0), text="Ground", color=color.black, yoffset=-12)
    target_label = label(pos=vector(T,1,0), text="Target", color=color.black, xoffset=20)
    egg_label = label(pos=vector(-0.3,p+0.3,0),text="Egg",color=color.black,xoffset=-20)
    egg_position_label = label(pos=vector(0,p+0.6,0),text="{:0.2f} meters from target in the horizontal direction,\n {:0.2f} meters above ground".format(T,p+0.3),box=False,color=color.black,xoffset=110,yoffset=124,line=False)
    platform_label = label(pos=vector(0.5,p,0),text="Platform",color=color.black,yoffset=-40)

    return p, T, target, platform, egg, ar, egg_label, egg_position_label

def launch():
    """
    Simulates the launching of an egg in a projectile motion game.
    
    This function calculates and simulates the motion of an egg launched at a specified angle and speed.
    It updates the egg's position and visual elements and provides feedback on the outcome of the launch.
    
    Returns:
    None
    """
    
    # Constants
    g = 9.81
    dt = 0.0001
    t = 0
    y = 0
    x = 0
    
    # User input for launch angle and speed
    dtheta = float(input("Input the initial angle in degrees: "))
    theta = radians(dtheta)
    v0 = float(input("Input the initial speed in meters/second: "))
    print()
    
    # Simulate egg motion while it's in the air
    while y >= 0:
        rate(1500)
        t = t + dt
        y = p + 0.3 + v0 * t * sin(theta) - (g * (t**2)) / 2
        x = v0 * t * cos(theta)
        # Update egg and arrow position and labels
        egg.pos = vector(x, y, 0)
        ar.pos = vector(x, y, 0)
        ar.axis = vector(0.1 * v0 * cos(theta), ((0.1 * v0 * sin(theta)) - (0.1 * g * t)), 0)
        egg_label.pos = vector(x - 0.3, y, 0)
        egg_position_label.pos = vector(x, y + 0.3, 0)
        egg_position_label.text = "{:0.2f} meters from target in the horizontal direction,\n{:0.2f} meters above ground".format(T - x, y)
        egg_position_label.xoffset = 0
        
        # Check if the egg hits the target
        if (T - 0.25) < x and x < (T + 0.25) and y <= 2:
            break
    
    # Determine the outcome of the launch
    if (T - 0.25) < x and x < (T + 0.25) and y <= 2:
        print("You have hit the target. YAY!")
        math(g, t, y, x, v0, theta)
    elif x > (T + 0.25) and y <= 2:
        print("Oops. Looks like you have overshot.\n\nThe egg landed {:0.2f} meters behind the target.\nTry again.".format(x - T))
        g, t, y, x, v0, theta = launch()
    else:
        print("Looks like you didn't put enough power.\n\nThe egg landed {:0.2f} meters in front of the target.\nTry again.".format(T - x))
        g, t, y, x, v0, theta = launch()

    return g, t, y, x, v0, theta

def math(g, t, y, x, v0, theta):
    """
    Calculates and evaluates the physics and outcome of the egg launch.
    
    This function computes various physical quantities related to the egg launch, including its momentum,
    applied forces, and torque. It then compares the applied torque with the restoring torque to determine
    whether the target topples or not. Depending on the outcome, it prints a message indicating whether
    the player won or needs to try again.
    
    Returns:
    None
    """
    
    # Constants
    mE = 0.1
    mT = 100
    
    # Calculate ball momentum, force applied, and torque applied
    ball_momentumV = vector((mE * v0 * cos(theta)), ((mE * v0 * sin(theta)) - (mE * g * t)), 0)
    ball_momentum = mag(ball_momentumV)
    
    force_appliedV = ball_momentumV / 0.01
    dV = vector(T + 0.25, 0, 0) - vector(x, y, 0)
    torque_appliedV = force_appliedV.cross(dV)
    torque_applied = mag(torque_appliedV)
    
    torque_restoring = -mT * g * (0.5 / 2)
    
    # Compare torques to determine outcome
    if torque_applied > abs(torque_restoring):
        print("Target falls. You won!\n\nThe egg hit the target {:0.2f} meters above ground.\nIts momentum at the point of impact is {:0.2f} Ns.\nThe torque applied on the target is {:0.2f} Nm.\nThe restoring torque is {:0.2f} Nm".format(y, ball_momentum, torque_applied, abs(torque_restoring)))
        target.rotate(angle=pi/2, axis=vector(0,0,1), origin=vector(T+0.5,1,0))
        text(pos=vector(7,8,0), text="You Win.", depth=-0.4, align="center", color=color.red, height=2)
    else:
        print("Your shot was too weak to topple the target. Try again")                                             
        g, t, y, x, v0, theta = launch()

# Initialize scene and objects
p, T, target, platform, egg, ar, egg_label, egg_position_label = setting()

# Launch the egg
g, t, y, x, v0, theta = launch()
