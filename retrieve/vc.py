#!/usr/bin/env python

import re
import urllib2
import crawler

url = "http://en.wikipedia.org/wiki/List_of_venture_capital_firms"
web_page = urllib2.urlopen(url)

#print web_page

vc_dict = dict()

crawler.crawl(url, vc_dict)

working_dict = vc_dict['http://en.wikipedia.org/wiki/List_of_venture_capital_firms']

#retrieve all the wiki links
for key in working_dict['sub_pages']:
	
        #/w/ denotes a non-existement page, and I dont care about anchors, so only look at /wiki/ links
        if '/wiki/' is not in key:
		continue

        #now crawl that new one
	url = 'http://en.wikipedia.org' + key
	sub_dict = {}
	crawler.crawl(url, sub_dict)
	#let's find out if it's actually a venture capital firm
        page_text_list = 

	names = set(sub_dict['title'].split(" "))
	
	bad_words = set(['a','an','Wikipedia,','free','-','the','encyclopedia','and']) 
	
	names = names.difference(bad_words)
	
	for link in sub_dict[url]['external_urls']
		for name in names:
			re_string = re.compile("www\..*"name

for line in web_page:
 #   print "next line:"
  #  print line
    if "external text" in line:
        re_string = re.compile("<th><a .*>(.*)</a>")
        vc_name = re.search(re_string, line)
        if vc_name is not None:
            vc_name = vc_name.group(1)
            #print vc_name
        
        re_string = re.compile('href="(.{,100}?)".*?>')
        vc_url = re.search(re_string, line)
        if vc_url is not None:
            vc_url = vc_url.group(1)        
            vc_dict[vc_name] = vc_url
            #print vc_dict[vc_name]
        else: 
            continue

    else:
        re_string = re.compile("<th><a.*>(.*)</a>")
        vc_name = re.search(re_string, line)

        if vc_name is not None:
            vc_name = vc_name.group(1)
            #print vc_name
        
        re_string = re.compile('href="(.{,100}?)".*?>')
        wiki_url = re.search(re_string, line)
        
        if wiki_url is not None:
            wiki_url = "http://en.wikipedia.org" + wiki_url.group(1)
#            print wiki_url
        else: 
            continue
        
        try:
            second_page = urllib2.urlopen(wiki_url)
            second_page_iter = iter(second_page)
            for line in second_page_iter:
                if "Website</th>" in line:
                    line = next(second_page_iter)
                    re_string = re.compile('href="(.{,100}?)".*?>')
                    vc_url = re.search(re_string, line)
                    if vc_url is not None:
                        vc_url = vc_url.group(1)
                        vc_dict[vc_name] = vc_url
#                        print vc_dict[vc_name]
                        break
                    
        except:
            print " "
        

for key in vc_dict.keys():
    print "%s :    %s" % (key, vc_dict[key])
                
                

              
                    
                                        
