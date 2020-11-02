# Modul Flask
from flask import jsonify, request

# Modul Utilitas
import requests
from datetime import datetime
from pytz import timezone

# Modul Projek
from api import app, db
from api.models import Tugas, Manager, Perintah
from api.services import planning, ordering, parsing


# Main Engine - Scheduler
# API untuk memasukan task dalam penjadwalan
# Argumen : kategori, tanggal, jumlah
@app.route("/api/schedule", methods=["POST"])
def scheduler():

	# Mendapatkan argumen
	kategori = request.json.get("kategori")
	tanggal = request.json.get("tanggal")
	jumlah =  request.json.get("jumlah")
	praproses = [
		{
			"nama": "Hapus Simbol",
			"parameter": {
				"simbol" : "()"
			}
		}
	]

	# Melakukan penjadwalan tugas
	planning(kategori, tanggal, jumlah, praproses)
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

	# Mendapatkan argumen
	perintah_id = request.json.get("perintah_id")
	perintah = Perintah.query.get(perintah_id)
	tugas_id = perintah.tugas_id
	manager_id = perintah.manager_id

	# Merubah status tugas dan manager
	change_status(tugas_id=tugas_id, manager_id=manager_id, status="diproses")

	# Melakukan penugasan dengan manager_id
	ordering(manager_id=manager_id)

	return jsonify({
			"status": "diterima",
			"pesan": "status tugas {} dan manager {} berhasil diubah menjadi 'diproses'".format(tugas_id, manager_id)
		})

# Main Engine - Workshop
# API untuk mengolah data hasil scraping
# Argumen : perintah_id, data
@app.route("/api/workshop", methods=["POST"])
def workshop():

	# Mendapatkan argumen
	perintah_id = request.json.get("perintah_id")
	data = request.json.get("data")

	# PUT Request ke observer_put
	perintah = Perintah.query.get(perintah_id)
	feedback = requests.put(url="http://localhost:5100/api/observe", json={"perintah_id": perintah_id})

	# Parsing data masukan sesuai praproses yang diinginkan
	parsing(perintah_id, data)

	return jsonify({
			"status": "diterima",
			"pesan": "hasil berhasil diterima",
		})

####################### UTILITAS #######################

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

from api.models import Hasil
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

# Trigger workshop
@app.route("/api/trigger", methods=["GET"])
def trigger_ws():
	perintah_id = request.args.get("perintah_id")

	dummy = [
		{
			"judul": "berita satu",
			"tanggal": "20/10/2020",
			"tags": ["a", "b", "c"],
			"isi": "isinya ceritanya () panjang!"
		},
		{
			"judul": "berita dua",
			"tanggal": "20/10/2020",
			"tags": ["a", "b"],
			"isi": "isinya lebih. panjang lagi."
		}
	]

	jdata = {
		"perintah_id": perintah_id,
		"data" : dummy,
	}
	feedback = requests.post(url="http://localhost:5100/api/workshop", json=jdata)

	return jsonify({
			"status": "berhasil",
		})