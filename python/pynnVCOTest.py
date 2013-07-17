import pynnVCO
import math
import numpy
import millis

dt = 0.5
simLength = 2000

# VCO:
VCOdirs=[[1,0],[0,0]]
VCOdirs = [[0.5*x,0.5*y] for x,y in VCOdirs]
Omega = 8.*2*math.pi
nPerVCO = 1
VCOLifOutputs = numpy.array([])

# Run the pynn simulation with 100x more precision
pynnVCO = pynnVCO.pynnVCO(VCOdirs, nPerVCO, dt, Omega)

VCOLifOutputs = [[[] for n in xrange(nPerVCO)] for d in xrange(len(VCOdirs))]
for i in range(simLength):
   dx,dy = [1,0]
   nrns = pynnVCO.update(dx,dy,dt)
   for d in xrange(len(VCOdirs)):
      for n in xrange(nPerVCO):
         VCOLifOutputs[d][n].append(nrns[d][n])


import pylab
pylab.figure(1)
for d in xrange(len(VCOdirs)):
   for n in xrange(nPerVCO):
      subplotNum = n*len(VCOdirs) + d + 1
      print "Subplot %d (%d, %d) " % (subplotNum, d, n)
      pylab.subplot(nPerVCO, len(VCOdirs), subplotNum) 
      pylab.plot(range(simLength), VCOLifOutputs[0][0])
      pylab.xlabel("time (ms)")
      pylab.ylabel("Vm (mV)")
      pylab.title("Dir %d, nrn %d" % (d, n))
pylab.show(1)

