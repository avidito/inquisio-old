from flask import request, jsonify

from api import app
from api.services import index_process


@app.route("/", methods=["GET"])
def index():
	data = request.args.get("data")
	result = index_process(data)
	return jsonify(result)