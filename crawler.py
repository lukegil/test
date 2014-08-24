import urllib2
import re
import string
import pprint

#find a url on a page based on a name--name can be a comma separated string

def retrieve_tags(line, tagname):
	global re_result
	re_string = re.compile('<'+ tagname + '.*?>.*?</' + tagname + '>')
	re_result = re.search(re_string, line)

	if re_result is not None:
		re_result = re_result.group(0)
		return re_result




#split each tag into a bunch of list elements, then parse those out
def parse_html_tag(line):
	
	tag_type = re.split('<| |>', line)[1]
	
	tag_attributes = set(re.split('<[A-Za-z]*? |" |">.*', line))
	
	tag_content = re.split('<.*?>', line)[1]
	
	if tag_type == 'title':
		url_title = tag_content
		return url_title
		
	if tag_type == 'a' and 'href=' in line:
		for attribute in tag_attributes:
			if 'href=' in attribute:
				url = attribute.split('href=')[1][1:]
			if 'title=' in attribute:
				url_title = attribute.split('title=')[1][1:]
		
		if 'url_title' not in locals():
			url_title = tag_content
	
	html_info = (url, url_title)
	return html_info


def find_page_info(url):
	page_text = urllib2.urlopen(url)
		

	for line in page_text:
		global page_title

		title = retrieve_tags(line, 'title')
		if title is not None:
			page_title = parse_html_tag(title)
			break
		

	global a_tags
	a_tags = set()
	for line in page_text:
		a_result = retrieve_tags(line, 'a')
		if a_result is not None and a_result != '':
			html_info = parse_html_tag(a_result)
			a_tags.add(html_info)
			
	


#########################
## Final Structure	 ##
#########################
#		 www.url.com : {
#				title: "Title of Page"
#				text : "total page text?"
#		 external_urls : [url, url]
#				sub_pages : {
#					  $url : {
#						   title : "$title"
#						   text : "the text of the page"
#				external_urls : []
#						   sub_pages : {}
#						   }
#					   },{
#					   $title : {}
#					   }
#				}
#########################
##The work:

crawled_urls = dict()

def crawl(seed_url, dictionary): 
	
	if seed_url not in dictionary.keys():
		dictionary[seed_url] = dict()
		
	working_dict = dictionary[seed_url]
	
	#returns the page title (page_title) and tags (a_tags)
	find_page_info(seed_url)  
	
	working_dict['title'] = page_title
	
	working_dict['sub_pages'] = dict()
	
	working_dict['text'] = urllib2.urlopen(seed_url).read()
	
	#returns url_title and url
	for tag in a_tags:
		if seed_url in tag[0] or 'http' not in tag[0]: 
			working_dict['sub_pages'][tag[0]] = dict()
			working_dict['sub_pages'][tag[0]]['title'] = tag[1]
		else:
			if 'external_urls' in working_dict.keys():
				working_dict['external_urls'].add(tag[0])
			else:
				working_dict['external_urls'] = set()
				working_dict['external_urls'].add(tag[0])

	

this_dict = dict()
crawl('http://www.kpcb.com/', this_dict)

pprint.pprint(this_dict, width=4)