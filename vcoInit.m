% TODO
%   Make a function that captures the essence of VCO in an object
%   Make VCO do the necessary integration
%   Make VCO take in a waveform to convolve with the deltas
%   Make the multiple cells per direction

%%%


function obj = vcoInit(numVectors, vcoCellsPerVector, initialTime)
%vco creates the state object for use with vcoUpdate
    obj.numVectors = numVectors;
    obj.vcoCellsPerVector = vcoCellsPerVector;
    obj.inputFrequency = 8;
    obj.currentTime = initialTime;
    
    %%% TODO: create d based on the params above
    % d represents the preferred velocity vectors for the VCOs
    obj.d = [[1;0], [0;1], [-1;0], [0;-1]];
    
    
    % omega is the instantaneous frequency of the VCOs
    obj.omega = zeros(length(obj.d),1);
    
    % theta is the instantaneous phase of the VCOs
    obj.theta = zeros(length(obj.d),1);
    
    
    obj.output = zeros(length(obj.d),1);
    
    
end

