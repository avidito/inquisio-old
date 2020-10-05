# Modul Sistem
import os

# Modul Scrapy
from scrapy.crawler import Crawler, CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy import signals
from scrapy.signalmanager import dispatcher

# Modul Threading
import crochet
crochet.setup()

# Modul Projek
from crawler.spiders import kompas

# Variable Global Spider
DAFTAR_SPIDER = {
	'kompas': kompas.KompasSpider,
}

DAFTAR_HASIL = {
	'kompas': [],
}

BERKERJA = {
	'kompas': False,
}

SELESAI = {
	'kompas': False,
}


# SERVIS PENUGASAN SPIDER
# Fungsi Perantara untuk menjalankan spider
def penugasan_spider(nama_spider, kategori, tanggal):
	global DAFTAR_HASIL
	global BERKERJA
	global SELESAI

	# Jika spider sedang bekerja, kembalikan status sibuk
	# Selainnya, tugaskan spider sesuai argumen
	if (BERKERJA[nama_spider]):
		return {'status': 'ditolak', 'message': 'spider sedang berkerja'}
	else:

		# Kosongkan hasil dan buat status berkerja
		DAFTAR_HASIL[nama_spider] = []
		BERKERJA[nama_spider] = True
		SELESAI[nama_spider] = False

		# Jalankan servis
		_crawling(nama_spider, kategori, tanggal)
		return {'status': 'diterima', 'message': 'penugasan untuk spider diterima'}

# Servis untuk membuat proses scraping oleh spider
@crochet.run_in_reactor
def _crawling(nama_spider, kategori, tanggal):
	# Pengaturan path ke settings scrapy
	settings_file_path = 'crawler.settings'
	os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)

	# Konfigurasi spider dan event-loop
	spider = DAFTAR_SPIDER[nama_spider]
	crawler = Crawler(spider, get_project_settings())
	dispatcher.connect(_menyimpan_data, signal=signals.item_scraped)
	dispatcher.connect(_tugas_selesai, signal=signals.spider_closed)

	# Menjalankan event
	runner = CrawlerRunner(get_project_settings())
	event = runner.crawl(spider, kategori=kategori, tanggal=tanggal)

# Fungsi menyimpan hasil scraping
def _menyimpan_data(item, response, spider):
	global DAFTAR_HASIL

	nama_spider = spider.name
	DAFTAR_HASIL[nama_spider].append(dict(item))

	print(dict(item))

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