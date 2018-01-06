# -*- coding: utf-8 -*-
import scrapy
import math


class GlassDoor(scrapy.Spider):
    name = 'glassdoor'
    allowed_domains = ['glassdoor.com']
    start_urls = ['https://www.glassdoor.com/Jobs/BJ-s-Restaurants-Jobs-E6490.htm']

    def parse(self, response):
        
        titles = response.xpath('//li[@class="jl"]//a[@class="jobLink"]/text()').extract()
        locations = response.xpath('//span[@class="subtle loc"]/text()').extract()
        dates = response.xpath('//span[@class="hideHH nowrap"]/span[@class="minor"]/text()').extract()
        for title, location, date in zip(titles, locations, dates):
            item = {}
            item['Title'] = title
            item['Location'] = location
            item['Date'] = date
            
            yield item







