from scrapy import Spider

# Modul request url. Pilih salah satu.
from scrapy import Request # normal
from scrapy_splash import SplashRequest # dengan Splash

# Modul untuk item penyimpanan
# Definisikan kelas item di items.py
from berita_scrapper.items import BeritaScrapperItem

# TEMPLATE KELAS SPIDER
# Berikan nama spider sesuai dengan nama website. contoh: Kompas
# Inisiasi spider dengan url. contoh: https://indeks.kompas.com
class TemplateSpider(Spider):
	name = 'template' 
	
	# Sesuaikan allowed_domains dan start_urls yang akan digunakan. 
	# Hilangkan 'https://www' pada allowed_domains (jika ada).
	allowed_domains = ['template.com']
	
	# Masukan seluruh halaman pencarian dari website.
	# Jika ada halaman yang mengindeks seluruh artikel, cukup gunakan halaman ini saja.
	start_urls = [
		'https://indeks.template.com',
		'https://indeks2.template.com',
	]

	# METHOD INISIASI
	# Definisikan __init__() untuk mengambil argumen
	# Gunakan 'kategori' dan 'tanggal' sebagai nama argumen
	def __init__(self, kategori="all", tanggal=None):
		self.kategori = kategori
		self.tanggal = tanggal

	# METHOD REQUESTS PERTAMA
	# Definisikan start_requests() untuk praproses dan request URL.
	# Kombinasikan URL dengan argumen 'kategori' dan 'tanggal'.
	def start_requests(self):
		for url in self.start_urls:
			absolute_url = url + "/?site=" + self.kategori
			if(self.tanggal is not None):
				absolute_url += "&date=" + self.tanggal
			
			# Request URL. Pilih salah satu:
			# Request Normal
			yield Request(url=absolute_url, callback=self.parse)
			
			# Request dengan Splash
			yield SplashRequest(url=absolute_url, callback=self.parse, endpoint='render.html')

	# METHOD PARSE UTAMA
	# Definisikan parse() untuk ekstraksi halaman artikel dan navigasi halaman berikutnya.
	def parse(self, response):

		# Ekstraksi URL dari artikel dan request ke URL artikel.
		# Gunakan nama variable 'daftar_url_<kategori>' untuk daftar url. contoh: daftar_url_berita
		# Gunakan xpath untuk mencari komponen
		# Iterasikan sesuai template
		daftar_url_berita = response.xpath('//div[@class="__berita__"]/a/@href').extract()  
		for url_berita in daftar_url_berita:
			absolute_url_berita = url_berita + '?page=all'
			yield Request(url=absolute_url_berita, callback=self.parse_info)

		# Request ke halaman berikutnya. Pilih salah satu:
		# Request Normal
		url_halaman_berikutnya = response.xpath('//a[@class="paging__link paging__link--next"]/@href')[-1].extract()
		absolute_url_halaman_berikutnya = response.urljoin(url_halaman_berikutnya)
		yield Request(url=absolute_url_halaman_berikutnya, callback=self.parse)
		# --------------

		# Request dengan Splash
		# Script Lua untuk simulasi (seperti Selenium)
		nav_script = """function main(splash)
							assert(splash:go(splash.args.url))
							splash:wait(1)
							button = splash:select("a[rel=next]")
							splash:set_viewport_full()
							splash:wait(10)
							button:mouse_click()
							splash:wait(3)
							return {url = splash:url(),
									html = splash:html()}
						end"""
		yield SplashRequest(url=response.url, callback=self.parse, endpoint='execute', args={'lua_source':nav_script})
		# --------------

	# METHOD PARSE INFO
	# Method untuk ekstraksi informasi dari halaman artikel pencarian
	# Definisikan parse_info() untuk mengambil informasi dari halaman artikel
	# Gunakan kelas item InquisioItem()
	# Tidak perlu melakukan praproses, akan diatur pada pipelines.py
	# Konten yang diambil : judul, kategori, tanggal, isi, jumlah_komentar
	def parse_info(self, response):
		item = BeritaScrapperItem({
					'judul'		: response.xpath('//*[@class="read__title"]/text()').extract_first(),
					'kategori'	: response.xpath('//*[@class="breadcrumb__item"]/a/span/text()').extract()[1:],
					'tanggal'	: response.xpath('//*[@class="read__time"]/text()').extract_first(),
					'isi'		: response.xpath('//*[@class="read__content"]/p//text()').extract(),
					'jumlah_komentar' : response.xpath('//*[@class="total_comment_share"]/text()').extract_first(),
					})
		yield item