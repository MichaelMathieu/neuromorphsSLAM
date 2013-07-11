function tick(cb, fps)
    waitTime = 1./(fps*24*3600);
	global stopTick;
    stopTick = 0;
	lastTick = now;
	nextTick = lastTick + waitTime;
	cb(0);
	while  stopTick == 0
        t = now;
        if t >= nextTick
            cb((t-lastTick)*24*3600);
            lastTick = t;
            nextTick = nextTick + waitTime;
        else
            pause(nextTick-t);
        end
	end
end
