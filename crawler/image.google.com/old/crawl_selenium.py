from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
import sys
import os.path
import time


#  Function to search file from local machine
def process(url):

	#  Decomment below to enable browser
	#browser = webdriver.Firefox()
	
	#  Comment below (1 line only) to disable headless when running Firefox
	browser = webdriver.PhantomJS(desired_capabilities=dcap)
	browser.implicitly_wait(60)

	print "Connecting to Google Image Search URL [%s]"%(url)
	browser.get(url)

	# Click "Search by image" icon
	elem = browser.find_element_by_class_name('gsst_a')
	elem.click()

	# Switch from "Paste image URL" to "Upload an image"
	browser.execute_script("google.qb.ti(true);return false")

	# Set the path of the local file and submit
	print "Uploading file to 'Search by Image'"
	elem = browser.find_element_by_id("qbfile")
	#elem.send_keys(filePath)
	elem.send_keys(filename)
	#  Clicking 'Visually Similar Images'
	print "Searching for most similar match"
	ele1 = browser.find_element_by_link_text("Visually similar images")
	ele1.click()

	#  Selecting Image
	print "Match Found"
	ele2 = browser.find_element_by_xpath("//div[@data-ri='0']/a")
	ele2.click()
	#  Clicking 'View image' to go to page
	ele3 = browser.find_element_by_link_text("View image")
	ele3.click()
	
	time.sleep(1)
	print browser.current_url

	#  Getting URL of image and writing it to imageurl.txt
	print "Saving URL of match to: imageurl.txt"
	writeurl = open('imageurl.txt', 'w')
	writeurl.write(browser.current_url)		
	writeurl.write("\n")
	writeurl.close()
	print "\n"
	browser.quit()

#  Function which takes last URL written to imageurl.txt and plugs it back into Google Image search
def searchurl():

	#  Decomment below to open browser
#	browser = webdriver.Firefox()

	print "Connecting to Google Image Search"
#	Comment below (1 line only) to disable headless when running Firefox
        browser = webdriver.PhantomJS(desired_capabilities=dcap)
	browser.implicitly_wait(60)
        browser.get('http://www.google.com.au/imghp')

        # Click "Search by image" icon
        elem = browser.find_element_by_class_name('gsst_a')
        elem.click()

	#  Sending the image URL from the last line
	#  Reading the last line of imageurl.txt
        print "Checking for the last URL from: imageurl.txt"
        fileHandle = open ( 'imageurl.txt',"r" )
        lineList = fileHandle.readlines()
        lasturl = lineList[len(lineList)-1]
	fileHandle.close()
        #print lineList
        print "The URL is:"
        print lasturl
	#print lineList[len(lineList)-1]

	print "Pasting URL into 'Search by image'"
	elem = browser.find_element_by_id("qbui")
        elem.send_keys(lasturl)

	#  Clicking 'Visually Similar Images'
	print "Searching for most similar match"
        ele1 = browser.find_element_by_link_text("Visually similar images")
        ele1.click()

        #  Selecting Image
	print "Match Found"
        ele2 = browser.find_element_by_xpath("//div[@data-ri='0']/a")
        ele2.click()

        #  Clicking 'View image' to go to page
        ele3 = browser.find_element_by_link_text("View image")
        ele3.click()


	#  Sleeping in order to get correct URL and not google redirect link
        print "snoozing.... zzzzzzz..... "
	time.sleep(1)

	#  Appending imageurl.txt with new url
	print "Writing new URL to imageurl.txt"
        writeurl = open('imageurl.txt', 'a')
        writeurl.write(browser.current_url)
	writeurl.write("\n")
        writeurl.close()
	print "\n"
	browser.quit()




# Main
url = "http://image.google.com"
print "Enter query to [%s]: "%(url)
search_query = raw_input()

#  Assigning the user agent string for PhantomJS
dcap = dict(webdriver.DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:29.0) Gecko/20100101 Firefox/29.0")

process(url, search_query)
