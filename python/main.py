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

lastNewPlaceCell = False
def placeCellCreation(slam):
    global lastNewPlaceCell
    global lastBump
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
    dirsBase2=[[0,1],[math.sqrt(3.)/2,-0.5],[-math.sqrt(3.)/2,-0.5]]
    factors = [1.,0.5]
    dirs = [[[x*k,y*k] for x,y in dirsBase] for k in factors]
    dirs += [[[x*k,y*k] for x,y in dirsBase2] for k in factors]
    nPhases = [16,32,16,32]
    #lineColors = [(0,1,0),(0,0,1)]
    #for dirs0,color,nph in zip(dirs,lineColors,nPhases):
    #    plotLines(dirs0, nph, th0, x_0, y_0, color = color)

    # robot
    noise = 0.
    robot = robot.Robot(gui=gui, x = x_0, y = y_0, theta = th0, noise = noise,
                        velocity = 0.033, rif=robotInterface)
    # SLAM
    R = 18.
    constants = [(R, 1., 0.001), (R, 1., 0.001),
                 (R, 1., 0.001), (R, 1., 0.001)]
    dirs = [(x,nph) for x,nph in zip(dirs,nPhases)]
    slam = SLAM.SLAM(dirs, constants)

    # Number of sub-iterations (neuron timesteps per robot timestep)
    nSubIters = 100
    Dt = 0.25
    nextTime = time.time()+Dt
    cheatFactor = 2.
    # the cheat factor is the ratio of the true world over 1meter.
    # Careful that the speed is also multiplied
    lastBump = False
    bumped = False
    it = 0
    try:
        while True:
            while gtk.events_pending():
                gtk.main_iteration()
            currentTime = time.time()
            sleepingTime = max(0, nextTime-currentTime)
            #print "Sleeping " + str(sleepingTime)
            time.sleep(sleepingTime)
            nextTime += Dt
                
            # Main loop : put code here
            if it % 10 == 0:
                if robot.rif:
                    robot.rif.setBumpStream(10)
            dtheta, dvelocity = controller(gui)
            Dx, Dy = robot.update(dt = Dt, dtheta = dtheta*Dt, dvelocity = dvelocity,
                                  bump = bumped)
            dx = Dx/nSubIters
            dy = Dy/nSubIters
            dt = Dt/nSubIters
            bumped = False
            for i in xrange(nSubIters):
                slam.update(dx, dy, dt/5, robot, gui)
                placeCellCreation(slam)
                if robot.rif:
                    bump = any(robot.rif.bumpData)
                    if bump and not lastBump:
                        print "BUMP"
                        bumped = True
                        slam.newPlaceCell()
                    lastBump = bump
                if not bumped:
                    robot.updateRobot(cheatFactor*dx,cheatFactor*dy,0)
            it += 1
                
    #except Exception as e:
    except KeyboardInterrupt:
        if robot.rif:
            robot.rif.setV(0,0,0)
            robot.rif.close()
        #raise e
