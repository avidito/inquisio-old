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
		for url in self.start_urls:
			absolute_url = url + '{kategori}?t={tanggal}'.format(kategori=self.kategori, tanggal=self.tanggal)

			# Request URL
			yield Request(url=absolute_url, callback=self.parse)

	# METHOD PARSE UTAMA
	def parse(self, response):
		# Ekstraksi URL dari artikel dan request ke URL artikel
		daftar_url_berita = response.xpath('//div[@class="indeks-title"]/a/@href').extract()
		for url_berita in daftar_url_berita:
			yield Request(url=url_berita, callback=self.parse_info)

		# Request ke halaman berikutnya
		# url_halaman_berikutnya = response.xpath('//a[@rel="next"]/@href').extract_first()
		# yield Request(url=url_halaman_berikutnya, callback=self.parse)

	# METHOD PARSE INFO
	def parse_info(self, response):
		item = BeritaScraperItem({
			'judul'		: response.xpath('//div[@class="article"]/h1/text()').extract_first(),
			'kategori'	: response.xpath('//ul[@class="breadcrumb"]//li[last()]//a/text()').extract_first(),
			'tanggal'	: response.xpath('//div[@class="article"]//time/text()').extract_first(),
			'isi'		: response.xpath('//div[@id="content"]//text()').extract(),
			'jumlah_sk'	: '0',
			})

		yield item