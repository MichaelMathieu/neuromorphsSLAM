from streamclient import StreamClient
import json
import re

class keyValueInterface(StreamClient):
   def __init__(self, host, port, namespace="slam"):
      super(keyValueInterface, self).__init__(host, port)
      self.namespace = namespace
      self.velocityCmdKey = self.namespace+"/velocity" 
      self.placeCellStatusKey = self.namespace+"/spikes"
      self.positionKey = self.namespace+"/position"
      self.quitKey = self.namespace+"/quit"
      self.velocityRegex = re.compile("dx=(\d+\.\d+) dy=(\d+\.\d+)")   
  
   def getQuitCmd(self):
      return bool(self.get(self.quitKey)) 

   def setQuitCmd(self, quitCmd):
      self.set(self.quitKey, json.dumps(bool(quitCmd)))

   def getVelocityCmd(self):
      velocityCmdRaw = self.get(self.velocityCmdKey)
      match = self.velocityRegex.match(velocityCmdRaw)
      if match:
         return [ float(match.group(1)), float(match.group(2)) ]
      else:
         print "self.velocityCmdKey has not been initialized; using default values"
	 return [0.0, 0.0]

   def setPosition(self, posX, posY):
      self.set(self.positionKey, "X=%f Y=%f" % ( posX, posY ))    
      print "Set Position X=%f Y%f" % (posX, posY)
   def setPlaceCellStatus(self, placeCellStatusRaw):
      placeCellStatus = json.dumps(placeCellStatusRaw)
      print "Converted placeCellStatusRaw to ", placeCellStatus
      self.set(self.placeCellStatusKey, placeCellStatus)
  
if __name__ == "__main__":
   import time
   k = keyValueInterface("10.1.95.75", 21567, "slam")
   
   k.set('slam/velocity', 'dx=0.1 dy=0.000')
   print "set velocity"
   for i in range(1000):
      value = k.get('slam/velocity')
      print value
      time.sleep(0.1)
      t = i % 10 + 1
      spikes = json.dumps([int(j % t == 0) for j in range(100)])
      print spikes
      k.set('slam/spikes', spikes)

   
    
