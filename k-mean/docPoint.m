classdef docPoint
   properties
       coord;
       cluster;
       id;
   end
   methods
       function docPoint = docPoint(id,coord,cluster)
                docPoint.id = id;
                docPoint.coord = coord;
                docPoint.cluster = cluster;
       end
       
       function idOut = getID(coord)
                
       end
   end
    
    
end