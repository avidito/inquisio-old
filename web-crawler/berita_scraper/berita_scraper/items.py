import scrapy

# Konten yang diambil : judul, kategori, tanggal, isi, jumlah share dan komentar
class BeritaScraperItem(scrapy.Item):
	judul = scrapy.Field()
	kategori = scrapy.Field()
	tanggal = scrapy.Field()
	isi = scrapy.Field()
	jumlah_sk = scrapy.Field()
