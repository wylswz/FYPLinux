 %T is new term-doc matrix, H is entropy matrix, U and S are matrics
%obtained by singular value decomposition
function [V_NEW] = Embed(T, H, U, S)
size_of_t = size(T);
rows = size_of_t(1);
cols = size_of_t(2);
sum_of_colT = sum(T,1); %%total terms in one document
W_NEW = zeros(rows,cols);
US = U*S;
M = pinv(US);
for i = 1:1:rows
    for j = 1:1:cols
    W_NEW(i,j) = (1-H(i))*T(i,j)/sum_of_colT(j);       
    end
end

V_NEW = M*W_NEW;
end