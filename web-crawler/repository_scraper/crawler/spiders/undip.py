from scrapy import Spider
from scrapy import Request

from datetime import datetime

from crawler.items import RepositoryScraperItem


class UndipSpider(Spider):
    name = 'undip'
    allowed_domains = ['eprints.undip.ac.id']
    start_urls = [
    	'http://eprints.undip.ac.id',
    	]

    custom_settings = {
        'ITEM_PIPELINES': {'crawler.pipelines.UndipPipeline': 300,},
    }

    # METHOD INISIASI
    def __init__(self, tahun="none"):
    	self.tahun = tahun if (tahun != "none") else datetime.now().strftime("%Y")

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
        		'tahun': response.xpath('//th[text()="Deposited On:"]/following::td/text()').extract_first(),
        		'divisi': response.xpath('//th[text()="Divisions:"]/following::a/text()').extract_first(),
        		'abstrak': response.xpath('//h2/following::p/text()').extract_first(),
    		})
    	yield item
