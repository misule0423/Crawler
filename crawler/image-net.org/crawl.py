#!/usr/bin/env python                                               
 
""" 
Image-net.org synset crawler 

han song 030315

Your username is coolcoon 
Your access key is f628f61462840c0097f277a13eab9e175a60d506

TODO (hsong):
- NONE
 
"""

import getopt

wget "http://www.image-net.org/download/synset?wnid=${WNID}&username=coolcoon&accesskey=${ACCESSKEY}&release=latest&src=stanford" -O /media/ddmi/data_hdd/caffe/data/pedestrian/n10289039.tar

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"i:o:")
    except getopt.GetoptError:
        print 'crawl.py -i <input synset wnid listing> -o <output path> '
        sys.exit(2)

    data_dir = ''
    is_import_domestic = ''
    is_validation_set = 0
    for opt, arg in opts:
        if opt in ('-q', '--query'):
            query = arg
            (make_id, model_id, model_name) = query.split('|', 2)
            print "Input query: Make [%s] Model [%s][%s]"%(make_id, model_id, model_name)
        elif opt == '-o':
            data_dir = arg
            print 'Output path: [%s]'%(data_dir)
        elif opt == '-d':
            is_import_domestic = arg
            if (is_import_domestic != "I" and is_import_domestic != "K"):
                print 'Wrong import domestic switch: [%s]'%(is_import_domestic)
                sys.exit(2)
            print 'Import domestic switch: [%s]'%(is_import_domestic)
        elif opt == '-v':
            if (is_validation_set != 0 and is_validation_set != 1):
                print 'Wrong validation set switch: [%d]'%(is_validation_set)
                sys.exit(2)
            print 'Validation set switch: [%d]'%(is_validation_set)
        else:
            print 'Wrong argument [%s] [%s]'%(opt, arg)
            sys.exit(2)

    car_listing_urls = build_car_listing_urls(make_id, model_id, is_import_domestic, is_validation_set)

    for car_listing_url in car_listing_urls:
        crawl_car_listing(make_id, model_id, model_name, car_listing_url, data_dir, is_validation_set)

if __name__ == "__main__":
    main(sys.argv[1:])

