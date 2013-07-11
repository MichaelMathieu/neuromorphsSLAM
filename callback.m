function callback(dt)
  global robot;
  % Update robot position
  border = 0.05;
  for iobs = 1:size(robot.obstacles, 1)
      robot = obstacleAvoidance(robot.obstacles(iobs,:), robot, border);
  end
  robot.theta = robot.theta + randn() * robot.noise;

  dx = robot.velocity*dt*cos(robot.theta);
  dy = robot.velocity*dt*sin(robot.theta);
  figure(1);
  drawLine(robot.x, robot.y, robot.x+dx, robot.y+dy, 'blue')
  robot.x = robot.x + dx;
  robot.y = robot.y + dy;

  % Update VCO and neurons, at faster rate
  nSubIters = 100;
  potentials = zeros(size(robot.VCO, 2), robot.nNeuronsPerVCO, nSubIters);
  v = [dx/nSubIters, dy/nSubIters];
  for iter = 1:nSubIters
    for i = 1:size(robot.VCO, 2)
      [robot.VCO(1,i), phi] = fakeVCOUpdate(robot.VCO(1,i), v, dt/nSubIters, robot.velocity);
      for j = 1:robot.nNeuronsPerVCO
	[robot.VCOlif(i, j), V] = lifUpdate(robot.VCOlif(i,j), max(phi(j),0), dt/nSubIters);
	potentials(i, j, iter) = V;
      end
    end
  end
  % Display neuron outputs
  figure(2);
  for i = 1:size(robot.VCO,2)
      subplot(robot.nNeuronsPerVCO/2, 2, i);
      plot(reshape(potentials(i,1,:), nSubIters));
      title(["(" num2str(robot.VCO(i).d(1)) " " num2str(robot.VCO(i).d(2)) ")"])
  end  
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
	    rx = robot.x-x1;
	    ry = robot.y-y1;
	    p = (rx*(x2-x1) + ry*(y2-y1)) / norm;
	    if (p > -border/2) && (p < norm+border/2)
	       p2 = (robot.x-x1)*nx + (robot.y-y1)*ny;
	       if p2 >= 0
		  p3 = cos(robot.theta)*nx + sin(robot.theta)*ny;
		  if p3 <= 0
		    if d <= 1.1*robot.velocity % We are too close ! emergency ! Follow the normal
		       robot.theta = atan2(ny, nx);
		    else
		      p4 = cos(robot.theta)*(x2-x1) + sin(robot.theta)*(y2-y1);
		      robot.theta = robot.theta + sign(p4) * 0.2 * pi;
		    end
		  end
	       end
	    end
	 end
end
