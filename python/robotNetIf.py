from network_client import ClientTCP

class RobotIF(ClientTCP):
   def __init__(self):
      super(RobotIF, self).__init__()

   def setV(vX, vY, vR):
      send("!D%d,%d,%d\n" % (vx, vy, vR))  

try:
   robotAddr = ("10.1.95.57", 56000)
   r = RobotIF()
   r.connect(*robotAddr)
   r.send("R\n", robotAddr)
except KeyboardInterrupt:
   r.close()

