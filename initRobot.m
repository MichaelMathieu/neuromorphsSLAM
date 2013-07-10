function robot = initRobot(x, y, theta, obstacles)
	 robot.x = x;
	 robot.y = y;
	 robot.theta = theta;
	 robot.velocity = 0.01;
	 robot.obstacles = obstacles
	 robot.noise = 0.3
end
