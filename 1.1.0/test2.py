import testdata as t
import datetime
import requests
import time
from pprintpp import pprint as pp

mycursor2 = t.mydb.cursor()
API_URL = "https://www.alphavantage.co/query"
available_sym_query = "select distinct(symbol) from intra_ohlc"
mycursor2.execute(available_sym_query)
symbols = mycursor2.fetchall()
count = 1
while(True):
	for sym in symbols :
		items=[]
		keys=[]
		if count >5:
			time.sleep(800)
			count=1
		else:
			try:
				time.sleep(15)
				interval = '15min'
				print ("Fetching data for  : " + sym[0])
				data = {"function": "TIME_SERIES_INTRADAY",
				        "symbol": sym[0]+'.NS',
				        "interval" : interval,
				        "datatype": "json", 
				        "apikey": "6TNKSICJONKW9TFG" }	#Sumukh Key
				response = requests.get(API_URL, data)
				dataLabel="Time Series ("+interval+")"
				print ("Response received for  : " + sym[0])
				items = response.json()[dataLabel].items()
				keys = list(items)
			except Exception as e:
				#print("Error while fetching data for "+sym[0])
				print("Error :" + str(e))
				continue
			for key in keys:
				try:
					open_price = float(str(key[1]['1. open']))
					close_price = float(str(key[1]['4. close']))
					high_price = float(str(key[1]['2. high']))
					low_price = float(str(key[1]['3. low']))
					volume = int(str(key[1]['5. volume']))
					date1 = datetime.datetime.strptime(str(key[0]),'%Y-%m-%d %H:%M:%S')
					val =(sym[0],date1,open_price,close_price,high_price,low_price,volume)
					sql ="INSERT INTO intra_ohlc (symbol,date1,open_price,close_price,high_price,low_price,volume)VALUES(%s,%s,%s,%s,%s,%s,%s)"
					mycursor2.execute(sql,val)
					t.mydb.commit()

				except Exception as e:
					#print("Error while inserting data :" + e)
					continue