import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from job_hunter.items import VC_Item
import hashlib
#vc crawl-- for a given url, find their About pages, Jobs page, and portfolio/companies page

class VC_Crawl(CrawlSpider):
#      def __init__(vc_list):
#            start_urls = vc_list
      #this should be integrated into the __init__ function, so the crawler can be called on a set of vc names

      start_urls = ['https://www.usv.com/']
      name = "vc_crawler"

      xpath_rule = "//*/a[normalize-space(text())={}]"
      about_rules = [xpath_rule.format('"About"'), xpath_rule.format('"About us"')]
      job_rules = [xpath_rule.format('"Jobs"'), xpath_rule.format('"Careers"')]
      companies_rules = [xpath_rule.format('"Companies"'), xpath_rule.format('"Portfolio"'), xpath_rule.format('"Portfolio Companies"')]
      print about_rules

      rules = (Rule(SgmlLinkExtractor(restrict_xpaths=about_rules), callback='parse_vc'),)

      #alright, so ideally, with the request you pass what type of page it is (http://stackoverflow.com/questions/21122436/passing-custom-parameter-to-scrapy-request#comment31784347_21122436) 
      def parse_vc(self, response):
            print "infunction"

            vc_item = VC_Item()
            item_dic = {'url' : response.url,
                        'md5' : hashlib.md5(response.body).hexdigest(),
                        'body' : response.body}
            print "item_dic:"
            print item_dic['url']
            print "page type:"
            #print page_type
            if page_type == "about":
                  vc_item['about_page'] = item_dic
            if page_type == "jobs":
                  vc_item['job_page'] = item_dic
            if page_type == ['companies']:
                  vc_item['companies_page'] = item_dic

      def parse_start_url(self, response):
            pass
       

                  
