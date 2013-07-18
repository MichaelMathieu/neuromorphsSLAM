from brian import *
from datetime import *
taum = 20 * ms
taue = 10 * ms
Vt = 10 * mV
Vr = 0 * mV
El = -51 * mvolt          # resting potential (same as the reset)
psp = 0.5 * mvolt         # postsynaptic potential size
N = 1000
eqs = Equations('''
      dV/dt  = (I-V)/taum : volt
      I : volt
      ''')

print "Loaded Brian"
G = NeuronGroup(N=N, model=eqs,
              threshold=Vt, reset=Vr)
G.I = 0.05
M = StateMonitor(G, 'V', record=0)
M2 = StateMonitor(G, 'I', record=0)
start = datetime.now()
for i in range(1000):
   G.I = 0.05 + 0.01 * i
   run(1 * msecond)
stop = datetime.now()
print "Ran in ", stop - start 
subplot(2,1,1)
xlabel('Time (in ms)')
ylabel('Membrane potential (in mV)')
title('Membrane potential for neuron 0')
plot(M.times / ms, M[0] / mV)
subplot(2,1,2)
plot(M.times / ms, M2[0] / mV)
show()

