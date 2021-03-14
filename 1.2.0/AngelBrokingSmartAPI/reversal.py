import testdata as t
import datetime
import json
import time
from AlgoStocks import AlgoStocks 
from datetime import timedelta
from pprintpp import pprint as pp
from tabulate import tabulate 
from camlevels import camlevels

aStocksList=[]
pivots={}
tabularData=[("symbol","closingtime","open","close","high","low","bodysize","wicksize","bodypercentage","closepercentage","candlesize","candlecolor")]
record_l1={}
record_l2={}
record_cur={}
mycursor = t.mydb.cursor()
symQuery = "select distinct symbol from candle_data"
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

		total_records = len(records)
		for record in records:
			#print("Symbol processed  : ",str(sym[0]))
			if(record_count==0):
				record_cur=record
				tabularData.append(record)
				pivotQuery="select * from pivots where symbol='"+str(sym[0])+"' and date(closingdate)=date(%s)"
				values=record[1]
				mycursor.execute(pivotQuery,(values,))
				temp_records = mycursor.fetchall()
				if(temp_records):
					for temp_record in temp_records:
						symbol1=temp_record[0]
						date1=temp_record[1]
						cpt_relationship=temp_record[2]
						bc=temp_record[3]
						pivot=temp_record[4]
						tc=temp_record[5]
						cpr_width=temp_record[6]
						l5=temp_record[7]
						l4=temp_record[8]
						l3=temp_record[9]
						l2=temp_record[10]
						l1=temp_record[11]
						h1=temp_record[12]
						h2=temp_record[13]
						h3=temp_record[14]
						h4=temp_record[15]
						h5=temp_record[16]
						temp_level=camlevels(symbol1,date1,cpt_relationship,bc,pivot,tc,cpr_width,l5,l4,l3,l2,l1,h1,h2,h3,h4,h5)
						pivots[str(sym[0])]=temp_level
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

			if(record_count==51 or record_count==total_records):
				avg_candlesize=round((total_candlesize/(record_count-1)),2)
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
tabularData2=[("symbol","Time","SMA10","Wick_reversal_signal","Extream_reversal_signal","H3 Reversal","L3 Reversal")]
for stock in aStocksList:
	
	#tabularData.append(stock.stock)
	
	signal1=" "
	signal2=" "
	signal3=" "
	signal4=" "
	h3Reversal=""
	l3Reversal=""
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
		
		cur_open = cur_candle[2]
		cur_close= cur_candle[3]
		cur_high=cur_candle[4]
		cur_low=cur_candle[5]
		closing_time=cur_candle[1]
		keys=pivots.keys()
		if(process_sym in keys):
			pivot_record= pivots[process_sym]
		else:
			pivot_record={}
		if(cur_close>cur_open):
			if( ( (cur_open-cur_low) >= 3.5* (cur_close-cur_open)) and (cur_candle[9]<=0.3) ):
				signal1="buy"
			if( (cur_candle[9]>=0.70) and ( (cur_high-cur_open) >= 3.5* (cur_close-cur_open)) ):
				signal1="sell"
		elif(cur_open>cur_close):
			if(  (cur_candle[9]>=0.70) and ( (cur_high-cur_open) >= 3.5* (cur_open-cur_close)) ):
				signal1="sell"
			if( ( (cur_open-cur_low) >= 3.5* (cur_close-cur_open)) and (cur_candle[9]<=0.3) ):
				signal1="buy"

		#wick reversal
		# if(cur_candle[7]>=2.5*cur_candle[6]):
		# 	if(cur_candle[9]<=0.35):
		# 		signal1="buy"
		# 	if(cur_candle[9]>=0.65):
		# 		signal1="sell"

		#extreme reversal
		if(prev_candle[10]>=2*process_avg_candlesize and prev_candle[8]>0.5 and prev_candle[8]<0.85):
			if(prev_candle[11]!=cur_candle[11]):
				if(cur_candle[11]=='G'):
					signal2="buy"
				else:
					signal2="sell"
		
		#Outside Reversal Setup
		if(cur_candle[5]<prev_candle[5] and cur_candle[3]>prev_candle[4] and cur_candle[10]>=process_avg_candlesize*1.20):
			signal3="buy"
		if(cur_candle[3]<prev_candle[5] and cur_candle[4]>prev_candle[4] and cur_candle[10]>=process_avg_candlesize*1.20):
			signal3="sell"

		#Doji Reversal Setup
		if(cur_candle[8]<=0.10):
			if(cur_candle[4]<=process_sma10):
				signal4="buy"
			if(cur_candle[5]>=process_sma10):
				signal4="sell"

		sym_count=0

		#H3 reversal
		if(pivot_record):
			if((cur_candle[4]>pivot_record.H3) and 
				(signal1=="sell" or signal2=="sell" or signal3=="sell" or signal4=="sell") and 
				(cur_candle[3]<pivot_record.H3)):
				h3Reversal = "sell"
			if((cur_candle[5]<pivot_record.L3) and 
				(signal1=="buy" or signal2=="buy" or signal3=="buy" or signal4=="buy") and 
				(cur_candle[3]>pivot_record.L3)):
				l3Reversal = "buy"	

		if(signal1!=" " or signal2!=" " or signal3!=" " or signal4!=" "):
			# tempTabular=cur_candle
			# tabularData.append(tempTabular)
			# print(tabulate(tabularData,headers="firstrow"))
			tempTabular = [process_sym,closing_time,process_sma10,signal1,signal2,h3Reversal,l3Reversal]
			tabularData2.append(tempTabular)
			# print("SMA10  : ",process_sma10)
			# print("Avergae Candlesize : ", process_avg_candlesize)
			# print("wick reversal signal = ",signal1)
			# print("extreme reversal signal = ",signal2)
		else:
			tempTabular = [process_sym,closing_time,process_sma10,signal1,signal2,h3Reversal,l3Reversal]
			tabularData2.append(tempTabular)	
print(tabulate(tabularData2,headers="firstrow",tablefmt="pretty"))
