import display
import gtk
import robot
import SLAM
import math
import numpy

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

def plotLines(dirs, nPhases, th_0, x_0, y_0, color=(0,1,0)):
    #TODO: only works with regularly samples dirs
    d0 = dirs[0][0] - dirs[1][0]
    d1 = dirs[0][1] - dirs[1][1]
    ndiff = math.sqrt(d0*d0+d1*d1)
    thetas = [math.atan2(y,x)+th_0 for x,y in dirs]
    for i in xrange(-20,20):
        for theta in thetas:
            d = float(i)/nPhases/ndiff+(math.cos(theta)*x_0+math.sin(theta)*y_0)
            nx = math.cos(theta)
            ny = math.sin(theta)
            l = math.sqrt(nx*nx+ny*ny)
            a = -ny / l
            b = nx  / l
            x0 = d*nx
            y0 = d*ny
            x1 = x0-200*a
            y1 = y0-200*b
            x2 = x0+200*a
            y2 = y0+200*b
            gui.line(x1,y1,x2,y2, width=1,color=color)

if __name__=="__main__":
    gui = display.GUI(scale = 400., wpixels = 400., hpixels=400.)

    x_0 = 0.1
    y_0 = 0.1
    th0 = -math.pi/2
    dirsBase=[[1,0],[-0.5,math.sqrt(3.)/2],[-0.5,-math.sqrt(3.)/2]]
    factors = [2.,1.]
    dirs = [[[x*k,y*k] for x,y in dirsBase] for k in factors]
    lineColors = [(0,1,0),(0,0,1)]
    for dirs0,color in zip(dirs,lineColors):
        plotLines(dirs0, 4, th0, x_0, y_0, color = color)

    # robot
    robot = robot.Robot(gui=gui, x = x_0, y = y_0, theta = th0,
                        noise = 0.01, velocity = 0.2)
    # SLAM
    k = 1
    dirs = [(x,4) for x in dirs]
    slam = SLAM.SLAM(dirs)

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
            for i in xrange(nSubIters):
                slam.update(dx, dy, dt, robot, gui)
                
    except KeyboardInterrupt:
        pass
