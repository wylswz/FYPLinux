function textInTopic(k,num,IDX)
numLimit = histc(IDX,k);
if num >= numLimit
   num = numLimit;
end  %%if that topic do not have so many aricles, just retuen all of the topics it has
 


end