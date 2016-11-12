classdef docPoint
   properties
       coord;
       cluster;
   end
   methods
       function docPoint = docPoint(coord,cluster)
                docPoint.coord = coord;
                docPoint.cluster = cluster;
       end
   end
    
    
end