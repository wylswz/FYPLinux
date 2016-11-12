 %T is new term-doc matrix, H is entropy matrix, U and S are matrics
%obtained by singular value decomposition
function [V_NEW] = Embed1(T, H, U, S)
size_of_t = size(T);
rows = size_of_t(1);
cols = size_of_t(2);
sum_of_colT = sum(T,1); %%total terms in one document
W_NEW = zeros(rows,cols);
US = U*S;

for i = 1:1:rows
    b = zeros(1,cols);
    for j = 1:1:cols
    b(1,j) = (1-H(i))*T(i,j)/sum_of_colT(j);       
    end
    W_NEW(i,:) = b;
end

V_NEW = transpose(W_NEW)*U*S^(-1);
end