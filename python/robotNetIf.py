from network_client import ClientTCP

class RobotNetIf(ClientTCP):
   def __init__(self, ip, port):
      super(RobotNetIf, self).__init__()
      self.ip = ip
      self.connect(ip, port)      

   def setV(self, vX, vY, vR):
      self.send(self, "!D%d,%d,%d\n" % (vX, vY, vR))  

   def reset(self):
      self.send(self, "R\n")

try:
   robotIp = "10.1.95.57"
   robotPort = 56000
   r = RobotNetIf(robotIp, robotPort)
except KeyboardInterrupt:
   r.close()

