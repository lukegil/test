import urllib2
import re
import string

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
	global html_info
	if '<title' in line:
		split_line = re.split('<title>|</title>', line)
		url_title = split_line[1]
		return url_title

	split_line = re.split('<[A-Za-z]*? |" |">|</', line)
	url_title = split_line[1]

	if 'href' not in split_line:
		return
	for element in split_line:
		print element
		if element == '':
			next
		
		if 'href=' in element:
			url = element.split('"')[1]
			print url
			
		if '>' not in element and url_title is None:
			url_title = element.split('"')[1]
			print url_title

		if 'title=' in element:
			url_title = element.split('"')[1]
			print url_title
	html_info = (url, url_title)
	

def find_page_info(url, dic):
	page_text = urllib2.urlopen(url)

	#find the title then find all <a> tags--I think this is inefficient, since all <a>s come after <title>, but I dont feel like solving this right now

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
		if a_result is not None:
			parse_html_tag(a_result)
			a_tags.add(html_info[0])
that = dict()
find_page_info('http://en.wikipedia.org/wiki/List', that)
print that

#########################
## Final Structure	 ##
#########################
#		 www.url.com : {
#				title: "Title of Page"
#				text : "total page text?"
#		 external_urls : [url, url]
#				sub_pages : {
#					  $title : {
#						   url : "/url"
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

def crawl(seed_url): 
	crawled_urls[seed_url] = dict()
	
	#returns the page title (page_title) and tags (a_tags)
	find_page_info(seed_url, crawled_urls[seed_url])  
	
	crawled_urls[seed_url]['title'] = page_title
	
	crawled_urls[seed_url]['sub_pages'] = dict()
	
	#returns url_title and url
	for line in a_tags:
		parse_html_tag(line)
		
		if seed_url in line or 'http' not in line: 
			crawled_urls[seed_url]['sub_pages'][html_info[0]] = dict()
			crawled_urls[seed_url]['sub_pages'][html_info[0]]['title'] = html_info[1]
		else:
			if 'external_urls' in crawled_urls[seed_url]['external_urls'].keys():
				crawled_urls[seed_url]['external_urls'] = [html_info[0]]
			else:
				crawled_urls[seed_url]['external_urls'] = [html_info[0]]

	print crawled_urls
	


#crawl('http://en.wikipedia.org/wiki/List')