# -*- coding: utf-8 -*-
import scrapy
import os
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy_splash import SplashRequest
dest='/home/pannaga/work/extraction/extraction/SWH'

class SwhSpider(CrawlSpider):
	name = 'swh'
	allowed_domains = ['www.smh.com.au']
	start_urls = ['http://www.smh.com.au/']

	'''def start_requests(self):
		for url in self.start_urls:
			yield SplashRequest(url, self.parse,meta={
				'splash':{
					'endpoint':'render.html',
					'args':{'wait': 0.5},
				}
			})'''
	def splash_request(self, request):
		return SplashRequest(request.url,self.parse_page,args={'wait': 10,'timeout':3600}, meta={'real_url': request.url})
	rules=(Rule(LxmlLinkExtractor(allow=(),deny=()),callback="parse_page",process_request="splash_request",follow=True),)
	def parse_page(self, response):
		t=str(response.css('title::text').extract()[0])
		nt=t+'.text'
		c=' '.join(response.css('._1665V').xpath('.//p//text()').extract()).encode('utf-8')
		if c:
			with open(os.path.join(dest,nt),'wb') as f:
				f.write(c)
			yield {'title':t}	