from mrjob.job import MRJob
import re 
import time
import statistics
class average_transactions(MRJob):

	def mapper(self,_, line):
		fields = line.split(',')
		try:
			if len(fields)==7:
				timef = int(fields[6])
				gasp = int(fields[5])
				months = time.strftime("%m", time.gmtime(timef))
				years = time.strftime("%y", time.gmtime(timef))
				yield((months,years),(gasp,1))
		except:
			pass
	def reducer1(self, date, price):
		average = 0
		count = 0
		for p, b in price:
			average = (average*count+p*b)/(count + b)
			count = count +b
		return(date, (average,count))

	def combiner(self, date, price):
		yield self.reducer1(date,price)
	def reducer(self,date,price):     
		date, (average,count) = self.reducer1(date,price)
		yield(date,average)

if __name__ == '__main__':
	average_transactions.run()
