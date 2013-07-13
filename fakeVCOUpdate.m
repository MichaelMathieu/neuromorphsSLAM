function [obj, out] = fakeVCOUpdate(obj, v, dt)
  dx = dt * norm(obj.d) * obj.Omega + obj.alpha*dot(v, obj.d);
  obj.phase = obj.phase + dx;
  %out = sin(obj.phase + obj.K);
  out = H(obj.phase + obj.K, dx/dt);
end

function y = H(x, dx)
  d = 0.01*dx;
  t = mod(x,2*pi);
  y = (t+d >= pi/2) .* (t-d <= pi/2);
end
