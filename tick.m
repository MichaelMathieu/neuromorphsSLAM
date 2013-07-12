function tick(cb, fps, fastforward)
  global stopTick;
  stopTick = 0;
  if fastforward
     while stopTick == 0
       cb(1/fps)
     end
  else
    waitTime = 1./(fps*24*3600);
	lastTick = now;
	nextTick = lastTick + waitTime;
	%cb(0);
	while  stopTick == 0
        t = now;
        if t >= nextTick
            %cb((t-lastTick)*24*3600);
	    cb(waitTime*24*3600)
            lastTick = t;
            nextTick = nextTick + waitTime;
        else
            pause(nextTick-t);
        end
	end
  end
end
