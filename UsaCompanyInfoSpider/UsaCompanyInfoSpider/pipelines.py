# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class UsacompanyinfospiderPipeline(object):
  	def __init__(self):
		try:
			self.file=open('./USA_Company_info.txt','w')
		except:
			print 'open file failed!'
		else:
			print 'open file successfully.'

	def process_item(self, item, spider):
		print item
		data_source=item.values()
		data_line='\t'.join(data_source)
		self.file.write(data_line+'\r\n')
        	return item

	def __del__(self):
		self.file.close()
