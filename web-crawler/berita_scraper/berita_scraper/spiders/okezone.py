from scrapy import Spider
from scrapy import Request

from datetime import datetime

from berita_scraper.items import BeritaScraperItem

class OkezoneSpider(Spider):
	name = 'okezone'
	allowed_domains = ['okezone.com']
	start_urls = [
		'http://index.okezone.com',
	]

	# METHOD INISIASI
	def __init__(self, kategori="1", tanggal=None):
		self.kategori = kategori
		self.tanggal = tanggal if tanggal is not None else datetime.now().strftime("%Y/%m/%d")

	# METHOD REQUEST PERTAMA
	def start_requests(self):
		for url in self.start_urls:
			absolute_url = url + '/bydate/channel/{t}/{k}'.format(k=self.kategori, t=self.tanggal)

			# Request URL
			yield Request(url=absolute_url, callback=self.parse)

	# METHOD PARSE UTAMA
	def parse(self, response):
		# Ekstraksi URL dari artikel dan request ke URL artikel
		daftar_url_berita = response.xpath('//li[@class="col-md-12 p-nol m-nol hei-index"]//h4/a/@href').extract()
		for url_berita in daftar_url_berita:
			absolute_url_berita = url_berita
			yield Request(url=absolute_url_berita, callback=self.parse_info)

		# Request ke halaman berikutnya
		url_halaman_berikutnya = response.xpath('//a[@rel="next"]/@href').extract_first()
		absolute_url_halaman_berikutnya = response.urljoin(url_halaman_berikutnya)
		yield Request(url=absolute_url_halaman_berikutnya, callback=self.parse)
	
	# METHOD PARSE INFO
	def parse_info(self, response):
		item = BeritaScraperItem({
					'judul'		: response.xpath('//div[@class="title"]/h1/text()').extract_first(),
					'kategori'	: response.xpath('//div[@class="breadcrumb"]/ul//li//text()').extract()[1:],
					'tanggal'	: response.xpath('//div[@class="namerep"]/b/text()').extract_first(),
					'isi'		: response.xpath('//div[@id="contentx"]/p//text()').extract(),
					'jumlah_sk' : response.xpath('//li[@class="totshare"]/a/span/text()').extract_first(),
					})
		yield item
