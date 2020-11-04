# Modul Utilitas
from datetime import datetime
from pytz import timezone
import requests
from multiprocessing import Process

# Modul Projek
from api import db
from api.models import Tugas, Manager, Hasil
from api.preprocessing import Preprocessing

# Endpoint Interpreter
MANAGER_ENDPOINT = "http://localhost:5050/api/order"
LOGGER_ENDPOINT = "http://localhost:5050/api/log"


# Service Planning
# Service untuk membuat masukan menjadi data Tugas
def planning(manager_id, kategori, tanggal, jumlah, praproses):
	
	# Penyesuaian format data masukan 
	tanggal_dtime = datetime.strptime(tanggal, "%d/%m/%Y")
	waktu_sekarang = datetime.now(timezone("Asia/Jakarta"))
	
	# Membuat data Tugas
	tugas = Tugas(
			manager_id = manager_id,
			kategori = kategori,
			tanggal = tanggal_dtime,
			jumlah = jumlah,
			waktu_diterima = waktu_sekarang,
			praproses = praproses,
		)
	db.session.add(tugas)
	db.session.commit()

	# Penugasan ke Manager (Async)
	p = Process(target=ordering, args=(tugas._id, "planning"))
	p.start()

# Service Ordering
# Service yang melakukan pengecekan kesiapan dan penugasan Manager
def ordering(tugas_id, sender):

	# Mendapatkan data Tugas dan Manager
	tugas = Tugas.query.get(tugas_id)
	manager = tugas.manager

	# Jika pengirim dari "workshop", dapatkan tugas yang belum dikerjakan
	# dari dengan manager yang sama
	if(sender == "workshop"):
		tugas = Tugas.query.filter_by(manager_id=manager._id, status="menunggu").first()

	# Jika manager dalam status siap dan terdapat tugas, berikan penugasan
	# Selainnya abaikan penugasan
	if (manager.status == "siap" and tugas):
		tanggal_str = tugas.tanggal.strftime("%d/%m/%Y")
		order = {
			"tugas_id": tugas_id,
			"kategori": tugas.kategori,
			"tanggal": tanggal_str,
			"jumlah": tugas.jumlah,
		}

		# Mengirimkan tugas ke Manager
		feedback = requests.post(url=MANAGER_ENDPOINT, json=order)
	else:
		return

	# Mencatat Waktu dimulainya pekerjaan
	waktu_sekarang = datetime.now(timezone("Asia/Jakarta"))
	tugas.waktu_dikerjakan = waktu_sekarang

	# Merubah Status Manager, Tugas, dan Perintah
	manager.status = "bekerja"
	tugas.status = "dikerjakan"

	db.session.commit()

# Service Gather Info
# Service untuk mendapatkan informasi dan catatan dari tugas
def gather_info(tugas_id):

	# Mendapatkan objek tugas dan status
	tugas = Tugas.query.get_or_404(tugas_id)
	status = tugas.status

	# Mendapatkan informasi daftar waktu
	waktu = {
		"waktu_diterima": tugas.waktu_diterima,
		"waktu_dikerjakan": tugas.waktu_dikerjakan,
		"waktu_diproses": tugas.waktu_diproses,
		"waktu_selesai": tugas.waktu_selesai,
	}

	# Mendapatkan informasi daftar catatan dari interpreter
	req = requests.get(url=LOGGER_ENDPOINT, params={"tugas_id": tugas_id})
	catatan = req.json()

	# Menggabungkan informasi
	info = {
		"status": status,
		"waktu": waktu,
		"catatan": catatan,
	}
	return info

# Service Get Result
# Service untuk mendapatkan hasil web-scraping
def get_result(tugas_id):

	# Mengambil seluruh data berdasarkan tugas_id
	hasil = Hasil.query.filter_by(tugas_id=tugas_id).all()

	return hasil

# Fungsi untuk Merubah Status
def change_status(tugas_id, status):
	
	# Mengambil data Tugas dan merubah statusnya
	tugas = Tugas.query.get(tugas_id)
	tugas.status = status
	
	# Mencatat waktu perubahan sesu		ai status
	# Jika status sama dengan "diproses", ubah status manager juga
	waktu_sekarang = datetime.now(timezone("Asia/Jakarta"))
	if (status == "diproses"):
		tugas.waktu_diproses = waktu_sekarang
		
		manager = Manager.query.get(tugas.manager_id)
		manager.status = "siap"
	else:
		tugas.waktu_selesai = waktu_sekarang

	db.session.commit()

# Service Parsing
# Service untuk melakukan pengolahan data hasil scraping
def parsing(tugas_id, data):

	# Merubah status tugas menjadi diproses
	change_status(tugas_id, "diproses")

	# Mendapatkan informasi parproses dari Perintah
	praproses = Tugas.query.get(tugas_id).praproses

	# Memulai praproses untuk pada data
	preprocessor = Preprocessing(praproses)
	processed_data = preprocessor(data)

	# Menyimpan hasil yang telah diolah ke tabel Hasil
	hasil = Hasil(
			tugas_id = tugas_id,
			data = processed_data,
		)
	db.session.add(hasil)
	db.session.commit()

	# Merubah status tugas menjadi selesai
	change_status(tugas_id, "selesai")