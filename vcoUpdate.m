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


    % determine current frequency of the VCO
    obj.omega = obj.baseFreq + dot(obj.d, V);

    % integrate omega to determine phase of the VCO
    obj.theta = (obj.theta + dt * obj.omega);

    % dynamics by sin of phase
    obj.output = sin(obj.theta);
    
    output = obj.output;
    
end
