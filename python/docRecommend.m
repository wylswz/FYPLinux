function recoList = docRecommend(newDoc,C,IDX)
sizeC = size(C);
dimen = sizeC(2);
recoList = [];
recNum = [6 2 1 1]; %% return 10 articles
nearK = knnsearch(C(:,1:dimen),newDoc(1:dimen),'K',4);
for i=1:1:4
    index = nearK(i);
    txtidx = textInTopic(index,recNum(i),IDX);
    recoList = [recoList ;txtidx];
end
end