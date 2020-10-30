# Modul Utilitas
from datetime import datetime
from pytz import timezone

# Modul Projek
from api import db
from api.models import Tugas, Perintah


# Service Planning
# Service untuk membuat masukan menjadi data Tugas
def planning(kategori, tanggal, jumlah):
	
	# Penyesuaian format data masukan 
	dtime_tanggal = datetime.strptime(tanggal, "%d/%m/%Y")
	waktu_sekarang = datetime.now(timezone("Asia/Jakarta"))
	praproses = ["tanpaSimbol", "bagiDenganTitik"]
	
	# Membuat data Tugas
	tugas = Tugas(
			kategori = kategori,
			tanggal = dtime_tanggal,
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
		)
	db.session.add(perintah)
	db.session.commit()

	# Penugasan Manager
	ordering(perintah._id)

# Service Ordering
# Service yang melakukan pengecekan kesiapan dan penugasan Manager
def ordering(perintah_id):
	pass