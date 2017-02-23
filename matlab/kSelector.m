% K selector, which is used to find a suitable value for k


function [  ] = kSelector(V,dimen,iter)

%IDX: which cluster
%C cluster location
%SUMD total distance
%D distance
var = zeros(3,iter); %% min, mean, max
for k = 1:1:iter %iter k from 1 to 30
    [IDX C SUMD D] = kmeans(V(:,1:dimen),k);
    vard = zeros(k,1); %%we have k variances for k clusters
    mean = zeros(k,1);
    for i = 1:1:k
        vard(i) = sum(D(find(ismember(IDX,i))).^2);
    end
    var(1,k) = min(vard);
    var(2,k) = sum(vard)/k;
    var(3,k) = max(vard);  
end
%plot(var(1,:))
%hold on
plot(var(2,:))
hold on
%plot(var(3,:))
%hold on

end

