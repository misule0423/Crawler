#!/usr/bin/env python                                               

""" 
crawl_<URL>_<TECH>.py is a crawler to scrape image files 
from querying the <URL> using the <TECH>.                                                                            

TODO (hsong):
- NONE
 
"""

import sys
import getopt
import time
import re
import os.path, errno
import inspect
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs
import urllib2

MAX_IMAGE_NUM = 500 # Collect 1000 most relevant images
WAIT_SEC  = 0     # Wait 5 sec to let web page data to come in 

# A parameter that determines whether to use Firefox window or not
is_headless = 1

# URL to crawl and its parameter to be appended
# before Selenium triggers HTTP GET
url_FQDN = "http://www.google.com"
url_path = "images"
param_source = "source=imghp"
param_misc = "surl=1&tbs=islt:qsvga"   # Show image url, size larger than QSVGA
param_query = "q="

# User agent string
# Google Bot 2.1: used for google image search
# to return the non-web2.0, non-dynamic result pages.
user_agent = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html"
# Generic Firefox 29
# user_agent = "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:29.0) Gecko/20100101 Firefox/29.0"


# Function to collect image files
def download_image(url, data_dir, f_url, image_index):
    file_name = url.split('/')[-1]
    file_size = 0
    print("INFO 00010: %08d|%016d|%s|%s\n" % (image_index, file_size, file_name, url))
    f_image = open(data_dir+"/"+file_name, 'wb')
    try:
        req = urllib2.Request(url, headers = {'User-Agent': user_agent})
        u = urllib2.urlopen(req, timeout = 3)
        meta = u.info()
        if meta:
            if len(meta.getheaders("Content-Length")) > 0:
                file_size = int(meta.getheaders("Content-Length")[0])
        image = u.read()
        f_image.write(image)
        if len(image) != file_size:
            print "ERROR 00001: [%s]" % (url)
    except:
        print "ERROR 00002: [%s]" % (url)
        file_size = -1
        pass

    f_url.write("%08d|%016d|%s|%s\n" % (image_index, file_size, file_name, url))
    f_image.close


# Function to crawl each page 
# within either process_1st_page() or process_subsequent_pages() fn.
def crawl_a_page(url, data_dir, page, browser):    
    print "Connecting to URL [%s]"%(url)
    browser.get(url)
    browser.implicitly_wait(WAIT_SEC)
    # Beautiful Soup
    out = browser.page_source
    soup = bs(out)
    f_html = open(data_dir+"/result_page"+`page`+".html", "w")
    html_out = soup.prettify("utf-8")
    f_html.write(html_out)
    f_html.close

    image_index = 0
    f_url = open(data_dir+"/images.url", "a+")
    if os.stat(data_dir+"/images.url").st_size == 0:
        f_url.write("# This is a machine generated file. Do NOT modify.\n")
        f_url.write("# INDEX|FILE_SIZE|FILE_NAME|URL\n")
    else:
        # Read last line and store its index.
        last_line = ''
        for line in f_url:
            if not line.startswith("#"):
                last_line = line
        if last_line != '':
            image_index = int(re.split('\|', last_line)[0])
    i = 0
    tbl = soup.find('table', {'class':'images_table'})
    for td in tbl.find_all('td'):
        i += 1
        image_index += 1
        link = td.find('img').get('src')
        image_url = re.search(':([^:]*)$', link).group(1)
        image_url = re.sub('^[/]+', '', image_url)
        download_image("http://"+image_url, data_dir, f_url, image_index)
    f_url.close
    print "INFO 00001: URLs: {%d}"%(i)
    return soup

def crawl(url, data_dir, page, user_agent):
    browser = ''
    if is_headless==1:
        # Headless exec
        # Assigning the user agent string for PhantomJS
        dcap = dict(webdriver.DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = (user_agent)
        browser = webdriver.PhantomJS(desired_capabilities=dcap)
    else:
        # Exec with Firefox head
        profile = webdriver.FirefoxProfile()
        profile.set_preference("general.useragent.override", user_agent)
        browser = webdriver.Firefox(profile)

    # Crawl images on the current page
    soup = crawl_a_page(url, data_dir, 1, browser)
    
    # Crawl URLs to subsequent pages
    i = 0
    tbl = soup.find('table', {'id':'nav'})
    for td in soup.find_all('td'):
        i+=1
        link = td.find('a', {'class':'fl'})
        if link:
            next_url = re.search('^(.*?)&start=(.*?)&(.*?)$', link.get('href'))
            if next_url:
                next_page_prefix = next_url.group(1)
                next_page_suffix = next_url.group(3)

    i = 0
    for start in xrange(20,MAX_IMAGE_NUM,20):
        i+=1
        next_url = url_FQDN+next_page_prefix+"&start="+`start`+"&"+next_page_suffix+"&"+param_misc
        crawl_a_page(next_url, data_dir, i, browser)
    browser.quit()


def mkdir(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise


def main(argv):
    global is_headless
    global param_query
    
    # Receive commandline arguments
    try:
        opts, args = getopt.getopt(argv,"q:o:h",["query="])
    except getopt.GetoptError:
        print 'crawl.py -q <query string> -o <output path> -h <optional: enable Firefox head.>'
        sys.exit(2)

    data_dir = ""
    for opt, arg in opts:
        if opt in ('-q', '--query'):
            param_query += arg
            print 'Input query: [%s]'%(param_query)
        elif opt == '-h':
            is_headless = 0
            print 'Executing with Firefox head'
        elif opt == '-o':
            data_dir = arg
            print 'Output path: [%s]'%(data_dir)

    # Combine baseline FQDN, path, and parameters and send out HTTP GET
    url = url_FQDN+"/"+url_path+"?"+param_source+"&"+param_misc+"&"+param_query
    mkdir(data_dir)
    crawl(url, data_dir, 1, user_agent)

if __name__ == "__main__":
    main(sys.argv[1:])
