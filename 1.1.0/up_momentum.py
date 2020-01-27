import testdata as t
import datetime
import requests
import json
import time
from datetime import timedelta
from pprintpp import pprint as pp
import matplotlib.pyplot as plt 
import itertools
from tabulate import tabulate 
import pandas as pd
import pytz
import os



mycursor = t.mydb.cursor()
sym_query = "select distinct symbol from intra_ohlc"
mycursor.execute(sym_query)
records_sym = mycursor.fetchall()

for symbol in records_sym:
	mycursor.execute("select * from intra_ohlc where symbol = '"+str(symbol[0])+"' order by date1 asc")
	records= mycursor.fetchall()
	today =''
	buy_trade=False
	buy_price=0.0
	sell_price=0.0
	profit=0.0
	profit_perc=0.0
	open_price=0.0
	success_trades=0
	failed_trades=0
	success_trades=0
	failed_trades=0
	volume_ma=0
	volume_ma_05=[]
	tabularData=[("Buy Date","Buy Price","SellPrice","Sell Date","Profit/Loss","Success/Fail","Volume","5 Day MA Volume")]
	print("Momentum trade data for :"+str(symbol[0]))
	for record in records:
		temp=datetime.datetime.strptime(record[1],'%Y-%m-%d %H:%M:%S')
		asiaTime=t.old_timezone.localize(temp).astimezone(t.new_timezone)
		volume_ma = record[6]
		if(len(volume_ma_05)<=5):
			volume_ma_05.append(volume_ma)
		else:
			total_volume = volume_ma_05[0]+volume_ma_05[1]+volume_ma_05[2]+volume_ma_05[3]+volume_ma
			volume_ma_05.append(int(total_volume/5))
			
		if(today=='' or today!=asiaTime.date()):
			''' 
			its a different day
			iitialize today
			initialize open price
			'''
			today=asiaTime.date()
			tradeCount=0
			open_price=record[2]
			buy_trade=False
			buy_price=0.0
			sell_price=0.0
			profit=0.0
			profit_perc=0.0
			buy_time=''
			#print("Open P;rice :"+str(record[2]))
		else:
			high_price=round(float(record[4]),2)
			low_price=round(float(record[5]),2)
			if(buy_trade == False and tradeCount ==0  and high_price >= (open_price+open_price*0.005) and volume_ma>=volume_ma_05[len(volume_ma_05)-1]):
				'''
				price breached 1% cut-off level
				buy price is 1% above open price
				buy trade initiated
				
				'''
				buy_trade=True
				buy_price = open_price+ round(open_price*0.01)
				tradeCount = tradeCount +1
				buy_time = asiaTime

			elif(buy_trade == False and tradeCount >0  and high_price >= (open_price+open_price*0.005) and high_price <= (open_price+open_price*0.0075) and volume_ma>=volume_ma_05[len(volume_ma_05)-1]):
				'''
				price breached 1% cut-off level again 
				buy price is 1% above open price
				buy trade initiated
				
				'''
				print("came for second trade on ",asiaTime," at open price : ",open_price)
				buy_trade=True
				buy_price = open_price + round((open_price*0.01),2)
				tradeCount = tradeCount +1
				buy_time = asiaTime

			
			elif(buy_trade==True and high_price >= (open_price+open_price*0.015)):

				'''
				Trade target is reached
				'''
				buy_trade = False
				sell_price = open_price + round((open_price*0.0175),2)
				profit = sell_price - buy_price
				profit_perc = round((profit*100/buy_price),2)
				success_trades = success_trades+1
				tabularData.append([str(buy_time),buy_price,sell_price,str(asiaTime),profit_perc,"Success",volume_ma,volume_ma_05[len(volume_ma_05)-1]])

			elif(buy_trade==True and low_price <= (open_price -open_price*0.005)):
				'''
				Trade stop loss is activated
				'''
				buy_trade = False
				sell_price = open_price - round((open_price*0.005),2)
				profit = sell_price - buy_price
				profit_perc = round((profit*100/buy_price),2)
				failed_trades = failed_trades+1
				tabularData.append([str(buy_time),buy_price,sell_price,str(asiaTime),profit_perc,"Failed",volume_ma,volume_ma_05[len(volume_ma_05)-1]])

			elif(buy_trade==True and str(asiaTime.time())=="15:15:00"):
				buy_trade = False
				sell_price = high_price
				profit = sell_price - buy_price
				profit_perc = round((profit*100/buy_price),2)
				if(profit<0):
					failed_trades = failed_trades+1
					tabularData.append([str(buy_time),buy_price,sell_price,str(asiaTime),profit_perc,"Failed",volume_ma,volume_ma_05[len(volume_ma_05)-1]])
				else:
					success_trades = success_trades+1
					tabularData.append([str(buy_time),buy_price,sell_price,str(asiaTime),profit_perc,"Success",volume_ma,volume_ma_05[len(volume_ma_05)-1]])

	print(tabulate(tabularData,headers="firstrow"))
	print("\n\nTotal Successful Trades :" + str(success_trades))
	print("Total Failed Trades :" + str(failed_trades))
	total_trades=success_trades+failed_trades
	if(total_trades==0):
		print("Success Ratio : NA")
	else:
		print("Success Ratio : ",round((success_trades*100/total_trades),2)," %")



