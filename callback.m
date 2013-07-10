function callback()
  global robot;
  dx = robot.velocity*cos(robot.theta);
  dy = robot.velocity*sin(robot.theta);
  drawLine(robot.x, robot.y, robot.x+dx, robot.y+dy, 'blue')
  robot.x += dx;
  robot.y += dy;
  
  border = 0.05;
  for iobs = 1:size(robot.obstacles, 1)
      robot = obstacleAvoidance(robot.obstacles(iobs,:), robot, border);
  end
  robot.theta += normrnd(0, 0.02);
end

function robot = obstacleAvoidance(obstacle, robot, border)
	 %obstacle : [x1, y1, x2, y2]
	 x1 = obstacle(1);
	 y1 = obstacle(2);
	 x2 = obstacle(3);
	 y2 = obstacle(4);
	 a = y2-y1;
	 b = -(x2-x1);
	 c = -a*x1 - b*y1;
	 norm = sqrt(a*a+b*b);
	 nx = -(y2-y1);
	 ny = x2-x1;
	 d = abs(a*robot.x+b*robot.y+c)/norm;
	 if d < border
	    p = (robot.x-x1)*(x2-x1) + (robot.y-y1)*(y2-y1);
	    if (p > -border) & (p < norm+border)
	       p2 = (robot.x-x1)*nx + (robot.y-y1)*ny;
	       if p2 >= 0
		  p3 = cos(robot.theta)*nx + sin(robot.theta)*ny;
		  if p3 <= 0
		    p4 = cos(robot.theta)*(x2-x1) + sin(robot.theta)*(y2-y1);
		    robot.theta += sign(p4) * 0.2 * pi;
		  end
	       end
	    end
	 end
end