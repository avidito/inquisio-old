# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class RepositoryScraperPipeline:
    def process_item(self, item, spider):
        return item

# UNAIR
class UnairPipeline:
	def process_item(self, item, spider):
		if(spider.name not in ["unair"]):
			return item

		# Judul
		# Mengecilkan seluruh tulisan dan membersihkan spasi.
		item['judul'] = item['judul'].lower().strip()

		# Tahun
		# Mengambil bagian tahun saja.
		item['tahun'] = item['tahun'].strip()[1:-1]

		# Divisi
		# Membersihkan dan menggabung fakultas dan departemen.
		divisi = item['divisi'].split('>')
		divisi[0] = divisi[0][4:].strip()
		if(len(divisi) > 1):
			divisi[1] = divisi[1].strip()
		item['divisi'] = ' | '.join(divisi[:min(2, len(divisi))])

		# Abstrak
		# Mengecilkan seluruh tulisan dan membersihkan spasi.
		item['abstrak'] = item['abstrak'].lower().strip()

		return item