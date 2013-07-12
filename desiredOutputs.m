
vcoBaseFreq = 8;

% Time
dt = 0.001;
t = dt:dt:2 * (2*pi/vcoBaseFreq);


% VCO
d = [1;0];
vcoObjs = [vcoInit(d, 0, vcoBaseFreq);
           vcoInit(d, 1, vcoBaseFreq);]
        
Vco = [];
for i=1 : length(t)
    Output = [];
    for j = 1 : length(vcoObjs)
        
        [vcoObjs(j), output] = vcoUpdate(vcoObjs(j), dt, d);
        Output = [Output ; output ];

    end
    Vco = [Vco Output];
end

% Create a bunch of lif cells with different parameters and see if the
% respond selectively to different phase offsets from the same VCO driven
% input
ncells = 2;
pcells = [];
for i = 1 : ncells
    abs_ref = .005;
    R = 20;
    C = 1;
    pcells = [pcells lif(C, R, abs_ref, 10) ]; 
end

% Desired output
I_offset = 1;
I_scale = 0.7;
pcell_I = zeros(1, length(t));
pcell_V = zeros(length(pcells), length(t));
for i = 1 : length(t)
    for j = 1 : length(vcoObjs)
        for k = 1 : length(pcells)
        	pcell_i = I_scale * Vco(j,i) + I_offset;
            pcell_I(i) =  pcell_i;
            [pcells(k), pcell_v] = lifUpdate(pcells(k), pcell_i, dt);
            pcell_V(k,i) =  pcell_v;
        end
    end
end




% Plots
figure();
subplot(2,1,1), plot(t, pcell_I), title('Input Current');
subplot(2,1,2), plot(t, pcell_V), title('Desired Outputs from LIF cells');



