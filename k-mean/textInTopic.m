%return some documents in a certain cluster
function [txtidx] = textInTopic(k,num,IDX)
numLimit = histc(IDX,k);
if num >= numLimit
   num = numLimit;
end  %%if that topic do not have so many aricles, just retuen all of the topics it has
base = find(ismember(IDX,k)); %the base to choose from
index = randperm(numLimit,num);
txtidx = base(index)

end