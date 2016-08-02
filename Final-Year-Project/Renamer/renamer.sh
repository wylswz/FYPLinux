#!/bin/bash
#this program can be used to formulate the file names, so that they can be processed easily
PATH = /bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
rm -rf temp
mkdir temp
i=0
ls *.txt|while read var1;do
i=`expr $i + 1`
cp "${var1}" temp/"${i}"
done


cd temp
var2=`ls`
iterTemp=0
for element1 in $var2
do
  iterTemp=`expr $iterTemp + 1`
  #echo "123 " >> `echo $element1` 
  sed -i 's/ /\n/g' `echo $element1`
done
                  ##end of second part: split the atricles so that each word will occupy a single line
cd ..
cd ..
rm -rf text
cp -r Renamer/temp text
exit 0
