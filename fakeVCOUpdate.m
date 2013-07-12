function [obj, out] = fakeVCOUpdate(obj, v, dt)
  A = 0.5;
  Omega = 15;
  vmax = 0.01;
  dx = A*(dt * norm(obj.d) * Omega + dot(v, obj.d)/vmax);
  obj.phase = obj.phase + dx;
  %out = sin(obj.phase + obj.K);
  out = H(obj.phase + obj.K, dx/dt);
end

function y = H(x, dx)
  d = 0.01*dx;
  t = mod(x,2*pi);
  y = (t+d >= pi/2) .* (t-d <= pi/2);
end
