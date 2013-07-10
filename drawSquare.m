function drawSquare(x1, y1, x2, y2, color)
	 if nargin < 5
	    color = 'b';
	 end
	 if (x1 < x2) & (y1 < y2)
	   drawLine(x1, y1, x2, y1, color);
	   drawLine(x2, y1, x2, y2, color);
	   drawLine(x2, y2, x1, y2, color);
	   drawLine(x1, y2, x1, y1, color);
	 end
end
