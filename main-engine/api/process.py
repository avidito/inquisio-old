# Fungsi Utilitas
import re
import string

# Praproses penghapusan simbol
# Argumen : simbol
class HapusSimbol:

	def __init__(self, simbol=None):
		self.sstr = simbol if (simbol) else re.escape(string.punctuation)
		self.sreg = re.compile("[{}]".format(self.sstr))

	def __call__(self, data):
		result = re.sub(self.sreg, "", data)
		return result

# Praproses membagi data dengan simbol
# Argumen : simbol
class BagiDenganSimbol:

	def __init__(self, simbol="."):
		self.sstr = simbol
		self.sreg = re.compile("[{}]".format(self.sstr))

	def __call__(self, data):
		results = re.split(self.divr, data)
		clean_results = [r for r in results if (r.strip() != "")] 
		return clean_results

# Daftar Proses
PROCESSOR_LIST = {
	"Bagi dengan Simbol": (1, BagiDenganSimbol),
	"Hapus Simbol": (2, HapusSimbol),
}
