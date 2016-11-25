function label = get_label(tokens,U,no,dimen)
label = strings(dimen,1)
test = U(:,no);
[weight index] = sort(test,'descend');
for i = 1:1:dimen
     label(i) = strcat(num2str(weight(i)),tokens(index(i)));
end
end