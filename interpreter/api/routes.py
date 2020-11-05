from flask import jsonify, request

from api import app
from api.models import Catatan
from api.serializer import CatatanSchema

from api.services import mapping, receiver_process


catatan_schema = CatatanSchema(many=True)


@app.route("/", methods=["GET"])
def index():
	return catatan_schema.jsonify(Catatan.query.all())


@app.route("/api/manager", methods=["POST"])
def manager():

	tugas_id = request.json.get("tugas_id")
	kategori = request.json.get("kategori")
	tanggal = request.json.get("tanggal")
	jumlah = request.json.get("jumlah")

	data = mapping(tugas_id, kategori, tanggal, jumlah)

	return jsonify ({
			"status": "diterima",
			"pesan": "perintah {} sedang dikerjakan".format(tugas_id)
		})


@app.route("/api/logger", methods=["GET"])
def logger():

	tugas_id = request.args.get("tugas_id")

	if tugas_id:
		data = Catatan.query.filter_by(tugas_id=tugas_id).all()
		return catatan_schema.jsonify(data)


@app.route("/api/receiver", methods=["POST"])
def receiver():

	spider = request.json.get("spider")
	data = request.json.get("data")

	result = receiver_process(spider, data)

	return jsonify (result)