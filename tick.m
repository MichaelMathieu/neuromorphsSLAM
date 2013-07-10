function tick(cb, fps)
	 waitTime = 1./(fps*24*3600);
	 nextTick = now + waitTime;
	 global stopTick = 0
	 cb()
	 while !stopTick
	       t = now;
	       if t >= nextTick
		 cb()
		 nextTick += waitTime;
	       else
		   pause(nextTick-t)
	       end
	 end
end
