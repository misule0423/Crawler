#!/bin/sh

FILE=$1
DATA_DIR=$2 # "/home/ddmi/data/crawler/bobaedream.co.kr/"
IS_IMPORT_DOMESTIC=$3
IS_VALIDATION=$4

# ./pre_crawl_bobaedream.co.kr.py ${DATA_DIR}
echo "File $FILE, Data_dir ${DATA_DIR}"
while read -r LINE; do
    echo "Processing $LINE"   
	python crawl_bobaedream.co.kr.py -q "$LINE" -o ${DATA_DIR} -d ${IS_IMPORT_DOMESTIC} -v ${IS_VALIDATION}
done < "$FILE"
