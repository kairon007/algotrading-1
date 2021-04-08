from smartapi import WebSocket
from smartapi import SmartConnect
import testdata as t
from datetime import datetime,timedelta
import os
from tabulate import tabulate 
import logging
import smartapi
import time

logging.basicConfig(filename='bhavcopy.log', filemode='w',
format='%(asctime)s,%(name)s - %(levelname)s - %(message)s',level=logging.DEBUG,datefmt='%Y-%m-%d %H:%M:%S')

obj=SmartConnect(api_key="JTy93cFP")
data = obj.generateSession("D43726","Vanisha@2019")
FEED_TOKEN=obj.getfeedToken() 
CLIENT_CODE="D43726"
cur_candle=[]
mycursor = t.mydb.cursor()
symQuery = "select symbol,token from algo_symbols"
mycursor.execute(symQuery)
data = mycursor.fetchall()
if (True):
	
	for symData in data:
		token = str(symData[1])
		sym=str(symData[0])
		historicParam={
		    "exchange": "NSE",
		    "symboltoken": token,
		    "interval": "ONE_DAY",
		    "fromdate": "2020-06-01 00:00",
		    "todate": "2021-04-08 23:00"
		}
		values=obj.getCandleData(historicParam)
		logging.debug(values)
		rawPrice=str(values['data'])
		if(rawPrice):
			prices = str(values['data']).split('\n')
			print("symbol :"+str(sym)+" Length : "+str(len(prices)))
			if(len(prices)>0):
				for priceData in prices:
					rawCandleData = priceData.split(',')
					openPrice = rawCandleData[1]
					highPrice=rawCandleData[2]
					lowPrice=rawCandleData[3]
					closePrice=rawCandleData[4]
					rawDateString = rawCandleData[0]
					datePart=rawDateString.split('T')[0]
					dateString=str(datePart)
					try:
						sqlQuery = "insert into bhavcopy(symbol,timestamp,open,close,high,low)values(%s,%s,%s,%s,%s,%s)"
						values=(sym,dateString,openPrice,closePrice,highPrice,lowPrice)
						mycursor.execute(sqlQuery,values)
						t.mydb.commit()
						logging.debug("Inserted data for : "+sym+ " for "+ dateString)
					except:
						logging.debug("Error while inserting data for "+priceData)
			time.sleep(0.35)


