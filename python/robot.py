import math
from math import sqrt, sin, cos
import random
import time
import numpy

class Robot():
    def __init__(self, x = 0., y = 0., theta = 0., velocity = 0.1, noise = 0.01, obstacles = [[0,0,1,0],[1,0,1,1],[1,1,0,1],[0,1,0,0]], gui = None, rif = None):
        self.x = x
        self.y = y
        self.constVX = 70
        self.constVY = 0
        self.theta = theta
        self.velocity = velocity
        self.obstacles = obstacles
        self.noise = noise
        self.dtheta_obs_avoidance = 0.1*math.pi
        self.gui = gui
        self.aim = ("forward",None)
        if rif:
            self.initRobot(rif)

    def initRobot(self, rif):
        self.rif = rif
        alpha = 206.6
        wheelradius = 0.0225
        beta = 360./(math.pi*2.*wheelradius)
        self.robotCoordinateMatrix = numpy.matrix(
            [[-beta*math.sqrt(3)/2, -beta*0.5, alpha],
             [                   0,      beta, alpha],
             [ beta*math.sqrt(3)/2, -beta*0.5, alpha]])
        self.robotTargetWheelsPosition = numpy.matrix(self.rif.get("Wi"),dtype='float').T

    def updateRobot(self, dx, dy, dtheta):
        #dtheta 
        dpos = numpy.matrix([[dx],[dy],[dtheta]])
        dwheels = self.robotCoordinateMatrix * dpos
        self.robotTargetWheelsPosition += dwheels
        self.rif.setW(self.robotTargetWheelsPosition[0,0],
                      self.robotTargetWheelsPosition[1,0],
                      self.robotTargetWheelsPosition[2,0])
        
    def update(self, dt, dtheta, dvelocity):
        dx = 0
        dy = 0
        if self.aim[0] == "forward":
            origTheta = self.theta
            self.theta += dtheta * dt
            self.velocity += dvelocity * dt
            self.theta += random.gauss(0, self.noise)
            nCollisions = 0
            theta0 = self.theta
            for x1, y1, x2, y2 in self.obstacles:
                nCollisions += self.avoidLine(x1, y1, x2, y2, dt, True)
            if nCollisions > 1:
                #self.aim = ("rotate", theta0 + math.pi)
                #return 0, 0
                self.theta = theta0 + math.pi
            else:
                dx = self.velocity*dt*cos(self.theta)
                dy = self.velocity*dt*sin(self.theta)
                self.x += dx
                self.y += dy
                if self.gui:
                    self.gui.line(self.x-dx, self.y-dy, self.x, self.y,
                                  color=(0,0,1), width=1)
        elif self.aim[0] == "rotate":
            #not used for now
            torotate = self.aim[1] - self.theta
            maxdtheta = 10.
            
        if self.rif:
            #dTheta = self.theta - origTheta
            #self.rif.setV(self.constVX,self.constVY,-900*dTheta)
            #self.rif.setV(self.constVX,self.constVY,-35.*dTheta/dt*1.08)
            #self.updateRobot(dx, dy, dtheta)
            pass
        return dx, dy
        
    def avoidLine(self, x1, y1, x2, y2, dt, smooth = True):
        a = y2-y1
        b = x1-x2
        c = -a*x1 - b*y1
        l = math.sqrt(a*a+b*b)
        nx = -a
        ny = -b
        border = 5. * dt * self.velocity
        # d : distance to the line
        d = abs(a*self.x + b*self.y + c) / l
        if d < border:
            rx = self.x - x1
            ry = self.y - y1
            # p : projection of (robot-(x1,y1)) on ((x2,y2)-(x1,y1))
            p = (-rx*b + ry*a) / l
            if (p > -border) and (p < l+border):
                # p2 < 0 if the robot is on the wrong side
                p2 = rx*nx + ry*ny
                if p2 >= 0:
                    dx = cos(self.theta)
                    dy = sin(self.theta)
                    # p3 : proj of the velocity on the normal
                    p3 = self.velocity*dt*(dx*nx + dy*ny)
                    if p3 <= 0.1:
                        if d <= 1.5*abs(p3):
                            self.theta = math.atan2(ny, nx)
                            return 1
                        else:
                            if smooth:
                                p4 = -dx*b + dy*a
                                if p4 >= 0:
                                    self.theta += self.dtheta_obs_avoidance
                                else:
                                    self.theta -= self.dtheta_obs_avoidance
                                return 1
                            else:
                                return 0
        return 0
