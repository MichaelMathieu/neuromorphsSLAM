import math
import numpy

class VCO():
    def __init__(self, d, n, Omega = 8.*2*math.pi):
        # d = [x,y] : direction of the VCO
        # n : number of outputs
        self.d = [float(d[0]), float(d[1])]
        self.dnorm = math.sqrt(self.d[0]*self.d[0]+self.d[1]*self.d[1])*2.5
        self.dnorm = 1
        print(self.dnorm)
        self.n = n
        self.phase = 0.
        self.alpha = 2.*math.pi
        self.Omega = 0#Omega
        self.K = numpy.array([2*math.pi*i/n for i in xrange(n)])
        
    def update(self, dx, dy, dt):
        dphase = dt*self.Omega*self.dnorm + self.alpha*(dx*self.d[0]+dy*self.d[1])
        self.phase += dphase
        return self.H(self.K + self.phase, dphase/dt)
        #return numpy.cos(self.K + self.phase)

    def H(self, x, dp):
        width = 0.01
        d = width*dp
        t = numpy.mod(x, 2*math.pi)
        return numpy.logical_and(t+d >= math.pi/2, t-d <= math.pi/2).astype('float')
