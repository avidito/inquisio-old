# Modul Flask
from flask import request, jsonify

# Modul Projek
from api import app
from api.services import crawling, extract_results


# API untuk membuat Spider memulai proses crawling
# Argumen : spider, kategori, tanggal, jumlah
@app.route("/api/spider", methods=["POST"])
def spider_worker():
	
	# Jika ada argumen "spider", lakukan penugasan
	# Selainnya, kembalikan pesan untuk mengisi argumen
	if ("spider" in request.json):
		spider = request.json["spider"]

		# Mengambil situs, tanggal, dan jumlah dari query
		kategori = request.json.get("kategori")
		tanggal = request.json.get("tanggal")
		jumlah = request.json.get("jumlah")

		# Jalankan service
		message = crawling(spider, kategori, tanggal, jumlah)
		return jsonify(message)

	else:
		return jsonify({
				"status": "ditolak",
				"pesan": "'spider' tidak dispesifikasikan",
			})

# API untuk mengekstraksi hasil crawling oleh Spider
# Argumen : spider
@app.route("/api/hasil/berita", methods=["GET"])
@app.route("/api/hasil/berita/<spider>", methods=["GET"])
def hasil_crawling_berita(spider=None):

	# Jika ada argumen "spider", ekstraksi hasil scraping (jika sudah ada)
	# Selainnya, kembalikan pesan untuk mengisi argumen
	if (spider is not None):
		hasil = extract_results(spider)
		return jsonify(hasil)
	else:
		return jsonify({
				"status": "ditolak",
				"message": "'spider' tidak dispesifikan",
			})