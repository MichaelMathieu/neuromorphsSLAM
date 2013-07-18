from streamclient import StreamClient
import json

class keyValueInterface(StreamClient):
   def __init__(self, host, port, namespace="slam"):
      super(keyValueInterface, self).__init__(host, port)
      self.namespace = namespace
      self.velocityCmdKey = self.namespace+"/velocity" 
      self.placeCellStatusKey = self.namespace+"/placeCellSpikes"

   def getVelocityCmd(self):
      velocityCmdRaw = self.get(self.velocityCmdKey)
      return velocityCmdRaw
      
   def setPlaceCellStatus(self, placeCellStatusRaw):
      placeCellStatus = json.dumps(placeCellStatusRaw)
      print "Converted placeCellStatusRaw to ", placeCellStatus
      self.set(self.placeCellStatusKey, placeCellStatus)
   
