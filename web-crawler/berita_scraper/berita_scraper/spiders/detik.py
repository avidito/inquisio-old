from scrapy import Spider
from scrapy import Request

from datetime import datetime
from berita_scraper.items import BeritaScraperItem

class DetikSpider(Spider):
	name = 'detik'
	allowed_domains = ['detik.com']
	start_urls = [
			'detik.com/indeks/',		
			]

	# METHOD INISIASI
	def __init__(self, kategori="news", tanggal=None):
		self.kategori = kategori
		self.tanggal = tanggal if tanggal is not None else datetime.now().strftime("%m%d%Y")

	# METHOD REQUEST PERTAMA
	def start_requests(self):
		for url in self.start_urls:
			absolute_url = "https://{kategori}.{url}?date={tanggal}".format(kategori=self.kategori, url=url, tanggal=self.tanggal)

			# Request URL
			yield Request(url=absolute_url, callback=self.parse)

	# METHOD PARSE UTAMA
	def parse(self, response):
		# Ekstraksi URL dari artikel dan request ke URL artikel
		daftar_url_berita = response.xpath('//h3[@class="media__title"]/a/@href').extract()
		for url_berita in daftar_url_berita:
			absolute_url_berita = url_berita + '?single=1'
			yield Request(url=absolute_url_berita, callback=self.parse_info)

		# Request ke halaman berikutnya
		url_halaman_berikutnya = response.xpath('//a[text()="Next"]/@href').extract_first()
		yield Request(url=url_halaman_berikutnya, callback=self.parse)

	# METHOD PARSE INFO
	def parse_info(self, response):
		item = BeritaScraperItem({
					'judul'		: response.xpath('//h1[@class="detail__title"]/text()').extract_first(),
					'kategori'	: response.xpath('//div[@class="page__breadcrumb"]/a/text()')[-1].extract(),
					'tanggal'	: response.xpath('//div[@class="detail__date"]/text()').extract_first(),
					'isi'		: response.xpath('//div[@class="detail__body-text itp_bodycontent"]/p//text()').extract(),
					'jumlah_sk'	: response.xpath('//div[@class="flex-between share-box"]//span/text()').extract_first(),
				})
		yield item