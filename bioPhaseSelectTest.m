
% Time
dt = 0.001;
t = dt:dt:2;

% Rat Motion
pos = [sin(t) + 2*t; zeros(1,length(t))];
%pos = [zeros(1,length(t)); zeros(1,length(t))];
v = zeros(2,length(t));

for i = 1 : length(t)
    if i > 1
        v(:,i) = [pos(1,i) - pos(1,i-1); pos(2,i) - pos(2,i-1); ];
    else
        v(:,1) = [3*dt;0];
    end
end


% VCO
vcoObjs = vcoInit([1;0], 0, 8);
        
Vco = [];
for i=1 : length(t)
    Output = [];
    for j = 1 : length(vcoObjs)
        
        [vcoObjs(j), output] = vcoUpdate(vcoObjs(j), dt, v(:,i));
        Output = [Output ; output ];
    end
    Vco = [Vco Output];
end

% Create a bunch of lif cells with different parameters and see if the
% respond selectively to different phase offsets from the same VCO driven
% input
ncells = 1;
pcells = [];
pcells2 = [];
pcell2_w = 0.05;
for i = 1 : ncells
    abs_ref = .001 + 0.01 * rand;
    R = 30 + 20 * rand;
    C = 1;
    pcells = [pcells lif(C, R, abs_ref, 10) ]; 
    pcells2 = [pcells2 lif(1, 40, .5, 10) ]; 
end


% Process the first layer of PCells updates
I_offset = 1;
I_scale = 0.7;
pcell_I = zeros(1, length(t));
pcell_V = zeros(length(pcells), length(t));
for i = 1 : length(t)
    for j = 1 : length(vcoObjs)
        for k = 1 : length(pcells)
        	pcell_i = Vco(j,i) + I_offset;
            pcell_I(i) =  pcell_i;
            [pcells(k), pcell_v] = lifUpdate(pcells(k), pcell_i, dt);
            pcell_V(k,i) =  pcell_v;
        end
    end
end

% Desired output
desired_spike = zeros(length(pcells),length(t));
for i = 1 : length(t)
    for j = 1 : length(vcoObjs)
        for k = 1 : length(pcells)
            if i ==  (k * length(t) / length(pcells))
                desired_spike(k,i) = 1;
            else
                desired_spike(k,i) = 0;
            end
        end
    end
end


% Desired output
input_spike = zeros(length(pcells),length(t));
for i = 1 : length(t)
    for j = 1 : length(vcoObjs)
        for k = 1 : length(pcells)
            if pcell_V(k,i) > 10
                input_spike(k,i) = 1;
            else
                input_spike(k,i) = 0;
            end
        end
    end
end

L1L2_weights = 0.015*rand(length(pcells), length(pcells2));

% Process the second layer of PCells updates
pcell2_I = zeros(1, length(t));
pcell2_V = zeros(length(pcells), length(t));
for i = 1 : length(t)
    for j = 1 : length(vcoObjs)
        for k_l2 = 1 : length(pcells2)
            pcell2_i = 0;
            for k_l1 = 1 : length(pcells)
                pcell2_i = pcell2_i + max(0, L1L2_weights(k_l1,k_l2) * pcell_V(k_l1,i));
            end
            pcell2_I(i) =  pcell_i;
            [pcells2(k_l2), pcell2_v] = lifUpdate(pcells2(k_l2), pcell2_i, dt);
            pcell2_V(k_l2,i) =  pcell2_v;
        end

    end
end

% Compute desired spikes


% Plots
figure();
subplot(4,1,1), plot(t, pcell_I), title('Input Current');
subplot(4,1,2), plot(t, pcell_V), title('Layer 1 random param LIF cells V trace');
subplot(4,1,3), plot(t, pcell2_V), title('Layer 2 fully connected projection with random weight');
subplot(4,1,4), plot(t, desired_spike), title('Desired Output');
%subplot(5,1,5), plot(t, input_spike), title('Input Spikes');
