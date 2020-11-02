# Modul Utilitas
from datetime import datetime
from pytz import timezone
import requests

# Modul Projek
from api import db
from api.models import Tugas, Perintah, Manager, Hasil
from api.preprocessing import Preprocessing

# Endpoint Interpreter
MANAGER_ENDPOINT = "http://localhost:5050/api/order"
LOGGER_ENDPOINT = "http://localhost:5050/api/log"



# Service Planning
# Service untuk membuat masukan menjadi data Tugas
def planning(kategori, tanggal, jumlah, praproses):
	
	# Penyesuaian format data masukan 
	tanggal_dtime = datetime.strptime(tanggal, "%d/%m/%Y")
	waktu_sekarang = datetime.now(timezone("Asia/Jakarta"))
	
	# Membuat data Tugas
	tugas = Tugas(
			kategori = kategori,
			tanggal = tanggal_dtime,
			jumlah = jumlah,
			waktu_diterima = waktu_sekarang,
			praproses = praproses,
		)
	db.session.add(tugas)
	db.session.commit()

	# Membuat data Perintah
	perintah = Perintah(
			tugas_id = tugas._id,
			manager_id = 1,
			ditugaskan = False,
		)
	db.session.add(perintah)
	db.session.commit()

	# Penugasan Manager
	ordering(perintah_id=perintah._id)

# Service Ordering
# Service yang melakukan pengecekan kesiapan dan penugasan Manager
def ordering(perintah_id=None, manager_id=None):

	# Jika menggunakan perintah_id
	if (perintah_id):

		# Mendapatkan data Perintah dan Manager
		perintah = Perintah.query.get(perintah_id)
		manager = perintah.manager

		# Jika Manager sedang "bekerja", abaikan penugasan
		if (manager.status == "bekerja"):
			return

	# Jika menggunakan manager_id
	elif (manager_id):

		# Mendapatkan data Manager dan Perintah
		manager = Manager.query.get(manager_id)
		d_perintah = [p for p in manager.penugasan if not (p.ditugaskan)]

		# Mendapatkan Perintah pertama yang belum ditugaskan
		# Jika tidak ada data, abaikan penugasan
		if (len(d_perintah)):
			perintah = d_perintah[0]
		else:
			return

	# Melakukan request ke Interpreter - Manager
	tugas = perintah.tugas
	tanggal_str = tugas.tanggal.strftime("%d/%m/%Y")
	order = {
		"kategori": tugas.kategori,
		"tanggal": tanggal_str,
		"jumlah": tugas.jumlah, 
	}
	feedback = requests.post(url=MANAGER_ENDPOINT, json=order)

	# Mencatat Waktu dimulainya pekerjaan
	waktu_sekarang = datetime.now(timezone("Asia/Jakarta"))
	tugas.waktu_dikerjakan = waktu_sekarang

	# Merubah Status Manager, Tugas, dan Perintah
	manager.status = "bekerja"
	tugas.status = "dikerjakan"
	perintah.ditugaskan = True

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
	catatan = []
	for perintah in tugas.penugasan:
		perintah_id = perintah._id
		req = requests.get(url=LOGGER_ENDPOINT, params={"id": tugas_id})
		catatan.extend(req.json())

	# Menggabungkan informasi
	info = {
		"status": status,
		"waktu": waktu,
		"catatan": catatan,
	}
	return info

# Service Parsing
# Service untuk melakukan pengolahan data hasil scraping
def parsing(perintah_id, data):

	# Mendapatkan informasi parproses dari Perintah
	perintah = Perintah.query.get(perintah_id)
	praproses = perintah.tugas.praproses

	# Memulai praproses untuk pada data
	prep = Preprocessing(praproses)
	rdata = prep(data)

	# Menyimpan hasil yang telah diolah ke tabel Hasil
	hasil = Hasil(
			perintah_id = perintah_id,
			data = rdata,
		)
	db.session.add(hasil)
	db.session.commit()