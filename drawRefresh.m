function drawRefresh()
  global drawQueue;
  lastfig = -1;
  for i = 1:size(drawQueue,1)
      todraw = drawQueue(i,:);
      if todraw(5) ~= lastfig
	 lastfig = todraw(5);
	 figure(todraw(5));
      end
      line([todraw(1), todraw(3)], [todraw(2), todraw(4)])
  end
end
