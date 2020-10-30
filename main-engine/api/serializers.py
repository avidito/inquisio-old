# Modul Flask
from marshmallow import fields

# Modul Projek
from api import ma


# Serializer Manager
class ManagerSchema(ma.Schema):
	class Meta:
		ordered = True
		fields = ("_id", "nama", "status")

# Serializer Tugas
class TugasSchema(ma.Schema):
	class Meta:
		ordered = True
		fields = ("_id", "kategori", "tanggal", "jumlah", "praproses", "status")
	
	tanggal = fields.DateTime("%d/%m/%Y", datakey="tanggal")

# Serializer Perintah
class PerintahSchema(ma.Schema):
	class Meta:
		ordered = True
		fields = ("_id", "tugas_id", "manager_id", "ditugaskan")

# Serializer Hasil
class HasilSchema(ma.Schema):
	class Meta:
		ordered = True
		fields = ("_id", "tugas_id", "spider")
