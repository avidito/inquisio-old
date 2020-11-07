from api import ma


class CatatanSchema(ma.Schema):
	class Meta:
		ordered = True
		fields = ("_id", "tugas_id", "waktu", "spider", "status", "pesan")