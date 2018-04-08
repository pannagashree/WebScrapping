# -*- coding: utf-8 -*-
import scrapy
import os
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
    
dest='/home/pannaga/work/extraction/extraction/USToday'
class ActualSpider(CrawlSpider):
    name = 'actual'
    allowed_domains = ['www.usatoday.com']
    start_urls = ['https://www.usatoday.com//']

    #Note:callback function name should always be something different from parse
    rules=(Rule(LxmlLinkExtractor(allow=(),deny=()),callback="parse_page",follow=True),)
    def parse_page(self, response):
        t=str(response.css('title::text').extract()[0])
        nt=t+'.text'
        c=' '.join(response.css('.p-text *::text').extract()).encode('utf-8')
        if c:
            with open(os.path.join(dest,nt),'w') as f:
                f.write(c)
        yield {'title':t}