#!/bin/sh

FILE=$1
DATA_DIR=$2 # "/home/ddmi/data/crawler/encar.co.kr/"

echo "File $FILE, Data_dir ${DATA_DIR}"
while read -r LINE; do
    echo "Processing $LINE"   
	python crawl_encar.co.kr.py -q "$LINE" -o ${DATA_DIR}
done < "$FILE"
