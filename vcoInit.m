% TODO
%   Make a function that captures the essence of VCO in an object
%   Make VCO do the necessary integration
%   Make VCO take in a waveform to convolve with the deltas
%   Make the multiple cells per direction

%%%


function obj = vcoInit(preferredVector, initialTime, baseFreq)
%vco creates the state object for use with vcoUpdate
    obj.d = preferredVector;
    obj.baseFreq = baseFreq;
    obj.currentTime = initialTime;
    
    % omega is the instantaneous frequency of the VCO
    obj.omega = 0;
    
    % theta is the instantaneous phase of the VCO
    obj.theta = 0;
    
    
    obj.output = 0;
end

