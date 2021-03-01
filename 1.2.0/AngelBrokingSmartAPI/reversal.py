import testdata as t
import datetime
import json
import time
from AlgoStocks import AlgoStocks 
from datetime import timedelta
from pprintpp import pprint as pp
from tabulate import tabulate 

aStocksList=[]
tabularData=[("symbol","closingtime","open","close","high","low","bodysize","wicksize","bodypercentage","closepercentage","candlesize","candlecolor")]
record_l1={}
record_l2={}
record_cur={}
mycursor = t.mydb.cursor()
symQuery = "select distinct symbol from algo_symbols"
mycursor.execute(symQuery)
symbols = mycursor.fetchall()
for sym in symbols:
		
		sqlquery =  "select * from candle_data where symbol='"+str(sym[0])+"' order by closingtime desc LIMIT 51"
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
			#print("Symbol processed  : ",str(sym[0]))
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
				aStock = AlgoStocks(record_cur[0],record_cur,avg_candlesize,SMA_10)
				aStocksList.append(aStock)
				aStock=AlgoStocks(record_cur[0],record_l1,0,0)
				aStocksList.append(aStock)
				aStock=AlgoStocks(record_cur[0],record_l2,0,0)
				aStocksList.append(aStock)
				break;
			

#wick reversal
# if(record_cur[7]>=2.5*record_cur[6]):
# 	if(record_cur[9]<=0.35):
# 		signal1="buy"
# 	if(record_cur[9]>=0.65):
# 		signal1="sell"


# #extreme reversal
# if(record_l1[10]>=2*avg_candlesize and record_l1[8]>0.5 and record_l1[8]<0.85):
# 	if(record_l1[11]!=record_cur[11]):
# 		if(record_cur[11]=='G'):
# 			signal2="buy"
# 		else:
# 			signal2="sell"



#print(tabulate(tabularData,headers="firstrow"))


process_sym=""
cur_candle=[]
prev_candle=[]
l2_candle=[]
process_avg_candlesize=0
process_sma10=0
sym_count=0
tabularData=[("symbol","closingtime","open","close","high","low","bodysize","wicksize","bodypercentage","closepercentage","candlesize","candlecolor")]
tabularData2=[("symbol","SMA10","Wick_reversal_signal","Extream_reversal_signal")]
for stock in aStocksList:
	
	#tabularData.append(stock.stock)
	
	signal1=" "
	signal2=" "
	if(process_sym=="" or sym_count==0):
		process_sym=stock.symbol
		cur_candle=stock.stock
		process_avg_candlesize=stock.avg_candlesize
		process_sma10=stock.sma10
		sym_count=sym_count+1
	elif(process_sym==stock.symbol and sym_count==1):
		prev_candle=stock.stock
		sym_count=sym_count+1
	elif(process_sym==stock.symbol and sym_count==2):
		l2_candle=stock.stock
		
		#wick reversal
		if(cur_candle[7]>=2.5*cur_candle[6]):
			if(cur_candle[9]<=0.35):
				signal1="buy"
			if(cur_candle[9]>=0.65):
				signal1="sell"

		#extreme reversal
		if(prev_candle[10]>=2*process_avg_candlesize and prev_candle[8]>0.5 and prev_candle[8]<0.85):
			if(prev_candle[11]!=cur_candle[11]):
				if(cur_candle[11]=='G'):
					signal2="buy"
				else:
					signal2="sell"
		sym_count=0

		if(signal1!=" " or signal2!=" "):
			# tempTabular=cur_candle
			# tabularData.append(tempTabular)
			# print(tabulate(tabularData,headers="firstrow"))
			tempTabular = [process_sym,process_sma10,signal1,signal2]
			tabularData2.append(tempTabular)
			# print("SMA10  : ",process_sma10)
			# print("Avergae Candlesize : ", process_avg_candlesize)
			# print("wick reversal signal = ",signal1)
			# print("extreme reversal signal = ",signal2)
print(tabulate(tabularData2,headers="firstrow"))
