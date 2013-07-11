function obj, out = fakeVCOUpdate(obj, v, dt, maxvelocity)
  obj.phase += 0.2*(dt * obj.Omega + dot(v, obj.d)/maxvelocity);
  out = sin(obj.phase + obj.K);
  ph = obj.phase
  dotp = dot(v, obj.d)/maxvelocity
  omeg = dt*obj.Omega
end
