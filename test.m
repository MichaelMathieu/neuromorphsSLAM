drawInit();
drawLine(0.2, 0.2, 0.8, 0.2)
drawLine(0.8, 0.2, 0.8, 0.8)
drawLine(0.8, 0.8, 0.2, 0.8)
drawLine(0.2, 0.8, 0.2, 0.2)
global robot = initRobot(0.1, 0.3, -pi/2);
tick(@callback, 1)
#waitforbuttonpress
