import scrapy

class testCrawl(scrapy.Spider):
      name = "test_crawler"
      allowed_domains = ['usv.com']
      start_urls = ['https://www.usv.com/']

      def parse(self, response):
            print response.xpath("//*[a='About']/a").extract()
