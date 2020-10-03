# Modul Flask
from flask import request, jsonify

# Modul Projek
from . import app
from .service import penugasan_spider


# Testing Koneksi
@app.route('/')
def indeks():
	return "<h1>Flask sudah berjalan</h1>"

# API untuk menjalankan Spider
@app.route('/api/berita')
def crawling_berita():
	
	# Jika ada argumen 'spider', lakukan penugasan dan kembalikan hasil scraping
	# Jika tidak, kembalikan list kosong
	if ('spider' in request.args):
		spider = request.args['spider']
		return jsonify(penugasan_spider(spider))
	else:
		return jsonify({'error': 'need all of parameters to be input'})