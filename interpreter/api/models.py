from api import db


class Catatan(db.Model):
	_id = db.Column(db.Integer, primary_key=True)
	tugas_id = db.Column(db.String, nullable=False)
	tanggal = db.Column(db.DateTime, nullable=False)
	spider = db.Column(db.String, nullable=False)
	status = db.Column(db.String, nullable=False)
	pesan = db.Column(db.String)

	def __repr__(self):
		return "Catatan({tid}, {s}, {p})".format(tid=self.tugas_id, s=self.status, p=self.pesan)