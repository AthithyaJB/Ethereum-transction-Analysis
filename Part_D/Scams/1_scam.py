from mrjob.job import MRJob
from mrjob.step import MRStep
import json

class scams(MRJob):
	def mapper1(self, _, lines):
		try:
			fields = lines.split(",")
			if len(fields) == 7:
				address1 = fields[2]
				value = float(fields[3])
				yield address1, (value,0)
			
			else:
				line = json.loads(lines)
				keys = line["result"]

				for i in keys:
					record = line["result"][i]
					category = record["category"]
					addresses = record["addresses"]

					for j in addresses:
						yield j, (category,1)

		except:
			pass

	def reducer1(self, key, values):
		tvalue=0
		category=None

		for k in values:
			if k[1] == 0:
				tvalue = tvalue + k[0]
			else:
				category = k[0]
		if category is not None:
			yield category, tvalue

	def mapper2(self,key,value):
		yield(key,value)
	def reducer2(self, key, value):
		yield(key,sum(value))

	def steps(self):
		return [MRStep(mapper = self.mapper1, reducer=self.reducer1), MRStep(mapper = self.mapper2, reducer = self.reducer2)]

if __name__ == '__main__':
	scams.run()
