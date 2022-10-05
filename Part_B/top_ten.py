from mrjob.job import MRJob

from mrjob.step import MRStep

class TOPTEN(MRJob):
	def mapper1(self, _, line):
		fields = line.split(',')
		try:
			if len(fields) == 7:
				address = fields[2]
				value = int(fields[3])
				yield address, (1,value)
			elif len(fields) == 5:
				address1 = fields[0]
				yield address1, (2,1)
		except:
			pass
	def reducer1(self, key, values):
		f = False
		allvalues = []
		for i in values:
			if i[0]==1:
				allvalues.append(i[1])
			elif i[0] == 2:
				f = True
		if f:
			yield key, sum(allvalues)

	def mapper2(self, key,value):
		yield None, (key,value)

	def reducer2(self, _, keys):
		sortedvalues = sorted(keys, reverse = True, key = lambda x: x[1])
		for i in sortedvalues[:10]:
			yield i[0], i[1]

	def steps(self):
		return [MRStep(mapper = self.mapper1, reducer=self.reducer1), MRStep(mapper = self.mapper2, reducer = self.reducer2)]

if __name__ == '__main__':
	TOPTEN.run()
