
% Time
dt = 0.001;
t = 0:dt:1;

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
ncells = 10;
pcells = [];
pcells2 = [];
pcell2_w = 0.05;
for i = 1 : ncells
    pcells = [pcells lif(1, 40 * rand, .5 * rand, 10 * rand) ];
    pcells2 = [pcells2 lif(1, 40, .005, 10) ];
end


% Process the first layer of PCells updates
pcell_I = zeros(1, length(t));
pcell_V = zeros(length(pcells), length(t));
for i = 1 : length(t)
    for j = 1 : length(vcoObjs)
        for k = 1 : length(pcells)
        	pcell_i = max(0,Vco(j,i));
            pcell_I(i) =  pcell_i;
            [pcells(k), pcell_v] = lifUpdate(pcells(k), pcell_i, dt);
            pcell_V(k,i) =  pcell_v;


        end

    end
end




% Plots
figure();
subplot(3,1,1), plot(t, pcell_I), title('Input Current');
subplot(3,1,2), plot(t, pcell_V), title('Layer 1 random param LIF cells V trace');
subplot(3,1,3), plot(t, pcell2_V), title('Layer 2 1:1 projection with low weight');

