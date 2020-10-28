# Modul Scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Request

# Modul Utilitas
from datetime import datetime

# Modul Projek
from crawler.items import BeritaScraperItem


class OkezoneSpider(CrawlSpider):
	name = "okezone"
	allowed_domains = ["okezone.com"]
	start_urls = [
		"http://index.okezone.com",
		]

	custom_settings = {
		"ITEM_PIPELINES": {"crawler.pipelines.OkezonePipeline": 300,}
	}

	# RULES UNTUK EXCLUDE BEBERAPA URL
	rules = (
        Rule(LinkExtractor(restrict_xpaths=["//h4[@class='f17']"],
        	allow_domains="news.okezone.com",
        	allow=[
        		r"/337/",
        		r"/338/",
        		r"/18/",
        		r"/340/",
        		r"/65/",
        	]),
            callback="parse_info", follow=False),

        Rule(LinkExtractor(restrict_xpaths=["//h4[@class='f17']"],
        	allow_domains="economy.okezone.com",
        	allow=[
        		r"/320/",
        		r"/622/",
        		r"/455/",
        		r"/470/",
        	]),
            callback="parse_info", follow=False),

        Rule(LinkExtractor(restrict_xpaths=["//h4[@class='f17']"],
        	allow_domains="techno.okezone.com",
        	allow=[
        		r"/16/",
        	]),
            callback="parse_info", follow=False),

        Rule(LinkExtractor(restrict_xpaths=["//a[contains(text(), 'Next>')]"]), 
        	follow=True),
    )
    
    # METHOD INISIASI
	def __init__(self, *a, **kw):
		super(OkezoneSpider, self).__init__(*a, **kw)
		self.kategori = kw.get("category", "1")
		self.tanggal = kw.get("date", datetime.now().strftime("%Y/%m/%d"))
		for i in range(len(self.start_urls)):
			url = self.start_urls[i]
			self.start_urls[i] = url + "/bydate/channel/{t}/{k}".format(k=self.kategori, t=self.tanggal)
	
	# METHOD PARSE INFO
	def parse_info(self, response):
		judul 	  = response.xpath("//h1//text()").extract()
		kategori  = response.xpath("//a[@class='ga_Tag']/text()").extract()
		tanggal   = response.xpath("//div[@class='namerep']/b/text()").extract_first()
		isi 	  = response.xpath("//div[@id='contentx']/p//text()[following::div[@style='display:none;'] and not(ancestor::a/ancestor::p[preceding::p[position()=1 or position()=2][contains(.//text(), 'aca')]])]").extract()
		jumlah_sk = response.xpath("//li[@class='totshare']/a/span/text()").extract_first()
		item = BeritaScraperItem({
				"judul": judul, "kategori": kategori, "tanggal": tanggal,"isi": isi,"jumlah_sk": jumlah_sk,
				})

		# Menambahkan isi pada halaman berbeda (jika ada)
		url_selanjutnya = response.xpath("//span[text()='Selanjutnya']/parent::a/@href").extract_first()
		if (url_selanjutnya is None or url_selanjutnya == "#"):
			yield item
		else:
			yield Request(url=url_selanjutnya, meta={"item": item}, callback=self.parse_next_content)
		
	# METHOD PARSE ISI BERITA DENGAN BANYAK HALAMAN
	def parse_next_content(self, response):
		item = response.meta["item"]
		tambahan = response.xpath("//div[@id='contentx']/p//text()[following::div[@style='display:none;'] and not(ancestor::a/ancestor::p[preceding::p[position()=1 or position()=2][contains(.//text(), 'aca')]])]").extract()
		item["isi"].extend(tambahan)

		# Jika masih ada halaman lagi
		url_selanjutnya = response.xpath("//span[text()='Selanjutnya']/parent::a/@href").extract_first()
		if (url_selanjutnya is None or url_selanjutnya == "#"):
			yield item
		else:
			yield Request(url=url_selanjutnya, meta={"item": item}, callback=self.parse_next_content)
