# Modul Sistem
import os

# Modul Threading
import crochet
crochet.setup()

# Modul Scrapy
from scrapy.utils.project import get_project_settings
from scrapy.crawler import Crawler, CrawlerRunner
from scrapy import signals
from scrapy.signalmanager import dispatcher

# Modul Projek
from crawler.spiders import detik, kompas, okezone, sindonews

# Variable Global Spider
DAFTAR_SPIDER = {
	'detik': detik.DetikSpider,
	'kompas': kompas.KompasSpider,
	'okezone': okezone.OkezoneSpider,
	'sindonews': sindonews.SindonewsSpider,
}

DAFTAR_HASIL = {
	'detik': [],
	'kompas': [],
	'okezone': [],
	'sindonews': [],
}

BERKERJA = {
	'detik': False,
	'kompas': False,
	'okezone': False,
	'sindonews': False,
}

SELESAI = {
	'detik': False,
	'kompas': False,
	'okezone': False,
	'sindonews': False,
}


# SERVIS PENUGASAN SPIDER
# Fungsi Perantara untuk menjalankan spider
def penugasan_spider(nama_spider, kategori, tanggal, jumlah):
	global DAFTAR_HASIL
	global BERKERJA
	global SELESAI

	# Jika spider sedang bekerja, kembalikan status sibuk
	# Selainnya, tugaskan spider sesuai argumen dan kembalikan status diterima
	if (BERKERJA[nama_spider]):
		return {'status': 'ditolak', 'message': 'spider sedang berkerja'}
	else:

		# Kosongkan hasil dan jalankan servis
		DAFTAR_HASIL[nama_spider] = []
		_crawling(nama_spider, kategori, tanggal, jumlah)

		# Buat status spider menjadi berkerja
		BERKERJA[nama_spider] = True
		SELESAI[nama_spider] = False

		return {'status': 'diterima', 'message': 'penugasan untuk spider diterima'}

# Servis untuk memulai proses scraping oleh spider
@crochet.run_in_reactor
def _crawling(nama_spider, kategori, tanggal, jumlah):
	
	# Pengaturan path ke settings scrapy
	settings_file_path = 'crawler.settings'
	os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
	
	# Konfigurasi setting yang akan digunakan
	s = get_project_settings()
	s.update({
			'CLOSESPIDER_ITEMCOUNT': jumlah,
		})

	# Konfigurasi spider dan event-loop
	spider = DAFTAR_SPIDER[nama_spider]
	crawler = Crawler(spider, s)
	dispatcher.connect(_menyimpan_data, signal=signals.item_scraped)
	dispatcher.connect(_tugas_selesai, signal=signals.spider_closed)

	# Menjalankan event
	runner = CrawlerRunner(s)
	event = runner.crawl(spider, kategori=kategori, tanggal=tanggal)

# Fungsi menyimpan hasil scraping
def _menyimpan_data(item, response, spider):
	global DAFTAR_HASIL

	nama_spider = spider.name
	DAFTAR_HASIL[nama_spider].append(dict(item))

# Fungsi alarm ketika spider telah selesai
def _tugas_selesai(spider):
	global BERKERJA
	global SELESAI

	nama_spider = spider.name

	# Membuat kondisi selesai dari spider
	BERKERJA[nama_spider] = False
	SELESAI[nama_spider] = True

###############################################################

# SERVICE EKSTRAKSI HASIL
def ekstraksi_hasil(nama_spider):
	global DAFTAR_HASIL
	global BERKERJA
	global SELESAI

	# Jika spider berkerja, kembalikan pesan spider sibuk
	# Jika spider selesai, kembalikan hasil scraping
	# Selainnya, kembalikan pesan spider sedang tidak bekerja
	if (BERKERJA[nama_spider]):
		return ({'status': 'sibuk', 'message': 'spider masih berkerja'}, None)
	elif (SELESAI[nama_spider]):
		return ('selesai', DAFTAR_HASIL[nama_spider])
	else:
		return ({'status': 'ditolak', 'message': 'spider sedang tidak berkerja'}, None)