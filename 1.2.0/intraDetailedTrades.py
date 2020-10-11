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
import pytz

mycursor = t.mydb.cursor()
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
symbol = "BAJFINANCE"
sql_query = "select * from intra_ohlc where symbol = '"+str(symbol)+"'order by date1 asc"
mycursor.execute(sql_query)
records_raw = mycursor.fetchall()
records = records_raw
count = 1
count1 = 5
count2=10
isListFull = False
w_avg5=[]
print("Crossover of ",count1," SMA and ",count2," SMA for ",symbol +"\n\n")
for row in records:
	#d1= datetime.datetime.strftime(row[1], '%d/%m')
	d1=row[1]
	d2= row[4]
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
tabularData=[("Buy Date","Buy Price","SellPrice","Sell Date","Profit/Loss","Success/Fail")]
buyDate = ''
sellDate=''
daychanged=False
currentDate=''
loopCount=0
old_timezone= pytz.timezone('US/Eastern')
new_timezone=pytz.timezone('Asia/Kolkata')
for (a,b,c,d) in zip(finalDate,finalWeight_05,finalWeight_10,price):
		convertedDate=datetime.datetime.strptime(a,'%Y-%m-%d %H:%M:%S')
		asiaTime=old_timezone.localize(convertedDate).astimezone(new_timezone)
		#print("Asia Time :" , asiaTime.time())
		if(loopCount==0 or currentDate==asiaTime.date()):
			daychanged=False
		else:
			daychanged=True
		if(daychanged==False):
			loopCount = loopCount+1
			currentDate=asiaTime.date()
			#print(currentDate)

			if(buyTrade==False and b>c):
				print ("Buy stock -- "+str(count1)+ " Day SMA "+ str(b) + " crosses "+str(count2)+" Day SMA "+str(c) + "on " +str(asiaTime))
				buyPrice = d
				buyTrade = True
				sellTrade=False
				buyDate =asiaTime
			# elif(buyTrade==True and str(asiaTime.time())=='15:15:00'):
			# 	print("sell  Stock -- "+str(count2)+" Day SMA "+ str(b) + " crosses "+str(count1)+" Day SMA "+str(c) + "on " +str(asiaTime))
			# 	sellDate =asiaTime
			# 	sellPrice = d
			# 	if(buyPrice<=sellPrice):
			# 		result='Success'
			# 		success_trade = success_trade+1
			# 	else:
			# 		result='Fail'
			# 		failed_trade = failed_trade+1
			# 	tradeCount = tradeCount+1
			# 	tabularData.append([str(buyDate),buyPrice,sellPrice,str(sellDate),round((sellPrice-buyPrice)*100/buyPrice,2),result])
			# 	sellTrade=True
			# 	buyTrade=False
			elif(buyTrade==True and sellTrade == False and b<c):
				print("sell  Stock -- "+str(count2)+" Day SMA "+ str(b) + " crosses "+str(count1)+" Day SMA "+str(c) + "on " +str(asiaTime))
				sellDate =asiaTime
				sellPrice = d
				if(buyPrice<=sellPrice):
					result='Success'
					success_trade = success_trade+1
				else:
					result='Fail'
					failed_trade = failed_trade+1
				tradeCount = tradeCount+1
				tabularData.append([str(buyDate),buyPrice,sellPrice,str(sellDate),round((sellPrice-buyPrice)*100/buyPrice,2),result])
				sellTrade=True
				buyTrade=False
		else:
				buyTrade = False
				sellTrade=False
				buyPrice=0
				sellPrice=0
				result=''
				tempDate=''
				loopCount = 0
# if(buyTrade==True):
# 	tabularData.append([str(buyDate),buyPrice,"","",""])
if(buyTrade==True):
	tabularData.append([str(buyDate),buyPrice,'','','',''])
print(tabulate(tabularData,headers="firstrow"))
print("\n\nTotal Successful Trades :" + str(success_trade))
print("Total Failed Trades :" + str(failed_trade))
print("Success Ratio : ",round((success_trade*100/tradeCount),2)," %")
# plt.plot(finalWeight_10[-50:],finalWeight_05[-50:])
# plt.show()