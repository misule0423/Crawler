#!/bin/bash

# Collection of codes to postprocess images collected.
# Author: hsong

# Combine different versions of car models into one.
/bin/ls -d */ > dirs_orig.txt
awk -F'+' '{out="";for(i=1;i<NF;i++){out=out$i;if(i!=NF-1){out=out"+";}}print out }' dirs_orig.txt | sort -u > dirs_ref.txt
awk -F'+' '{out="";for(i=1;i<NF;i++){out=out$i;if(i!=NF-1){out=out"+";}}print "if [ ! -d \""out"\" ];then mkdir "out";fi; mv -f "$0"*.jp*g "out }' dirs_orig.txt > run_mv.sh
awk -F'+' '{out="";for(i=1;i<NF;i++){out=out$i;if(i!=NF-1){out=out"+";}}print "if [ ! -d \""out"\" ];then mkdir "out";fi; mv -f "$0"*.Jp*g "out }' dirs_orig.txt >> run_mv.sh
awk -F'+' '{out="";for(i=1;i<NF;i++){out=out$i;if(i!=NF-1){out=out"+";}}print "if [ ! -d \""out"\" ];then mkdir "out";fi; mv -f "$0"*.JP*G "out }' dirs_orig.txt >> run_mv.sh
chmod 755 run_mv.sh
./run_mv.sh


for f in `cat dirs_ref.txt`:
do 
    mv $f "/media/ddmi/New Volume/imagenet/data/ILSVRC2012_img_train/"
done

# Move the consolidated dirs into where ILSVRC2012_img_train is (/media/ddmi/New Volume/imagenet/ILSVRC2012_img_train/addition_cars)
...

# Create the same directories to store resized/uncorrupted copies (/media/ddmi/New Volume/imagenet/ILSVRC2012_img_train/addition_cars2)
...

# Resize files and store addition_cars2 dir
cd "/media/ddmi/New Volume/imagenet/data/ILSVRC2012_img_train"
cd addition_cars
find . -name "*.jp*g" > ../jpg_list.txt
find . -name "*.Jp*g" >> ../jpg_list.txt
find . -name "*.JP*G" >> ../jpg_list.txt
cd .. && sort jpg_list.txt > jpg_list.srt && rm -f jpg_list.txt

for f in `cat jpg_list.srt`:
do
    convert -resize 256x256\! addition_cars/$f addition_cars2/$f
done
 

for f in `cat jpg_list.srt`; do convert -resize 256x256\! addition_cars/$f addition_cars2/$f; done
 
