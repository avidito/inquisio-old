import json, requests
from datetime import datetime

from api import db
from api.models import Catatan


SPIDER_ENDPOINT = "http://localhost:5000/api/post/"
ME_ENDPOINT = "http://localhost:5000/api/get"

spiders = json.load(open("api/map.json"))
list_spider = []

counter = 0
spider_counts = 0

result_data = []
current_id = -1



def order_process(perintah_id, kategori, tanggal, jumlah):

	global SPIDER_ENDPOINT
	global spider_counts
	global list_spider
	global current_id

	current_id = perintah_id

	for spider in spiders:
		if spiders[spider]["kategori"].get(kategori):
			spider_counts += 1
			order_url = SPIDER_ENDPOINT + spiders[spider]["spider"]
			order_data = {
				"kategori": spiders[spider]["kategori"][kategori],
				"tanggal": datetime.strptime(tanggal, "%d%m%Y").strftime(spiders[spider]["tanggal"]),
				"jumlah": jumlah
			}

			request_data = requests.post(url=order_url, json=order_data)
			result = request_data.json()

			if result["status"] == "ditolak":
				spider_counts -= 1

			data = Catatan(
				perintah_id = perintah_id,
				waktu = datetime.now(),
				spider = spiders[spider]["spider"],
				status = result["status"],
				pesan = result["pesan"]
			)

			db.session.add(data)
			db.session.commit()

			list_spider.append(spider)

	return list_spider


def receiver_process(spider, data):

	global counter
	global spider_counts
	global result_data
	global current_id

	result_data.extend(data)
	counter += 1

	data = Catatan(
		perintah_id = current_id,
		waktu = datetime.now(),
		spider = spider,
		status = "selesai",
		pesan = "{} spider telah selesai".format(spider)
	)

	db.session.add(data)
	db.session.commit()

	if counter == spider_counts:
		receiver_data = {
			"perintah_id": current_id,
			"data": result_data
		}

		request_data = requests.post(url=ME_ENDPOINT, json=receiver_data)
		result = request_data.json()

		result_data = []
		counter = 0
		spider_counts = 0
		current_id = -1
	
	return {
		"status": "diterima",
		"pesan": "data dari spider {} telah diterima".format(spider)
	}