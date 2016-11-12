function [docSet] = clusterGenerate(idx,V,dimen)
num = size(idx);
docSet = cell(num(1),1);
for i = 1:1:num
    docSet{i} = docPoint(V(i,1:dimen),idx(i));
end