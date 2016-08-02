#!/bin/bash
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
rm -rf text
cd Renamer
sh renamer.sh
cd ..
##in root
cp text/* MatrixGenerator/text
cd MatrixGenerator/text
sh textCounter.sh
cd ..;cd ..
##in root
cd MatrixGenerator
g++ *.cpp -o exe
./exe
cd ..
exit

