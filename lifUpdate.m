function [obj, V] = lifUpdate(obj, I, dt)
	 % /!\ dt is in seconds
	 if obj.ref <= 0
	    obj.V = obj.V + dt*1000*( - (obj.V/(obj.R*obj.C)) + (I/obj.C));
	 else
	     obj.ref = obj.ref - dt;
	     obj.V = obj.V_reset;
	 end
	 if obj.V > obj.V_th
	    obj.V = obj.V_spike;
	    obj.ref = obj.abs_ref;
	 end
	 V = obj.V;
end
