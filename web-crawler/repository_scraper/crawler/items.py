import scrapy

# Konten yang diambil : judul, divisi, tahun, abstrak
class RepositoryScraperItem(scrapy.Item):
    judul = scrapy.Field()
    tahun = scrapy.Field()
    divisi = scrapy.Field()
    abstrak = scrapy.Field()
