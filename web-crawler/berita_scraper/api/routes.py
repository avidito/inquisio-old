# Modul Flask
from flask import request, jsonify

# Modul Projek
from . import app
from .service import penugasan_spider, ekstraksi_hasil


# Testing Koneksi
@app.route("/")
def indeks():
	return "<h1>Flask sudah berjalan</h1>"


# API untuk menjalankan Spider
# Argumen : spider, kategori, tanggal, jumlah
@app.route("/api/crawl/berita", methods=["POST"])
def mulai_crawling_berita():
	
	# Jika ada argumen "spider", lakukan penugasan dan kembalikan hasil scraping
	# Selainnya, kembalikan pesan untuk mengisi argumen
	if ("spider" in request.json):
		spider = request.json["spider"]

		# Mengambil situs, tanggal, dan jumlah dari query
		kategori = "default" if ("kategori" not in request.json) else request.json["kategori"]
		tanggal = "none" if ("tanggal" not in request.json) else request.json["tanggal"]
		jumlah = 0 if ("jumlah" not in request.json) else request.json["jumlah"]

		# Jalankan service
		pesan = penugasan_spider(spider, kategori, tanggal, jumlah)
		return jsonify(pesan)

	else:
		return jsonify({
				"status": "ditolak",
				"message": "'spider' belum dispesifikasikan",
			})

# API untuk mengekstraksi hasil crawling oleh Spider
# Argumen : spider
@app.route("/api/hasil/berita", methods=["GET"])
@app.route("/api/hasil/berita/<spider>", methods=["GET"])
def hasil_crawling_berita(spider=None):

	# Jika ada argumen "spider", ekstraksi hasil scraping (jika sudah ada)
	# Selainnya, kembalikan pesan untuk mengisi argumen
	if (spider is not None):
		hasil = ekstraksi_hasil(spider)
		return jsonify(hasil)
	else:
		return jsonify({
				"status": "ditolak",
				"message": "'spider' belum dispesifikasikan",
			})