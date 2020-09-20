# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BeritaScraperPipeline:
    def process_item(self, item, spider):
        return item

# Kompas
class KompasPipeline:
	def process_item(self, item, spider):
		if spider.name not in ['kompas']:
			return item

		# Judul
		# Mengecilkan seluruh tulisan
		item['judul'] = item['judul'].lower()

		# Kategori
		# Menggabungkan kategori dan sub kategori dengan '|'
		item['kategori'] = ' | '.join(item['kategori'])

		# Tanggal
		# Mengambil bagian tanggal saja
		item['tanggal'] = item['tanggal'].split(' - ')[1].split(',')[0] 
		
		# Jumlah Komentar
		# Mengambil bagian angka saja
		if (item['jumlah_sk'] is not None):
			item['jumlah_sk'] = item['jumlah_sk'][1:-1]
		
		# Memberikan nilai 0 jika tidak ada komentar
		else:
			item['jumlah_sk'] = 0

		# Isi.
		# Menghilangkan iklan atau referensi ke artikel lain
		iklan_idx = [idx for (idx, val) in enumerate(item['isi']) if val.startswith('Baca juga')]
		for i in range(len(iklan_idx)-1, -1, -1):
			del item['isi'][iklan_idx[i]+1]
			del item['isi'][iklan_idx[i]]

		# Menggabungkan seluruh bagian teks menjadi bagian yang utuh
		for idx in range(len(item['isi'])):
			item['isi'][idx] = item['isi'][idx].strip()
		item['isi'] = ' '.join(item['isi'])

		return item

# Okezone
class OkezonePipeline:
	def process_item(self, item, spider):
		if spider.name not in ['okezone']:
			return item

		# Judul
		# Menggabungkan seluruh bagian judul
		judul = ' '.join([kata.strip() for kata in item['judul']])

		# Kategori
		# Menggabungkan kategori dan sub kategori dengan '|'
		item['kategori'] = ' | '.join(item['kategori'])

		# Tanggal
		# Mengambil bagian tanggal saja
		item['tanggal'] = ' '.join(item['tanggal'].split(' ')[1:4]) 
		
		# Jumlah Komentar
		# Mengonversi menjadi angka
		item['jumlah_sk'] = int(item['jumlah_sk'])

		# Isi.
		# Menghilangkan iklan atau referensi ke artikel lain
		iklan_idx = [idx for (idx, val) in enumerate(item['isi']) if val.startswith('Baca juga')]
		for i in range(len(iklan_idx)-1, -1, -1):
			del item['isi'][iklan_idx[i]+1]
			del item['isi'][iklan_idx[i]]

		# Menggabungkan seluruh bagian teks menjadi bagian yang utuh
		for idx in range(len(item['isi'])):
			item['isi'][idx] = item['isi'][idx].strip()
		item['isi'] = ' '.join(item['isi'])
		
		return item

# Detik
class DetikPipeline:
	def process_item(self, item, spider):
		if spider.name not in ['detik']:
			return item

		# Judul
		# Menggabungkan seluruh kata pada judul
		judul = item['judul'].strip()

		# Mengecilkan seluruh tulisan
		item['judul'] = judul.lower()

		# Tanggal
		# Mengambil bagian tanggal saja
		item['tanggal'] = ' '.join(item['tanggal'].split(' ')[1:4])

		# Isi
		# Menggabungkan seluruh bagian teks menjadi utuh
		item['isi'] = ''.join([kata for kata in item['isi']])

		# Jumlah Komentar
		# Mengambil angka yang merupakan jumlah komentar
		item['jumlah_sk'] = int(item['jumlah_sk'].split(' ')[0])

		return item
