%This program is used to naomalize term-doc matrix
%The terms with high frequency is not necessarily important
%for each number in the matrix, add 0.001 to make sure there's 
%no row of zero
function [W H] = Normalize(T)
size_of_t = size(T);
rows = size_of_t(1);
cols = size_of_t(2);
sum_of_rowT = sum(T,2);
sum_of_colT = sum(T,1);
W = zeros(rows,cols);
P = zeros(rows,cols);
H = zeros(rows,1);
parfor i = 1:1:rows  %%parallel conputing to accelerate
    a = P(i,:);
    for j = 1:1:cols
        J = j
        a(1,J) = T(i,J)/sum_of_rowT(i); %term occurance probability
        if a(1,J) == 0
            H(i,1) = H(i,1) + 0;
        else
            H(i,1) = H(i,1) - 1/log(rows)*a(1,J)*log(a(1,J));
        %entropy of a word
        end
    end
end
 
parfor i = 1:1:rows
    b = zeros(1,cols);
    for j = 1:1:cols
        b(1,j) = (1-H(i,1)).*T(i,j)./sum_of_colT(j);%*1/(1+exp((sum_of_rowT(i)-1)));
    end
    W(i,:) = b
end
%p = gcp;
%delete(p);
end
