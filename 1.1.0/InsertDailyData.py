import testdata as t
import datetime
import requests
import time
from pprintpp import pprint as pp

mycursor = t.mydb.cursor()
API_URL = "https://www.alphavantage.co/query"
symbols= t.stocks_to_scan
count = 1
for sym in symbols :
	items=[]
	keys=[]
	if count >5:
		time.sleep(80)
		count=1
	else:
		try:
			print ("Fetching data for  : " + sym)
			data = {"function": "TIME_SERIES_DAILY",
			        "symbol": sym+'.NS',
			        "outputsize" : "full",
			        "datatype": "json", 
			        "apikey": "01LSAIRK0QTB0QMN" }	#Dipesh Key
			response = requests.get(API_URL, data)   
			print ("Response received for  : " + sym)
			items = response.json()['Time Series (Daily)'].items()
			keys = list(items)
		except Exception:
			print("Error while fetching data for "+sym)
			continue
		for key in keys:
			try:
				open_price = float(str(key[1]['1. open']))
				close_price = float(str(key[1]['4. close']))
				high_price = float(str(key[1]['2. high']))
				low_price = float(str(key[1]['3. low']))
				volume = int(str(key[1]['5. volume']))
				date1 = datetime.datetime.strptime(str(key[0]),'%Y-%m-%d')
				val =(sym,date1,open_price,close_price,high_price,low_price,volume)
				sql ="INSERT INTO daily_ohlc (symbol,date1,open_price,close_price,high_price,low_price,volume)VALUES(%s,%s,%s,%s,%s,%s,%s)"
				mycursor.execute(sql,val)
				t.mydb.commit()				
			except Exception:
				continue