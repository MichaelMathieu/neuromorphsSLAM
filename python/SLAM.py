import numpy
import math
import VCO
import lif
import itertools
import plots

class VCOBank():
    def __init__(self, dirs, nPhases, R = 40, C = 3, abs_ref = 0.005):
        self.Omega = 8.*2*math.pi
        self.nDirs = len(dirs)
        self.nPhases = nPhases
        self.VCOs = [VCO.VCO(dir, self.nPhases, Omega=self.Omega) for dir in dirs]
        self.neurons = [lif.LIFBank(R=R, C=C, abs_ref=abs_ref, n=self.nPhases) \
                        for x in xrange(self.nDirs)]
        self.outputs = numpy.zeros([self.nDirs, self.nPhases])

    def update(self, dx, dy, dt):
        for iDir in xrange(self.nDirs):
            I = self.VCOs[iDir].update(dx, dy, dt)
            I = numpy.maximum(I, 0.)
            self.outputs[iDir,:] = self.neurons[iDir].update(I, dt)
        return self.outputs

class GridCellBank():
    def __init__(self, nDirs, nPhases, connectionGrid,
                 R = 14., C = 1, abs_ref = 0.005, one_weight = 1./30):
        self.nDirs = nDirs
        self.nPhases = nPhases
        self.nGridCells = len(connectionGrid)
        self.w = numpy.zeros([self.nGridCells, nDirs*nPhases])
        for iDir in xrange(nDirs):
            for iGridCell in xrange(self.nGridCells):
                iPhase = connectionGrid[iGridCell][iDir]
                self.w[iGridCell, iDir*nPhases+iPhase] = one_weight
        self.neurons = lif.LIFBank(n = self.nGridCells, R=R, C=C, abs_ref = abs_ref)
        self.outputs = numpy.array(self.nGridCells)

    def update(self, V, dt):
        I = self.w.dot(V.reshape(self.nDirs*self.nPhases,1)).squeeze()
        self.outputs = self.neurons.update(I, dt)
        return self.outputs

class SLAM():
    def __init__(self, VCOblocks=[([0,1],[1,0],[0,-1],[-1,0], 4)]):
        gridCellsCoBase = [[0,0,0],[0,0,1],[0,0,2],[0,0,3],
                            [0,1,0],[0,1,1],[0,1,2],[0,1,3],
                            [0,2,0],[0,2,1],[0,2,2],[0,2,3],
                            [0,3,0],[0,3,1],[0,3,2],[0,3,3]]
        gridCellsCo = [gridCellsCoBase for x in VCOblocks]
        self.VCOs = [VCOBank(dirs, nPhases) for dirs, nPhases in VCOblocks]
        self.gridCells = [GridCellBank(len(dirs), nPhases, pcc) \
                          for (dirs, nPhases),pcc in zip(VCOblocks, gridCellsCo)]
        
    def update(self, dx, dy, dt, robot = None, gui = None):
        for i in xrange(len(self.VCOs)):
            V = self.VCOs[i].update(dx, dy, dt)
            self.gridCells[i].update(V, dt)
        
        # debug
        colorsBase = [0.,0.33,0.67,1.]
        colors = [i for i in itertools.product(colorsBase, colorsBase, colorsBase)]
        if (robot != None) and (gui != None):
            for i in xrange(len(self.gridCells)):
                pc = self.gridCells[i]
                for j in xrange(pc.nGridCells):
                    if pc.outputs[j] > 40:
                        print str(i) + "," + str(j) + " spiking"
                        gui.point(robot.x, robot.y, color=tuple(colors[j]), width=4-i)
                        
                
