import numpy
import math
import pynnVCO
import lif
import itertools

class SLAM():
    def __init__(self, simStepS, VCOdirs=[[0,1],[1,0],[0,-1],[-1,0]], nPerVCO=4):
        # VCO:
        Omega = 8.*2*math.pi
        self.VCOlifoutputs = numpy.zeros([len(VCOdirs), nPerVCO])
	# Run the pynn simulation with 100x more precision
	pynnSimStepS = simStepS/100
 	self.pynnVCO = pynnVCO.pynnVCO(VCOdirs, nPerVCO, pynnSimStepS, Omega)
        self.nVCO = len(VCOdirs)
        self.nPerVCO = nPerVCO
        
        # Place cells:
        placeCellsCo = [[0,0,0],[0,1,0],[0,2,0],[0,3,0],
                        [0,0,1],[0,1,1],[0,2,1],[0,3,1],
                        [0,0,2],[0,1,2],[0,2,2],[0,3,2],
                        [0,0,3],[0,1,3],[0,2,3],[0,3,3]]
        #placeCellsCo = [i for i in itertools.product(range(nPerVCO), range(nPerVCO))]
        self.nPlaceCells = len(placeCellsCo)
        self.wPlaceCells = numpy.zeros([self.nPlaceCells, self.nVCO*self.nPerVCO])
        for k in xrange(self.nPlaceCells):
            for i in xrange(self.nVCO):
                self.wPlaceCells[k, i*self.nPerVCO + placeCellsCo[k][i]] = 1./15
        C = 1
        R = 2.3*1./(C*1e-9*math.log(2.)*2*math.pi*Omega)/1e6
        self.placeCells = lif.LIFBank(self.nPlaceCells, R=R, C=C, abs_ref=0.005)

        self.testPC = [[] for i in xrange(self.nPlaceCells)]
        self.t = 0
        
    def update(self, dx, dy, dt, robot = None, gui = None):
        self.VCOlifoutputs = self.pynnVCO.update(dx,dy,dt)
        # debug
#         if (robot != None) and (gui != None):
#             colors = [i for i in itertools.product([0.,0.5,1.], [0.,0.5,1.], [0.,0.5,1.])]
#             #if controlOutput > 0.5:
#             #    gui.point(robot.x, robot.y, color=(0,0,0), width = 5)
#             for i in xrange(len(self.VCOlifoutputs)):
#                 outputLine = self.VCOlifoutputs[i]
#                 #for j in xrange(len(outputLine)):
#                 for j in xrange(1):
#                     output = outputLine[j]
#                     if (output > 40):# and (controlOutput > 0.5):
#                         #color = [0,0,0,0.5]
#                         #color[i] = float(j+1)/4
#                         color = colors[i*4+j]
#                         gui.point(robot.x, robot.y, color=tuple(color), width = 4)

        # Place cells:
        I = self.wPlaceCells.dot(self.VCOlifoutputs.reshape(self.nVCO*self.nPerVCO,1)).squeeze()
        self.placeCellsOutputs = self.placeCells.update(I, dt)
#         self.t += dt
#         for i in xrange(self.nPlaceCells):
#             if I[i].squeeze() > 40:
#                 self.testPC[i].append((self.t,I[i].squeeze()/50))
#         deltat = 10./(8*2*math.pi*10)
#         self.testPC = [[(t,a) for (t,a) in x if t > self.t-deltat] for x in self.testPC]
#         #print self.testPC
#         self.placeCellsOutputs = [sum([a for (t,a) in x]) for x in self.testPC]

        # debug
        colors = [i for i in itertools.product([0.,0.5,1.], [0.,0.5,1.], [0.,0.5,1.])]
        if (robot != None) and (gui != None):
            for i in xrange(self.nPlaceCells):
                if self.placeCellsOutputs[i] > 40:
                #if self.placeCellsOutputs[i] > 2.5:
                    print i
                    gui.point(robot.x, robot.y, color=tuple(colors[i]), width=4)
                
