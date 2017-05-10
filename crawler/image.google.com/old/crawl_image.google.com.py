#!/usr/local/bin/python

import re
import mechanize
from bs4 import BeautifulSoup as bs
from splinter import Browser

WAIT_TIME = 10000
out = ""
with Browser() as browser:
    url = "https://www.google.com/search?q=sonata+nf&client=ubuntu&hs=LPU&channel=fs&source=lnms&tbm=isch&sa=X&ei=_OCgVIasJMrYggTps4LQDg&ved=0CAgQ_AUoAQ&biw=1855&bih=985#channel=fs&tbm=isch&q=sonata+nf&imgdii=AmJbqV8Fn76YcM%3A%3BiA8NHMSdzAiMhM%3BAmJbqV8Fn76YcM%3A"
#file:///home/ddmi/code/crawler/sonataNF.html"
    browser.visit(url)

    if browser.is_element_present_by_id('smb', WAIT_TIME):
        button = browser.find_by_id("smb")
        button.click()
#        browser.select('smb', '.paywithcc, .buy_now_button')
    out = browser.html

soup = bs(out)

# br = mechanize.Browser()
# response1 = br.open("file:///home/ddmi/code/crawler/sonataNF.html")
# # follow second link with element text matching regular expression
# #response1 = br.follow_link(text_regex=r"cheese\s*shop", nr=1)
# assert br.viewing_html()
# br.submit(name='')
# #print br.title()
# #print response1.geturl()
# #print response1.info()  # headers
# #print response1.read()  # body
# soup = bs(response1.read())

f_out = open("bs_output.html", "w")
html_out = soup.prettify("utf-8")
f_out.write(html_out)
f_out.close

# Beautiful Soup
i = 0
for c in soup.find_all('div', {'class':'rg_di'}):
    i+=1
    link = c.find('a').get('href')

    url = re.search('imgurl=(.+)&imgrefurl', link)
    if url:
        print "[{}] URL: {}".format(i, url.group(1))

###


# br.select_form(name="order")
# # Browser passes through unknown attributes (including methods)
# # to the selected HTMLForm.
# br["cheeses"] = ["mozzarella", "caerphilly"]  # (the method here is __setitem__)
# # Submit current form.  Browser calls .close() on the current response on
# # navigation, so this closes response1
# response2 = br.submit()

# # print currently selected form (don't call .submit() on this, use br.submit())
# print br.form

# response3 = br.back()  # back to cheese shop (same data as response1)
# # the history mechanism returns cached response objects
# # we can still use the response, even though it was .close()d
# response3.get_data()  # like .seek(0) followed by .read()
# response4 = br.reload()  # fetches from server

# for form in br.forms():
# print form
# # .links() optionally accepts the keyword args of .follow_/.find_link()
# for link in br.links(url_regex="python.org"):
# print link
#     br.follow_link(link)  # takes EITHER Link instance OR keyword args
#     br.back()


