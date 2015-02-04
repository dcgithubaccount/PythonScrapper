# Scrapy settings for FTCompanyData project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'FTCompanyData'

SPIDER_MODULES = ['FTCompanyData.spiders']
NEWSPIDER_MODULE = 'FTCompanyData.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'FTCompanyData (+http://www.yourdomain.com)'
#ITEM_PIPELINES = ['FTCompanyData.pipelines.FtcompanydataPipeline']
