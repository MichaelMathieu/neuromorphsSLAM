function [obj, out] = fakeVCOUpdate(obj, v, dt, maxvelocity)  
  obj.phase = obj.phase + 0.2*(dt * obj.Omega + dot(v, obj.d)/maxvelocity);
  out = sin(obj.phase + obj.K);
end
