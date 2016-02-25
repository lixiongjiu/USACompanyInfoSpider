#!/usr/bin/env python
#coding=utf8
from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from UsaCompanyInfoSpider.items import UsacompanyinfospiderItem
import re
class USACompanyInfoSpider(BaseSpider):
	name='USABizSpider'
	allowed_domains=['suchbiz.com']
	start_urls=['http://www.suchbiz.com']
	states_url=None
	cities_url=None
	keep_digit_pattern=re.compile('\D')
	page_pattern=re.compile('.*?Of.*?(\d+).*?')

	def parse(self,response):
		hxs=HtmlXPathSeleter(response)
		#get USA states infomation	
		self.states_url=hxs.select('//div[@class="statel"]/ul/li/a/@href').extract()		
		for state_url in self.states_url:
			yield Request(state_url).callback=self.state_parser

	def state_parser(self,response):
		hxs=HtmlXPathSelector(response)
		#get city name infomation
		self.cities_url=hxs.select('//div[@class="statel"]/ul/li/a/@href').extract()
		for city_url in self.cities_url:
			yield Request(city_url).callback=self.biz_info_parser

	def biz_info_parser(self,reponse):
		hxs=HtmlXPathSelector(response)
		#need to deal with the situation of more than one page
		page_info=hxs.select('//html/body/table//tr/td[2]/div[5]/div[2]/table//tr/td/div/text()').extract()
		page_str=re.search(self.page_pattern,page_info).group(1)
		page_int=int(page_str)
		if page_int>1:
			for i in page_int:
				yield Request(re.sub('.html','-page'+page_int+'.html',response.url))	
		metas=hxs.select('//div[@class="usrmainc"]/div')
		for meta in metas:
			self.single_item(meta)
	def other_biz_info_parser(self,response):
		hxs=HtmlXPathSelector(response)
		metas=hxs.select('//div[@class="usrmainc"]/div')
		for meta in metas:
			self.single_item(meta)

	def single_item(meta):
		item=UsacompanyinfospiderItem()
		item['Company_Name']=meta.select('//table/tr[1]//a/span/text()').extract()
		item['SIC_Code']=meta.select('./table/tr[2]/td/text()').extract()[0]
		item['SIC_Description']=meta.select('./table/tr[2]/td/a/text()').extract()[0]
		item['Address']=meta.select('./table/tr[3]/td//span[1]/text()').extract()[0]
		item['City']=meta.select('./table/tr[3]/td//span[2]/text()').extract()[0]
		item['State']=meta.select('./table/tr[3]/td//span[3]/text()').extract()[0]
		item['ZIP_Code']=meta.select('./table/tr[3]/td//span[5]/text()').extract()[0]
		item['Tel']=meta.select('./table/tr[4]/td[1]/span[1]/text()').extract()[0]
		item['Fax']=meta.select('./table/tr[4]/td[2]/span[1]/text()').extract()[0]
		return item
