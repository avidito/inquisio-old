from marshmallow import fields

from api import ma


class ManagerSchema(ma.Schema):
	class Meta:
		ordered = True
		fields = ("_id", "nama", "status")

class TugasSchema(ma.Schema):
	class Meta:
		ordered = True
		fields = ("_id", "kategori", "tanggal", "jumlah")
	
	tanggal = fields.DateTime("%d/%m/%Y", datakey="tanggal")

class HasilSchema(ma.Schema):
	class Meta:
		ordered = True
		fields = ("_id", "tugas_id", "spider")