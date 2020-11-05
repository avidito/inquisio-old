from api.process import PROCESSOR_LIST

# Kelas untuk Pengolahan Data
class Preprocessing:

	def __init__(self, preprocessing):
		self.pcls = []
		self.pstr = []

		processor = []
		for process in preprocessing:
			priority, proc = PROCESSOR_LIST[process["nama"]]
			parameter = process["parameter"]

			proc_cls = proc(**parameter)
			processor.append((priority, process["nama"], proc_cls))
		processor = sorted(processor)

		for process in processor:
			self.pstr.append(process[1])
			self.pcls.append(process[2])

	def __call__(self, data_list):
		processed = [res["isi"] for res in data_list].copy()
		for processor in self.pcls:
			result = []
			for data in processed:
				result.append(processor(data))
			processed = result.copy()

		for data, res in zip(data_list, processed):
			data["isi"] = res

		return data_list
