from flask import jsonify, request

from api import app
from api.models import Catatan
from api.serializer import CatatanSchema

from api.service import order_process, receiver_process


catatan_schema = CatatanSchema(many=True)


@app.route("/", methods=["GET"])
def index():
	return catatan_schema.jsonify(Catatan.query.all())


@app.route("/api/order", methods=["POST"])
def api_order():

	perintah_id = request.json.get("perintah_id")
	kategori = request.json.get("kategori")
	tanggal = request.json.get("tanggal")
	jumlah = request.json.get("jumlah")

	data = order_process(perintah_id, kategori, tanggal, jumlah)

	return jsonify ({
			"status": "diterima",
			"pesan": "perintah {} sedang dikerjakan".format(perintah_id)
		})


@app.route("/api/log", methods=["GET"])
def api_log():

	perintah_id = request.args.get("perintah_id")

	if perintah_id:
		data = Catatan.query.filter_by(perintah_id=perintah_id).all()
		return catatan_schema.jsonify(data)


@app.route("/api/receiver", methods=["POST"])
def api_receiver():

	spider = request.json.get("spider")
	data = request.json.get("data")

	result = receiver_process(spider, data)

	return jsonify (result)