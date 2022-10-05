
from mrjob.job import MRJob
from mrjob.step import MRStep

class top_ten_miners(MRJob):
	def mapper1(self, _, line):
		fields = line.split(',')
		try:
			if len(fields) == 9:
				miner = fields[2]
				size = fields[4]
				yield (miner, int(size))

		except:
			pass

	def reducer1(self, miner, size):
		try:
			yield(miner, sum(size))

		except:
			pass


	def mapper2(self, miner, totalsize):
		try:
			yield(None, (miner,totalsize))
		except:
			pass

	def reducer2(self, _, msize):
		j = 0
		try:
			sortsize = sorted(msize, reverse = True, key = lambda x:x[1])
			for i in sortsize[:10]:
				yield(i[0],i[1])
		except:
			pass
	

	def steps(self):
		return [MRStep(mapper = self.mapper1, reducer=self.reducer1), MRStep(mapper = self.mapper2, reducer = self.reducer2)]

if __name__ == '__main__':
	top_ten_miners.run()
