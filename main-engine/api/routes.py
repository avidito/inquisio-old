# Modul Flask
from flask import jsonify, request

# Modul Utilitas
import requests
from datetime import datetime
from pytz import timezone

# Modul Projek
from api import app, db
from api.services import planning, ordering, parsing, change_status, gather_info


# Main Engine - Scheduler
# API untuk memasukan task dalam penjadwalan
# Argumen : kategori, tanggal, jumlah
@app.route("/api/schedule", methods=["POST"])
def scheduler():

	# Mendapatkan argumen
	manager_id = request.json.get("manager_id")
	kategori = request.json.get("kategori")
	tanggal = request.json.get("tanggal")
	jumlah =  request.json.get("jumlah")
	praproses = request.json.get("praproses")

	# Melakukan penjadwalan tugas
	planning(manager_id, kategori, tanggal, jumlah, praproses)

	return jsonify({
			"status": "diterima",
			"pesan": "tugas berhasil diterima",
		})

# Main Engine - Observer (GET)
# API untuk mendapatkan status pengerjaan 
# Argumen : tugas_id
@app.route("/api/observe", methods=["GET"])
def observer():
	tugas_id = request.args.get("tugas_id")
	info = gather_info(tugas_id)

	return jsonify(info)

# Main Engine - Workshop
# API untuk mengolah data hasil scraping
# Argumen : tugas_id, data
@app.route("/api/workshop", methods=["POST"])
def workshop():

	# Mendapatkan argumen
	tugas_id = request.json.get("tugas_id")
	data = request.json.get("data")

	# Merubah status tugas dan manager
	# change_status(tugas_id, "diproses")

	# Melakukan penugasan dengan manager_id
	# ordering(tugas_id, "workshop")

	# PUT Request ke observer_put
	# feedback = requests.put(url="http://localhost:5100/api/observe", json={"tugas_id": tugas_id})

	# Parsing data masukan sesuai praproses yang diinginkan
	parsing(tugas_id, data)

	return jsonify({
			"status": "diterima",
			"pesan": "hasil berhasil diterima",
		})


####################### UTILITY #######################

from api.models import Manager, Tugas, Hasil
from api.serializers import ManagerSchema, TugasSchema, HasilSchema

dm_schema = ManagerSchema(many=True)
dt_schema = TugasSchema(many=True)
dh_schema = HasilSchema(many=True)
utility = {
		"manager": (Manager, dm_schema),
		"tugas": (Tugas, dt_schema),
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