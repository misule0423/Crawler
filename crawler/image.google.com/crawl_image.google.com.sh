#!/bin/sh
FILE=$1   # ~/data/crawler/queries.txt
mkdir -p /home/ddmi/data/crawler/image.google.com/
while read -r LINE; do
    echo "Processing $LINE"
    python crawl_image.google.com.py -q $LINE -o /home/ddmi/data/crawler/image.google.com/$LINE
done < "$FILE"
