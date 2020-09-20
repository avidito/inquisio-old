from scrapy import Spider
from scrapy import Request

from datetime import datetime
from berita_scraper.items import BeritaScraperItem

class SindonewsSpider(Spider):
	name = 'sindonews'
	allowed_domains = ['sindonews.com']
	start_urls = [
		'https://index.sindonews.com/index/',
		]

	# METHOD INISIASI
	def __init__(self, kategori='0', tanggal=None):
		self.kategori = kategori
		self.tanggal = tanggal if tanggal is not None else datetime.now().strftime("%Y-%m-%d")


	# METHOD REQUEST PERTAMA
	def start_requests(self):
		for url in start_urls:
			absolute_url = url + '{kategori}?t={tanggal}'.format(kategori=self.kategori, tanggal=self.tanggal)

			# Request URL
			yield Request(url=absolute_url, callback=self.parse)