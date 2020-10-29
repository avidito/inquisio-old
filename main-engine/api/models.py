from datetime import datetime

from api import db


# Tabel Status Manager
class Manager(db.Model):

	_id = db.Column(db.Integer, primary_key=True)

	nama = db.Column(db.String(20), nullable=False, unique=True)
	status = db.Column(db.String(10), nullable=False, default="siap")

	def __repr__(self):
		return "Manager({})".format(self.nama)

# Tabel Pencatatan Tugas
class Tugas(db.Model):

	_id = db.Column(db.Integer, primary_key=True)

	kategori = db.Column(db.String(20), nullable=False)
	tanggal = db.Column(db.DateTime, nullable=False)
	jumlah = db.Column(db.Integer, nullable=False, default=10)
	waktu_diterima = db.Column(db.DateTime)
	waktu_dikerjakan = db.Column(db.DateTime)
	waktu_diproses = db.Column(db.DateTime)
	waktu_selesai = db.Column(db.DateTime)
	status = db.Column(db.String(10), nullable=False, default="menunggu")
	praproses = db.Column(db.String(10), default='-')

	hasil = db.relationship("Hasil", backref="tugas", lazy=True)

	def __repr__(self):
		tgl = self.tanggal.strftime("%d/%m/%Y")
		return "Tugas({}, {}, {}, {})".format(self._id, self.kategori, tgl, self.jumlah)

# Tabel Penyimpanan Data untuk Diproses
class Hasil(db.Model):

	_id = db.Column(db.Integer, primary_key=True)
	tugas_id = db.Column(db.Integer, db.ForeignKey("tugas._id"), nullable=False)
	
	spider = db.Column(db.String(20), nullable=False)
	data = db.Column(db.String(100), nullable=False)

	def __repr__(self):
		return "Hasil({}, tugas={}, {})".format(self._id, self.tugas_id, self.spider)

