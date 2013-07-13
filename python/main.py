import display
import gtk
import robot
import SLAM

if __name__=="__main__":
    gui = display.GUI(scale = 400., wpixels = 400., hpixels=400.)
    robot = robot.Robot(x = 0.1, y = 0.1, theta = 3.14/2, noise = 0.3, gui=gui,
                        velocity = 0.2)
    slam = SLAM.SLAM(VCOdirs=[[0,1]])
    nSubIters = 100
    try:
        while True:
            while gtk.events_pending():
                gtk.main_iteration()
            Dt = 0.05
            Dx, Dy = robot.update(Dt)
            dx = Dx/nSubIters
            dy = Dy/nSubIters
            dt = Dt/nSubIters
            for i in range(nSubIters):
                slam.update(dx, dy, dt, robot, gui)
                
                
            
    except KeyboardInterrupt:
        pass
