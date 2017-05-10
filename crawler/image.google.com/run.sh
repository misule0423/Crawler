#!/bin/sh

DATA="/home/ddmi/data/crawler/image.google.com/"

./crawl_image.google.com.sh ${DATA}/queries_bag.txt

echo "# FILENAME|#IMAGES_ATTEMPTED_TO_CRAWL|#IMAGES_CRAWLED\n" > ${DATA}/image_collection_report.txt
for f in ${DATA}/*/images.url;do awk -F'|' 'BEGIN{i=0;j=0}{if($2> 10000){j++}i++}END{print FILENAME"|"i"|"j}' $f;done >> ${DATA}/image_collection_report.txt
