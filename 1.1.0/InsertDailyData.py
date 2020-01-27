import testdata as t
import datetime
import requests
import time
from pprintpp import pprint as pp

mycursor = t.mydb.cursor()
API_URL = "https://www.alphavantage.co/query"
available_sym_query = "select distinct(symbol) from daily_ohlc"
mycursor.execute(available_sym_query)
symbols = mycursor.fetchall()
symbols=[('AVANTIFEED',)]
#print(symbols)
count = 1
for sym in symbols :
	items=[]
	keys=[]
	if count >5:
		time.sleep(80)
		count=1
	else:
		try:
			time.sleep(13)
			print ("Fetching data for  : ",sym[0])
			data = {"function": "TIME_SERIES_DAILY",
			        "symbol": sym[0]+'.NS',
			        "outputsize" : "full",
			        "datatype": "json", 
			        "apikey": "01LSAIRK0QTB0QMN" }	#Dipesh Key
			response = requests.get(API_URL, data)   
			print ("Response received for  : " + sym[0])
			items = response.json()['Time Series (Daily)'].items()
			keys = list(items)
		except Exception:
			print("Error while fetching data for ",sym[0])
			continue
		for key in keys:
			try:
				open_price = float(str(key[1]['1. open']))
				close_price = float(str(key[1]['4. close']))
				high_price = float(str(key[1]['2. high']))
				low_price = float(str(key[1]['3. low']))
				volume = int(str(key[1]['5. volume']))
				date1 = datetime.datetime.strptime(str(key[0]),'%Y-%m-%d')
				if(open_price>0 and close_price >0 and high_price>0 and low_price>0 and volume>0):
					val =(sym[0],date1,open_price,close_price,high_price,low_price,volume)
					sql ="INSERT INTO daily_ohlc (symbol,date1,open_price,close_price,high_price,low_price,volume)VALUES(%s,%s,%s,%s,%s,%s,%s)"
					mycursor.execute(sql,val)
					t.mydb.commit()				
			except Exception:
				continue
