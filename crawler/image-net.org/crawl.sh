#!/bin/bash

#NAME="biker"
#NAME="pedestrian"
NAME="ped_attr"
INPUT=/home/ddmi/data/crawler/image-net.org/${NAME}.txt
OUTPUT=/media/ddmi/data/data/crawler/image-net.org/${NAME}

USERNAME="coolcoon"
ACCESSKEY="f628f61462840c0097f277a13eab9e175a60d506"


if [ ! -d ${OUTPUT}/val ];
then
        mkdir -p ${OUTPUT}/val
fi

for WNID in `awk -F'[/ ]' '{if($0!~"#"){print $2}}' ${INPUT}`; 
do
    # Crawl
    if [ ! -f ${OUTPUT}/${WNID}.tar ];
    then
        wget "http://www.image-net.org/download/synset?wnid=${WNID}&username=${USERNAME}&accesskey=${ACCESSKEY}&release=latest&src=stanford" -O ${OUTPUT}/${WNID}.tar
    fi
    if [ ! -d ${OUTPUT}/${WNID} ];
    then
        mkdir -p ${OUTPUT}/${WNID}
    fi
    tar -xf ${OUTPUT}/${WNID}.tar -C ${OUTPUT}/${WNID}


    # Resize
    for f in `find ${OUTPUT}/${WNID} -name "*.JPEG"`; do convert -resize 256x256\! $f $f; done

    # Separate out validation set
    for f in `/bin/ls ${OUTPUT}/${WNID}/* | head -50`; do mv $f ${OUTPUT}/val/; done

    echo "Verify results and run:  /bin/mv ${OUTPUT}/${WNID} /media/ddmi/data_hdd/caffe/data/ilsvrc14/ILSVRC2012_img_train/"
done

echo "Verify results and run:  /bin/mv ${OUTPUT}/val/* /media/ddmi/data_hdd/caffe/data/ilsvrc14/ILSVRC2012_img_val/"


