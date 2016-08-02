classdef DOC_POINT
    %UNTITLED2 Summary of this class goes here
    %   Detailed explanation goes here
    
    properties
        coord = zeros(1,2);
        class = 0;
    end
    
    methods
        function a = DOC_POINT(coord,class)
            a.class = class;
            a.coord = coord; 
        end
    end
    
end

