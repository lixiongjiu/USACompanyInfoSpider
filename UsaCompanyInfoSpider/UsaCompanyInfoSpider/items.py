# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item,Field

class UsacompanyinfospiderItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
	Company_Name=Field()
	SIC_Code=Field()
	SIC_Description=Field()
	Address=Field()
	City=Field()
	State=Field()
	ZIP_Code=Field()
	Tel=Field()
	Fax=Field()
