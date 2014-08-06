import urllib2
import re
import string

#find a url on a page based on a name--name can be a comma separated string

def find_url_by_text(url, names):
    global re_result
    names = string.replace(names, ',','|')
    print "names: " + names
    page_text = urllib2.urlopen(url).read()


    re_string = re.compile('href="(.{,100}?)".*?>(' + names + ')')

    re_result = re.search(re_string, page_text)
    if re_result is not None:
        re_result = re_result.group(1)

    else:
        return


    print "re_result: " + re_result

    re_suffix = re.compile('\.com|\.org|\.net|\.edu')

    if re.search(re_suffix, re_result) is None or re.search(re_suffix, re_result) is False:
        re_result = url + re_result

    print re_result
    return re_result


# top-level Dictionary constructor--take a site name (url) and use it as a key, with an empty dictionary as its value

def create_top_level_dic(url):
    if url_dictionary is None:
        return 
    
    url_dictionary[url] = {}

url_dictionary = {}

def add_entry_to_dic(url, key, value):
    if url_dictionary is None:
        return

    url_dictionary[url][key] = value


def crawl(url, forwhat, pagename):

    find_url_on_page(url, forwhat)

    if re_result is not None:
        if url not in url_dictionary:
            create_top_level_dic(url)
    
    print re_result
    add_entry_to_dic(url, pagename, re_result)

##Rule 1: source other files based on name

find_url_by_text(url, 'Portfolio,Compan')







