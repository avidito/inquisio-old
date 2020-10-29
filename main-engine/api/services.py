from datetime import datetime
from pytz import timezone

from api import db
from api.models import Tugas, Perintah

# Service Planning
# Service untuk membuat masukan menjadi data Tugas
def planning(kategori, tanggal, jumlah):
	dtime_tanggal = datetime.strptime(tanggal, "%d/%m/%Y")
	waktu_sekarang = datetime.now(timezone("Asia/Jakarta"))
	
	tugas = Tugas(
			kategori= kategori,
			tanggal= dtime_tanggal,
			jumlah= jumlah,
			waktu_diterima= waktu_sekarang
		)
	db.session.add(tugas)
	db.session.commit()

	perintah = Perintah(
			tugas_id = tugas._id,
			manager_id = 1,
		)
	db.session.add(perintah)
	db.session.commit()