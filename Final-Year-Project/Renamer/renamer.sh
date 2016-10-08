#!/bin/bash
#this program can be used to formulate the file names, so that they can be processed easily
PATH=/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games
#<<<<<<< 1441d55ef0d8b5e242e34427404d9d5041159095
rm -rf temp
mkdir temp
i=0
ls *.txt|while read var1;do
i=`expr $i + 1`
cp "${var1}" temp/"${i}"
done


=======

test -e temp || mkdir temp

var1=`ls *.txt`
i=0
tempCounter=0  ##this indicates how many files are already in the temp folder
cd temp  ##enter temp
lsTemp=`ls`
for element in $lsTemp
do
tempCounter=`expr $tempCounter + 1`
done
cd ..  ##exit temp after counting the number of files


for element in $var1
do
  i=`expr $i + 1`
  echo "$i $element \n"
  cp `echo $element` temp/`expr $i + $tempCounter`
done
                  ##end of first part: rename all the txt files with number.

#>>>>>>> asd
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
#<<<<<<< 1441d55ef0d8b5e242e34427404d9d5041159095
rm -rf text
cp -r Renamer/temp text
=======
cp -r Renamer/temp temp
#>>>>>>> asd
exit 0
