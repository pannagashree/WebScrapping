
# -*- coding: utf-8 -*-
import scrapy
import os
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
    
#dest='/home/pannaga/work/extraction/extraction/scraped_data'
class ActualSpider(CrawlSpider):
    name = 'newsite'
    allowed_domains = ['edition.cnn.com','economictimes.indiatimes.com']
    start_urls = ['https://edition.cnn.com/','https://economictimes.indiatimes.com/']

    '''def abs_link(value):
        return urlparse.urljoin(response.url, value.strip())'''
    #Note:callback function name should always be something different from parse
    rules=(Rule(LxmlLinkExtractor(allow=('https://edition.cnn.com/','https://economictimes.indiatimes.com/'),deny=('https://plus.google.com/',)),callback="parse_page",follow=True),)
    def parse_page(self, response):
        site=response.meta['download_slot']
        t=str(response.css('title::text').extract()[0])
        nt=t+'.text'
        if site=="edition.cnn.com":
            sel='.zn-body__paragraph *::text'
            dest='/home/pannaga/work/extraction/extraction/CNN'
        elif site=="economictimes.indiatimes.com":
            sel='.Normal *::text'
            dest='/home/pannaga/work/extraction/extraction/ET'
        c=' '.join(response.css(sel).extract()).encode('utf-8')
        if c:
            with open(os.path.join(dest,nt),'w') as f:
                f.write(c)
            #yield {'title':t}
            yield{'desti':dest}

   
'''NOTE:SINCE IT IS RECCURSIVE SCRAPING,ONCE IT'S STARTS FETCHING ONE OF THE DOMAINS,IT CAN'T COME OUT AND FETCH OTHER DOMAINS.SO IT'S BETTER TO WRITE DIFFERENT SPIDERS FOR EACH DOMAIN'''