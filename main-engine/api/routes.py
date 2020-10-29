from flask import jsonify, request

from api import app
from api.models import Manager, Tugas

# Main Engine - Scheduler
# API untuk memasukan task dalam penjadwalan
# Argumen : kategori, tanggal, jumlah
@app.route("/api/schedule", methods=["POST"])
def scheduler():
	return jsonify({
			"status": "diterima",
			"pesan": "tugas berhasil diterima",
		})

# Main Engine - Observer
# API untuk mendapatkan status pengerjaan 
# Argumen : _id
@app.route("/api/observe", methods=["GET"])
def observer():
	return jsonify({
			"id": 1,
			"status": "working",
			"waktu": {
				"diterima": "29-10-2020",
			},
			"catatan": {
				"status": "dikerjakan"
			}
		})

# Main Engine - Workshop
# API untuk mengolah data hasil scraping
# Argumen : tugas_id, data
@app.route("/api/workshop", methods=["POST"])
def workshop():
	return jsonify({
			"status": "diterima",
			"pesan": "hasil berhasil diterima",
		})