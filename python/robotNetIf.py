from network_client import ClientTCP

class RobotNetIf(ClientTCP):
   def __init__(self, ip, port):
      super(RobotNetIf, self).__init__()
      self.address = (ip, port)
      self.connect(ip, port)      

   def setV(self, vX, vY, vR):
      self.send( "!D%d,%d,%d\n" % (vX, vY, vR), self.address)  
   
   def getV(self):
      self.send( "?Vm\n", self.address)  

   def reset(self):
      self.send( "R\n", self.address)

robotIp = "10.1.95.57"
robotPort = 56000
r = RobotNetIf(robotIp, robotPort)
r.close()

