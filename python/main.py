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

if __name__=="__main__":
    gui = display.GUI(scale = 400., wpixels = 400., hpixels=400.)

    x_0 = 0.1
    y_0 = 0.1
    th0 = -math.pi/2
    dirs=[[1,0],[-0.5,math.sqrt(3.)/2],[-0.5,-math.sqrt(3.)/2]]
    diffs = [[dirs[a][0]-dirs[b][0],dirs[a][1]-dirs[b][1]] for a,b in [(0,1),(1,2),(2,0)]]
    thetas = [th0,th0+2.*math.pi/3,th0+4*math.pi/3]
    #k = 0.5/(math.cos(math.pi/6)*math.sqrt(2.))
    k = 1
    for i in xrange(-10,10):
        for j in xrange(3):
            theta = thetas[j]
            a0,b0 = diffs[j]
            d = float(i)/(k*4)/math.sqrt(3)+(math.cos(theta)*x_0+math.sin(theta)*y_0)
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
            gui.line(x1,y1,x2,y2, width=1,color=(0,1,0))        

    # robot
    robot = robot.Robot(gui=gui, x = x_0, y = y_0, theta = th0,
                        noise = 0.01, velocity = 0.2)
    # SLAM
    #k = 0.5/(math.cos(math.pi/6)*math.sqrt(2.)) 
    k *= 1
    dirs = [[k*x,k*y] for x,y in dirs]
    dirs2 = [[2*x, 2*y] for x,y in dirs] # half frequencies
    slam = SLAM.SLAM(VCOdirs=dirs2+dirs)

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
