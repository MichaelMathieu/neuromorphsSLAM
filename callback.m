function callback(dt)
  global robot;
  dx = robot.velocity*dt*cos(robot.theta);
  dy = robot.velocity*dt*sin(robot.theta);
  figure(1);
  drawLine(robot.x, robot.y, robot.x+dx, robot.y+dy, 'blue')
  robot.x = robot.x + dx;
  robot.y = robot.y + dy;

  global debugVCO
  nSubIters = 100;
  v = [dx/nSubIters, dy/nSubIters];
  for iter = 0:(nSubIters-1)
    n = size(debugVCO, 2)+1;
    for i = 1:size(robot.VCO, 2)
      [robot.VCO(1,i), phi] = fakeVCOUpdate(robot.VCO(1,i), v, dt/nSubIters, robot.velocity);
      for j = 1:robot.nNeuronsPerVCO
	[robot.VCOlif(i, j), V] = lifUpdate(robot.VCOlif(i,j), max(phi(j),0), dt/nSubIters);
	if j == 1
	  debugVCO(i, n) = V;
	end
      end
    end
  end
  
  figure(2);
  for j = 1:robot.nNeuronsPerVCO
      nVals = 500;
      vMax = size(debugVCO,2);
      vMin = max(1,vMax-nVals);
      subplot(robot.nNeuronsPerVCO, 1, j);
      plot(debugVCO(j,vMin:vMax));
      title([num2str(robot.VCO(j).d(1)) " " num2str(robot.VCO(j).d(2))])
  end
  
  if 0 %debug curves     
    figure(2);
    global debugVCO;
    %[robot.VCO(1,1), phi] = fakeVCOUpdate(robot.VCO(1,1), [dx,, dt, robot.velocity);
    n = size(debugVCO,2)+1
    debugVCO(1, n) = size(debugVCO,2);
    debugVCO(2, n) = phi(1);
    debugVCO(6, n) = phi(2);
    dotp = dot(robot.VCO.d, [dx, dy]);
    debugVCO(4, n) = robot.VCO.phase;
    if dt ~= 0
      debugVCO(3, n) = dotp/(robot.velocity*dt*norm(robot.VCO.d));
      %derivative = (debugVCO(4, n) - debugVCO(4, n-1))/dt;
      derivative = (atan2(debugVCO(2, n),debugVCO(6, n)) ...
		    - atan2(debugVCO(2, n-1), debugVCO(6, n-1)))/dt;
      derivative = mod(derivative, 2*pi);
      debugVCO(5, n) = (derivative/0.2-dt*robot.VCO.Omega)/(dt*norm(robot.VCO.d));
      if (debugVCO(5, n) < -1.2) | (debugVCO(5, n) > 1.2)
	debugVCO(5, n) = debugVCO(5, n-1);
      end
      debugVCO(5, n) = max(-1, min(debugVCO(5, n), 1))
      subplot(2,1,1); plot(debugVCO(1,:), debugVCO(2,:), 'Color', 'blue', ...
			   debugVCO(1,:), debugVCO(6,:), 'Color', 'red');
      subplot(2,1,2); plot(debugVCO(1,:), debugVCO(3,:),'Color', 'blue', ...
			   debugVCO(1,:), debugVCO(5,:),'Color', 'red');
    end
  end
  
  
  border = 0.05;
  for iobs = 1:size(robot.obstacles, 1)
      robot = obstacleAvoidance(robot.obstacles(iobs,:), robot, border);
  end
  robot.theta = robot.theta + randn() * robot.noise;
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
