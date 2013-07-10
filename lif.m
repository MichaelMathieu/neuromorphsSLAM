function obj = lif(C, R, abs_ref, V_th)
	 obj.C = C;             % capacitance (nF)
	 obj.R = R;             % leak resistance (M omhs)
	 obj.abs_ref = abs_ref; % absolure refractory period (seconds)
	 obj.V_th = V_th;       % spike threshold (V)
	 obj.ref = 0;           % absolute refractory period counter
	 obj.V = 0;
	 obj.V_reset = 0.2 * obj.V_th;
	 obj.V_spike = 50;
end
