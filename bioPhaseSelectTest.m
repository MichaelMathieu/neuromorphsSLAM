

% Time
dt = 0.1;
t = 0:dt:10;

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

% Phase selective cell
% pcell = lif(1, 1, 5*dt, 10);
% pcell_I = [];
% pcell_V = [];
% for i = 1 : length(t)
%     for j = 1 : length(vcoObjs)
%         pcell_i = max(0, Vco(j,i))
%         pcell_I = [pcell_I  pcell_i];
%         [pcell, pcell_v] = lifUpdate(pcell, pcell_i, dt);
%         pcell_V = [pcell_V pcell_v];
%     end
% end
pcell = lif(1, 1, 5*dt, 10);
pcell_I = [];
pcell_V = [];
for i = 1 : length(t)
    for j = 1 : length(vcoObjs)
        pcell_i = 1
        pcell_I = [pcell_I  pcell_i];
        [pcell, pcell_v] = lifUpdate(pcell, pcell_i, dt);
        pcell_V = [pcell_V pcell_v];
    end
end


% Plots
figure();
subplot(5,1,1), plot(t, pos), title('Position');
subplot(5,1,2), plot(t, v), title('Velocity');
subplot(5,1,3), plot(t, Vco), title('VCO phase');
subplot(5,1,4), plot(t, pcell_I), title('LIF cell I');
subplot(5,1,5), plot(t, pcell_V), title('LIF cell response to phase modulated I');

