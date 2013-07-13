function obj = fakeVCOInit(d, n)
% Creates the object for fake vco. d is the vco direction, n is the number of outputs
  obj.d = d;
  obj.phase = 0;
  obj.alpha = 2*pi;
  obj.Omega = 8;
  obj.K = [];
  for i = 0:(n-1)
    obj.K(i+1) = 2*pi*i/n;
  end
end
