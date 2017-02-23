function label = get_label(tokens,U,no,dimen) 
%%no indicates which dimension
%dimens indicates how many keywords to display
labels = strings(1,dimen);
test = U(:,no);
[weight index] = sort(test,'descend');
for i = 1:1:dimen
     labels(i) = strcat(num2str(weight(i)),tokens(index(i)));
end
label = strcat(labels);
end