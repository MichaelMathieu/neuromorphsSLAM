vcoObj = vcoInit(4, 1, 0);

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

% VCOs 
Vco = [];
for i=1 : length(t)        
    [vcoObj, output] = vcoUpdate(vcoObj, dt, v(:,i));
    Vco = [Vco output];
end

% Plots
figure(); 
subplot(5,1,1), plot(t, pos), title('Position');
subplot(5,1,2), plot(t, v), title('Velocity');
subplot(5,1,3), plot(t, Vco), title('VCO phase');

