import math
from math import sqrt, sin, cos,pi
import time
import numpy

class RobotAbstraction(object):
   def __init__(self, x, y, noise):
      self.x = x
      self.y = y
      self.noise = noise
      self.rif = None

class RealRobot(RobotAbstraction):
   def __init__(self, rif, cheatFactor = 2., x = 0., y = 0., noise = 0.01):
      super(RealRobot, self).__init__(x, y, noise)
      self.rif = rif 
      self.cheatFactor = cheatFactor
      alpha = 206.6
      wheelradius = 0.0225
      beta = 360./(math.pi*2.*wheelradius) * self.cheatFactor
      self.robotCoordinateMatrix = numpy.matrix(
         [[-beta*math.sqrt(3)/2, -beta*0.5, alpha],
          [                   0,      beta, alpha],
          [ beta*math.sqrt(3)/2, -beta*0.5, alpha]])
      self.robotTargetWheelsPosition = numpy.matrix(self.rif.get("Wi"),dtype='float').T
      print "initial wheelPos ", self.robotTargetWheelsPosition
      self.bumpSensorsAngles = [pi/6, 3.*pi/6,5.*pi/6,7.*pi/6,9.*pi/6,11.*pi/6]
      
   def update(self, dx, dy):
      dtheta = 0
      dpos = numpy.matrix([[dx],[dy],[dtheta]])
      dwheels = self.robotCoordinateMatrix * dpos
      self.robotTargetWheelsPosition += dwheels
      self.rif.setW(self.robotTargetWheelsPosition[0,0],
                    self.robotTargetWheelsPosition[1,0],
                    self.robotTargetWheelsPosition[2,0])
      self.x += dx
      self.y += dy
      return self.x, self.y
      
   def getBumps(self):
      return self.rif.bumpData

   def getNewBumps(self):
      out = self.rif.newBumpEvent
      self.rif.newBumpEvent = [False for i in self.rif.newBumpEvent]
      return out

   def getBumpAngle(self, bumps):
      angles = [self.bumpSensorsAngles[i] for i in xrange(len(bumps)) if bumps[i]]
      X = [cos(a) for a in angles]
      Y = [sin(a) for a in angles]
      n = sum([1 for i in angles])
      out = math.atan2(sum(Y)/n, sum(X)/n)
      print out
      return 0.

class SimRobot(RobotAbstraction):
   def __init__(self, x = 0., y = 0., noise = 0.01):
      super(SimRobot, self).__init__(x, y, noise)
      
   def update(self, dx, dy):
      self.x += dx
      self.y += dy
      return self.x, self.y

   def getBumps(self):
      return [False for i in xrange(6)]

   def getNewBumps(self):
      return [False for i in xrange(6)]
