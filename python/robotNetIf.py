from network_client import ClientTCP
import time
import re

class RobotFunc(object):
   def __init__(self, queryStr, regexStr, regexGroups, dataType):
      self.queryStr = queryStr
      self.regexStr = regexStr
      self.regex = re.compile(regexStr)
      self.regexGroups = tuple(range(regexGroups+1)[1:])
      self.dataType = dataType
      self.buf = str()
  
   def getValue(self):
      match = self.regex.match(self.buf)      
      self.buf = str()
      return [self.dataType(match.group(g)) for g in self.regexGroups]

class TouchSenseFunc(RobotFunc):
   def __init__(self, queryStr, regexStr, regexGroups, dataType):
      super(TouchSenseFunc, self).__init__(queryStr, regexStr, regexGroups, dataType)

   def getValue(self):
      bitmask = super(TouchSenseFunc, self).getValue()[0]
      bitArr = [False, False, False, False, False, False] 
      for i in range(len(bitArr)):
         if bitmask & pow(2,i):
            bitArr[i] = True
      return bitArr

   
      
class RobotNetIf(ClientTCP):
   def __init__(self, ip, port, debug = False):
      super(RobotNetIf, self).__init__()
      self.address = (ip, port)
      self.connect(ip, port)
      self.sleepTime = 0.1
      self.maxV = 70
      self.minV = -70 
      self.QueryFuncs = { 
         "T":TouchSenseFunc("?T\n", "-T=(\d*)", 1, int),
         "Vs":RobotFunc("?Vs\n", "-V0=([-]*\d*) r/m, 1=([-]*\d*) r/m, 2=([-]*\d*) r/m", 3, int),
         "Wi":RobotFunc("?Wi\n", "-Wi0=([-]*\d*), 1=([-]*\d*), 2=([-]*\d*)", 3, int)
         }

      self.recvV = str()
      self.rxBuffer = str()
      self.debug = debug
      self.reset()
      time.sleep(self.sleepTime)

   def data_received(self, data, address):
      self.rxBuffer = self.rxBuffer + data
      strings = self.rxBuffer.split("\n")
      for s in strings[:-1]:
         print "Processing " + s
         # finished with packet, now process it
         for f in self.QueryFuncs:
            if self.QueryFuncs[f].regex.match(s):
	       print "Got " + f
	       self.QueryFuncs[f].buf = s 
            elif s.find("N-OmniRob Control") == 0:
               print "Init String recd: " + s
               self.init = True 
            elif self.debug:
               print "RobotNetIf ignoring packet: " + s
      self.rxBuffer = strings[-1] # non-empty incomplete packet 

         
   def setV(self, vX, vY, vR):
      vX = max(self.minV, min(self.maxV, int(vX)))
      vY = max(self.minV, min(self.maxV, int(vY)))
      vR = max(self.minV, min(self.maxV, int(vR)))
      self.send( "!D%d,%d,%d\n" % (vX, vY, vR), self.address)  
      #print "!D%d,%d,%d\n" % (vX, vY, vR)

   def setW(self, w0, w1, w2):
      self.send( "!w%d,%d,%d\n" % (w0, w1, w2), self.address)  
   

   def get(self, request):
      val = None
      if request in self.QueryFuncs:
         func = self.QueryFuncs[request]
	 self.send( func.queryStr, self.address)
         while len(func.buf) == 0:
            time.sleep(self.sleepTime) 
         val = func.getValue()
      else:
	 print "Error - attempted to get unsupported value " + request
      return val
   
   def reset(self):
      self.init = False
      self.send( "R\n", self.address)
      print "Waiting for robot init string..."
      while not self.init:
         time.sleep(self.sleepTime) 
      self.send( "!E2\n", self.address) #Disable command echo
      
if __name__ == "__main__":
   robotIp = "10.1.95.57"
   robotPort = 56000
   debug = False
   r = RobotNetIf(robotIp, robotPort, debug)
  
   #r.setW(10,20,30) 
   #print "get(Vs) ", r.get("Vs")
   #r.setV(20,0,0)
   #print "get(Wi) ", r.get("Wi")
   #print "get(Wi) ", r.get("Wi")
   #print "get(Wi) ", r.get("Wi")
   #print "get(Wi) ", r.get("Wi")

   #r.setV(0,0,0)
   #print "get(T) ", r.get("T")
   #print r.getTouch()
   r.close()

