#!bin/bash
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
#count the number of documents
i=0 ##docs
j=0 ##words
rm texts/*.config
totalName=`ls`
totalWord=`cat key.txt`
for name in $totalName
do
  i=`expr $i + 1`
done

i=`expr $i - 4`
touch fconfig.config
echo $i >> fconfig.config ##number of documents

for word in $totalWord
do
  j=`expr $j + 1`
  
done
echo $j >> fconfig.config ##write number of keywords

exit

