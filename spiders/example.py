# -*- coding: utf-8 -*-
import scrapy
import re

class ExampleSpider(scrapy.Spider):
    name = 'example'
    allowed_domains = ['www.usatoday.com/story/life/movies/2018/03/04/oscars-2018-minute-minute-breakdown-academy-awards/386048002/']
    start_urls = ['https://www.usatoday.com/story/life/movies/2018/03/04/oscars-2018-minute-minute-breakdown-academy-awards/386048002//']

    def parse(self, response):
      nm=response.css("title::text").extract()
      time=[]
      para=response.css('.p-text')
      for tag in para.xpath('.//strong/text()'):
       	t=tag.extract()
       	if(t[0].isdigit()):
       		time.append(t[:-1])
      parag=' '.join(response.css('.p-text *::text').extract())
      paragraphs=re.split("\d:\d{2}",parag)
      paragraphs.pop(0)	#removes the part of the page that is above time 
      paragraphs=[s.replace(s[0],'') for s in paragraphs] #To remove the :
      combine=zip(time,paragraphs)
      for item in combine:
        scraped_info={		
        	'timing':item[0],
        	'cont':item[1]}
        yield scraped_info
