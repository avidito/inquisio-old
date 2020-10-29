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
	return jsonify ({
			"status": "OK",
			"pesan": "ini interpreter logger"
		})


@app.route("/api/receiver", methods=["POST"])
def api_receiver():
	return jsonify ({
			"status": "OK",
			"pesan": "ini interpreter receiver"
		})