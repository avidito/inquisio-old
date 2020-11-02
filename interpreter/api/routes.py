from flask import jsonify

from api import app, db



@app.route("/api/order", methods=["POST"])
def api_order():
	return jsonify ({
			"status": "OK",
			"pesan": "ini interpreter manager"
		})


@app.route("/api/log", methods=["GET"])
def api_log():
	return jsonify ([
			{
				"_id": 1,
				"perintah_id": 1,
				"waktu": "02/11/2020 16:40",
				"spider": "kompas",
				"status": "mulai",
				"pesan": "kompas spider mulai mengerjakan",
			},
			{
				"_id": 2,
				"perintah_id": 1,
				"waktu": "02/11/2020 17:00",
				"spider": "kompas",
				"status": "selesai",
				"pesan": "kompas spider selesai mengerjakan",
			},
		])


@app.route("/api/receiver", methods=["POST"])
def api_receiver():
	return jsonify ({
			"status": "OK",
			"pesan": "ini interpreter receiver"
		})