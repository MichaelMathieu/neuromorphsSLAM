from math import sqrt, sin, cos
import math
import random 

class controllerAbstraction(object):
   def __init__(self):
      pass

   def updateControl(self, posX, posY, posTheta):
      print "Should not use the abstract method"
      exit(-1)

class guiController(controllerAbstraction):
   def __init__(self, gui, obstacles, speed = 0.033):
      self.gui = gui
      self.obstacles = obstacles
      self.dtheta_obs_avoidance = 0.1*math.pi
      self.theta = 0
      self.speed = speed

   def updateControl(self, robot, dt):
      incr_theta = 5. # in rad PER SECOND
      dtheta = 0.
      dx = 0
      dy = 0
      if self.gui.keyState("Left"):
         dtheta -= incr_theta * dt
      if self.gui.keyState("Right"):
         dtheta += incr_theta * dt
      origTheta = self.theta
      self.theta += dtheta * dt
      self.theta += random.gauss(0, robot.noise)
      nCollisions = 0
      theta0 = self.theta
      for x1, y1, x2, y2 in self.obstacles:
         nCollisions += self.avoidLine(x1, y1, x2, y2, dt, robot, True)
      if nCollisions > 1:
         self.theta = theta0 + math.pi
      if any(robot.getBumpSensors()):
         self.theta = theta0 + math.pi
      dx = self.speed*dt*cos(self.theta)
      dy = self.speed*dt*sin(self.theta)
      if self.gui:
         self.gui.line(robot.x, robot.y, robot.x+dx, robot.y+dy,
                       color=(0,0,1), width=1)
      return dx, dy

   def avoidLine(self, x1, y1, x2, y2, dt, robot, smooth = True):
        a = y2-y1
        b = x1-x2
        c = -a*x1 - b*y1
        l = math.sqrt(a*a+b*b)
        nx = -a
        ny = -b
        border = 5. * dt * self.speed
        # d : distance to the line
        d = abs(a*robot.x + b*robot.y + c) / l
        if d < border:
            rx = robot.x - x1
            ry = robot.y - y1
            # p : projection of (robot-(x1,y1)) on ((x2,y2)-(x1,y1))
            p = (-rx*b + ry*a) / l
            if (p > -border) and (p < l+border):
                # p2 < 0 if the robot is on the wrong side
                p2 = rx*nx + ry*ny
                if p2 >= 0:
                    dx = cos(self.theta)
                    dy = sin(self.theta)
                    # p3 : proj of the velocity on the normal
                    p3 = self.speed*dt*(dx*nx + dy*ny)
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
