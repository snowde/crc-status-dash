# -*- coding: utf-8 -*-
import scrapy
import math


class GlassDoor(scrapy.Spider):
    name = 'glassdoor'
    allowed_domains = ['glassdoor.com']
    start_urls = ['https://www.glassdoor.com/Benefits/BJ-s-Restaurants-US-Benefits-EI_IE6490.0,16_IL.17,19_IN1.htm']

    def parse(self, response):
        
        
        ratings = [response.xpath('//li[contains(@class,"benefitReview")][{}]//span[@class="rating"]/span/@title'.format(i)).extract() for i in range(1, 11)]
        review_dates = response.xpath('//div[@class="dtreviewed minor date"]/text()').extract()
        employees = [' '.join(response.xpath('//li[contains(@class,"benefitReview")][{}]//span[@class="authorInfo minor cell middle"]//text()'.format(i)).extract()) for i in range(1, 11)]
        descriptions = [response.xpath('//li[contains(@class,"benefitReview")][{}]//p[contains(@class,"description")]//text()'.format(i)).extract() for i in range(1, 11)]

        for rating, review_date, employee, description in zip(ratings, review_dates, employees, descriptions):
            item = {}
            item['Rating'] = rating[0]
            item['Review Date'] = review_date.strip()
            item['Employee'] = employee.strip()
            item['Description'] = description
            yield item

        next_page = response.xpath('//li[@class="next"]//@href').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)







