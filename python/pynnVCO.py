import VCO
import lif
import math
import numpy

class pynnVCO():
   def __init__(self, dirs, nPerVCO, Omega=8*2*math.pi):
      self.dirs = dirs
      self.Omega = Omega
      self.nPerVCO = nPerVCO
      self.VCOs = [VCO.VCO(d, nPerVCO, Omega) for d in self.dirs]
      self.VCOoutputs = numpy.zeros([len(self.VCOs), nPerVCO])
      self.VCOlifoutputs = numpy.zeros([len(self.VCOs), nPerVCO])
      self.VCOlif = [[lif.LIF(R=40, abs_ref = 0.01) for i in xrange(nPerVCO)] for j in xrange(len(dirs))]
     
   def update(self, dx, dy, dt):
     for i in xrange(len(self.VCOs)):
        self.VCOoutputs[i,:] = self.VCOs[i].update(dx, dy, dt)
        for j in xrange(self.nPerVCO):
           I = 1 * max(self.VCOoutputs[i][j],0)
           self.VCOlifoutputs[i][j] = self.VCOlif[i][j].update(I, dt)

     return self.VCOlifoutputs    
