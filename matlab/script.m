
scatter3(V([1:3 16:17 31:33],2),V([1:3 16:17 31:33],3),V([1:3 16:17 31:33],4))
hold on
scatter3(V([4:6 18:20 34:36],2),V([4:6 18:20 34:36],3),V([4:6 18:20 34:36],4))
hold on
scatter3(V([7:9 21:24 37:39],2),V([7:9 21:24 37:39],3),V([7:9 21:24 37:39],4))
hold on
scatter3(V([10:12 25:27 40:42],2),V([10:12 25:27 40:42],3),V([10:12 25:27 40:42],4))
hold on
scatter3(V([13:15 28:30 43:45],2),V([13:15 28:30 43:45],3),V([13:15 28:30 43:45],4))


legend('Computer','Battle','Music','Religion','Electronic')
xlabel('x')
ylabel('y')
zlabel('z')
text(V_NEW(1,2),V_NEW(1,3),V_NEW(1,4),'history');
text(V_NEW(2,2),V_NEW(2,3),V_NEW(2,4),'electronic');
text(V_NEW(3,2),V_NEW(3,3),V_NEW(3,4),'music');
text(V_NEW(4,2),V_NEW(4,3),V_NEW(4,4),'religion');
text(V_NEW(5,2),V_NEW(5,3),V_NEW(5,4),'computer');


%{
newTextPlot(V,44,1,2,3,4)
newTextPlot(V,58,1,2,3,4)
newTextPlot(V,96,1,2,3,4)
newTextPlot(V,190,1,2,3,4)
newTextPlot(V,200,1,2,3,4)
newTextPlot(V,235,1,2,3,4)
newTextPlot(V,344,1,2,3,4)
newTextPlot(V,402,1,2,3,4)
newTextPlot(V,417,1,2,3,4)
newTextPlot(V,434,1,2,3,4)
newTextPlot(V,463,1,2,3,4)
newTextPlot(V,746,1,2,3,4)

%}