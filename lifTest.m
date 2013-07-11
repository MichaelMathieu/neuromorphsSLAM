

% Time
dt = 0.001;
t = 0:dt:1;

% LIF Cell 
lifCell = lif(1, 40, 0.05, 10);
lifCell_I = [];
lifCell_V = [];
for i = 1 : length(t)

    lifCell_i = max(0,sin(i/60) );
    lifCell_I = [lifCell_I  lifCell_i];
    [lifCell, lifCell_v] = lifUpdate(lifCell, lifCell_i, dt);
    lifCell_V = [lifCell_V lifCell_v];

end


% Plots
figure();
subplot(2,1,1), plot(t, lifCell_I), title('LIF cell I');
subplot(2,1,2), plot(t, lifCell_V), title('LIF cell response to phase modulated I');

