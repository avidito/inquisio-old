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
# Argumen : spider, tanggal, jumlah
@app.route('/api/crawl/repo', methods=['GET'])
def mulai_crawling_repo():

	# Jika ada argumen 'spider', lakukan penugasan dan kembalikan hasil scraping
	# Selainnya, kembalikan pesan untuk mengisi argumen
	if ('spider' in request.args):
		spider = request.args['spider']

		# Mengambil tahun dan jumlah dari query
		tahun = "none" if ('tahun' not in request.args) else request.args['tahun']
		jumlah = 0 if ('jumlah' not in request.args) else request.args['jumlah']

		# Jalankan service
		pesan = penugasan_spider(spider, tahun, jumlah)
		return jsonify(pesan)

	else:
		return jsonify({'status': 'ditolak', 'message': 'membutuhkan argumen "spider" untuk menjalankan spider'})

# API untuk mendapatkan hasil
# Argumen : spider
@app.route('/api/hasil/repo', methods=['GET'])
def hasil_crawling_repo():
	
	# Jika ada argumen 'spider', lakukan penugasan dan kembalikan hasil scraping
	# Selainnya, kembalikan pesan untuk mengisi argumen
	if ('spider' in request.args):
		spider = request.args['spider']
		pesan, hasil = ekstraksi_hasil(spider)

		# Jika pesannya sudah selesai, kembalikan hasil
		# Selainnya, kembalikan pesan untuk mengisi argumen
		if(pesan == 'selesai'):
			return jsonify(hasil)
		else:
			return jsonify(pesan)
	else:
		return jsonify({'status': 'ditolak', 'message': 'membutuhkan argumen "spider" untuk menjalankan spider'})






