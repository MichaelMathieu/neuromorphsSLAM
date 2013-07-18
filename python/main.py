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
import controller
from itertools import groupby
from keyValueInterface import keyValueInterface

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
        slam.newPlaceCell(robot.x, robot.y)
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

    gui = display.GUI(scale = 400., wpixels = 400., hpixels=400.)

    obstacles = [[0,0,1,0],[1,0,1,1],[1,1,0,1],[0,1,0,0]]
    kvInterface = None
    if args.kvServerIp:
        print "Connecting to Key Value server ", args.kvServerIp,":", args.kvServerPort
        kvInterface = keyValueInterface(args.kvServerIp, args.kvServerPort,"slam")
        kvInterface.setQuitCmd(False)
        ctrl = controller.remoteController(gui, obstacles, kvInterface)
    else:
        ctrl = controller.guiController(gui, obstacles)
    
    
    noise = 0.05
    x_0 = 0.1
    y_0 = 0.1
    th0 = 0
    dirsBase=[[1,0],[-0.5,math.sqrt(3.)/2],[-0.5,-math.sqrt(3.)/2]]
    dirsBase2=[[0,1],[math.sqrt(3.)/2,-0.5],[-math.sqrt(3.)/2,-0.5]]
    factors = [0.6,1.2]
    dirs = [[[x*k,y*k] for x,y in dirsBase] for k in factors]
    dirs += [[[x*k,y*k] for x,y in dirsBase2] for k in factors]
    nPhases = [16,16,16,16]
    #lineColors = [(0,1,0),(0,0,1)]
    #for dirs0,color,nph in zip(dirs,lineColors,nPhases):
    #    plotLines(dirs0, nph, th0, x_0, y_0, color = color)

    # robot
    robotInterface = None
    if args.robotIp:
       robotInterface = robotNetIf.RobotNetIf(args.robotIp, args.robotPort, False)
       robot = robot.RealRobot(x = x_0, y = y_0, noise = noise, rif = robotInterface)


    else:
       print "Using simulated robot"
       robot = robot.SimRobot(x = x_0, y = y_0, noise = noise)
    
    # SLAM
    R = 10.
    Vth=9.
    constants = [(R, 1., 0.001,Vth), (R, 1., 0.001,Vth),
                 (R, 1., 0.001,Vth), (R, 1., 0.001,Vth)]
    dirs = [(x,nph) for x,nph in zip(dirs,nPhases)]
    slam = SLAM.SLAM(dirs, constants)

    # Number of sub-iterations (neuron timesteps per robot timestep)
    nSubIters = 75
    Dt = 0.25
    nextTime = time.time()+Dt
    
    lastBump = False
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
            Dx, Dy, newPlaceCell = ctrl.updateControl(robot, Dt)
             
            dx = Dx/nSubIters
            dy = Dy/nSubIters
            dt = Dt/nSubIters
            
            if newPlaceCell:
               slam.newPlaceCell(robot.x, robot.y)

            dxRobot = 0.
            dyRobot = 0.

            subIterActivePlaceCells = []
            for i in xrange(nSubIters):
                slam.update(dx, dy, dt/5, robot, gui)
                placeCellCreation(slam)
                subIterActivePlaceCells += slam.getActivePlaceCells()
                dxRobot += dx
                dyRobot += dy
                if i % 10 == 0:
                    robot.update(dxRobot,dyRobot)
                    dxRobot = 0.
                    dyRobot = 0.
            subIterActivePlaceCells.sort()
            iterActivePlaceCells = [ key for key,_ in groupby(subIterActivePlaceCells) ]
            if kvInterface:
                kvInterface.setPlaceCellStatus(iterActivePlaceCells)
                placeCellPositions = [ (p.x, p.y) for p in slam.placeCells]
                kvInterface.setPlaceCellPositions(placeCellPositions)
            it += 1
                
    except KeyboardInterrupt:
	if kvInterface:
           kvInterface.setQuitCmd(True)
        if robotInterface:
           robotInterface.setV(0,0,0)
	   robotInterface.close() 
