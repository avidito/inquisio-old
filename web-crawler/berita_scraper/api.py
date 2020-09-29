# Flask Module
from flask import Flask
from flask import jsonify, request
app = Flask(__name__)


# Web-Crawling Module
from twisted.internet import reactor
from scrapy import signals
from scrapy.crawler import Crawler, CrawlerRunner
from scrapy.utils.project import get_project_settings

# Project Module
from berita_scraper.spiders.kompas import KompasSpider

# Utility Module
import json
from itemadapter import ItemAdapter


SPIDER_LIST = {
	'kompas': KompasSpider,
}

# API
@app.route('/api/data', methods=['GET'])
def export_data():
	
	# Konfigurasi untuk mengambil hasil scraping
	items = []

	if ('spider' in request.args):
		spider_name = request.args['spider']
		spider_cls = SPIDER_LIST[spider_name]

		def collect_items(item, response, spider):
			json_line = json.dumps(ItemAdapter(item).asdict())
			json_obj = json.loads(json_line)
			items.append(json_obj)

		crawler = Crawler(spider_cls)
		crawler.signals.connect(collect_items, signals.item_scraped)

		# Menjalankan Spider
		runner = CrawlerRunner(get_project_settings())
		runner.crawl(crawler)

		d = runner.join()
		d.addBoth(lambda _: reactor.stop())
		reactor.run()

	return jsonify(items)

if __name__ == '__main__':
	app.run()