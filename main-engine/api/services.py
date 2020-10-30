# Modul Utilitas
from datetime import datetime
from pytz import timezone
import requests

# Modul Projek
from api import db
from api.models import Tugas, Perintah, Manager

# Endpoint Interpreter
MANAGER_ENDPOINT = "http://localhost:5050/api/order"

# Service Planning
# Service untuk membuat masukan menjadi data Tugas
def planning(kategori, tanggal, jumlah):
	
	# Penyesuaian format data masukan 
	tanggal_dtime = datetime.strptime(tanggal, "%d/%m/%Y")
	waktu_sekarang = datetime.now(timezone("Asia/Jakarta"))
	praproses = ["tanpaSimbol", "bagiDenganTitik"]
	
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

# Service Ordering - Perintah
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
		d_perintah = manager.penugasan

		# Mendapatkan Perintah pertama yang belum ditugaskan
		# Jika tidak ada data, abaikan penugasan
		if (len(d_perintah)):
			perintah = [p for p in d_perintah if not (p.ditugaskan)][0]
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

