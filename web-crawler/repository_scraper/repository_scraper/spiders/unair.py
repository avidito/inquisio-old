from scrapy import Spider
from scrapy import Request

from datetime import datetime

from repository_scraper.items import RepositoryScraperItem

class UnairSpider(Spider):
    name = 'unair'
    allowed_domains = ['repository.unair.ac.id']
    start_urls = [
    	'http://repository.unair.ac.id',
    	]

    # METHOD INISIASI
    def __init__(self, tahun=None):
    	self.tahun = tahun if (tahun is not None) else datetime.now().strftime("%Y")

    # METHOD REQUESTS PERTAMA
    def start_requests(self):
    	for url in self.start_urls:
    		absolute_url = url + "/view/year/{t}.html".format(t=self.tahun)
    		yield Request(url=absolute_url, callback=self.parse)

    def parse(self, response):
        pass
