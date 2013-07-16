import VCO
import lif
import math
import numpy
import pyNN.brian as pynnSim

from datetime import datetime
from datetime import timedelta
start_time = datetime.now()
# returns the elapsed milliseconds since the start of the program
def millis():
   dt = datetime.now() - start_time
   ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
   return ms


class pynnVCO():
   def __init__(self, dirs, nPerVCO, dt, Omega=8*2*math.pi):
      self.dirs = dirs
      self.Omega = Omega
      self.nPerVCO = nPerVCO
      self.VCOs = [VCO.VCO(d, nPerVCO, Omega) for d in self.dirs]
      self.VCOoutputs = numpy.zeros([len(self.VCOs), nPerVCO])
      self.VCOlifoutputs = numpy.zeros([len(self.VCOs), nPerVCO])

      # Need to make sure that the pyNN timestep is smaller or equal to the robot motion velocity
      dt = 0.1
      pynnSim.setup(timestep=dt/10, min_delay=dt/10)
      self.currSimTime = pynnSim.get_current_time()
      self.VCOlif = [[pynnSim.create(pynnSim.IF_curr_exp, {'v_thresh':-55.0, 'tau_refrac':5.0}) for i in xrange(nPerVCO)] for j in xrange(len(dirs))]
      for i in xrange(len(dirs)):
	 for j in xrange(nPerVCO):
	    pynnSim.record_v(self.VCOlif[i][j], "Results/StepCurrentSource_nest.v") 
     
   def update(self, dx, dy, dt):
      for i in xrange(len(self.VCOs)):
         self.VCOoutputs[i,:] = self.VCOs[i].update(dx, dy, dt)
         for j in xrange(self.nPerVCO):
            I = 1 * max(self.VCOoutputs[i][j],0)
	    source = pynnSim.DCSource(amplitude = I, start = self.currSimTime, stop = self.currSimTime+dt) #nA, ms, ms  
            source.inject_into(self.VCOlif[i][j])
	 
      #print "Starting update at %d" % (millis())
      pynnSim.run(dt)
      #print "Finished update at %d" % (millis())
      self.currSimTime = pynnSim.get_current_time()
      for i in xrange(len(self.VCOs)):
         for j in xrange(self.nPerVCO):
	    # get_v returns history of whole sim, so just get the most recent row.  Each row is [id, T, v], so v is [2]
	    self.VCOlifoutputs[i][j] = self.VCOlif[i][j].get_v()[-1][2]

      return self.VCOlifoutputs    
