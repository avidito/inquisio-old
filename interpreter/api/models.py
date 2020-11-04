from api import db


class Catatan(db.Model):
	_id = db.Column(db.Integer, primary_key=True)
	perintah_id = db.Column(db.Integer, nullable=False)
	waktu = db.Column(db.DateTime, nullable=False)
	spider = db.Column(db.String, nullable=False)
	status = db.Column(db.String, nullable=False)
	pesan = db.Column(db.String)

	def __repr__(self):
		return "Catatan({tid}, {s}, {p})".format(tid=self.perintah_id, s=self.status, p=self.pesan)