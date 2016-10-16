%This program is used to naomalize term-doc matrix
%The terms with high frequency is not necessarily important
%for each number in the matrix, add 0.001 to make sure there's 
%no row of zero
function W = Normalize(T)
parpool('local',2)
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
            H(i,1) = H(i,1) - a(1,J)*log(a(1,J))*atan((sum_of_rowT(i)-5)/2 + 1.7);
        %entropy of a word
        end
    end
end

    
parfor i = 1:1:rows
    b = zeros(1,cols);
    for j = 1:1:cols
        b(1,j) = sqrt((1-H(i,1)).*T(i,j))./sum_of_colT(j);
    end
    W(i,:) = b
end
p = gcp;
delete(p);
end
