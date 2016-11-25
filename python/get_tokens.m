function tokens = get_tokens(dir,num)
tokens = strings(num,1);
f = fopen(dir,'r');
for i = 1:1:num
    tokens(i) = fscanf(f,'%s',1);
end
fclose(f);


end