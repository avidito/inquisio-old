# Modul Flask
from flask import jsonify, request

# Modul Utilitas
from datetime import datetime
from pytz import timezone

# Modul Projek
from api import app, db
from api.models import Tugas, Manager
from api.services import planning, ordering


# Main Engine - Scheduler
# API untuk memasukan task dalam penjadwalan
# Argumen : kategori, tanggal, jumlah
@app.route("/api/schedule", methods=["POST"])
def scheduler():

	# Mendapatkan data
	kategori = request.json.get("kategori")
	tanggal = request.json.get("tanggal")
	jumlah =  request.json.get("jumlah")

	# Melakukan penjadwalan tugas
	planning(kategori, tanggal, jumlah)
	return jsonify({
			"status": "diterima",
			"pesan": "tugas berhasil diterima",
		})

# Main Engine - Observer (GET)
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

# Main Engine - Observer (PUT)
# API untuk merubah status pengerjaan 
# Argumen : tugas_id, manager_id
@app.route("/api/observe", methods=["PUT"])
def observer_put():

	# Mendapatkan data
	tugas_id = request.json.get("tugas_id")
	manager_id = request.json.get("manager_id")

	# Merubah status tugas dan manager
	change_status(tugas_id=tugas_id, manager_id=manager_id, status="diproses")

	# Melakukan penugasan dengan manager_id
	ordering(manager_id=manager_id)

	return jsonify({
			"status": "diterima",
			"status": "status tugas {} dan manager {} berhasil diubah menjadi 'diproses'".format(tugas_id, manager_id)
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


# Fungsi untuk Merubah Status
def change_status(**kwargs):
	
	# Mengambil data tugas dan status
	tugas_id = kwargs.get("tugas_id")
	tugas = Tugas.query.get(tugas_id)
	status = kwargs.get("status")

	# Jika status akan diubah menjadi "diproses", ubah informasi tugas dan manager
	# Jika status akan diubah menjadi "selesai", ubah informasi tugas saja
	# Memasukan timestamps sesuai kategori status
	waktu_sekarang = datetime.now(timezone("Asia/Jakarta"))
	if (status == "diproses"):
		tugas.waktu_diproses = waktu_sekarang

		# Mengubah status manager
		manager_id = kwargs.get("manager_id")
		manager = Manager.query.get(manager_id)
		manager.status = "siap"

	elif (status == "selesai"):
		tugas.waktu_selesai = waktu_sekarang

	# Merubah status tugas
	tugas.status = status
	db.session.commit()

####################### UTILITY #######################

from api.models import Hasil, Perintah
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