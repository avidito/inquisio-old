from scrapy import Spider
from scrapy import Request

from datetime import datetime

from crawler.items import BeritaScraperItem


class DetikSpider(Spider):
	name = 'detik'
	allowed_domains = ['detik.com']
	start_urls = [
			'detik.com/indeks/',		
			]

	custom_settings = {
		'ITEM_PIPELINES': {'crawler.pipelines.DetikPipeline': 300,}
	}

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
		daftar_url_berita = response.xpath('//h3/a/@href').extract()
		if not daftar_url_berita:
			daftar_url_berita = response.xpath('//li/article//a/@href').extract()
		for url_berita in daftar_url_berita:
			absolute_url_berita = url_berita + '?single=1'
			yield Request(url=absolute_url_berita, callback=self.parse_info)

		# Request ke halaman berikutnya
		# url_halaman_berikutnya = response.xpath('//a[text()="Next"]/@href').extract_first()
		# yield Request(url=url_halaman_berikutnya, callback=self.parse)

	# METHOD PARSE INFO
	def parse_info(self, response):
		judul		= response.xpath('//h1/text()').extract_first()
		kategori	= response.xpath('//div[@class="nav" or @class="detail_tag"]/a/text()').extract()
		tanggal		= response.xpath('//*[contains(@class, "date")]/text()').extract_first()
		isi			= response.xpath('//div[contains(@class, "itp_bodycontent")]//text()[(ancestor::p or ancestor::li)]').extract()
		jumlah_sk	= response.xpath('//div[contains(@class, "share-box")]//a[contains(@class,"komentar")]//span/text()').extract_first()
		
		item = BeritaScraperItem({
			'judul': judul, 'kategori': kategori, 'tanggal': tanggal, 'isi': isi, 'jumlah_sk': jumlah_sk
			})

		yield item