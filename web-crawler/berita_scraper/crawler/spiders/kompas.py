# Modul Scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Request

# Modul Utilitas
from datetime import datetime

# Modul Projek
from crawler.items import BeritaScraperItem


class KompasSpider(CrawlSpider):
	name = "kompas"
	allowed_domains = ["kompas.com"]
	start_urls = [
		"https://indeks.kompas.com",
		]

	custom_settings = {
		"ITEM_PIPELINES": {"crawler.pipelines.KompasPipeline": 300,}
	}

	# RULES UNTUK EXCLUDE BEBERAPA URL
	rules = (
        Rule(LinkExtractor(restrict_xpaths=["//a[@class='article__link']"], 
            allow_domains="kompas.com",
            allow=[
            	r"/global/",
            	r"/tren/",
            	r"/sains/",
            	r"/edu/",
            	r"/skola/",
            ]),
            callback="parse_info", process_links="process_links", follow=False),

        Rule(LinkExtractor(restrict_xpaths=["//a[@class='article__link']"], 
            allow_domains="tekno.kompas.com",
            deny=[
            	r"/galeri/"
            ]),
            callback="parse_info", process_links="process_links", follow=False),

        Rule(LinkExtractor(restrict_xpaths=["//a[@class='article__link']"], 
            allow_domains=[
            	"nasional.kompas.com",
            	"regional.kompas.com",
            	"megapolitan.kompas.com",
            	"inside.kompas.com",
            	"kilasdaerah.kompas.com",
            	"kilaskementerian.kompas.com",
            	"kilasbadannegara.kompas.com",
            	"kilaskorporasi.kompas.com",
            	"kilasparlemen.kompas.com",
            	"sorotpolitik.kompas.com",
            	"money.kompas.com",
            	"kilasbumn.kompas.com",
            	"kilasbadan.kompas.com",
            	"kilastransportasi.kompas.com",
            	"kilasfintech.kompas.com",
            	"health.kompas.com",
            ]),
            callback="parse_info", process_links="process_links", follow=False),

        Rule(LinkExtractor(restrict_xpaths=["//a[@rel='next']"]), follow=True),
    )
    
    # METHOD INISIASI
	def __init__(self, *a, **kw):
		super(KompasSpider, self).__init__(*a, **kw)
		self.kategori = kw.get("kategori", "all")
		self.tanggal = kw.get("tanggal", datetime.now().strftime("%Y-%m-%d"))
		for i in range(len(self.start_urls)):
			url = self.start_urls[i]
			self.start_urls[i] = url + "/?site={k}&date={t}".format(k=self.kategori, t=self.tanggal)

	# METHOD PROSES LINK
	def process_links(self, links):
		for link in links:
			link.url = link.url + "?page=all"
		return links

	# METHOD PARSE INFO
	def parse_info(self, response):
		judul 	  = response.xpath("//h1[@class='read__title']/text()").extract_first()
		kategori  = response.xpath("//li[@class='tag__article__item']//text()").extract()
		tanggal   = response.xpath("//div[@class='read__time']/text()").extract_first()
		isi 	  = response.xpath("//div[@class='read__content']/*[self::p or self::ul/li or self::h2]//text()").extract()
		jumlah_sk = response.xpath("//div[@class='total_comment_share']/text()").extract_first()
		item = BeritaScraperItem({
				"judul": judul, "kategori": kategori, "tanggal": tanggal, "isi": isi, "jumlah_sk": jumlah_sk})
		yield item
