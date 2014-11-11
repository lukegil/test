import urllib2
import re
import string
import pprint
import connect

#remove all html tags from a string
def remove_html_tags(text):
        strip_text = ''
        flag = ''
        last_character = ''
        count = 0
#look through every character
        for character in text:
                #if it has a <, it might be the start of a tag
                if character == '<':
                        #grab everything before a space
                        tag_name = find_type_of_tag(text, count)
                        path = tag_tree 
                        #now actually check if it's a tag
                        for i in range(len(tag_name)):
                                if tag_name[i] in path.keys():
                                        path = path[tag_name[i]]
                                        continue
                                elif 'tag_name' in path.keys():
                                        tag_name = path['tag_name']
                                else: 
                                        tag_name = ''
                        #if it's not, add it to the working doc
                        if tag_name = '':
                                strip_text += '<'
                                continue
                        #if it's a header tag, let's set a flag so we skip everything until we hit the end of the header
                        if tag_name = '<head':
                                flag = 'head'
                                             
                        if flag == 'head' and tag_name != '</head':
                                continue

                        #note to Luke: so now, if a tag is in < here > or </here> or <here/>, then throw it away, otherwise, add it to the working doc

                        
                                       
                if tag_name == '<head':
                        flag = 'head'
                if tag_name == '</head':
                        flag = ''
                if flag == 'head':
                        continue
                if 


def find_type_of_tag(text, iteration):
        tag_name = ''
        while text[iteration] != ' ':
                tag_name += text[iteration]
                iteration += 1
        return tag_name

#create a dictionary of each character of the tag, so if you progress forward you can spell out an entire tag
#this should be called at the top of whatever function wants to use it, not each iteration its used for
def create_tag_tree():
        global tag_tree
        tag_tree = {}
        for line in open('tags.txt'):
                current_depth = tag_tree
                for character in line:
                        if character == '\n':
                                current_depth['tag_name'] = line.strip()
                                continue
                        if character not in current_depth.keys():
                                current_depth[character] = {}
                                current_depth = current_depth[character]
                        else:
                                current_depth = current_depth[character]


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
			#print attribute
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
			#print html_info
			a_tags.add(html_info)
			
	


#########################
## Final Structure	 ##
#########################
#		 www.url.com : {
#				title: "Title of Page"
#				text : "total page text?"
#		 #		sub_pages : {
#					  $url : {
#						   title : "$title"
#						   text : "the text of the page"
#						}
#				external_urls : { $url : {title : $title}}
#				}
#
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
		if tag is None:
			continue
		if 'http://' not in tag[0] and 'https://' not in tag[0]: 
			working_dict['sub_pages'][tag[0]] = dict()
			working_dict['sub_pages'][tag[0]]['title'] = tag[1]
		else:
			if 'external_urls' in working_dict.keys():
				working_dict['external_urls'][tag[0]] = dict()
                                working_dict['external_urls'][tag[0]]['title'] = tag[1]
			else:
				working_dict['external_urls'] = dict()
				working_dict['external_urls'][tag[0]] = dict()
                                working_dict['external_urls'][tag[0]]['title'] = tag[1]


	
#put dic inot db:

def flatten_urls(base_url, dic, url_type):
        cursor = connect.mysql_connection.cursor()
        for url in dic.keys():
                destination_url = url
                relation_title = dic[url]['title']
                if url_type == 'external_urls':
                        print (base_url, relation_title, destination_url)
                        params = (base_url, relation_title, destination_url)
                        query = (' INSERT INTO external_relations '
                                       ' SET origin_url = %s,'
                                       ' relation_title = %s,'
                                       ' destination_url = %s')

                        cursor.execute(query, params)

                if url_type == 'internal_urls':
                        cursor.execute(' INSERT INTO internal_relations '
                                       ' SET origin_url = %s,'
                                       ' relation_title = %s,'
                                       ' destination_url = %s',
                                       (base_url, relation_title, destination_url))
                connect.mysql_connection.commit()

#        cursor.close()
                
def move_dic_to_DB(dic):
        for key in dic.keys():
                if 'external_urls' in dic[key].keys():
                        flatten_urls(key, dic[key]['external_urls'],'external_urls')

                if 'sub_pages' in dic[key].keys():
                        flatten_urls(key, dic[key]['sub_pages'], 'internal_urls')

                        


this_dict = dict()


#crawl('http://en.wikipedia.org/wiki/List_of_venture_capital_firms', this_dict)
#move_dic_to_DB(this_dict)

create_tag_tree()
pprint.pprint(tag_tree, width=4)
