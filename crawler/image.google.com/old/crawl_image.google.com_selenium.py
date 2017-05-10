#!/usr/local/bin/python

import sys
import getopt
import time
import re
import os.path
import inspect
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs

#  Function to search file from local machine
def process(isHeadless, url, search_query):
    browser = ''
    if isHeadless==1:
        # Headless exec
        # Assigning the user agent string for PhantomJS
        dcap = dict(webdriver.DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:29.0) Gecko/20100101 Firefox/29.0")
                
        browser = webdriver.PhantomJS(desired_capabilities=dcap)
    else:
        # Exec with Firefox head
        browser = webdriver.Firefox()

    browser.implicitly_wait(1)
    print "Connecting to URL [%s], sending query [%s]"%(url, search_query)
    browser.get(url)
    browser.find_element_by_class_name('gsfi').send_keys(search_query)
    browser.find_element_by_class_name('lsb').click()
    browser.implicitly_wait(5)
    

    # Beautiful Soup
    out = browser.page_source
    soup = bs(out)
    f_out = open("bs_output1.html", "w")
    html_out = soup.prettify("utf-8")
    f_out.write(html_out)
    f_out.close
    i = 0
    j = 0
    for c in soup.find_all('div', {'class':'rg_di'}):
        i+=1
        link = c.find('a').get('href')
        if link:
            url = re.search('imgurl=(.+)&imgrefurl', link)
            if url:
                j+=1
    print "INFO 00001: DIVs: {} URLs: {}".format(i, j)

    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    browser.implicitly_wait(5)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    browser.implicitly_wait(5)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    browser.implicitly_wait(5)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    browser.implicitly_wait(5)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    browser.implicitly_wait(5)
    
#   try:
#       elem = WebDriverWait(browser, 10).until(EC.presense_of_element_located((By.ID, "smb")))
#   finally:
#       browser.quit()
        
    print "DEBUG 00002: "+browser.current_url

    out = browser.page_source
    #print out
    soup = bs(out)
    
    f_out = open("bs_output2.html", "w")
    html_out = soup.prettify("utf-8")
    f_out.write(html_out)
    f_out.close
    
    # Beautiful Soup
    i = 0
    j = 0
    for c in soup.find_all('div', {'class':'rg_di'}):
        i+=1
        link = c.find('a').get('href')
        if link:
            url = re.search('imgurl=(.+)&imgrefurl', link)
            if url:
                j+=1
    print "INFO 00001: DIVs: {} URLs: {}".format(i, j)

    # Click "Show more" icon
    #elem = browser.find_element_by_class_name('ksb._kvc')
    elem= browser.find_element_by_id('smb')
    elem.click()
    time.sleep(10)

    print "DEBUG 00003: "+browser.current_url

    #  Getting URL of image and writing it to imageurl.txt
    print "Saving URL of match to: imageurl.txt"
    writeurl = open('imageurl.txt', 'w')
    writeurl.write(browser.current_url)		
    writeurl.write("\n")
    writeurl.close()
    print "\n"
    
    # Beautiful Soup
    out = browser.page_source
    soup = bs(out)
    f_out = open("bs_output3.html", "w")
    html_out = soup.prettify("utf-8")
    f_out.write(html_out)
    f_out.close
    i = 0
    j = 0
    for c in soup.find_all('div', {'class':'rg_di'}):
        i+=1
        link = c.find('a').get('href')
        if link:
            url = re.search('imgurl=(.+)&imgrefurl', link)
            if url:
                j+=1
                #print "[{}] URL: {}".format(i, url.group(1))
    print "INFO 00002: DIVs: {} URLs: {}".format(i, j)
    browser.quit()


def main(argv):
    isHeadless = 1
    query = ""
    url = "http://image.google.com"
    try:
        opts, args = getopt.getopt(argv,"q:h",["query="])
    except getopt.GetoptError:
        print 'crawl.py -q <query string> -h <optional: enable execution with Firefox head.>'
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-q', '--query'):
            query = arg
            print 'Input query: [%s]'%(query)
        elif opt == '-h':
            isHeadless = 0
            print 'Executing with Firefox head'
        
    process(isHeadless, url, query, 1)

if __name__ == "__main__":
    main(sys.argv[1:])
