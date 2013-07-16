#!/usr/bin/python

from pyNN.utility import get_script_args
from pyNN.brian import *

dt = 0.05
setup(timestep=dt, min_delay=dt/10)

cell = create(IF_curr_exp, {'v_thresh': -55.0, 'tau_refrac': 5.0})

record_v(cell, "Results/StepCurrentSource_nest.v") 
#runs = 10
#runlen = 1000
#for i in range(runs):
#   source = ACSource(amplitude=10, frequency=i, start=runlen*i, stop=runlen*i+runlen)
#   source.inject_into(cell)
#   run(runlen)
#
#source = ACSource(amplitude=1, frequency=4, start=0, stop=10000)
simLen = 3000
innerLoop = dt
i=0
for i in range(simLen):
   source = DCSource(amplitude = i/500, start = innerLoop*i, stop = innerLoop*i + innerLoop) #nA, ms,     
   source.inject_into(cell)
   run(innerLoop)
   

import pylab
id, t, v = cell.get_v().T
pylab.figure(1)
pylab.plot(t, v)
pylab.xlabel("time (ms)")
pylab.ylabel("Vm (mV)")
pylab.show(1)

