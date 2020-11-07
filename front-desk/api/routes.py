from flask import request, jsonify

from api import app
from api.services import pesan, cek, result



@app.route("/api/task", methods=["POST"])
def task():
	tugas = request.json.get("tugas")
	parameter = request.json.get("parameter")

	if tugas: 
		if(tugas == "pesan"):
			feedback = pesan(parameter)
			return jsonify(feedback)

		elif(tugas == "cek"):
			feedback = cek(parameter)
			return jsonify(feedback)

		elif(tugas == "hasil"):
			feedback = result(parameter)
			return jsonify(feedback)

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