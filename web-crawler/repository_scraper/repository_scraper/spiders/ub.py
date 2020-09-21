from scrapy import Spider
from scrapy import Request

from datetime import datetime

from repository_scraper.items import RepositoryScraperItem

class UbSpider(Spider):
    name = 'ub'
    allowed_domains = ['repository.ub.ac.id']
    start_urls = [
    	'http://repository.ub.ac.id',
    	]

    # METHOD INISIASI
    def __init__(self, tahun=None):
    	self.tahun = tahun if (tahun is not None) else datetime.now().strftime("%Y")

    # METHOD REQUESTS PERTAMA
    def start_requests(self):
    	for url in self.start_urls:
    		absolute_url = url + "/view/year/{t}.html".format(t=self.tahun)
    		yield Request(url=absolute_url, callback=self.parse)

    # METHOD PARSE UTAMA
    def parse(self, response):
    	# Ekstraksi URL dari artikel dan request ke URL artikel
    	daftar_url_artikel = response.xpath('//p/a/@href').extract()
    	for url_artikel in daftar_url_artikel:
    		absolute_url_artikel = url_artikel
    		yield Request(url=absolute_url_artikel, callback=self.parse_info)

    # METHOD PARSE INFO
    def parse_info(self, response):
    	item = RepositoryScraperItem({
    		'judul': response.xpath('//em/text()').extract_first(),
    		'tahun': response.xpath('//span[@class="person_name" and last()]/following::text()').extract_first(),
    		'divisi': response.xpath('//th[text()="Divisions:"]/following::td/a/text()').extract_first(),
    		'abstrak': response.xpath('//h2[text()="Indonesian Abstract"]/following::p/text()').extract_first(),
    		})
    	yield item


