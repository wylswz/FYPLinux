function newTextPlot(v,numOfNew,d1,d2,d3)
for i = 1:1:numOfNew
    text(v(i,d1),v(i,d2),v(i,d3),num2str(i))
end
end