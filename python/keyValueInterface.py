from streamclient import StreamClient
import json
import re

class keyValueInterface(StreamClient):
   def __init__(self, host, port, namespace="slam"):
      super(keyValueInterface, self).__init__(host, port)
      self.namespace = namespace
      self.placeCellPositionKey = self.namespace+"/placeCellPos"
      self.placeCellStatusKey = self.namespace+"/spikes"
      self.positionKey = self.namespace+"/position"
      self.quitKey = self.namespace+"/quit"
  
   def getQuitCmd(self):
      return bool(self.get(self.quitKey)) 

   def setQuitCmd(self, quitCmd):
      self.set(self.quitKey, json.dumps(bool(quitCmd)))

   def setPosition(self, posX, posY):
      self.set(self.positionKey, "X=%f Y=%f" % ( posX, 1 - posY ))    
      #print "Set Position X=%f Y%f" % (posX, posY)
   
   def setPlaceCellPositions(self, positionMatrix):
      #print "Set place cell positions ", positionMatrix
      self.set(self.placeCellPositionKey, json.dumps(positionMatrix))    
   def setPlaceCellStatus(self, placeCellStatusRaw):
      placeCellStatus = json.dumps(placeCellStatusRaw)
      #print "Converted placeCellStatusRaw to ", placeCellStatus
      self.set(self.placeCellStatusKey, placeCellStatus)
  
if __name__ == "__main__":
   import time
   k = keyValueInterface("10.1.95.82", 21567, "slam")
   
   k.set('slam/velocity', 'dx=0.1 dy=0.000')
   print "set velocity"
   for i in range(1000000):
      time.sleep(0.5)
      j = 0
      if i % 10 == 0:
         if i % 20 == 0:
            j = 1
         else:
            j = 2
      spikes = [ fk * i / 10 for fk in range(j)  ]
      t = i % 10 + 1
      spikes = json.dumps(spikes)
      print spikes
      k.set('slam/spikes', spikes)

   
    
