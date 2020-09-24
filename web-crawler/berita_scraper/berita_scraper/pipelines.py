# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

# Daftar Bulan
DAFTAR_BULAN = {
	'Januari':'01', 'Februari':'02', 'Maret':'03', 'April':'4', 'Mei':'5', 'Juni':'6', 'Juli':'7',
	'Agustus':'08', 'September':'09', 'Oktober':'10', 'November':'11', 'Desember':'12',
	}

class BeritaScraperPipeline:
    def process_item(self, item, spider):
        return item

# Kompas
class KompasPipeline:
	def process_item(self, item, spider):
		# Judul
		# Mengecilkan seluruh tulisan dan membersihkan spasi
		item['judul'] = item['judul'].lower().strip()

		# Kategori
		# Menggabungkan seluruh kategori dengan '|'
		daftar_kategori = [kategori.lower() for kategori in item['kategori']]
		item['kategori'] = ' | '.join(daftar_kategori)

		# Tanggal
		# Mengambil bagian tanggal saja
		item['tanggal'] = item['tanggal'].split(' - ')[1].split(',')[0] 
		
		# Jumlah Komentar
		# Mengambil bagian angka saja (berikan nilai 0 jika None)
		item['jumlah_sk'] = item['jumlah_sk'][1:-1] if (item['jumlah_sk'] is not None) else 0

		# Isi.
		# Mengecilkan seluruh potongan tulisan
		isi = [potongan.lower() for potongan in item['isi']]

		# Menghilangkan iklan atau referensi ke artikel lain
		iklan_idx = [idx for (idx, val) in enumerate(isi) if val.startswith('baca juga')]
		for i in range(len(iklan_idx)-1, -1, -1):
			del isi[iklan_idx[i]+1]
			del isi[iklan_idx[i]]

		# Menggabungkan seluruh bagian teks dan membersihkan spasi berlebih
		isi = ' '.join((' '.join(isi)).strip().split())

		# Menghapus publisher
		strip = isi.find('-')
		endash = isi.find(b'\xe2\x80\x93'.decode('utf-8'))
		if(strip == -1):
			pub = endash
		elif(endash != -1):
			pub = min(strip, endash)
		else:
			pub = strip
		item['isi'] = isi[pub+1:].lstrip()

		return item

# Okezone
class OkezonePipeline:
	def process_item(self, item, spider):
		# Judul
		# Menggabungkan seluruh bagian judul
		daftar_potongan = [potongan.lower().strip() for potongan in item['judul']]
		item['judul'] = ' '.join(daftar_potongan)

		# Kategori
		# Menggabungkan semua kategori dengan '|' dan menghapus '#'
		daftar_kategori = [kategori.lower().strip() for kategori in item['kategori']]
		item['kategori'] = ' | '.join(daftar_kategori).replace('#', '')

		# Tanggal
		# Mengambil bagian tanggal saja
		tanggal = item['tanggal'].split(' ')[1:4]

		# Konversi format tanggal menjadi angka
		bulan = DAFTAR_BULAN[tanggal[1]]
		item['tanggal'] = '{thn}/{bln}/{tgl}'.format(thn=tanggal[2], bln=bulan, tgl=tanggal[0])
		
		# Jumlah Komentar
		# Mengonversi menjadi angka
		item['jumlah_sk'] = int(item['jumlah_sk'])

		# Isi.
		# Menghilangkan penulis
		daftar_potongan = [potongan.lower().strip() for potongan in item['isi'][1:-1]]

		# Menghilangkan link "Baca Juga"
		iklan_idx = [idx for (idx, val) in enumerate(daftar_potongan) if ('baca juga' in val)]
		for i in range(len(iklan_idx)-1, -1, -1):
			while(len(daftar_potongan[iklan_idx[i]]) <= 13):
				del daftar_potongan[iklan_idx[i]]
			del daftar_potongan[iklan_idx[i]]
		
		# Menggabung seluruh potongan dan membersihkan spasi
		item['isi'] = ' '.join((' '.join(daftar_potongan)).split())

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
