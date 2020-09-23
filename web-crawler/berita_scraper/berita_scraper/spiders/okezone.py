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

	custom_settings = {
		'ITEM_PIPELINES': {'berita_scraper.pipelines.OkezonePipeline': 300,}
	}

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
		daftar_url_berita = response.xpath('//h4[@class="f17"]/a/@href').extract()
		for url_berita in daftar_url_berita:
			absolute_url_berita = url_berita
			yield Request(url=absolute_url_berita, callback=self.parse_info)

		# Request ke halaman berikutnya
		url_halaman_berikutnya = response.xpath('//a[contains(text(), "Next>")]/@href').extract_first()
		absolute_url_halaman_berikutnya = response.urljoin(url_halaman_berikutnya)
		yield Request(url=absolute_url_halaman_berikutnya, callback=self.parse)
	
	# METHOD PARSE INFO
	def parse_info(self, response):
		judul 	  = response.xpath('//h1//text()').extract()
		kategori  = response.xpath('//a[@class="ga_Tag"]/text()').extract()
		tanggal   = response.xpath('//div[@class="namerep"]/b/text()').extract_first()
		isi 	  = response.xpath('//div[@id="contentx"]/p//text()').extract()
		jumlah_sk = response.xpath('//li[@class="totshare"]/a/span/text()').extract_first()
		item = BeritaScraperItem({
				'judul': judul, 'kategori': kategori, 'tanggal': tanggal,'isi': isi,'jumlah_sk': jumlah_sk,
				})

		# Menambahkan isi pada halaman berbeda (jika ada)
		url_selanjutnya = response.xpath('//span[text()="Selanjutnya"]/parent::a/@href').extract_first()
		if (url_selanjutnya is None or url_selanjutnya == '#'):
			yield item
		else:
			yield Request(url=url_selanjutnya, meta={'item': item}, callback=self.parse_isi_berita)
		
	# METHOD PARSE ISI BERITA DENGAN BANYAK HALAMAN
	def parse_isi_berita(self, response):
		item = response.meta['item']
		tambahan = response.xpath('//div[@id="contentx"]/p//text()').extract()
		item['isi'].extend(tambahan)

		# Jika masih ada halaman lagi
		url_selanjutnya = response.xpath('//span[text()="Selanjutnya"]/parent::a/@href').extract_first()
		if (url_selanjutnya is None or url_selanjutnya == '#'):
			yield item
		else:
			yield Request(url=url_selanjutnya, meta={'item': item}, callback=self.parse_isi_berita)
