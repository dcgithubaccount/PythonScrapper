from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request

from FTCompanyData.items import FTCompanydataItem
#from .. import items

import time
import re
import math

class FTCompanyDataSpider(Spider):
    name = "FTCompanyData"
    allowed_domains = ["ft.com"]
    
    def __init__(self, ric=None, *args, **kwargs):
        super(FTCompanyDataSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['http://markets.ft.com/research/Markets/Tearsheets/Summary?s=%s' % ric] 
    #start_urls = [
    #     "http://markets.ft.com/research/Markets/Tearsheets/Summary?s=AAL:LSE"
    #]

    def parse(self, response):
        #filename = response.url.split("/")[-1]
        #open(filename, 'wb').write(response.body)
        sel = Selector(response)
        data = FTCompanydataItem()
        data['symbol'] = sel.xpath('//div/input[contains(@name,"symbol")]/@value').extract()[0]
	data['date'] = time.strftime("%d-%m-%Y") 
        data['ric'] = sel.xpath('//div/input[contains(@name,"ric")]/@value').extract()[0]
        data['issue_name'] = sel.xpath('//div/input[contains(@name,"issueName")]/@value').extract()[0]
        data['Closing_price'] = sel.xpath('//div[contains(@class,"contains wsodModuleContent")]/table/tbody/tr/td/span/text()').extract()[0]
        data['Open'] = sel.xpath('//table[contains(@class, "horizontalTable col1of")]/tbody/tr[th[text()="Open"]]/td/text()').extract()[0]
        data['Day_high'] = sel.xpath('//table[contains(@class, "horizontalTable col1of")]/tbody/tr[th[text()="Day high"]]/td/text()').extract()[0]
        data['Day_low'] = sel.xpath('//table[contains(@class, "horizontalTable col1of")]/tbody/tr[th[text()="Day low"]]/td/text()').extract()[0]
        data['Previous_close'] = sel.xpath('//table[contains(@class, "horizontalTable col1of")]/tbody/tr[th[text()="Previous close"]]/td/text()').extract()[0]
        data['Bid'] = sel.xpath('//table[contains(@class, "horizontalTable col1of")]/tbody/tr[th[text()="Bid"]]/td/text()').extract()[0]
        data['Offer'] = sel.xpath('//table[contains(@class, "horizontalTable col1of")]/tbody/tr[th[text()="Offer"]]/td/text()').extract()[0]
        data['Average_volume'] = sel.xpath('//table[contains(@class, "horizontalTable col1of")]/tbody/tr[th[text()="Average volume"]]/td/text()').extract()[0]
        data['Average_volume'] = sel.xpath('//table[contains(@class, "horizontalTable col1of")]/tbody/tr[th[text()="Average volume"]]/td/text()').extract()[0]
        data['Shares_outstanding'] = sel.xpath('//table[contains(@class, "horizontalTable col1of")]/tbody/tr[th[text()="Shares outstanding"]]/td/text()').extract()[0]
        data['Free_float'] = sel.xpath('//table[contains(@class, "horizontalTable col1of")]/tbody/tr[th[text()="Free float"]]/td/text()').extract()[0]
        data['P_E_TTM'] = sel.xpath('//table[contains(@class, "horizontalTable col1of")]/tbody/tr[th[contains(.,"P/E")]]/td/text()').extract()[0]
        
	try:
	     data['Market_cap'] = sel.xpath('//table[contains(@class, "horizontalTable col1of")]/tbody/tr[th[text()="Market cap"]]/td/text()').extract()[0]
	except IndexError:
	     data['Market_cap'] = 'NA'
        
	try:
             data['Market_cap_ccy'] = sel.xpath('//table[contains(@class, "horizontalTable col1of")]/tbody/tr[th[text()="Market cap"]]/td/span/text()').extract()[0]
	except IndexError:
	     data['Market_cap_ccy'] = 'NA'
        
	try:
	     data['EPS_TTM'] = sel.xpath('//table[contains(@class, "horizontalTable col1of")]/tbody/tr[th[contains(.,"EPS")]]/td/text()').extract()[0]
	except IndexError:
	     data['EPS_TTM'] = 'NA'

	try:
             data['EPS_TTM_ccy'] = sel.xpath('//table[contains(@class, "horizontalTable col1of")]/tbody/tr[th[contains(.,"EPS")]]/td/span/text()').extract()[0]
	except IndexError:
	     data['EPS_TTM_ccy'] = 'NA'
        
	try:
	     data['Annual_div_TTM'] = sel.xpath('//table[contains(@class, "horizontalTable col1of")]/tbody/tr[th[contains(.,"Annual div")]]/td/text()').extract()[0]
	except IndexError:
	     data['Annual_div_TTM'] = 'NA'
	
	try:
             data['Annual_div_ccy'] = sel.xpath('//table[contains(@class, "horizontalTable col1of")]/tbody/tr[th[contains(.,"Annual div")]]/td/span/text()').extract()[0]
	except IndexError:
	     data['Annual_div_ccy'] = 'NA'
	
	try:
             data['Annual_div_yield'] = sel.xpath('//table[contains(@class, "horizontalTable col1of")]/tbody/tr[th[contains(.,"Annual div")]]/td/text()').extract()[1]
	except IndexError:
	     data['Annual_div_yield'] = 'NA'
	
	try:
             data['Div_ex_date'] = sel.xpath('//table[contains(@class, "horizontalTable col1of")]/tbody/tr[th[text()="Div ex-date"]]/td/span/text()').extract()[0]
	except IndexError:
	     data['Div_ex_date'] = 'NA'

	try:
             data['Div_pay_date'] = sel.xpath('//table[contains(@class, "horizontalTable col1of")]/tbody/tr[th[text()="Div pay-date"]]/td/span/text()').extract()[0]
	except IndexError:
	     data['Div_pay_date'] = 'NA'

	data['Weeklowprice'] = sel.xpath('//div[contains(@class,"fleft lowPriceAndDate")]/div[contains(@class,"hiLoPrice")]/text()').extract()[0]
        data['Weeklowdate'] = sel.xpath('//div[contains(@class,"fleft lowPriceAndDate")]/div[contains(@class,"hiLoDate")]/text()').extract()[0]
        data['Weekhighprice'] = sel.xpath('//div[contains(@class,"fright hiPriceAndDate")]/div[contains(@class,"hiLoPrice")]/text()').extract()[0]
        data['Weekhighdate'] = sel.xpath('//div[contains(@class,"fright hiPriceAndDate")]/div[contains(@class,"hiLoDate")]/text()').extract()[0]

        #return data
	request = Request('http://markets.ft.com/research/Markets/Tearsheets/Financials?s=%s&subview=BalanceSheet' % data['symbol'] , meta={'data':data},callback = self.balance_sheet)
        #request.meta['data'] = data
	return request 

    def balance_sheet(self, response):
	#filename = response.url.split("/")[-1]
	#open(filename, 'wb').write(response.body)
	data = response.request.meta['data']
	sel = Selector(response)
	data['bs_ccy'] = sel.xpath('//div[contains(@class,"currencyDisclaimer contains")]/span/text()').extract()[0]
	data['years'] = sel.xpath('//table/thead/tr[td[contains(.,"Fiscal data as of")]]/td/text()').extract()[1]
	data['total_assets'] = sel.xpath('//table/tbody/tr[td[contains(.,"Total assets")]]/td/text()').extract()[1]
	data['total_liabilities'] = sel.xpath('//table/tbody/tr[td[contains(.,"Total liabilities")]]/td/text()').extract()[1]
	data['total_equity'] = sel.xpath('//table/tbody/tr[td[contains(.,"Total equity")]]/td/text()').extract()[1]
	data['common_shares'] = sel.xpath('//table/tbody/tr[td[contains(.,"Total common shares outstanding")]]/td/text()').extract()[1]
	data['treasury_shares'] = sel.xpath('//table/tbody/tr[td[contains(.,"Treasury shares - common primary issue")]]/td/text()').extract()[1]
	#data['csti'] = sel.xpath('//table/tbody/tr[td[contains(.,"Cash And Short Term Investments")]]/td/text()').extract()[1:5]
	#data['net_tr'] = sel.xpath('//table/tbody/tr[td[contains(.,"Total Receivables, Net")]]/td/text()').extract()[1:5]
	#data['ti'] = sel.xpath('//table/tbody/tr[td[contains(.,"Total Inventory")]]/td/text()').extract()[1:5]
	#data['ppe'] = sel.xpath('//table/tbody/tr[td[contains(.,"Prepaid expenses")]]/td/text()').extract()[1:5]
	#data['oca'] = sel.xpath('//table/tbody/tr[td[contains(.,"Other current assets, total")]]/td/text()').extract()[1:5]
	#data['tca'] = sel.xpath('//table/tbody/tr[td[contains(.,"Total current assets")]]/td/text()').extract()[1:5]
	#data['net_property'] = sel.xpath('//table/tbody/tr[td[contains(.,"Property, plant")]]/td/text()').extract()[1:5]
	#data['net_goodwill'] = sel.xpath('//table/tbody/tr[td[contains(.,"Goodwill, net")]]/td/text()').extract()[1:5]
	#data['net_intangibles'] = sel.xpath('//table/tbody/tr[td[contains(.,"Intangibles, net")]]/td/text()').extract()[1:5]
	#data['lti'] = sel.xpath('//table/tbody/tr[td[contains(.,"Long term investments")]]/td/text()').extract()[1:5]
	#data['long_term_notes_receivable'] = sel.xpath('//table/tbody/tr[td[contains(.,"Note receivable - long term")]]/td/text()').extract()[1:5]
	#data['other_long_term_assets'] = sel.xpath('//table/tbody/tr[td[contains(.,"Other long term assets")]]/td/text()').extract()[1:5]
	request = Request('http://markets.ft.com/research/Markets/Tearsheets/Business-profile?s=%s' % data['symbol'] , meta={'data':data}, callback = self.business_profile)
	return request	

    def business_profile(self, response):
	data = response.request.meta['data']
        sel = Selector(response)
	try:
	     data['industry'] = sel.xpath('//div[contains(@class,"keyinfo")]/span[contains(@class,"value")]/a/@href').extract()[0].encode('utf-8')
	     data['industry'] = data['industry'].rsplit('/')[-1]
	except IndexError:
	     data['industry'] = 'NA'
	
	try:
	     data['website'] = sel.xpath('//div[contains(@class,"keyinfo")]/span[contains(@class,"value")]/a/@href').extract()[1].encode('utf-8')
	except IndexError:
	     data['website'] = 'NA'
	
	request = Request('http://markets.ft.com/research/Markets/Tearsheets/Financials?s=%s&subview=IncomeStatement' % data['symbol'] , meta={'data':data}, callback = self.income_statement)
        return request
	#return data
   
    def income_statement(self, response):
	data = response.request.meta['data']
        sel = Selector(response)
	data['total_revenue'] = sel.xpath('//table/tbody/tr[td[contains(.,"Total revenue")]]/td/text()').extract()[1]
	data['total_op_expense'] = sel.xpath('//table/tbody/tr[td[contains(.,"Total operating expense")]]/td/text()').extract()[1]
	data['op_income'] = sel.xpath('//table/tbody/tr[td[contains(.,"Operating income")]]/td/text()').extract()[1]
	data['EBT'] = sel.xpath('//table/tbody/tr[td[contains(.,"Net income before taxes")]]/td/text()').extract()[1]
	data['EAT'] = sel.xpath('//table/tbody/tr[td[contains(.,"Net income after taxes")]]/td/text()').extract()[1]
	#data['Net_income'] = sel.xpath('//table/tbody/tr[td[contains(.,"Net income")]]/td/text()').extract()[1]
	data['Net_income'] = sel.xpath('//table/tbody/tr[td[text()="Net income"]]/td/text()').extract()[1]
        filename = data['symbol'].split(":")[-2] + ".csv"
	str1 = data['symbol'] + "|" + data['date'] + "|" + data['ric'] + "|" + data['issue_name'] + "|" + data['Closing_price'] + "|" + data['Open'] + "|" + data['Day_high'] + "|" + data['Day_low'] + "|" + data['Previous_close'] + "|" + data['Bid'] + "|" + data['Offer'] + "|" + data['Average_volume'] + "|" + data['Shares_outstanding'] + "|" + data['Free_float'] + "|" + data['P_E_TTM'] + "|" + data['Market_cap'] + "|" + data['Market_cap_ccy'] + "|" + data['EPS_TTM'] + "|" + data['EPS_TTM_ccy'] + "|" + data['Annual_div_TTM'] + "|" + data['Annual_div_ccy'] + "|" + data['Annual_div_yield'] + "|" + data['Div_ex_date'] + "|" + data['Div_pay_date'] + "|" + data['Weeklowprice'] + "|" + data['Weeklowdate'] + "|" + data['Weekhighprice'] + "|" + data['Weekhighdate'] + "|" + data['bs_ccy'] + "|" + data['years'] + "|" + data['total_assets'] + "|" + data['total_liabilities'] + "|" + data['total_equity'] + "|" + data['common_shares'] + "|" + data['treasury_shares'] + "|" + data['industry'] + "|" + data['total_revenue'] + "|" + data['total_op_expense'] + "|" + data['op_income'] + "|" + data['EBT'] + "|" + data['EAT'] + "|" + data['Net_income'] + "|"
	str2 =  data['website']
	str3 = "\n"
	str = str1 + str2 + str3 
        open(filename, 'wb').write(str)
	
	return data

