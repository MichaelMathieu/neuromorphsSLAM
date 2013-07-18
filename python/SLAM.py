import numpy
import math
import VCO
import lif
import itertools
import plots

class VCOBank():
    def __init__(self, dirs, nPhases, R = 40, C = 1, abs_ref = 0.001):
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
                 R = 6., C = 1.4, abs_ref = 0.001, V_th = 10., one_weight = 1./12):
        self.nDirs = nDirs
        self.nPhases = nPhases
        self.nGridCells = len(connectionGrid)
        self.w = numpy.zeros([self.nGridCells, nDirs*nPhases])
        for iDir in xrange(nDirs):
            for iGridCell in xrange(self.nGridCells):
                iPhase = connectionGrid[iGridCell][iDir]
                self.w[iGridCell, iDir*nPhases+iPhase] = one_weight
        self.neurons = lif.LIFBank(n = self.nGridCells, R = R,C = C,
                                    abs_ref = abs_ref, V_th = V_th)
        self.outputs = numpy.array(self.nGridCells)

    def update(self, V, dt):
        I = self.w.dot(V.reshape(self.nDirs*self.nPhases,1)).squeeze()
        self.outputs = self.neurons.update(I, dt)
        return self.outputs

class PlaceCell():
    def __init__(self, connections, R = 40, C = 1, abs_ref = 0.005, V_th = 10):
        # connections : [(iGridResolution, iGridCell, w)]
        self.connections = connections
        self.neuron = lif.LIF(R=R, C=C, abs_ref=abs_ref, V_th = V_th)
        self.output = 0.
        
    def update(self, gridCells, dt):
        I = 0.
        for iGridRes, iGridCell, w in self.connections:
        #if gridCells[iGridRes].outputs[iGridCell] > 40:
            I += w * gridCells[iGridRes].outputs[iGridCell]
        self.output = self.neuron.update(I, dt)
        return self.output

class SLAM():
    def __init__(self, VCOblocks=[([[0,1],[1,0],[0,-1],[-1,0]],4)],
                 gridCellsConstants = [(6.,1.4,0.001,10.)]):
        # VCO
        self.VCOs = [VCOBank(dirs, nPhases) for dirs, nPhases in VCOblocks]
        # Grid cells
        gcb = xrange(7)
        gridCellsCo = [[[0,i,j] for i,j in itertools.product(xrange(nph),xrange(nph))] \
                       for vco,nph in VCOblocks]
        self.gridCells = [GridCellBank(len(dirs),nPhases,pcc,R=R,C=C,abs_ref=ar,V_th=Vth) \
                          for (dirs, nPhases),pcc,(R,C,ar,Vth) \
                          in zip(VCOblocks, gridCellsCo, gridCellsConstants)]
        # Place cells
        self.placeCells = []
        self.winSize = 200 #TODO: dt
        self.iWin = 0
        self.gridCellsSpikes = [numpy.zeros([gc.nGridCells, self.winSize]) \
                                for gc in self.gridCells]
        self.it = 0
        self.placeCellsToPut = []

    def newPlaceCell(self):
        self.placeCellsToPut.append(self.it+self.winSize/2)

    def newPlaceCellDephased(self):
        #TODO: this is not centered
        w = [x.sum(1) for x in self.gridCellsSpikes]
        connections = []
        total_incoming = 0.
        for i in xrange(len(w)):
            for j in xrange(w[i].size):
                if w[i][j] > 0:
                    connections.append((i,j,float(w[i][j])))
                    total_incoming += w[i][j]
        if total_incoming < len(w):
            print "No possible place cell here : No enough incomming spikes..."
            return
        W = 1.5/total_incoming
        connections = [(i,j,weight*W) for (i,j,weight) in connections]
        print connections
        self.placeCells.append(PlaceCell(connections, R=50, C=1, V_th=9))
        print "New place cell  \o/"
        
    def update(self, dx, dy, dt, robot = None, gui = None):
        # VCO + Grid cells
        for i in xrange(len(self.VCOs)):
            I = self.VCOs[i].update(dx, dy, dt)
            V = self.gridCells[i].update(I, dt)
            self.gridCellsSpikes[i][:,self.iWin] = (V>40)
        # Place cells
        for pc in self.placeCells:
            pc.update(self.gridCells, dt)
        self.iWin = (self.iWin + 1) % self.winSize
        for placeCellToPut in self.placeCellsToPut:
            if placeCellToPut == self.it:
                self.newPlaceCellDephased()
        self.it += 1
        
        # debug
        #colorsBase = [0.,0.125,0.25,0.5,0.75,0.875,1.]
        #colorsBase = [0.,0.33,0.67,1.]
        # colors = [i for i in itertools.product(colorsBase, colorsBase, colorsBase)]
        # if (robot != None) and (gui != None):
        #     for i in xrange(len(self.gridCells)):
        #         pc = self.gridCells[i]
        #         for j in xrange(pc.nGridCells):
        #             if pc.outputs[j] > 40:
        #                 if i == 1:
        #                     print str(i) + "," + str(j) + " spiking"
        #                     gui.point(robot.x, robot.y, color=tuple(colors[j%len(colors)]), width=i+3)

        colorsBase = [0,0.5,1]
        placeCellColors = [i for i in itertools.product(colorsBase,colorsBase,colorsBase) \
                           if i != (1,1,1)]
        if (robot != None) and (gui != None):
            for i in xrange(len(self.placeCells)):
                pc = self.placeCells[i]
                if pc.output > 40:
                    print "PC: " + str(i) + " spiking"
                    gui.point(robot.x, robot.y, color=placeCellColors[i%len(placeCellColors)], width=5)
        
                
