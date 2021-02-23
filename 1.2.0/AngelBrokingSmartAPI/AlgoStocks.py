from stockdata import stockdata as stock

class AlgoStocks:

	def __init__(self,symbol,stock,avg_candlesize,sma10):
		self.symbol=symbol
		self.stock=stock
		self.avg_candlesize=avg_candlesize
		self.sma10=sma10

