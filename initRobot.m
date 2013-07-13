function robot = initRobot(x, y, theta, obstacles)
	 robot.x = x;
	 robot.y = y;
	 robot.theta = theta;
	 robot.velocity = 0.1;
	 robot.obstacles = obstacles;
	 robot.noise = 0.;
	 robot.tick = 1;
	 
	 % VCO
	 robot.nNeuronsPerVCO = 4;
	 dirs = [[0;1],[1;0],[0;-1],[-1;0]];
	 robot.VCO = [];
	 for i = 1:size(dirs,2)
	   robot.VCO = [robot.VCO fakeVCOInit(dirs(:,i), robot.nNeuronsPerVCO)];
	 end
	 robot.VCOlif = [];
	 for i = 1:size(robot.VCO, 2)
	     for j = 1:robot.nNeuronsPerVCO
	       robot.VCOlif = [ robot.VCOlif lif(1, 40, 0.010, 10)];
	     end
	 end
	 robot.VCOlif = reshape(robot.VCOlif, [size(robot.VCO, 2), robot.nNeuronsPerVCO]);
	 
	 % Place cells
	 robot.nPlaceCells = 64;
	 connec = zeros(robot.nPlaceCells, size(dirs,2));
	 robot.placeCells = [];
	 for i = 1:robot.nPlaceCells
	   %while length(unique(connec(i,:))) ~= length(connec(i,:))
	     for j = 1:size(dirs,2)
	       connec(i,j) = ceil(rand()*robot.nNeuronsPerVCO);
	     end
	   %end
	   robot.placeCells = [ robot.placeCells lif(1, 100, 0.005, 10)];
	 end
	 connec(1,:) = [1,1,1,1];
	 connec(2,:) = [2,1,4,1];
	 connec(3,:) = [3,1,3,1];
	 connec(4,:) = [4,1,2,1];
	 robot.wPlaceCells = zeros(robot.nPlaceCells, robot.nNeuronsPerVCO*size(dirs,2));
	 for i = 1:robot.nPlaceCells;
	   for j = 1:size(dirs,2)
	     k = connec(i,j);
	     robot.wPlaceCells(i, (j-1)*robot.nNeuronsPerVCO+k) = 1/70;
	   end
	 end
end
