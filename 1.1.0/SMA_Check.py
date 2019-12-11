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
count1 = 50
count2=100
tabularData=[("symbol","Success","Failures","Success Ratio","OpenTrade","Rec. Date","Price")]
mycursor = t.mydb.cursor()
sym_query = "select distinct symbol from daily_ohlc"
mycursor.execute(sym_query)
records_sym = mycursor.fetchall()
print("Crossover of ",count1," SMA and ",count2," SMA \n\n")
for symbol in records_sym:
		mycursor.execute("select * from daily_ohlc where symbol = '"+str(symbol[0])+"' order by date1 asc")
		records= mycursor.fetchall()
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
		count = 1
		isListFull = False
		w_avg5=[]
		#print("Total number of rows for "+str(symbol[0])+" : "+ mycursor.rowcount)
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
		tempDate = ''

		for (a,b,c,d) in zip(finalDate,finalWeight_05,finalWeight_10,price):
			if(buyTrade==False and b>c):
				#print ("Buy stock -- "+str(count1)+ " Day SMA "+ str(b) + " crosses "+str(count2)+" Day SMA "+str(c) + "on " +str(a))
				buyPrice = d
				buyTrade = True
				sellTrade=False
				tempDate =a
			elif(buyTrade==True and sellTrade == False and b<c):
				#print("sell  Stock -- "+str(count2)+" Day SMA "+ str(b) + " crosses "+str(count1)+" Day SMA "+str(c) + "on " +str(a))
				sellPrice = d
				if(buyPrice<=sellPrice):
					result='Success'
					success_trade = success_trade+1
				else:
					result='Fail'
					failed_trade = failed_trade+1
				tradeCount = tradeCount+1
				#tabularData.append([str(a),buyPrice,sellPrice,(sellPrice-buyPrice),result])
				sellTrade=True
				buyTrade=False
		# if(buyTrade==True):
		# 	tabularData.append([str(tempDate),buyPrice,"","",""])
		if(tradeCount==0):
			success_ratio = "NA"
		else:
			success_ratio = round((success_trade*100/tradeCount),2)
		if(buyTrade==True):
			tabularData.append([symbol[0],str(success_trade),str(failed_trade),str(success_ratio)+" %","Buy",str(datetime.datetime.strftime(tempDate, '%d/%m/%y')),str(buyPrice)])
		else:
			tabularData.append([symbol[0],str(success_trade),str(failed_trade),str(success_ratio)+" %","No","",""])

print(tabulate(tabularData,headers="firstrow"))
# print("Total Successful Trades :" + str(success_trade))
# print("Total Failed Trades :" + str(failed_trade))
# print("Success Ratio : "+str(success_trade*100/tradeCount)+" %")
# plt.plot(finalWeight_10[-50:],finalWeight_05[-50:])
# plt.show()

# df = pd.DataFrame.from_dict(tabularData)
# df.to_excel('test.xlsx', header=True, index=False)