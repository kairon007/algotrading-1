import testdata as t
import datetime
import requests
import json
import time
from datetime import timedelta
from pprintpp import pprint as pp
import matplotlib.pyplot as plt 
import itertools

mycursor = t.mydb.cursor()
dates=[]
w_avg10=[]
Totalweight=[]
finalDate=[]
finalWeight_10=[]
finalWeight_05=[]
avg = 0
avg5=0
Totalweight_5=[]
sql_query = "select * from daily_ohlc where symbol = 'tcs' order by date1 asc"
mycursor.execute(sql_query)
records = mycursor.fetchall()
count = 1;
isListFull = False
w_avg5=[]
print("Total number of rows in Laptop is: ", mycursor.rowcount)
for row in records:
	#d1= datetime.datetime.strftime(row[1], '%d/%m')
	d1=row[1]
	d2= row[4]
	if(isListFull==False and count<10):
		dates.append(d1)
		Totalweight.append(d2)
		finalDate.append(d1)
		finalWeight_10.append(d2)
		w_avg10.append(d2)
		avg = avg+d2
		if(count<6):
			w_avg5.append(d2)
			Totalweight_5.append(d2)
			finalWeight_05.append(d2)
			avg5 = avg5+d2
		else:
			avg5 = avg5+d2-Totalweight_5[0]
			w_avg5.append(int(avg5/5))
			w_avg5.pop(0)
			Totalweight_5.pop(0)
			finalWeight_05.append(int(avg5/5))
			Totalweight_5.append(d2)
		count=count+1
	elif (isListFull == False and count==10):
		w_avg5.pop(0)
		avg5 = avg5+d2-Totalweight_5[0]
		w_avg5.append(int(avg5/5))
		finalWeight_05.append(int(avg5/5))
		Totalweight_5.pop(0)
		Totalweight_5.append(d2)
		avg = avg+d2
		dates.append(d1)
		Totalweight.append(d2)
		w_avg10.append(int(avg/10))
		isListFull =True
		finalDate.append(d1)
		finalWeight_10.append(int(avg/10))
	elif (isListFull == True):
		w_avg5.pop(0)
		avg5 = avg5+d2-Totalweight_5[0]
		w_avg5.append(int(avg5/5))
		finalWeight_05.append(int(avg5/5))
		Totalweight_5.pop(0)
		Totalweight_5.append(d2)
		dates.pop(0)
		avg = avg+d2-Totalweight[0]
		Totalweight.pop(0)
		w_avg10.pop(0)
		dates.append(d1)
		Totalweight.append(d2)
		w_avg10.append(int(avg/10))
		finalDate.append(d1)
		finalWeight_10.append(int(avg/10))

#print(finalWeight_05)
#print(finalWeight_10)
buyTrade = False
sellTrade=False
for (a,b,c) in zip(finalDate,finalWeight_05,finalWeight_10):
	if(buyTrade==False and b>c):
		print ("Buy stock -- "+ "5 Day SMA "+ str(b) + " crosses 10 Day SMA "+str(c) + "on " +str(a))
		buyTrade = True
		sellTrade=False
	elif(sellTrade == False and b<c):
		print("sell  Stock -- ""5 Day SMA "+ str(b) + " crosses 10 Day SMA "+str(c) + "on " +str(a))
		sellTrade=True
		buyTrade=False
		





# plt.plot(finalDate,finalWeight_10)
# plt.show()