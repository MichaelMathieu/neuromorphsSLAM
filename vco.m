% Time
dt = 0.1;
t = 0:dt:10;

% Rat Motion
pos = [sin(t) + 2*t; cos(t)];
v = zeros(2,length(t));

for i = 1 : length(t)
    if i > 1
        v(:,i) = [pos(1,i) - pos(1,i-1); pos(2,i) - pos(2,i-1); ];
    else
        v(:,1) = [3*dt;0];
        
    end
end

% VCOs 
d = [[1;0], [0;1], [-1;0], [0;-1]];
w = zeros(length(d), length(t));
for j = 1 : length(d)
    for i=1 : length(t)
        w(j,i) = dot(d(:,j), v(:,i)); 
    end
end

% Phase Selectivity
%place_count = 1;
%place_cells = zeros(1,place_count);
%syn = zeros(length(d), length(place_cells));
syn = [2;0;0;0];
place_I = zeros(1, length(t));
for i = 1 : length(syn)
    place_I = place_I + syn(i)* w(i,:);
end

place_V = lif(place_I);

% Plots
figure(); 
subplot(5,1,1), plot(t, pos), title('Position');
subplot(5,1,2), plot(t,v), title('Velocity');
subplot(5,1,3), plot(t,w), title('VCO phase responding to UP vector');
subplot(5,1,4), plot(t,place_I), title('Place cell current injection');
subplot(5,1,5), plot(t,place_V), title('Place cell voltage');

