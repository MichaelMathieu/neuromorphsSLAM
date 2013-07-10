function callback()
  global robot;
  dx = robot.velocity*cos(robot.theta);
  dy = robot.velocity*sin(robot.theta);
  drawLine(robot.x, robot.y, robot.x+dx, robot.y+dy, 'blue')
  robot.x += dx;
  robot.y += dy;
  %robot.x, robot.y
  
  #robot.theta = mod(robot.theta, 2*pi);
  border = 0.05;
  ## if robot.y < border
  ##   if dy < 0
  ##     robot.theta += sign(dx)*0.2*pi;
  ##   end
  ## end
  ## if robot.x < border
  ##   if dx < 0
  ##     robot.theta -= sign(dy)*0.2*pi;
  ##   end
  ## end
  ## if robot.y > 1-border
  ##    if dy > 0
  ## 	robot.theta -= sign(dx)*0.2*pi;
  ##    end
  ## end
  ## if robot.x > 1-border
  ##   if dx > 0
  ##     robot.theta += sign(dy)*0.2*pi;
  ##   end
  ## end
  robot = obstacleAvoidance([0,0,1,0],robot,border);
  robot = obstacleAvoidance([1,0,1,1],robot,border);
  robot = obstacleAvoidance([1,1,0,1],robot,border);
  robot = obstacleAvoidance([0,1,0,0],robot,border);
  robot = obstacleAvoidance([0.2, 0.2, 0.2, 0.8], robot, border);
  robot = obstacleAvoidance([0.2, 0.8, 0.8, 0.8], robot, border);
  robot = obstacleAvoidance([0.8, 0.8, 0.8, 0.2], robot, border);
  robot = obstacleAvoidance([0.8, 0.2, 0.2, 0.2], robot, border);
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
