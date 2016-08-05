#!bin/bash
PATH = /bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
#count the number of documents
i=0
rm *.config
totalName=`ls`
for name in $totalName
do
  i=`expr $i + 1`
done

i=`expr $i - 2`
touch fconfig.config
echo $i >> fconfig.config
exit

