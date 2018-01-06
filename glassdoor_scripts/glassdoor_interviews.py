# -*- coding: utf-8 -*-
import scrapy
import math


class GlassDoor(scrapy.Spider):
    name = 'glassdoor'
    allowed_domains = ['glassdoor.com']
    start_urls = ['https://www.glassdoor.com/Interview/BJ-s-Restaurants-Interview-Questions-E6490.htm']

    def parse(self, response):
        item = {}
        titles = response.xpath('//h2[@class="summary strong noMargTop tightTop margBotXs"]//span/text()').extract()
        interview_dates = response.xpath('//time[@class="date subtle small"]/text()').extract()
        employees = [' '.join(response.xpath('//li[contains(@class,"empReview")][{}]//div[@class="author minor"]//text()'.format(i)).extract()) for i in range(1, 11)]
        offers = [response.xpath('//li[contains(@class,"empReview")][{}]//div[@class="tightLt col span-1-3"][1]//text()'.format(i)).extract() for i in range(1, 11)]
        experiences = [response.xpath('//li[contains(@class,"empReview")][{}]//div[@class="tightLt col span-1-3"][2]//text()'.format(i)).extract() for i in range(1, 11)]
        interview_types = [response.xpath('//li[contains(@class,"empReview")][{}]//div[@class="tightLt col span-1-3"][3]//text()'.format(i)).extract() for i in range(1, 11)]
        applications = [response.xpath('//li[contains(@class,"empReview")][{}]//p[@class="applicationDetails mainText truncateThis wrapToggleStr "]//text()'.format(i)).extract() for i in range(1, 11)]
        interviews = [response.xpath('//li[contains(@class,"empReview")][{}]//p[@class="interviewDetails mainText truncateThis wrapToggleStr "]//text()'.format(i)).extract() for i in range(1, 11)]
        questions = [response.xpath('//li[contains(@class,"empReview")][{}]//span[@class="interviewQuestion noPadVert truncateThis wrapToggleStr "]//text()'.format(i)).extract() for i in range(1, 11)]

        for title, interview_date, employee, offer, experience, interview_type, application, interview, question in zip(titles, interview_dates, employees, offers, experiences, interview_types, applications, interviews, questions):
            item['Title'] = title
            item['Interview Date'] = interview_date
            item['Employee Type'] = employee
            item['Offer'] = offer
            item['Experience'] = experience
            item['Interview Type'] = interview_type
            item['Application'] = application
            item['Interview'] = interview
            item['Question'] = question
            yield item

        next_page = response.xpath('//li[@class="next"]//@href').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)







