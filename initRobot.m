function robot = initRobot(x, y, theta, obstacles)
	 robot.x = x;
	 robot.y = y;
	 robot.theta = theta;
	 robot.velocity = 0.01;
	 robot.obstacles = obstacles;
	 robot.noise = 0.05; %TODO : 0.3
	 robot.nNeuronsPerVCO = 4;
	 dirs = [[0;1],[1;0],[0;-1],[-1;0]];
	 robot.VCO = [];
	 for i = 1:size(dirs,2)
	   robot.VCO = [robot.VCO fakeVCOInit(dirs(:,i), robot.nNeuronsPerVCO)];
	 end
	 robot.VCOlif = [];
	 for i = 1:size(robot.VCO, 2)
	     for j = 1:robot.nNeuronsPerVCO
	       robot.VCOlif = [ robot.VCOlif lif(1, 40, 0.005, 10)];
	     end
	 end
	 robot.VCOlif = reshape(robot.VCOlif, [size(robot.VCO, 2), robot.nNeuronsPerVCO]);
end
