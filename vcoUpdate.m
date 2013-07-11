function [obj, output] = vcoUpdate( obj, dt, V )
%vcoUpdate given velocity V and dt, compute theta
%
%   theta represents the current(instantaneous) phase of 
%   each of the the velocity controlled oscillator cells.
%
%   theta is computed by integrating omega, which represents
%   the instantaneous frequency of the vco cells, which vary
%   in time with respect to the current agent velocity V given as
%   an input.
% 

    for i = 1 : length(obj.d)
        % determine current frequency of the VCO
        obj.omega(i) = obj.inputFrequency + dot(obj.d(:,i), V);
        
      
        % integrate omega to determine phase of the VCO
        obj.theta(i) = (obj.theta(i) + dt * obj.omega(i));
        
        % dynamics by sin of phase
        obj.output(i) = sin(obj.theta(i));
    end
    output = obj.output;
    
    
    % TODO add a ring of cells per d vector
    
end
