# Modul Flask
from flask import request, jsonify

# Modul Projek
from api import app
from api.service import crawling, extract_results


# API untuk membuat Spider memulai proses crawling
# Argumen : spider, category, date, total
@app.route("/api/crawl/berita", methods=["POST"])
def spider_worker():
	
	# Jika ada argumen "spider", lakukan penugasan
	# Selainnya, kembalikan pesan untuk mengisi argumen
	if ("spider" in request.json):
		spider = request.json["spider"]

		# Mengambil situs, tanggal, dan jumlah dari query
		category = request.json.get("category")
		date = request.json.get("date")
		total = request.json.get("total")

		# Jalankan service
		message = crawling(spider, category, date, total)
		return jsonify(message)

	else:
		return jsonify({
				"status": "denied",
				"message": "'spider' must be specified",
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
				"status": "denied",
				"message": "'spider' must be specified",
			})