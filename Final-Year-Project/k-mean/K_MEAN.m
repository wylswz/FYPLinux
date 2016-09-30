function [K_OUT] = K_MEAN(K,P_COORSET,EPOCH)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here
K_DIST = zeros(K,1);   %the distance from k clusters and one single point
P_SIZE = size(P_COORSET);
P_NUM = P_SIZE(1);
P_DIM = P_SIZE(2);
pSet = cell(1,P_NUM);
kSet = unifrnd(-1,1,[K 2]);   %generate random k points as cluster heads
value = 0;
index = 0;
classCounter = zeros(1,K);
classCounterX = zeros(1,K);
classCounterY = zeros(1,K);
classifier = cell(K,K);
colors = {'y' 'm' 'c' 'r' 'g' 'b' 'w' 'k'}


for z = 1:1:EPOCH
  for i = 1:1:P_NUM
      pSet{i} = DOC_POINT(P_COORSET(i,:),0);
      for j = 1:1:K
          K_DIST(j) = norm(P_COORSET(i,:) - kSet(j,:));
      end
      [value index] = min(K_DIST);
      pSet{i}.class = index;
      classCounterX(index) = classCounterX(index) + pSet{i}.coord(1);
      classCounterY(index) = classCounterY(index) + pSet{i}.coord(2);
      classCounter(index) = classCounter(index) + 1;
      scatter(pSet{i}.coord(1),pSet{i}.coord(2),'x');
      hold on;
  end
  for j = 1:1:K
      kSet(j,1) = classCounterX(j)/classCounter(j);
      kSet(j,2) = classCounterY(j)/classCounter(j);
      scatter(kSet(j,1),kSet(j,2),'o');
     % hold on;
      drawnow;
  end   % for each loop, update the coordinate of the K clusters.
 K_OUT = kSet;
end
      for i = 1:1:P_NUM
          scatter(P_COORSET(i,1),P_COORSET(i,2),strcat(colors{pSet{i}.class},'x'));
      end
end

