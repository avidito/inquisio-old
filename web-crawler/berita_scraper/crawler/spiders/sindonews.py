from scrapy import Spider
from scrapy import Request

from datetime import datetime

from crawler.items import BeritaScraperItem


class SindonewsSpider(Spider):
	name = 'sindonews'
	allowed_domains = ['sindonews.com']
	start_urls = [
		'https://index.sindonews.com/index/',
		]

	custom_settings = {
		'ITEM_PIPELINES': {'crawler.pipelines.SindonewsPipeline': 300,}
	}

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
			absolute_url_berita = url_berita + "?showpage=all"
			yield Request(url=absolute_url_berita, callback=self.parse_info)

		# Request ke halaman berikutnya
		url_halaman_berikutnya = response.xpath('//a[@rel="next"]/@href').extract_first()
		yield Request(url=url_halaman_berikutnya, callback=self.parse)

	# METHOD PARSE INFO
	def parse_info(self, response):
		judul		= response.xpath('//*[@class="title" or self::h1]/text()').extract_first()
		kategori	= response.xpath('//*[contains(@class, "tag") or @class="category-relative"]//li//a/text()').extract()
		tanggal		= response.xpath('//time/text()').extract_first()
		isi			= response.xpath('//section[@class="article col-md-11"]//text()[(parent::section or preceding::figcaption and following::span[@class="reporter"])]').extract()
		jumlah_sk	= '0'

		if not isi:
			isi = response.xpath('//div[@itemprop="articleBody"]//text()[(following::div[@class="reporter" or @class="editor"]) and not(ancestor::div[@class="baca-inline" or contains(@class,"ads300")])]').extract()
		
		item = BeritaScraperItem({
			'judul': judul, 'kategori': kategori, 'tanggal': tanggal, 'isi': isi, 'jumlah_sk': jumlah_sk
			})

		yield item