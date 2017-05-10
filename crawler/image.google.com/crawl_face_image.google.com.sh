#!/bin/sh
FILE=$1   # ~/data/crawler/queries.txt
mkdir -p /home/ddmi/data/crawler/face_image.google.com/
while read -r LINE; do
    echo "Processing $LINE"
    python crawl_face_image.google.com.py -q $LINE -o /home/ddmi/data/crawler/face_image.google.com/$LINE
done < "$FILE"
