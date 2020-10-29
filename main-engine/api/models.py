from api import db


# Tabel Status Manager
class Manager(db.Model):

	_id = db.Column(db.Integer, primary_key=True)

	nama = db.Column(db.String(20), nullable=False, unique=True)
	status = db.Column(db.String(10), nullable=False, default="idle")

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
	status = db.Column(db.String(10), nullable=False)
	praproses = db.Column(db.String(10), default='-')

	hasil = db.relationship("Hasil", backref="tugas", lazy=True)

# Tabel Penyimpanan Data untuk Diproses
class Hasil(db.Model):

	_id = db.Column(db.Integer, primary_key=True)
	tugas_id = db.Column(db.Integer, db.ForeignKey("tugas._id"), nullable=False)
	
	spider = db.Column(db.String(20), nullable=False)
	data = db.Column(db.String(100), nullable=False)

