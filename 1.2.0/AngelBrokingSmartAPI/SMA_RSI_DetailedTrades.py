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

mycursor = t.mydb.cursor()
sym_query = "select distinct symbol from bhavcopy"
mycursor.execute(sym_query)
records_sym = mycursor.fetchall()
rsi_periode=14
for symbol in records_sym:
	rs=0
	rsi=[]
	dates=[]
	w_avg10=[]
	Totalweight=[]
	finalDate=[]
	finalWeight_10=[]
	finalWeight_05=[]
	price=[]
	avg = 0
	avg5=0
	Totalweight_5=[]
	sql_query = "select * from bhavcopy where symbol = '"+str(symbol[0])+"'order by timestamp asc"
	mycursor.execute(sql_query)
	records_raw = mycursor.fetchall()
	records = records_raw
	count = 1
	count1 = 20
	count2=50
	isListFull = False
	w_avg5=[]
	gain=[]
	loss=[]
	avg_gain=0
	avg_loss=0
	previous_close=0
	for row in records:
		#d1= datetime.datetime.strftime(row[1], '%d/%m')
		d1=row[1]
		d2= row[3]
		close=row[3]
		if(previous_close!=0 and close>=previous_close):
			# Its a gain for he day. Calculate gain
			gain.append(round(close - previous_close))
			loss.append(0)
			avg_gain = avg_gain + close - previous_close
			previous_close=close
		elif (previous_close!=0 and close<previous_close):
			#Its a loss for the day. Calculate loss
			loss.append(round(previous_close - close))
			gain.append(0)
			avg_loss = avg_loss + previous_close - close
			previous_close=close
		else:
			#assign previous close as close
			previous_close=close
			gain.append(0)
			loss.append(0)
		if(count>=rsi_periode):
			rs= (avg_gain/rsi_periode)/(avg_loss/rsi_periode)
			rsi.append(round(100-(100/(1+rs))))
			avg_gain=avg_gain - gain[0]
			gain.pop(0)
			avg_loss = avg_loss - loss[0]
			loss.pop(0)
		else :
			temp=0
			rsi.append(temp)
		price.append(d2)
		if(isListFull==False and count<count2):
			dates.append(d1)
			Totalweight.append(d2)
			finalDate.append(d1)
			finalWeight_10.append(d2)
			w_avg10.append(d2)
			avg = avg+d2
			if(count<(count1+1)):
				w_avg5.append(d2)
				Totalweight_5.append(d2)
				finalWeight_05.append(d2)
				avg5 = avg5+d2
			else:
				avg5 = avg5+d2-Totalweight_5[0]
				w_avg5.append(int(avg5/count1))
				w_avg5.pop(0)
				Totalweight_5.pop(0)
				finalWeight_05.append(int(avg5/count1))
				Totalweight_5.append(d2)
			count=count+1
		elif (isListFull == False and count==count2):
			w_avg5.pop(0)
			avg5 = avg5+d2-Totalweight_5[0]
			w_avg5.append(int(avg5/count1))
			finalWeight_05.append(int(avg5/count1))
			Totalweight_5.pop(0)
			Totalweight_5.append(d2)
			avg = avg+d2
			dates.append(d1)
			Totalweight.append(d2)
			w_avg10.append(int(avg/count2))
			isListFull =True
			finalDate.append(d1)
			finalWeight_10.append(int(avg/count2))
		elif (isListFull == True):
			w_avg5.pop(0)
			avg5 = avg5+d2-Totalweight_5[0]
			w_avg5.append(int(avg5/count1))
			finalWeight_05.append(int(avg5/count1))
			Totalweight_5.pop(0)
			Totalweight_5.append(d2)
			dates.pop(0)
			avg = avg+d2-Totalweight[0]
			Totalweight.pop(0)
			w_avg10.pop(0)
			dates.append(d1)
			Totalweight.append(d2)
			w_avg10.append(int(avg/count2))
			finalDate.append(d1)
			finalWeight_10.append(int(avg/count2))

	#print(finalWeight_05)
	#print(finalWeight_10)
	buyTrade = False
	sellTrade=False
	buyPrice=0
	sellPrice=0
	result=''
	success_trade=0
	failed_trade=0
	tradeCount=0
	tabularData=[("Buy Date","Buy Price","RSI","SellPrice","Sell Date","Profit/Loss","Success/Fail")]
	buyDate = ''
	sellDate=''
	buyRSI=0
	smaCrossed = False
	for (a,b,c,d,e) in zip(finalDate,finalWeight_05,finalWeight_10,price,rsi):
		if(buyTrade==False and smaCrossed == False and b>c):
			#print ("Buy stock -- "+str(count1)+ " Day SMA "+ str(b) + " crosses "+str(count2)+" Day SMA "+str(c) + "on " +str(a))
			smaCrossed = True
			if(e > 0 and e <100):
				buyPrice = d
				buyTrade = True
				sellTrade=False
				buyDate =a
				buyRSI = e
		elif(b<c):
			smaCrossed = False
			if(buyTrade==True and sellTrade == False):
				#print("sell  Stock -- "+str(count2)+" Day SMA "+ str(b) + " crosses "+str(count1)+" Day SMA "+str(c) + "on " +str(a))
				sellDate =a
				sellPrice = d
				if(buyPrice<=sellPrice):
					result='Success'
					success_trade = success_trade+1
				else:
					result='Fail'
					failed_trade = failed_trade+1
				tradeCount = tradeCount+1
				tabularData.append([str(buyDate),buyPrice,buyRSI,sellPrice,str(sellDate),round((sellPrice-buyPrice)*100/buyPrice,2),result])
				buyRSI=0
				sellTrade=True
				buyTrade=False
	if(buyTrade==True):
		tabularData.append([str(buyDate),buyPrice,buyRSI,"","",""])
	if(tradeCount>0 and buyTrade==True):
		if((success_trade*100/tradeCount) >70):

			print('\n\nSymbol : ',symbol[0])
			print(tabulate(tabularData,headers="firstrow"))
			print("\n\nTotal Successful Trades :" + str(success_trade))
			print("Total Failed Trades :" + str(failed_trade))
			print("Success Ratio : ",round(success_trade*100/tradeCount),"%")
	# plt.plot(finalWeight_10[-50:],finalWeight_05[-50:])
	# plt.show()