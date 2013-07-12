function drawLine(x1, y1, x2, y2, fig, color)
	 if nargin < 5
	    fig = 1
	 end
	 if nargin < 6
	    color = 'black';
	 end
	 global drawQueue;
	 drawQueue = [drawQueue; [x1 y1 x2 y2 fig] ];
	 %line([x1 x2], [y1 y2], 'Color', color)
end
