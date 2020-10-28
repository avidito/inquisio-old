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
def crawling(spider_name, category, date, total):
	global RESULTS
	global WORKING
	global FINISH

	# Jika spider sedang bekerja, kembalikan status sibuk
	# Selainnya, tugaskan spider sesuai argumen dan kembalikan status diterima
	if (WORKING[spider_name]):
		return {
			"status": "busy",
			"message": "'{s}' spider is still running".format(s=spider_name)
		}
	else:

		# Kosongkan hasil dan jalankan servis
		RESULTS[spider_name] = []
		_crawling(spider_name, category, date, total)

		# Buat status spider menjadi bekerja
		WORKING[spider_name] = True
		FINISH[spider_name] = False

		return {
			"status": "accepted",
			"message": "task successfully assign to '{s}' spider".format(s=spider_name)
		}

# Servis untuk memulai proses scraping oleh spider
@crochet.run_in_reactor
def _crawling(spider_name, category, date, total):
	global SPIDER_LIST

	# Pengaturan path ke settings scrapy
	settings_file_path = "crawler.settings"
	os.environ.setdefault("SCRAPY_SETTINGS_MODULE", settings_file_path)
	
	# Konfigurasi dan insiasi argumen spider
	s = get_project_settings()
	s.update({
			"CLOSESPIDER_ITEMCOUNT": total,
		})

	# Konfigurasi spider dan event-loop
	spider = SPIDER_LIST[spider_name]
	crawler = Crawler(spider, s)
	dispatcher.connect(_store_data, signal=signals.item_scraped)
	dispatcher.connect(_work_finish, signal=signals.spider_closed)

	# Menjalankan event
	runner = CrawlerRunner(s)
	event = runner.crawl(spider, category=category, date=date)

# Fungsi menyimpan hasil scraping
def _store_data(item, response, spider):
	global RESULTS

	spider_name = spider.name
	RESULTS[spider_name].append(dict(item))

# Fungsi alarm ketika spider telah selesai
def _work_finish(spider):
	global WORKING
	global FINISH

	spider_name = spider.name

	# Membuat kondisi selesai dari spider
	WORKING[spider_name] = False
	FINISH[spider_name] = True

###############################################################

# SERVICE EKSTRAKSI HASIL
def extract_results(spider_name):
	global RESULTS
	global WORKING
	global FINISH

	# Jika spider bekerja, kembalikan pesan spider sibuk
	# Jika spider selesai, kembalikan hasil scraping
	# Selainnya, kembalikan pesan spider sedang tidak bekerja
	if (WORKING[spider_name]):
		return {
			"status": "busy",
			"message": "'{s}' spider is still working".format(s=spider_name),
		}
	elif (FINISH[spider_name]):
		return {
			"status": "accepted",
			"spider": spider_name,
			"data": RESULTS[spider_name],
		}
	else:
		return {
			"status": "denied",
			"message": "'{s}' spider doesn't have any job".format(s=spider_name),
		}