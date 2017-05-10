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
MAX_PAGES = 200 # was 15
PROGRESS_INT = 10 # was 100
MAX_TIMEOUT = 1
#MAX_TIMEOUT = 10
MAX_TIMEOUT_JPG = 2
MAX_SLEEP = 1
MAX_CAR_LISTING_URLS_WITH_NO_JPG = 3

def build_car_listing_urls(make_id, model_id):
    # Build urls for car listing. Each url contains 50 cars each, 
    # we collect MAX_PAGES number of such pages.
    car_listing_urls = []
    for page_id in xrange(MIN_PAGES, MAX_PAGES):
        car_listing_url = "http://www.encar.com/pr/pr_price.do?method=sellCar" + \
                          "&company=" + make_id + \
                          "&model=" + model_id + \
                          "&pageNo=" + str(page_id) + \
                          "&carType=truck";
        #print "DEBUG 00000: [%s]"%car_listing_url
        car_listing_urls.append(car_listing_url)
    return car_listing_urls

def crawl_car_listing(make_id, model_id, model_name, car_listing_url, data_dir):
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
        return 0

    # For debug
    #
    # car_listing_html = sys.argv[1]
    # f_car_listing_html = open(car_listing_html,'r+')
    # soup = bs(''.join(f_car_listing_html))
    # f_car_listing_html.close()
    # make_id = '49'
    # model_id = '903'

    div_class_value = 'area list'
    image_class_value = 'thumb'
    
    # Obtain urls of full size images from urls of thumbnails
    urls = []
    div = soup.find('div', {'class':div_class_value})
    for field in div.findAll('img', {'class':image_class_value}): 
        url = field["src"]
        if "_001.jpg" in url:
            urls.append(url);
            urls.append(url.replace("_001.jpg", "_002.jpg"))
            urls.append(url.replace("_001.jpg", "_003.jpg"))
            urls.append(url.replace("_001.jpg", "_004.jpg"))
        else:
            print "ERROR 30000: Skipping invalid .jpg url: %s"%url

    #print "DEBUG 20000: %s"%(data_dir+"/make"+make_id+"_model"+model_id+"_jpg.url")
    f_jpg_url = open(data_dir+"/make"+make_id+"_model"+model_id+"_jpg.url", 'a+')
    for url in urls:
        f_jpg_url.write("%s\n" % url)
    f_jpg_url.close()

    i = 0
    for url in urls:
        i+=1
        #print "INFO 20001 url: [%s]" % url
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

    #print "DEBUG 20001: %s"%(len(urls))
    return len(urls)

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
        print 'crawl.py -q <query string> -o <output path> '
        sys.exit(2)
        
    data_dir = ''
    for opt, arg in opts:
        if opt in ('-q', '--query'):
            query = arg
            (make_id, model_id, model_name) = query.split('|', 2)
            print "Input query: Make [%s] Model [%s][%s]"%(make_id, model_id, model_name)
        elif opt == '-o':
            data_dir = arg
            print 'Output path: [%s]'%(data_dir)
        else:
            print 'Wrong argument [%s] [%s]'%(opt, arg)
            sys.exit(2)

    car_listing_urls = build_car_listing_urls(make_id, model_id)

    nCar_listing_urls_with_no_jpg = 0
    for car_listing_url in car_listing_urls:
        if crawl_car_listing(make_id, model_id, model_name, car_listing_url, data_dir) == 0:
            nCar_listing_urls_with_no_jpg += 1
            if nCar_listing_urls_with_no_jpg > MAX_CAR_LISTING_URLS_WITH_NO_JPG:
                break

if __name__ == "__main__":
    main(sys.argv[1:])
