from network_client import ClientTCP
import time
import re

class RobotFunc:
   def __init__(self, queryStr, regexStr):
      self.queryStr = queryStr
      self.regex = re.compile(regexStr)
      self.buf = str()

class RobotNetIf(ClientTCP):
   def __init__(self, ip, port, debug = False):
      super(RobotNetIf, self).__init__()
      self.address = (ip, port)
      self.connect(ip, port)
      self.sleepTime = 0.1
      self.maxV = 70
      self.minV = -70 
      
      self.TouchFn = RobotFunc("?T\n", "-T=(\d*)")
      self.recvV = str()
      self.rxBuffer = str()
      self.debug = debug
      #self.reset()
      #time.sleep(self.sleepTime)

   def data_received(self, data, address):
      self.rxBuffer = self.rxBuffer + data
      strings = self.rxBuffer.split("\n")
      for s in strings[:-1]:
         # finished with packet, now process it
         if s.find("-V") >= 0:
            self.recvV = s 
         #elif s.find("-T") >= 0:
         elif self.TouchFn.regex.match(s):
            print "Got Touch " + s
            self.TouchFn.buf = s
         elif self.debug:
            print "RobotNetIf ignoring packet: " + s
      self.rxBuffer = strings[-1] # non-empty incomplete packet 

         
   def setV(self, vX, vY, vR):
      vX = max(self.minV, min(self.maxV, int(vX)))
      vY = max(self.minV, min(self.maxV, int(vY)))
      vR = max(self.minV, min(self.maxV, int(vR)))
      self.send( "!D%d,%d,%d\n" % (vX, vY, vR), self.address)  
      #print "!D%d,%d,%d\n" % (vX, vY, vR)
   
   def getVs(self):
      self.send( "?Vs\n", self.address)
      while len(self.recvV) == 0:
         time.sleep(self.sleepTime) 
      Vs = self.recvV
      self.recvV = str()
      return Vs

   def getTouch(self):
      
      self.send( self.TouchFn.queryStr, self.address)
      while len(self.TouchFn.buf) == 0:
         time.sleep(self.sleepTime) 
      touch = self.TouchFn.buf
      self.TouchFn.buf = str()
      bitmask = int(self.TouchFn.regex.match(touch).group(1))
      bitArr = [False, False, False, False, False, False] 
      for i in range(len(bitArr)):
         if bitmask & pow(2,i):
            bitArr[i] = True
      return bitArr
      

   def reset(self):
      self.send( "R\n", self.address)
      self.send( "!E2\n", self.address) #Disable command echo
      
if __name__ == "__main__":
   robotIp = "10.1.95.57"
   robotPort = 56000
   r = RobotNetIf(robotIp, robotPort, True)
   #print "getVs " + r.getVs()
   #r.setV(20,0,0)
   #print "getVs " + r.getVs()
   #r.setV(0,0,0)
   #print "getVs " + r.getVs()
   for i in range(100):
      print r.getTouch()
   r.close()

