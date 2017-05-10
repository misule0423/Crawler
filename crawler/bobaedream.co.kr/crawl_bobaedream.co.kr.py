#!/usr/bin/env python                                               
 
""" 
crawl_<URL>_<TECH>.py is a crawler to scrape image files 
from querying the <URL> using the <TECH>.                                                                            

TODO (hsong):
- NONE
 
"""

import getopt
import urllib2
from bs4 import BeautifulSoup as bs
import sys
import re
import os.path, errno
from random import randint
from time import sleep

MIN_PAGES = 1
MAX_PAGES = 15 # was 15
PROGRESS_INT = 10 # was 100
MAX_TIMEOUT = 10
MAX_TIMEOUT_JPG = 2
MAX_SLEEP = 1

def build_car_listing_urls(make_id, model_id, is_import_domestic, is_validation_set):
    # Build urls for car listing. Each url contains 50 cars each, we collect MAX_PAGES number of such pages.
    car_listing_urls = []
    for page_id in xrange(MIN_PAGES, MAX_PAGES):
        if (is_validation_set):
            car_listing_url = "http://www.bobaedream.co.kr/cyber/CyberCar.php?refer_page=%2Fcyber%2FCyberCar.php&gubun="+is_import_domestic+"&order=S11&view_size=50&maker_no="+make_id+"&model_no="+model_id+"&page="+str(page_id)+"&search_field=car_name&view_stat="
        else:
            car_listing_url = "http://www.bobaedream.co.kr/mycar/mycar_list.php?refer_page=%2Fmycar%2Fmycar_list.php&gubun="+is_import_domestic+"&tab=1&order=S11&view_size=50&maker_no="+make_id+"&sold=1&model_no[]="+model_id+"&page="+str(page_id);

        print "DEBUG 00000: [%s]"%car_listing_url
        car_listing_urls.append(car_listing_url)
    return car_listing_urls

def crawl_car_listing(make_id, model_id, model_name, car_listing_url, data_dir, is_validation_set):
    # Crawl the car_listing_urls here
    # Parse the listings and put them into car_thumb_jpg_urls
    car_thumb_jpg_urls = []
    print "INFO 00010: [%s]" % car_listing_url
    try:  
        soup = bs(urllib2.urlopen(car_listing_url, timeout = MAX_TIMEOUT).read())
        sleep(randint(1,MAX_SLEEP))
    except:
        print "ERROR 00001: [%s]" % car_listing_url
        pass
        return

    # For debug
    #
    # car_listing_html = sys.argv[1]
    # f_car_listing_html = open(car_listing_html,'r+')
    # soup = bs(''.join(f_car_listing_html))
    # f_car_listing_html.close()
    # make_id = '49'
    # model_id = '903'

    if (is_validation_set):
        class_value = 'imgbox'
        width_value = 120
    else:
        class_value = 'thumimgbox'
        width_value = 116
        
    for div in soup.findAll('div', {'class':class_value}):
        field = div.find('img', width=width_value)
        if field:
            url = field["src"]
            car_thumb_jpg_urls.append(url)

    # Obtain urls of full size images from urls of thumbnails
    urls = []
    for line in car_thumb_jpg_urls:
        line = line.rstrip()
        
        if "_s1.jpg" in line:
            line = line.replace("_s1.jpg", ".jpg")
        elif "thum" in line:
            line = line.replace("thum2_", "img_")
            line = line.replace(".jpg", "_1.jpg")

        # Replicate the front side view image into side and back side view 
        # and append to urls list.
        urls.append(line)
        urls.append(line.replace("_1.jpg", "_2.jpg"))
        urls.append(line.replace("_1.jpg", "_3.jpg"))

#    print "DEBUG 20000: %s"%(data_dir+"/make"+make_id+"_model"+model_id+"_jpg.url")
    f_jpg_url = open(data_dir+"/make"+make_id+"_model"+model_id+"_jpg.url", 'a+')
    for url in urls:
        f_jpg_url.write("%s\n" % url)
    f_jpg_url.close()

    i = 0
    for url in urls:
        i+=1
#        print "INFO url: [%s]" % url
        jpg_name = url.split("/")[-1]
        out_path = data_dir+"/make"+make_id+"/model"+model_id
        if not os.path.isdir(out_path):
            mkdir_p(out_path)
        
        # Skip this jpg if it exists
        if os.path.isfile(out_path+"/"+jpg_name):
            print "INFO file already exists, skipping: [%s]" % out_path+"/"+jpg_name
            continue
        
        try:
            jpg = urllib2.urlopen(url, timeout = MAX_TIMEOUT_JPG)
            sleep(randint(0,MAX_SLEEP))
            f_jpg = open(out_path+"/"+jpg_name, 'w+')
            f_jpg.write(jpg.read())
            f_jpg.close()
        except:
            print "ERROR 00002: [%s]" % (url)
            pass

        if i % PROGRESS_INT == 0:
            print "\nINFO progress: Make [%s] Model [%s][%s], Img [%d] out of [%d], [%d] perc.\n" % (make_id, model_id, model_name, i, len(urls), int(i * 100 / len(urls)))

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"q:o:d:v:",["query="])
    except getopt.GetoptError:
        print 'crawl.py -q <query string> -o <output path> -d <I for import cars, K for domestic> -v <0 or 1 to crawl \"cyber\" listings for validation set>'
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
