function newTextPlot(v,start,numOfNew,d1,d2,d3)
for i = start:1:numOfNew+start-1
    text(v(i,d1),v(i,d2),v(i,d3),num2str(i))
end
end