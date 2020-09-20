from itemadapter import ItemAdapter

# TEMPLATE KELAS PIPELINE
# Buat pipeline untuk masing masing spider
# Berikan nama pipeline sama dengan nama spider
# Contoh : KompasPipeline
class TemplatePipeline:
	def process_item(self, item, spider):
		if spider.name not in ['template']:
			return item

		# Pra-proses tiap Field (jika dibutuhkan)
		item['judul'] = item['judul'].lower()
		return item

# Registrasi SpiderPipeline ke ITEM_PIPELINES di settings.py
# dengan menambahkan baris seperti berikut (berikan angka 
# lebih besar (+1) dari pipeline di atasnya):
# 'berita_scraper.pipelines.TemplatePipeline': 301,
