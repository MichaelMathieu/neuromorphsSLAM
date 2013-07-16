import numpy
import display
import math

def phaseplot(phases, figure = None):
    w = int(math.ceil(len(phases)*0.5))
    if figure == None:
        scale = 50
        h = 2
        figure = display.GUI(scale,scale*w,scale*h)
    figure.erase()
    i = 0
    for theta in phases:
        polarplot(theta, i%w,i/w, figure)
        i += 1
    return figure

def polarplot(theta, x, y, figure):
    xcenter = x+0.5
    ycenter = y+0.5
    r = 0.45
    figure.line(xcenter-r,ycenter,xcenter+r,ycenter,width=1,color=(0,0,0))
    figure.line(xcenter,ycenter-r,xcenter,ycenter+r,width=1,color=(0,0,0))
    figure.point(xcenter+r*math.cos(theta),
                 ycenter+r*math.sin(theta))
    return figure

if __name__=="__main__":
    fig = None
    for i in range(10):
        fig = phaseplot(i, fig)
