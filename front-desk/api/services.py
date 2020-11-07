import requests


SCHEDULER_ENDPOINT = "http://localhost:5100/api/schedule"
OBSERVER_ENDPOINT = "http://localhost:5100/api/observe"
RESULT_ENDPOINT = "http://localhost:5100/api/result"


def pesan(parameter):
	manager_id = parameter.get("manager_id")
	kategori = parameter.get("kategori")
	tanggal = parameter.get("tanggal")
	jumlah = parameter.get("jumlah")
	praproses = parameter.get("praproses")

	if manager_id and kategori and tanggal and jumlah and praproses:
		data = {
			"manager_id": manager_id,
			"kategori": kategori,
			"tanggal": tanggal,
			"jumlah": jumlah,
			"praproses": praproses
		}

		feedback = requests.post(url=SCHEDULER_ENDPOINT, json=data)
		result = feedback.json()
		
		return result

	else:
		return {
			"status": "ditolak",
			"pesan": "parameter tidak sesuai"
		}


def cek(parameter):
	tugas_id = parameter.get("tugas_id")

	feedback = requests.get(url=OBSERVER_ENDPOINT, params={"tugas_id": tugas_id})
	result = feedback.json()

	return result


def result(parameter):
	tugas_id = parameter.get("tugas_id")

	feedback = requests.get(url=RESULT_ENDPOINT, params={"tugas_id": tugas_id})
	result = feedback.json()

	return result