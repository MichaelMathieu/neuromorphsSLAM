drawInit();
obstacles = [
	     [0, 0, 1, 0];
	     [1, 0, 1, 1];
	     [1, 1, 0, 1];
	     [0, 1, 0, 0];
	     [0.2, 0.2, 0.2, 0.8];
	     [0.2, 0.8, 0.8, 0.8];
	     [0.8, 0.8, 0.8, 0.6];
	     [0.8, 0.6, 0.4, 0.6];
	     [0.4, 0.6, 0.2, 0.2]
	    ];

for iobs = 1:size(obstacles, 1)
    drawLine(obstacles(iobs, 1), obstacles(iobs, 2), obstacles(iobs, 3), obstacles(iobs, 4),1);
end
%drawRefresh()

global spikes = []
global robot;
robot = initRobot(0.2, 0.1, -pi/2, obstacles);
tick(@callback, 1, 1)
