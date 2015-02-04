# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import signals
from scrapy.exceptions import DropItem
from scrapy.contrib.exporter import CsvItemExporter
from FTCompanyData import items
import csv

#class FtcompanydataPipeline(object):

#	def __inti__(self):
#	  self.CSV = csv.writer(open(spider.name+'.csv','w+b',newline=''))
#	  self.CSV.writerow([		'symbol', 'ric', 
#				  	'issue_name',
#					'Open',
#					'Day_high',
#					'Day_low',
#					'Previous_close',
#					'Average_volume',
#					'Shares_outstanding',
#					'Free_float',
#					'P_E_TTM',
#					'Market_cap',
#					'Market_cap_ccy',
#					'EPS_TTM',
#					'EPS_TTM_ccy',
#					'Annual_div_TTM',
#					'Annual_div_ccy',
#					'Annual_div_yield',
#					'Div_ex_date',
#					'Div_pay_date',
#					'Weeklowprice',
#					'Weeklowdate',
#					'Weekhighprice',
#					'Weekhighdate',
#					'bs_ccy',
#					'years',
#					'total_assets',
#					'csti',
#					'net_tr',
#					'ti',
#					'ppe',
#					'oca',
#					'tca',
#					'net_property',
#					'net_goodwill',
#					'net_intangibles',
#					'lti',
#					'long_term_notes_receivable',
#					'other_long_term_assets'
#	])
	
#	def process_item(self, item, spider):
#	   self.CSV.writerow([item['symbol'].encode('utf-8'),
#				item['ric'].encode('utf-8'),
#				item['issue_name'].encode('utf-8'),
#				item['Open'].encode('utf-8'),
#				item['Day_high'].encode('utf-8'),
#				item['Day_low'].encode('utf-8'),
#				item['Previous_close'].encode('utf-8'),
#				item['Average_volume'].encode('utf-8'),
#				item['Shares_outstanding'].encode('utf-8'),
#				item['Free_float'].encode('utf-8'),
#				item['P_E_TTM'].encode('utf-8'),
#				item['Market_cap'].encode('utf-8'),
#				item['Market_cap_ccy'].encode('utf-8'),
#				item['EPS_TTM'].encode('utf-8'),
#				item['EPS_TTM_ccy'].encode('utf-8'),
#				item['Annual_div_TTM'].encode('utf-8'),
#				item['Annual_div_ccy'].encode('utf-8'),
#				item['Annual_div_yield'].encode('utf-8'),
#				item['Div_ex_date'].encode('utf-8'),
#				item['Div_pay_date'].encode('utf-8'),
#				item['Weeklowprice'].encode('utf-8'),
#				item['Weeklowdate'].encode('utf-8'),
#				item['Weekhighprice'].encode('utf-8'),
#				item['Weekhighdate'].encode('utf-8'),
#				item['bs_ccy'].encode('utf-8'),
#				item['years'].encode('utf-8'),
#				item['total_assets'].encode('utf-8'),
#				item['csti'].encode('utf-8'),
#				item['net_tr'].encode('utf-8'),
#				item['ti'].encode('utf-8'),
#				item['ppe'].encode('utf-8'),
#				item['oca'].encode('utf-8'),
#				item['tca'].encode('utf-8'),
#				item['net_property'].encode('utf-8'),
#				item['net_goodwill'].encode('utf-8'),
#				item['net_intangibles'].encode('utf-8'),
#				item['lti'].encode('utf-8'),
#				item['long_term_notes_receivable'].encode('utf-8'),
#				item['other_long_term_assets'].encode('utf-8')
#]) 
#           return item
class FtcompanydataPipeline(object):

    def __init__(self):
        self.files = {}
    
    @classmethod
    def from_crawler(cls, crawler):
         pipeline = cls()
         crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
         crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
         return pipeline

    def spider_opened(self, spider):
        file = open('%s_.csv' % spider.name, 'w+b')
        self.files[spider] = file
        self.exporter = CsvItemExporter(file)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item	   	
