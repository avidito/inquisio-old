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
@app.route('/api/crawl/berita', methods=['GET'])
def mulai_crawling():
	
	# Jika ada argumen 'spider', lakukan penugasan dan kembalikan hasil scraping
	# Selainnya, kembalikan pesan untuk mengisi argumen
	if ('spider' in request.args):
		spider = request.args['spider']
		pesan = penugasan_spider(spider)
		return jsonify(pesan)
	else:
		return jsonify({'status':'ditolak', 'message': 'membutuhkan argumen untuk menjalankan spider'})

# API untuk mengekstraksi hasil crawling oleh Spider
@app.route('/api/hasil/berita', methods=['GET'])
def hasil_crawling():

	# Jika ada argumen 'spider', ekstraksi hasil scraping
	# Selainnya, kembalikan list kosong
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