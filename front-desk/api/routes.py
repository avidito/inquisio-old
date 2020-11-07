from flask import request, jsonify

from api import app
from api.services import pesan



@app.route("/api/task", methods=["POST"])
def task():
	tugas = request.json.get("tugas")
	parameter = request.json.get("parameter")

	if tugas: 
		if tugas == "pesan":
			result = pesan(parameter)
			return jsonify(result)

		else:
			return jsonify({
					"status": "ditolak",
					"pesan": "tugas tidak sesuai"
				})
	else:
		return jsonify({
				"status": "ditolak",
				"pesan": "tugas tidak boleh kosong"

			})