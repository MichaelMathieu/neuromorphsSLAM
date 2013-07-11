

% Time
dt = 0.1;
t = 0:dt:10;

% LIF Cell 
lifCell = lif(1, 5, 5*dt, 10);
lifCell_I = [];
lifCell_V = [];
for i = 1 : length(t)
    for j = 1 : length(vcoObjs)
        lifCell_i = 1
        lifCell_I = [lifCell_I  lifCell_i];
        [lifCell, lifCell_v] = lifUpdate(lifCell, lifCell_i, dt);
        lifCell_V = [lifCell_V lifCell_v];
    end
end


% Plots
figure();
subplot(2,1,1), plot(t, lifCell_I), title('LIF cell I');
subplot(2,1,2), plot(t, lifCell_V), title('LIF cell response to phase modulated I');

