# Modul Flask
from flask import request, jsonify

# Modul Projek
from . import app
from .service import penugasan_spider, ekstraksi_hasil


# Testing Koneksi
@app.route('/')
def indeks():
	return "<h1>Flask sudah berjalan</h1>"

# API untuk menjalankan Spider
# Argumen : spider, kategori, tanggal, jumlah
@app.route('/api/crawl/berita', methods=['GET'])
def mulai_crawling_berita():
	
	# Jika ada argumen 'spider', lakukan penugasan dan kembalikan hasil scraping
	# Selainnya, kembalikan pesan untuk mengisi argumen
	if ('spider' in request.args):
		spider = request.args['spider']

		# Mengambil situs, tanggal, dan jumlah dari query
		kategori = "default" if ('kategori' not in request.args) else request.args['kategori']
		tanggal = "none" if ('tanggal' not in request.args) else request.args['tanggal']
		jumlah = 0 if ('jumlah' not in request.args) else request.args['jumlah']

		# Jalankan service
		pesan = penugasan_spider(spider, kategori, tanggal, jumlah)
		return jsonify(pesan)
	else:
		return jsonify({'status':'ditolak', 'message': 'membutuhkan argumen "spider" untuk menjalankan spider'})

# API untuk mengekstraksi hasil crawling oleh Spider
# Argumen : spider
@app.route('/api/hasil/berita', methods=['GET'])
def hasil_crawling_berita():

	# Jika ada argumen 'spider', lakukan penugasan dan kembalikan hasil scraping
	# Selainnya, kembalikan pesan untuk mengisi argumen
	if ('spider' in request.args):
		spider = request.args['spider']
		pesan, hasil = ekstraksi_hasil(spider)

		# Jika pesannya sudah selesai, kembalikan hasil
		# Selainnya, kembalikan pesan untuk mengisi argumen
		if (pesan == 'selesai'):
			return jsonify(hasil)
		else:
			return jsonify(pesan)
	else:
		return jsonify({'status':'ditolak', 'message': 'membutuhkan argumen untuk ekstraksi hasil spider'})