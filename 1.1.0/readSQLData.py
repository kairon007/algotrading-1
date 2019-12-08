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
symbol = "CESC"
sql_query = "select * from daily_ohlc where symbol = '"+str(symbol)+"'order by date1 asc"
mycursor.execute(sql_query)
records_raw = mycursor.fetchall()
records = records_raw
count = 1
count1 = 100
count2=200
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

for (a,b,c,d) in zip(finalDate,finalWeight_05,finalWeight_10,price):
	if(buyTrade==False and b>c):
		#print ("Buy stock -- "+str(count1)+ " Day SMA "+ str(b) + " crosses "+str(count2)+" Day SMA "+str(c) + "on " +str(a))
		buyPrice = d
		buyTrade = True
		sellTrade=False
		buyDate =a
	elif(buyTrade==True and sellTrade == False and b<c):
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
		tabularData.append([str(buyDate),buyPrice,sellPrice,str(sellDate),round((sellPrice-buyPrice)*100/buyPrice,2),result])
		sellTrade=True
		buyTrade=False
if(buyTrade==True):
	tabularData.append([str(buyDate),buyPrice,"","",""])
print(tabulate(tabularData,headers="firstrow"))
print("\n\nTotal Successful Trades :" + str(success_trade))
print("Total Failed Trades :" + str(failed_trade))
print("Success Ratio : "+str(success_trade*100/tradeCount)+" %")
# plt.plot(finalWeight_10[-50:],finalWeight_05[-50:])
# plt.show()