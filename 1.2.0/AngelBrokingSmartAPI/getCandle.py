from smartapi import WebSocket
from smartapi import SmartConnect
import testdata as t
from datetime import datetime,timedelta
import os
from tabulate import tabulate 
import logging
import smartapi
import time

logging.basicConfig(filename='getCandle.log', filemode='w',
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
minute_intervals=[0,15,30,45]
while (True):
	nowTime = datetime.now()
	nowMinutes = int(nowTime.minute)
	pastTime=nowTime
	newTime=nowTime
	if(nowMinutes >= minute_intervals[0] and nowMinutes < minute_intervals[1]):
		newTime=nowTime.replace(minute=00)
	elif(nowMinutes >= minute_intervals[1] and nowMinutes < minute_intervals[2] ):
		newTime=nowTime.replace(minute=15)
	elif(nowMinutes >= minute_intervals[2] and nowMinutes < minute_intervals[3] ):
		newTime=nowTime.replace(minute=30)
	elif(nowMinutes >= minute_intervals[3]):
		newTime=nowTime.replace(minute=45)
	
	pastTime=newTime-timedelta(hours=0, minutes=15)
	strPast = str(pastTime.strftime("%Y-%m-%d %H:%M"))
	strNow = str(newTime.strftime("%Y-%m-%d %H:%M"))
	logging.debug(strPast)
	logging.debug(strNow)
	for symData in data:
		token = str(symData[1])
		sym=str(symData[0])
		historicParam={
		    "exchange": "NSE",
		    "symboltoken": token,
		    "interval": "FIFTEEN_MINUTE",
		    "fromdate": strPast,
		     "todate": strNow
		}
		values=obj.getCandleData(historicParam)
		logging.debug(values)
		priceData = str(values['data']).split('\n')[0]
		if(len(priceData)>0):
			rawCandleData = priceData.split(',')
			openPrice = rawCandleData[1]
			highPrice=rawCandleData[2]
			lowPrice=rawCandleData[3]
			closePrice=rawCandleData[4]
			rawDateString = rawCandleData[0]
			datePart=rawDateString.split('T')[0]
			timePart=rawDateString.split('T')[1].split('+')[0]
			dateString=str(datePart)+" "+str(timePart)
			try:
				sqlQuery = "insert into candle_data(symbol,closingtime,open,close,high,low)values(%s,%s,%s,%s,%s,%s)"
				values=(sym,dateString,openPrice,closePrice,highPrice,lowPrice)
				mycursor.execute(sqlQuery,values)
				t.mydb.commit()
				logging.debug("Inserted data for : "+sym+ " for "+ dateString)
			except:
				logging.debug("Error while inserting data for "+priceData)
			time.sleep(0.35)

	time.sleep(875)
