import display
import gtk
import robot
import SLAM
import math
import numpy
import sys
import robotNetIf
import time 
import argparse
from keyValueInterface import keyValueInterface

def controller(gui):
    incr_theta = 3. # in rad PER SECOND
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

lastNewPlaceCell = False
def placeCellCreation(slam):
    global lastNewPlaceCell
    while gtk.events_pending():
        gtk.main_iteration()
    space = gui.keyState("space")
    if space and not lastNewPlaceCell:
        slam.newPlaceCell()
        lastNewPlaceCell = True
    if not space:
        lastNewPlaceCell = False


if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Bio-Inspired VCO controlled robotic SLAM implementation.")
    parser.add_argument("--robotIp", help="IP Address of the robot to be used- optional")
    parser.add_argument("--robotPort", default=56000, type=int, help="TCP Port for the robot to be controlled")
    parser.add_argument("--kvServerIp", help="IP for the key-value server used to communicate with matlab and other processes")
    parser.add_argument("--kvServerPort", default=21567, type=int, help="UDP port for use with the key value server")
    args = parser.parse_args()

    robotInterface = None
    if args.robotIp:
       robotInterface = robotNetIf.RobotNetIf(args.robotIp, args.robotPort)
       robotInterface.reset()
       #Just to make sure the reset is done before we start
       time.sleep(1)

    else:
       print "Using simulated robot"

    kvInterface = None
    if args.kvServerIp:
        print "Connecting to Key Value server ", args.kvServerIp,":", args.kvServerPort
        kvInterface = keyValueInterface(args.kvServerIp, args.kvServerPort,"slam")

    

    gui = display.GUI(scale = 400., wpixels = 400., hpixels=400.)

    x_0 = 0.5
    y_0 = 0.5
    th0 = 0
    dirsBase=[[1,0],[-0.5,math.sqrt(3.)/2],[-0.5,-math.sqrt(3.)/2]]
    factors = [1.,0.5]
    dirs = [[[x*k,y*k] for x,y in dirsBase] for k in factors]
    nPhases = [16,32]
    #lineColors = [(0,1,0),(0,0,1)]
    #for dirs0,color,nph in zip(dirs,lineColors,nPhases):
    #    plotLines(dirs0, nph, th0, x_0, y_0, color = color)

    # robot
    noise = 0
    robot = robot.Robot(gui=gui, x = x_0, y = y_0, theta = th0, noise = noise, velocity = 0.22, rif=robotInterface)
    # SLAM
    constants = [(6.1, 1.76, 0.001), (5., 1.2, 0.001)]
    dirs = [(x,nph) for x,nph in zip(dirs,nPhases)]
    slam = SLAM.SLAM(dirs, constants)

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
                placeCellCreation(slam)
                
    except KeyboardInterrupt:
	robot.rif.setV(0,0,0)
	robot.rif.close() 
