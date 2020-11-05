# Modul Sistem
import os

# Modul Threading
import crochet
crochet.setup()

import requests

# Modul Scrapy
from scrapy.utils.project import get_project_settings
from scrapy.crawler import Crawler, CrawlerRunner
from scrapy import signals
from scrapy.signalmanager import dispatcher

# Modul Projek
from crawler.spiders import detik, kompas, okezone, sindonews


RECEIVER_ENDPOINT = "http://localhost:5050/api/receiver"

# Inisiasi Variable Global Spider
SPIDER_LIST = {
	"detik": detik.DetikSpider,
	"kompas": kompas.KompasSpider,
	"okezone": okezone.OkezoneSpider,
	"sindonews": sindonews.SindonewsSpider,
}
RESULTS = {}
WORKING = {}
FINISH  = {}

for key, _ in SPIDER_LIST.items():
	RESULTS[key] = []
	WORKING[key] = False
	FINISH[key] = False


# SERVIS PENUGASAN SPIDER
# Fungsi Perantara untuk menjalankan spider
def crawling(nama_spider, kategori, tanggal, jumlah):
	global RESULTS
	global WORKING
	global FINISH

	# Jika spider sedang bekerja, kembalikan status sibuk
	# Selainnya, tugaskan spider sesuai argumen dan kembalikan status diterima
	if (WORKING[nama_spider]):
		return {
			"status": "ditolak",
			"message": "'{s}' spider masih bekerja".format(s=nama_spider)
		}
	else:

		# Kosongkan hasil dan jalankan servis
		RESULTS[nama_spider] = []
		_crawling(nama_spider, kategori, tanggal, jumlah)

		# Buat status spider menjadi bekerja
		WORKING[nama_spider] = True
		FINISH[nama_spider] = False

		return {
			"status": "diterima",
			"pesan": "tugas diterima oleh '{s}' spider".format(s=nama_spider)
		}

# Servis untuk memulai proses scraping oleh spider
@crochet.run_in_reactor
def _crawling(nama_spider, kategori, tanggal, jumlah):
	global SPIDER_LIST

	# Pengaturan path ke settings scrapy
	settings_file_path = "crawler.settings"
	os.environ.setdefault("SCRAPY_SETTINGS_MODULE", settings_file_path)
	
	# Konfigurasi dan insiasi argumen spider
	s = get_project_settings()
	s.update({
			"CLOSESPIDER_ITEMCOUNT": jumlah,
		})

	# Konfigurasi spider dan event-loop
	spider = SPIDER_LIST[nama_spider]
	crawler = Crawler(spider, s)
	dispatcher.connect(_store_data, signal=signals.item_scraped)
	dispatcher.connect(_work_finish, signal=signals.spider_closed)

	# Menjalankan event
	runner = CrawlerRunner(s)
	event = runner.crawl(spider, kategori=kategori, tanggal=tanggal)

# Fungsi menyimpan hasil scraping
def _store_data(item, response, spider):
	global RESULTS

	nama_spider = spider.name
	RESULTS[nama_spider].append(dict(item))

# Fungsi alarm ketika spider telah selesai
def _work_finish(spider):
	global WORKING
	global FINISH

	nama_spider = spider.name

	# Membuat kondisi selesai dari spider
	WORKING[nama_spider] = False
	FINISH[nama_spider] = True

	data = {
		"spider": nama_spider,
		"data": RESULTS[nama_spider]
	}

	feedback = requests.post(url=RECEIVER_ENDPOINT, json=data)

###############################################################

# SERVICE EKSTRAKSI HASIL
def extract_results(nama_spider):
	global RESULTS
	global WORKING
	global FINISH

	# Jika spider bekerja, kembalikan pesan spider sibuk
	# Jika spider selesai, kembalikan hasil scraping
	# Selainnya, kembalikan pesan spider sedang tidak bekerja
	if (WORKING[nama_spider]):
		return {
			"status": "ditolak",
			"message": "'{s}' spider masih bekerja".format(s=nama_spider),
		}
	elif (FINISH[nama_spider]):
		return {
			"spider": nama_spider,
			"data": RESULTS[nama_spider],
		}
	else:
		return {
			"status": "ditolak",
			"message": "'{s}' spider tidak memiliki pekerjaan".format(s=nama_spider),
		}