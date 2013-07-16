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

    th0 = -math.pi/2
    thetas = [th0,th0+2.*math.pi/3,th0+4*math.pi/3]
    #k = 0.5/(math.cos(math.pi/6)*math.sqrt(2.)) 
    k = 1
    for i in xrange(-10,10):
        for j in xrange(3):
            theta = thetas[j]
            d = float(i)/(k*4)
            #d = i*0.5
            #d = float(i)*k + 0.1*math.cos(theta)+0.1*math.sin(theta)
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

    A = numpy.matrix([[2./3,-1./3,-1./3],[0,math.sqrt(3)/3,-math.sqrt(3)/3]])
    colors=[(0,1,1),(1,0,0),(0,1,0),(0,0,1)]
    for th1 in xrange(8,9):
        for th2 in xrange(4,5):
            for th3 in xrange(3,4):
                for k2,k3 in [(1,0)]:
                    dth1 = 0.#0.1
                    dth2 = 0.#0.1*(-0.5)+0.1*math.sqrt(3)/2
                    dth3 = 0.#0.1*(-0.5)-0.1*math.sqrt(3)/2
                    p = A*numpy.matrix([[float(th1)/4.+dth1],
                                        [float(th2)/4.+dth2+k2],
                                        [float(th3)/4.+dth3+k3]])
                    print(p)
                    print math.sqrt(p[0]*p[0]+p[1]*p[1])
                    gui.point(p[0],p[1],width=6,
                              color = colors[k2*2+k3])
        

    # robot
    robot = robot.Robot(gui=gui, x = 0, y = 0, theta = 3.14/3,
                        noise = 0.01, velocity = 0.2)
    # SLAM
    dirs=[[1,0],[-0.5,math.sqrt(3.)/2],[-0.5,-math.sqrt(3.)/2]]
    #k = 0.5/(math.cos(math.pi/6)*math.sqrt(2.)) 
    k *= 1
    dirs = [[k*x,k*y] for x,y in dirs]
    dirs2 = [[0.5*x, 0.5*y] for x,y in dirs] # half frequencies
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
            for i in xrange(nSubIters):
                slam.update(dx, dy, dt, robot, gui)
                
    except KeyboardInterrupt:
        pass
