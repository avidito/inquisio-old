# Modul Flask
from flask import jsonify, request

# Modul Utilitas
from datetime import datetime

# Modul Projek
from api import app
from api.services import planning


# Main Engine - Scheduler
# API untuk memasukan task dalam penjadwalan
# Argumen : kategori, tanggal, jumlah
@app.route("/api/schedule", methods=["POST"])
def scheduler():

	kategori = request.json.get("kategori")
	tanggal = request.json.get("tanggal")
	jumlah =  request.json.get("jumlah")

	planning(kategori, tanggal, jumlah)
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

####################### UTILITY #######################
from api import db
from api.models import Manager, Tugas, Hasil, Perintah
from api.serializers import ManagerSchema, TugasSchema, HasilSchema, PerintahSchema

dm_schema = ManagerSchema(many=True)
dt_schema = TugasSchema(many=True)
dp_schema = PerintahSchema(many=True)
dh_schema = HasilSchema(many=True)
utility = {
		"manager": (Manager, dm_schema),
		"tugas": (Tugas, dt_schema),
		"perintah" : (Perintah, dp_schema),
		"hasil": (Hasil, dh_schema),
	}


# Cek Tabel
@app.route("/api/cek", methods=["GET"])
def cek_tabel():
	nama = request.args.get("tabel")
	t, s = utility[nama]

	return s.jsonify(t.query.all())

# Reset Tabel
@app.route("/api/reset", methods=["DELETE"])
def reset_tabel():
	nama = request.args.get("tabel")
	t = utility[nama][0]
	
	if(nama == "manager"):
		daftar_manager = t.query.all()
		for manager in daftar_manager:
			manager.status = "siap"
	else:
		daftar = t.query.all()
		for data in daftar:
			db.session.delete(data)

	db.session.commit()
	return jsonify({
			"pesan": "tabel {} sudah di-reset".format(nama)
		})