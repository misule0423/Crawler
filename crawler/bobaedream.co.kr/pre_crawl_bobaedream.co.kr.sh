#!/bin/bash

#
# Crawler for bobaedream.co.kr
# Author: hsong
#

DATA_DIR="~/data/crawler/bobaedream.co.kr/"

# Crawl car makers and models
wget "http://www.bobaedream.co.kr/mycar/mycar_list_maker.php?gubun=K" -O ${DATA_DIR}/bobaedream.co.kr_carlist.html
wget "http://www.bobaedream.co.kr/mycar/mycar_list_maker.php?gubun=I" -O ${DATA_DIR}/bobaedream.co.kr_importcarlist.html   

# Extract the most popular cars
N_CARS=0
egrep "input id=" ${DATA_DIR}/bobaedream.co.kr_carlist.html | awk '{print $4,$7,$8,$9}' | awk -F'["()]' '{if($6>"${N_CARS}"){print $2,$4,$5,$6}}' |  sed 's/^chk_\(.*\)\[\] car_\(.*\) >\(.*\)<span> \(.*\)/\1|\2|\3/' > ${DATA_DIR}/bobaedream.co.kr_carlist.txt
egrep "input id=" ${DATA_DIR}/bobaedream.co.kr_importcarlist.html | awk '{print $5,$8,$9,$10}' | awk -F'["()]' '{if($6>"${N_CARS}"){print $2,$4,$5,$6}}' | sed 's/^chk_\(.*\)\[\] car_\(.*\) >\(.*\)<span> \(.*\)/\1|\2|\3|\4/' > ${DATA_DIR}bobaedream.co.kr_importcarlist.txt

# Handpick bobaedream.co.kr_carlist.txt and save as bobaedream.co.kr_carlist.ref
# 

# Build url for sold cars 
# TODO (hsong): do the same for import cars
for maker in `awk -F'|' '{print $1}' bobaedream.co.kr_carlist.ref | uniq`
do
    for model in `awk -F'|' '{print $2}' bobaedream.co.kr_carlist.ref | uniq`
    do
	echo "http://www.bobaedream.co.kr/mycar/mycar_list.php?refer_page=%2Fmycar%2Fmycar_list.php&gubun=K&tab=1&order=S11&view_size=50&maker_no=${maker}&sold=1&model_no\[\]=${model}" > bobaedream.co.kr_maker${maker}_model${model}.url
    done
done


for maker in `awk -F'|' '{print $1}' bobaedream.co.kr_carlist.ref | uniq`
do
    for model in `awk -F'|' '{print $2}' bobaedream.co.kr_carlist.ref | uniq`
    do
	rm -f bobaedream.co.kr_maker${maker}_model${model}_jpg.url
	for f in `cat bobaedream.co.kr_maker${maker}_model${model}.url`
	do
#	    curl "$f" -o bobaedream.co.kr_maker${maker}_model${model}.html
	    egrep ".jpg" bobaedream.co.kr_maker${maker}_model${model}.html | egrep "height=\'91\'" | awk '{print $5}' | sed 's/^src="\(.*\)"/\1/' >> bobaedream.co.kr_maker${maker}_model${model}_jpg.url
	    ./crawl.py $f
	done
    done
done

