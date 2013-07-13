function tick(cb, fps, fastforward)
  global stopTick;
  total_time = 0;
  stopTick = 0;
  if fastforward
     dt = 1/fps;
     while stopTick == 0
       total_time = total_time + dt;
       cb(dt, total_time)
     end
  else
    waitTime = 1./(fps*24*3600);
	lastTick = now;
	nextTick = lastTick + waitTime;
	%cb(0);
	while  stopTick == 0
        t = now;
        if t >= nextTick
	  %dt = (t-lastTick)*24*3600;
	   dt = waitTime*24*3600;
	   total_time = total_time + dt;
	   cb(dt, total_time);
            lastTick = t;
            nextTick = nextTick + waitTime;
        else
            pause(nextTick-t);
        end
	end
  end
end
