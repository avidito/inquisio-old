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
		# Judul
		# Menghilangkan \r\n dan mengecilkan seluruh tulisan.
		item['judul'] = " ".join(item['judul'].strip().split()).lower()

		# Tahun
		# Mengambil bagian tahun saja.
		item['tahun'] = item['tahun'].split()[2]

		# Divisi
		# Merubah format dan membersihkan spasi pada tulisan.
		# Jika Fakultas Vokasi
		divisi = item['divisi'].lower()
		if(divisi.find("vokasi") != -1):
			# Hanya mengambil nama departemen dan prodi
			departemen, prodi = divisi.split(' > ')[1:]
			departemen = departemen[11:]
			prodi = prodi[3:]
			item['divisi'] = ' | '.join([departemen, prodi])
		
		# Selain Fakultas Vokasi
		else:
			# Hanya mengambil nama fakultas dan departemen
			divisi_split = divisi.split(' > ')
			fakultas = divisi_split[0][13:]

			# Jika departemen dispesifikan
			if(len(divisi_split) > 1):
				# Menghapus doktoral / magister
				departemen = divisi_split[1]
				if(departemen.find("doktoral") != -1 or departemen.find("magister") != -1):
					departemen = departemen[9:]
				item['divisi'] = ' | '.join([fakultas, departemen])

			# Jika hanya fakultas yang dispesifikan
			else:
				item['divisi'] = fakultas

		# Abstrak
		# Menghilangkan \r\n dan mengecilkan seluruh tulisan.
		item['abstrak'] = " ".join(item['abstrak'].strip().split()).lower()

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