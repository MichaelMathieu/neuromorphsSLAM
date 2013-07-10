function drawLine(x1, y1, x2, y2, color)
	 if nargin < 5
	    color = 'black';
	 end
	 line([x1 x2], [y1 y2], 'Color', color)
end
