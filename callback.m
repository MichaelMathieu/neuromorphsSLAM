function callback(dt, total_time)
  global robot;
  % Update robot position
  % border = 0.05;
  % for iobs = 1:size(robot.obstacles, 1)
  %     robot = obstacleAvoidance(robot.obstacles(iobs,:), robot, border);
  % end
  robot.theta = robot.theta + randn() * robot.noise;

  dx = robot.velocity*dt*cos(robot.theta);
  dy = robot.velocity*dt*sin(robot.theta);
  %robot.theta = robot.theta + pi/4;
  drawLine(robot.x, robot.y, robot.x+dx, robot.y+dy, 1, 'blue')
  drawRefresh();
  robot.x = robot.x + dx;
  robot.y = robot.y + dy;
  robot.tick = robot.tick + 1;

  % Update VCO and neurons, at faster rate
  nSubIters = 500;
  potentials = zeros(size(robot.VCO, 2), robot.nNeuronsPerVCO, nSubIters);
  v = [dx/nSubIters, dy/nSubIters];
  for iter = 1:nSubIters
    for i = 1:size(robot.VCO, 2)
      [robot.VCO(1,i), phi] = fakeVCOUpdate(robot.VCO(1,i), v, dt/nSubIters);
      for j = 1:robot.nNeuronsPerVCO
	[robot.VCOlif(i, j), V] = lifUpdate(robot.VCOlif(i,j), 0.8*max(phi(j),0), dt/nSubIters);
	potentials(i, j, iter) = V;
      end
    end
  end
  % Display VCO neuron outputs
<<<<<<< HEAD
  ## figure(2);
  ## for i = 1:size(robot.VCO,2)
  ##     subplot(1+robot.nNeuronsPerVCO/2, 2, i);
  ##     plot(reshape(potentials(i,1,:), nSubIters));
  ##     title(["(" num2str(robot.VCO(i).d(1)) " " num2str(robot.VCO(i).d(2)) ")"])
  ## end
  % Display VCO phase
  figure(4);
  phases = [];
  for i = 1:size(robot.VCO,2)
    phase = robot.VCO(i).phase;
    phase = phase - robot.VCO(i).Omega * total_time;
    phases(i) = phase;
    subplot(1,4,i); polar(phase, 1, 'ko');
  end
  
  % Update place cells
  %potentials = reshape(potentials, robot.nNeuronsPerVCO*size(robot.VCO,2), nSubIters);
  kInputs = robot.nNeuronsPerVCO*size(robot.VCO,2);
  placeCellsOutputs = zeros(robot.nPlaceCells, nSubIters);
  placeCellsHist = [];
  todisp = [];
  global spikes;
  colors = [1,1,0;1,0,1;0,1,1;1,0,0;0,1,0;0,0,1;0,0,0];
  for i = 1:nSubIters
    I = robot.wPlaceCells * reshape(transpose(squeeze(potentials(:,:,i))), [kInputs,1]);
    todisp(i) = I(1);
    for j = 1:robot.nPlaceCells
      [robot.placeCells(j), W] = lifUpdate(robot.placeCells(j), I(j), dt/nSubIters);
      if W > 40
	 spikes = [spikes; [robot.x-dx+dx*i/nSubIters,robot.y-dy+dy*i/nSubIters, ceil(j/7), colors(mod(j,7)+1,:)] ];
   	['Spike from cell ' num2str(j) ' at (' num2str(robot.x-dx+dx*i/nSubIters) ' ' num2str(robot.y-dy+dy*i/nSubIters) ')']
	placeCellsHist = [placeCellsHist j];
      end
      placeCellsOutputs(j,i) = W;
    end
  end
  %if length(placeCellsHist) > 0
  %figure(2);
  %hist(placeCellsHist,linspace(1,robot.nPlaceCells,robot.nPlaceCells));
  % subplot(1+robot.nNeuronsPerVCO/2, 2, 5);
  % plot(placeCellsOutputs(1,:))
  % subplot(1+robot.nNeuronsPerVCO/2, 2, 6);
  % plot(todisp);
  %end
  if size(spikes,1) > 0
    figure(3);
    scatter(spikes(:,1), spikes(:,2), (spikes(:,3)+1)*4, spikes(:,4:6));
    axis([0,1,-.5,.5])
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
