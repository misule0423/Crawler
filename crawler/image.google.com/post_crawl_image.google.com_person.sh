#!/bin/bash

# Collection of codes to postprocess images collected.
# Author: hsong

# Create the same directories to store resized/uncorrupted copies (/media/ddmi/data/images/resized_images/image.google.com/person/*)
...

# Resize files and store into person2 dir
cd "/media/ddmi/data/images/resized_images/image.google.com/person/"
find . -name "*.jp*g" > jpg_list.txt
find . -name "*.Jp*g" >> jpg_list.txt
find . -name "*.JP*G" >> jpg_list.txt

for f in `cat jpg_list.txt`:
do
    convert -resize 256x256\! $f ../person2/$f
done
 
