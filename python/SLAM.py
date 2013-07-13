import numpy
import math
import VCO
import lif
import itertools

class SLAM():
    def __init__(self, VCOdirs=[[0,1],[1,0],[0,-1],[-1,0]], nPerVCO=4):
        # VCO:
        self.controlVCO = VCO.VCO([0,0], 1)
        self.VCOs = [VCO.VCO(d, nPerVCO) for d in VCOdirs]
        self.VCOoutputs = numpy.zeros([len(self.VCOs), nPerVCO])
        self.VCOlif = [[lif.LIF(R=40, abs_ref = 0.01) for i in xrange(nPerVCO)] \
                           for j in xrange(len(VCOdirs))]
        self.VCOlifoutputs = numpy.zeros([len(self.VCOs), nPerVCO])
        self.nVCO = len(VCOdirs)
        self.nPerVCO = nPerVCO
        
        # Place cells:
#         placeCellsCo = [i for i in itertools.product(range(nPerVCO), range(nPerVCO))]
#         self.nPlaceCells = len(placeCellsCo)
#         self.wPlaceCells = numpy.zeros([self.nPlaceCells, self.nVCO*self.nPerVCO])
#         for k in xrange(self.nPlaceCells):
#             for i in xrange(self.nVCO):
#                 for j in xrange(self.nPerVCO):
#                     self.wPlaceCells[k, i*self.nPerVCO + j] = 1/70
#         self.placeCells = [lif.LIF(R=100, abs_ref = 0.005) for i in xrange(self.nPlaceCells)]
#         self.placeCellsOutputs = numpy.zeros([self.nPlaceCells])        
        
    def update(self, dx, dy, dt, robot = None, gui = None):
        # VCO:
        controlOutput = self.controlVCO.update(0, 0, dt)
        for i in xrange(len(self.VCOs)):
            self.VCOoutputs[i,:] = self.VCOs[i].update(dx, dy, dt)
            for j in xrange(self.nPerVCO):
                I = 1 * max(self.VCOoutputs[i][j],0)
                self.VCOlifoutputs[i][j] = self.VCOlif[i][j].update(I, dt)
        # debug
        if (robot != None) and (gui != None):
            #if controlOutput > 0.5:
            #    gui.point(robot.x, robot.y, color=(0,0,0), width = 5)
            for i in xrange(len(self.VCOlifoutputs)):
                outputLine = self.VCOlifoutputs[i]
                for j in xrange(len(outputLine)):
                    output = outputLine[j]
                    if (output > 40) and (controlOutput > 0.5):
                        color = [0,0,0,0.5]
                        color[i] = float(j+1)/4
                        gui.point(robot.x, robot.y, color=tuple(color), width = 4)

        # Place cells:
#         I = self.wPlaceCells * self.VCOlifoutputs.reshape(self.nVCO*self.nPerVCO)
#         for i in xrange(self.nPlaceCells):
#             cell = self.placeCells[i]
#             V = cell.update(self.VCO, I[i], dt)
#             self.placeCellsOutputs[i] = V

        # debug
#         colors = [i for i in itertools.product([0., 0.5, 1.], 
#         if (robot != None) and (gui != None):
#             for i in xrange(self.nPlaceCells):
                
