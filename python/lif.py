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
        if self.ref < 0:
            self.V += dt*1000*( - self.V/(self.R*self.C) + I/self.C)
            self.V = max(self.V, 0)
        else:
            self.ref -= dt
            self.V = self.V_reset
        if self.V > self.V_th:
            self.V = self.V_spike
            self.ref = self.abs_ref
        return self.V
