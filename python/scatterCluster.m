function scatterCluster(V,IDX,K)  %%scatter the points in class K
txtidx = textInTopic(K,10000,IDX); %%find all the documents in K
scatter3(V(txtidx,2),V(txtidx,3),V(txtidx,4));
hold on
end