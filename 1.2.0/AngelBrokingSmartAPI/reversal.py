import testdata as t
import datetime
import json
import time
from datetime import timedelta
from pprintpp import pprint as pp
from tabulate import tabulate 

tabularData=[("symbol","closingtime","open","close","high","low","bodysize","wicksize","bodypercentage","closepercentage","candlesize","candlecolor")]
record_l1={}
record_l2={}
record_cur={}
mycursor = t.mydb.cursor()
sqlquery =  "select * from candle_data where symbol='SBIN' order by closingtime desc LIMIT 51"
mycursor.execute(sqlquery)
records = mycursor.fetchall()
record_count=0
SMA_10=0
total_candlesize=0
avg_candlesize=0
total_price=0
signal1=""
signal2=""
for record in records:
	if(record_count==0):
		record_cur=record
		tabularData.append(record)
	if(record_count==1):
		record_l1=record
		total_price=total_price + record[3]
		total_candlesize= total_candlesize + record[10]
		tabularData.append(record)
	if(record_count==2):
		record_l2=record
		total_price=total_price + record[3]
		total_candlesize= total_candlesize + record[10]
		tabularData.append(record)
	if(record_count >2 and record_count<11):
		total_price=total_price + record[3]
		total_candlesize= total_candlesize + record[10]
	if(record_count ==11):
		SMA_10=round((total_price/10),2)
		total_candlesize= total_candlesize + record[10]
	if(record_count >11):
		total_candlesize= total_candlesize + record[10]
	record_count=record_count+1
	if(record_count==51):
		avg_candlesize=round((total_candlesize/50),2)
		break;

#wick reversal
if(record_cur[7]>=2.5*record_cur[6]):
	if(record_cur[9]<=0.35):
		signal1="buy"
	if(record_cur[9]>=0.65):
		signal1="sell"


#extreme reversal
if(record_l1[10]>=2*avg_candlesize and record_l1[8]>0.5 and record_l1[8]<0.85):
	if(record_l1[11]!=record_cur[11]):
		if(record_cur[11]=='G'):
			signal2="buy"
		else:
			signal2="sell"



print(tabulate(tabularData,headers="firstrow"))
print("SMA10  : ",SMA_10)
print("Avergae Candlesize : ", avg_candlesize)
print("wick reversal signal = ",signal1);
print("extreme reversal signal = ",signal2);