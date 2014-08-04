#!/usr/bin/env python

import re
import urllib2

url = "http://en.wikipedia.org/wiki/List_of_venture_capital_firms"

web_page = urllib2.urlopen(url)

#print web_page

vc_dict = dict()

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
                
                

              
                    
                                        
