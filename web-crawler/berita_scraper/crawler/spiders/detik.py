# Modul Scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Request

# Modul Utilitas
from datetime import datetime

# Modul Projek
from crawler.items import BeritaScraperItem


class DetikSpider(CrawlSpider):
	name = 'detik'
	allowed_domains = ['detik.com']
	start_urls = [
		'detik.com/indeks/',		
		]

	custom_settings = {
		'ITEM_PIPELINES': {'crawler.pipelines.DetikPipeline': 300,}
	}

	rules = (
        Rule(LinkExtractor(restrict_xpaths=["//h3"], 
            allow_domains="news.detik.com",
            deny=[
                r"/x/",
                r"/blak-blakan/",
                r"/infografis/",
                r"/foto-news/",
                r"/video/",
            ]),
            callback='parse_info', process_links="proses_link", follow=False),

        Rule(LinkExtractor(restrict_xpaths=["//h3"], 
            allow_domains="finance.detik.com",
            deny=[
                r"/infografis/",
            ]),
            callback='parse_info', process_links="proses_link", follow=False),

        Rule(LinkExtractor(restrict_xpaths=["//article"], 
            allow_domains="health.detik.com",
            allow=[
                r"/berita-detikhealth/",
                r"/diet/",
                r"/kebugaran/"
            ]),
            callback='parse_info', process_links="proses_link", follow=False),

        Rule(LinkExtractor(restrict_xpaths=["//a[text()='Next']"],
            allow_domains=[
                "news.detik.com",
                "finance.detik.com",
                "health.detik.com"
            ]), follow=True),
    )
    
    # METHOD INISIASI
	def __init__(self, *a, **kw):
		super(DetikSpider, self).__init__(*a, **kw)
		self.kategori = kw.get('kategori', 'health')
		self.tanggal = kw.get('tanggal', datetime.now().strftime("%m/%d/%Y"))
		for i in range(len(self.start_urls)):
			url = self.start_urls[i]
			self.start_urls[i] = "https://{kategori}.{url}?date={tanggal}".format(kategori=self.kategori, url=url, tanggal=self.tanggal)

	# METHOD PROSES LINK
	def proses_link(self, links):
		for link in links:
			link.url = link.url + "?single=1"
		return links

	# METHOD PARSE INFO
	def parse_info(self, response):
		judul		= response.xpath('//h1/text()').extract_first()
		kategori	= response.xpath('//div[@class="nav" or @class="detail_tag"]/a/text()').extract()
		tanggal		= response.xpath('//*[contains(@class, "date")]/text()').extract_first()
		isi			= response.xpath('//div[contains(@class, "itp_bodycontent")]//text()[(ancestor::p or ancestor::li)]').extract()
		jumlah_sk	= response.xpath('//div[contains(@class, "share-box")]//a[contains(@class,"komentar")]//span/text()').extract_first()
		
		item = BeritaScraperItem({
			'judul': judul, 'kategori': kategori, 'tanggal': tanggal, 'isi': isi, 'jumlah_sk': jumlah_sk
			})

		yield item