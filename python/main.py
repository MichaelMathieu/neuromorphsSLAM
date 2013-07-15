import display
import gtk
import robot
import SLAM
import math

def controller(gui):
    incr_theta = 5. # in rad PER SECOND
    incr_velocity = 0.1 # in meter (the world is 1m wide) per second square
    dtheta = 0.
    dvelocity = 0.
    if gui.keyState("Left"):
        dtheta -= incr_theta
    if gui.keyState("Right"):
        dtheta += incr_theta
    if gui.keyState("Up"):
        dvelocity += incr_velocity
    if gui.keyState("Down"):
        dvelocity -= incr_velocity
    return dtheta, dvelocity

if __name__=="__main__":
    gui = display.GUI(scale = 400., wpixels = 400., hpixels=400.)

    # robot
    robot = robot.Robot(gui=gui, x = 0.1, y = 0.1, theta = 3.14/2,
                        noise = 0.01, velocity = 0.2)
    # SLAM
    dirs=[[1,0],[-0.5,math.sqrt(3.)/2],[-0.5,-math.sqrt(3.)/2]]
    dirs = [[0.5*x,0.5*y] for x,y in dirs]
    slam = SLAM.SLAM(VCOdirs=dirs)

    # Number of sub-iterations (neuron timesteps per robot timestep)
    nSubIters = 100
    try:
        while True:
            while gtk.events_pending():
                gtk.main_iteration()
                
            # Main loop : put code here
            dtheta, dvelocity = controller(gui)
            Dt = 0.05
            Dx, Dy = robot.update(dt = Dt, dtheta = dtheta, dvelocity = dvelocity)
            dx = Dx/nSubIters
            dy = Dy/nSubIters
            dt = Dt/nSubIters
            for i in range(nSubIters):
                slam.update(dx, dy, dt, robot, gui)
        
    except KeyboardInterrupt:
        pass
