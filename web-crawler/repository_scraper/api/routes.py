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
# Argumen : spider, tanggal, jumlah
@app.route("/api/crawl/repo", methods=["POST"])
def mulai_crawling_repo():

	# Jika ada argumen "spider", lakukan penugasan dan kembalikan hasil scraping
	# Selainnya, kembalikan pesan untuk mengisi argumen
	if ("spider" in request.json):
		spider = request.json["spider"]

		# Mengambil tahun dan jumlah dari query
		tahun = "none" if ("tahun" not in request.json) else request.json["tahun"]
		jumlah = 0 if ("jumlah" not in request.json) else request.json["jumlah"]

		# Jalankan service
		pesan = penugasan_spider(spider, tahun, jumlah)
		return jsonify(pesan)

	else:
		return jsonify({
				"status": "ditolak",
				"message": "'spider' belum dispesifikasikan",
			})

# API untuk mengekstraksi hasil crawling oleh Spider
# Argumen : spider
@app.route("/api/hasil/repo", methods=["GET"])
@app.route("/api/hasil/repo/<spider>", methods=["GET"])
def hasil_crawling_repo(spider=None):
	
	# Jika ada argumen "spider", lakukan penugasan dan kembalikan hasil scraping
	# Selainnya, kembalikan pesan untuk mengisi argumen
	if (spider is not None):
		hasil = ekstraksi_hasil(spider)

		# Jika ada argumen "spider", ekstraksi hasil scraping (jika sudah ada)
		# Selainnya, kembalikan pesan untuk mengisi argumen
		return jsonify(hasil)
	else:
		return jsonify({
				"status": "ditolak",
				"message": "'spider' belum dispesifikasikan",
			})






