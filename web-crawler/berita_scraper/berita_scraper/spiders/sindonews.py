from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Request

from datetime import datetime
from berita_scraper.items import BeritaScraperItem

class SindonewsSpider(CrawlSpider):
	name = 'sindonews'
	allowed_domains = ['sindonews.com']
	start_urls = [
		'https://index.sindonews.com/index/',
		]

	custom_settings = {
		'ITEM_PIPELINES': {'berita_scraper.pipelines.SindonewsPipeline': 300,}
	}

	# RULES UNTUK EXCLUDE BEBERAPA URL
	rules = (
        Rule(LinkExtractor(restrict_xpaths=["//div[@class='indeks-title']"], 
            allow_domains=[
            	"nasional.sindonews.com",
            	"metro.sindonews.com",
            	"daerah.sindonews.com",
            	"makassar.sindonews.com",
            	"ekbis.sindonews.com",
            	"international.sindonews.com",
            	"edukasi.sindonews.com"
            ]),
            callback='parse_info', process_links="proses_link", follow=False),

        Rule(LinkExtractor(restrict_xpaths=["//a[@rel='next']"]), follow=True),
    )
    
    # METHOD INISIASI
	def __init__(self, *a, **kw):
		super(SindonewsSpider, self).__init__(*a, **kw)
		self.kategori = kw.get('kategori', '0')
		self.tanggal = kw.get('tanggal', datetime.now().strftime("%Y-%m-%d"))
		for i in range(len(self.start_urls)):
			url = self.start_urls[i]
			self.start_urls[i] = url + "{kategori}?t={tanggal}".format(kategori=self.kategori, tanggal=self.tanggal)

	# METHOD PROSES LINK
	def proses_link(self, links):
		for link in links:
			link.url = link.url + "?showpage=all"
		return links

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
        