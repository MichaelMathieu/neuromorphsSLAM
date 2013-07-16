import numpy

class LIF():
    def __init__(self, C = 1, R = 40, abs_ref = 0.005, V_th = 10, V_spike = 50):
        # R in nF
        # C in M ohms
        # all V in volts
        # all times in seconds
        self.C = C
        self.R = R
        self.abs_ref = abs_ref
        self.V_th = V_th
        self.ref = 0
        self.V = 0
        self.V_reset = 0.2 * V_th
        self.V_spike = 50

    def update(self, I, dt):
        if self.ref < 0.001:
            self.V += dt*1000*( - self.V/(self.R*self.C) + I/self.C)
            self.V = max(self.V, 0)
        else:
            self.ref -= dt
            self.V = self.V_reset
        if self.V > self.V_th:
            self.V = self.V_spike
            self.ref = self.abs_ref
        return self.V

class LIFBank():
    def __init__(self, n, C = 1, R = 40, abs_ref = 0.005, V_th = 10, V_spike = 50):
        # computes n neurons at a time. faster than LIF
        # R in M ohms 
        # C in nF 
        # all V in volts
        # all times in seconds
        self.C = C
        self.R = R
        self.abs_ref = abs_ref
        self.V_th = V_th
        self.ref = numpy.zeros(n)
        self.V = numpy.zeros(n)
        self.V_reset = 0.2 * V_th
        self.V_spike = 50

    def update(self, I, dt):
        nrefs = self.ref < 0.001
        self.V += (-self.V/(self.R*self.C) + I/self.C)*dt*1000
        self.V = self.V * (self.V > 0)
        refs = 1-nrefs
        self.ref -= refs*dt
        self.V = nrefs*self.V + refs*self.V_reset
        th = self.V > self.V_th
        nth = 1-th
        self.V = nth*self.V + th*self.V_spike
        self.ref = nth*self.ref + th*self.abs_ref
        return self.V

# unit test
if __name__=="__main__":
    n = 10
    dt = 0.001
    I = numpy.random.randn(n)
    lif = [LIF() for i in xrange(n)]
    lifs = LIFBank(n)
    for k in xrange(100):
        V1 = numpy.zeros(n)
        for i in xrange(n):
            V1[i] = lif[i].update(I[i], dt)
        V2 = lifs.update(I, dt)
        assert abs(sum(V1-V2) < 0.1)
        
