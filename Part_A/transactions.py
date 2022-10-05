from mrjob.job import MRJob
import re
import time
import statistics

class transactions(MRJob):
	
	def mapper(self, _,line):
		fields = line.split(',')
		try:
			if len(fields) == 7:
				timef = int(fields[6])
				months = time.strftime("%m", time.gmtime(timef))
				year = time.strftime("%y", time.gmtime(timef))
				yield ((months,year), 1)
		except:
			pass

	def reducer(self, word, counts):
		yield(word,sum(counts))

if __name__ == '__main__':
	transactions.run()
