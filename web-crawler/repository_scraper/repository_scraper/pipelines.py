# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from string import printable

class RepositoryScraperPipeline:
    def process_item(self, item, spider):
        return item

# UNAIR
class UnairPipeline:
	def process_item(self, item, spider):
		if(spider.name not in ["unair"]):
			return item

		# Judul
		# Mengecilkan seluruh tulisan dan membersihkan spasi pada tulisan.
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

# UB
class UbPipeline:
	def process_item(self, item, spider):
		if(spider.name not in ['ub']):
			return item

		# Judul
		# Mengecilkan seluruh tulisan dan membersihkan spasi pada tulisan.
		daftar_kata = item['judul'].lower().split('\r')
		item['judul'] = ' '.join([kata.strip() for kata in daftar_kata])

		# Tahun
		# Mengambil bagian tahun saja.
		item['tahun'] = item['tahun'].strip()[1:-1]

		# Divisi
		# Merubah format dan membersihkan spasi pada tulisan.
		item['divisi'] = ' | '.join([d.strip() for d in item['divisi'].split('>')])

		# Abstrak
		# Jika abstrak tidak ada, isi dengan '-'
		if (item['abstrak'] is None):
			item['abstrak'] = '-'
		# Jika abstrak ada, kecilkan seluruh tulisan dan bersihkan spasi.
		else:
			daftar_kalimat = item['abstrak'].lower().split('\r')
			item['abstrak'] = ' '.join([kalimat.strip() for kalimat in daftar_kalimat])

		return item

# Undip
class UndipPipeline:
	def process_item(self, item, spider):
		if(spider.name not in ['undip']):
			return item

		# Judul
		# Mengecilkan tulisan dan menghapus unprintable characters.
		item['judul'] = item['judul'].lower().encode("ascii", "ignore").decode()

		# Tahun
		# Mengambil bagian tahun saja.
		item['tahun'] = item['tahun'].split(' ')[2]

		# Divisi
		# Jika divisi tidak ada, isi dengan '-'
		if (item['divisi'] is None):
			item['divisi'] = '-'
		# Jika divisi ada, ubah tanda pemisah.
		else:
			item['divisi'] = item['divisi'].replace('>', '|')

		# Abstrak
		# Jika abstrak tidak ada, isi dengan '-'
		if (item['abstrak'] is None):
			item['abstrak'] = '-'
		# Jika abstrak ada, kecilkan seluruh tulisan dan bersihkan spasi.
		else:
			daftar_kalimat = item['abstrak'].lower().split('\r')
			item['abstrak'] = ' '.join([kalimat.strip() for kalimat in daftar_kalimat])

		return item