import testdata as t
from datetime import datetime
import json
import time
from AlgoStocks import AlgoStocks 
from datetime import timedelta
from pprintpp import pprint as pp
from tabulate import tabulate 
from camlevels import camlevels
import time
import os
# from smartapi import WebSocket
# from smartapi import SmartConnect
import logging
import mysql

# obj=SmartConnect(api_key="rkq08Xgf")
# data = obj.generateSession("D43726","Vanisha@2019")
candle_start_times={"1","16","32","46","43"}
candle_start_seconds={"1","2"}
symbol_ohlc={}

logging.basicConfig(filename='trade360.log', filemode='w',
format='%(asctime)s,%(name)s - %(levelname)s - %(message)s',level=logging.DEBUG,datefmt='%Y-%m-%d %H:%M:%S')
tabularData2=[("symbol","Target","SL","Entry Price","Breakout Signal","Breakout Conviction","Reversal signal","Reversal Conviction","Remarks","Entry Time")]
		
if(True):
		os.system('cls')
		print("scanning time : " ,datetime.now())
		aStocksList=[]
		pivots={}
		tabularData=[("symbol","closingtime","open","close","high","low","bodysize","wicksize","bodypercentage","closepercentage","candlesize","candlecolor")]
		record_l1={}
		record_l2={}
		record_cur={}
		mycursor = t.mydb.cursor()
		symQuery = "select distinct symbol from symbol_tracking"
		mycursor.execute(symQuery)
		symbols = mycursor.fetchall()	
		tokenQuery = "select symbol,token from algo_symbols"
		mycursor.execute(tokenQuery)
		tokenSym = mycursor.fetchall()
		groupQuery="select s2.*, s1.open from candle_data s1 , (select symbol,max(high),min(low) from candle_data where closingtime like %s group by symbol)s2 where s1.symbol=s2.symbol and s1.closingtime = %s";
		openDate=datetime.now().strftime("%Y-%m-%d")
		openDateTime=str(openDate)+" 09:30:00"
		groupTime=str(openDate)+"%"
		values=(str(groupTime),str(openDateTime))
		mycursor.execute(groupQuery,values)
		ohlcData = mycursor.fetchall()
		for ohlc in ohlcData:
			sym1=str(ohlc[0])
			openPrice=float(ohlc[3])
			highPrice=float(ohlc[1])
			lowPrice=float(ohlc[2])
			symbol_ohlc[sym1]=[openPrice,highPrice,lowPrice]
			#logging.debug(" data for "+sym1+" "+str(symbol_ohlc[sym1]))

		# for token2 in tokenSym:
		# 	sym1 = str(token2[0])
		# 	token1=str(token2[1])
		# 	print("NSE",sym1+"-EQ",token1)
		# 	logging.info('ltp request for '+sym1)
		# 	ltpData = obj.ltpData("NSE",sym1+"-EQ",token1)
		# 	print(ltpData)
		# 	symbol_ohlc[sym1]=[ltpData['data']['open'],ltpData['data']['high'],ltpData['data']['low']]
		# 	logging.info(ltpData)
		keys = symbol_ohlc.keys()
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
						pivotQuery="select * from pivots where symbol='"+str(sym[0])+"' order by closingdate desc limit 1"
						#values=record[1]
						mycursor.execute(pivotQuery)
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
		#tabularData2=[("symbol","Target","SL","Entry Price","Breakout Signal","Breakout Conviction","Reversal signal","Reversal Conviction","Remarks","Entry Time")]
		tabularData=[("symbol","closingtime","open","close","high","low","bodysize","wicksize","bodypercentage","closepercentage","candlesize","candlecolor")]
		for stock in aStocksList:
			
			#tabularData.append(stock.stock)
			signal1=" "
			signal2=" "
			signal3=" "
			signal4=" "
			h3Reversal=""
			l3Reversal=""
			h4Breakout=""
			l4Breakout=""
			target=0
			sl=0
			entry=0
			remarks=[]
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
						logging.info(process_sym + " has formed wick reversal pattern-buy")
					if( (cur_candle[9]>=0.70) and ( (cur_high-cur_open) >= 3.5* (cur_close-cur_open)) ):
						signal1="sell"
						logging.info(process_sym + " has formed wick reversal pattern-sell")
				elif(cur_open>cur_close):
					if(  (cur_candle[9]>=0.70) and ( (cur_high-cur_open) >= 3.5* (cur_open-cur_close)) ):
						signal1="sell"
						logging.info(process_sym + " has formed wick reversal pattern-sell")
					if( ( (cur_open-cur_low) >= 3.5* (cur_close-cur_open)) and (cur_candle[9]<=0.3) ):
						signal1="buy"
						logging.info(process_sym + " has formed wick reversal pattern-buy")
				if(signal1!=" "):
					remarks.append("Formed Wick Reversal signal ("+str(signal1)+") around "+str(cur_close))

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
							logging.info(process_sym + " has formed extream reversal pattern - buy")
						else:
							signal2="sell"
							logging.info(process_sym + " has formed extream reversal pattern - sell")
				if(signal2!=" "):
					remarks.append("Formed Extreme Reversal signal ("+str(signal2)+") around "+str(cur_close))
				
				#Outside Reversal Setup
				if(cur_candle[5]<prev_candle[5] and cur_candle[3]>prev_candle[4] and cur_candle[10]>=process_avg_candlesize*1.20):
					signal3="buy"
					logging.info(process_sym + " has formed outside reversal pattern - buy")
				if(cur_candle[3]<prev_candle[5] and cur_candle[4]>prev_candle[4] and cur_candle[10]>=process_avg_candlesize*1.20):
					signal3="sell"
					logging.info(process_sym + " has formed outside reversal pattern - sell")

				if(signal3!=" "):
					remarks.append("Formed Outside Reversal signal ("+str(signal3)+") around "+str(cur_close))

				#Doji Reversal Setup
				if(cur_candle[8]<=0.10):
					if(cur_candle[4]<=process_sma10):
						signal4="buy"
						logging.info(process_sym + " has formed doji reversal pattern-buy")
					if(cur_candle[5]>=process_sma10):
						signal4="sell"
						logging.info(process_sym + " has formed doji reversal pattern-sell")


				if(signal4!=" "):
					remarks.append("Formed Doji Reversal signal ("+str(signal4)+") around "+str(cur_close))
				
				sym_count=0

				#H3 and L3 reversal
				# logging.info("candle High price"+str(cur_candle[4]))
				# logging.info("candle Low price"+str(cur_candle[5]))
				# logging.info("candle Close price"+str(cur_candle[3]))
				# logging.info("pivot H3 price"+str(pivot_record.H3))
				# logging.info("pivot H4 price"+str(pivot_record.H4))
				# logging.info("pivot L3 price"+str(pivot_record.L3))
				# logging.info("pivot L4 price"+str(pivot_record.L4))
				if(pivot_record):
					if((cur_candle[4]>pivot_record.H3) and 
						(signal1=="sell" or signal2=="sell" or signal3=="sell" or signal4=="sell") and 
						(cur_candle[3]<pivot_record.H3)):
						h3Reversal = "sell"
						logging.info(process_sym + " has formed H3 reversal pattern-sell")
						target=pivot_record.L3
						sl=pivot_record.H4
						entry=pivot_record.H3
					if((cur_candle[5]<pivot_record.L3) and 
						(signal1=="buy" or signal2=="buy" or signal3=="buy" or signal4=="buy") and 
						(cur_candle[3]>pivot_record.L3)):
						l3Reversal = "buy"
						logging.info(process_sym + " has formed L3 reversal pattern-buy")	
						target=pivot_record.H3
						sl=pivot_record.L4
						entry=pivot_record.L3
				#H4 and L4 Breakout play
				if(pivot_record):
					if((cur_candle[3]>pivot_record.H4) and cur_candle[8]>0.8 and 
						(pivot_record.H5 - cur_candle[3])*100/cur_candle[3] > 1 and
						cur_candle[10]>=process_avg_candlesize*1.20):
						h4Breakout="buy"
						logging.info(process_sym + " has formed H4 breakout pattern-buy")
						target=pivot_record.H5
						sl=pivot_record.H3
						entry=pivot_record.H4
					if((cur_candle[3]<pivot_record.L4) and cur_candle[8]>0.8 and 
						(cur_candle[3] - pivot_record.L5)*100/cur_candle[3] > 1 and
						cur_candle[10]>=process_avg_candlesize*1.20):
						l4Breakout="sell"
						logging.info(process_sym + " has formed L4 breakout pattern-sell")
						target=pivot_record.L5
						sl=pivot_record.L3
						entry=pivot_record.L4

				h3ConvictionCounts=0
				l3ConvictionCounts=0
				h4ConvictionCounts=0
				l4ConvictionCounts=0

				reversalConviction="NA"
				breakoutConviction="NA"
				reversalSignal="NA"
				breakoutSignal="NA"
				#Calculate conviction percentage
				if(pivot_record):
					
					if(h3Reversal=="sell"):
						h3ConvictionCounts=h3ConvictionCounts+1
					if(l3Reversal=="buy"):
						l3ConvictionCounts=l3ConvictionCounts+1
					if(l4Breakout=="sell"):
						l4ConvictionCounts=l4ConvictionCounts+1
					if(h4Breakout=="buy"):
						h4ConvictionCounts=h4ConvictionCounts+1

					if(pivot_record.cpr_width<0.25):
						h4ConvictionCounts=h4ConvictionCounts+1
						l4ConvictionCounts=l4ConvictionCounts+1
					else:
						h3ConvictionCounts=h3ConvictionCounts+1
						l3ConvictionCounts=l3ConvictionCounts+1

					if(pivot_record.cpt_relationship=="Outside" or pivot_record.cpt_relationship=="LV" or pivot_record.cpt_relationship=="OLV"):
						h3ConvictionCounts=h3ConvictionCounts+1
					if(pivot_record.cpt_relationship=="Outside" or pivot_record.cpt_relationship=="HV" or pivot_record.cpt_relationship=="OHV" ):
						l3ConvictionCounts=l3ConvictionCounts+1
					if(pivot_record.cpt_relationship=="Inside" or pivot_record.cpt_relationship=="LV" or pivot_record.cpt_relationship=="OLV"):
						l4ConvictionCounts=l4ConvictionCounts+1
					if(pivot_record.cpt_relationship=="Inside" or pivot_record.cpt_relationship=="HV" or pivot_record.cpt_relationship=="OHV"):	
						h4ConvictionCounts=h4ConvictionCounts+1

					if(symbol_ohlc[pivot_record.symbol][0]>pivot_record.pivot):
						h4ConvictionCounts=h4ConvictionCounts+1
						l4ConvictionCounts=l4ConvictionCounts-1
						remarks.append("Price opened above pivot - "+str(pivot_record.pivot))
					if(symbol_ohlc[pivot_record.symbol][0]<pivot_record.pivot):
						l4ConvictionCounts=l4ConvictionCounts+1
						h4ConvictionCounts=h4ConvictionCounts-1
						remarks.append("Price opened below pivot - "+str(pivot_record.pivot))
					if(symbol_ohlc[pivot_record.symbol][0]<pivot_record.pivot):
						h3ConvictionCounts=h3ConvictionCounts+1
					if(symbol_ohlc[pivot_record.symbol][0]>pivot_record.pivot):
						l3ConvictionCounts=l3ConvictionCounts+1
					remarks.append("CPR width is "+str(pivot_record.cpr_width)+" and cpr relationship is "+str(pivot_record.cpt_relationship))
					remarks.append("10 SMA is "+str(process_sma10))
					day_high_price=float(symbol_ohlc[pivot_record.symbol][1])
					if(day_high_price > pivot_record.H5):
						remarks.append("Today's high price "+str(day_high_price)+" is above H5")
					if(day_high_price > pivot_record.H3 and day_high_price < pivot_record.H4):
						remarks.append("Today's high price "+str(day_high_price)+" is between H3 and H4")
					if(day_high_price > pivot_record.H4 and day_high_price < pivot_record.H5):
						remarks.append("Today's high price "+str(day_high_price)+" is between H4 and H5")
					if(day_high_price > pivot_record.L3 and day_high_price < pivot_record.H3):
						remarks.append("Today's high price "+str(day_high_price)+" is between L3 and H3")
					if(day_high_price > pivot_record.L4 and day_high_price < pivot_record.L3):
						remarks.append("Today's high price "+str(day_high_price)+" is between L4 and L3")
					if(day_high_price > pivot_record.L5 and day_high_price < pivot_record.L4):
						remarks.append("Today's high price "+str(day_high_price)+" is between L5 and L4")
					if(day_high_price < pivot_record.L5):
						remarks.append("Today's high price "+str(day_high_price)+" is below L5")

					day_low_price=float(symbol_ohlc[pivot_record.symbol][2])
					if(day_low_price > pivot_record.H5):
						remarks.append("Today's low price "+str(day_low_price)+" is above H5")
					if(day_low_price > pivot_record.H3 and day_low_price < pivot_record.H4):
						remarks.append("Today's low price "+str(day_low_price)+" is between H3 and H4")
					if(day_low_price > pivot_record.H4 and day_low_price < pivot_record.H5):
						remarks.append("Today's low price "+str(day_low_price)+" is between H4 and H5")
					if(day_low_price > pivot_record.L3 and day_low_price < pivot_record.H3):
						remarks.append("Today's low price "+str(day_low_price)+" is between L3 and H3")
					if(day_low_price > pivot_record.L4 and day_low_price < pivot_record.L3):
						remarks.append("Today's low price "+str(day_low_price)+" is between L4 and L3")
					if(day_low_price > pivot_record.L5 and day_low_price < pivot_record.L4):
						remarks.append("Today's low price "+str(day_low_price)+" is between L5 and L4")	
					if(day_low_price < pivot_record.L5):
						remarks.append("Today's low price "+str(day_low_price)+" is below L5")

					# logging.info(pivot_record.symbol)
					# logging.info("l4ConvictionCounts"+str(l4ConvictionCounts))
					# logging.info("l3ConvictionCounts"+str(l3ConvictionCounts))
					# logging.info("H4ConvictionCounts"+str(h4ConvictionCounts))
					# logging.info("H3ConvictionCounts"+str(h3ConvictionCounts))
					# logging.info(remarks)

					if(h3ConvictionCounts >0 and h3Reversal=="sell"):
						reversalConviction = str(round(((h3ConvictionCounts*100)/4),2))+"%"
						if(round(((h3ConvictionCounts*100)/3),0)>10):
							reversalSignal="Sell"
					if(l3ConvictionCounts >0 and l3Reversal=="buy" ):
						reversalConviction = str(round(((l3ConvictionCounts*100)/4),2))+"%"
						if(round(((l3ConvictionCounts*100)/3),0)>10):
							reversalSignal="Buy"

					if(h4ConvictionCounts >0 and h4Breakout=="buy"):
						breakoutConviction=str(round(((h4ConvictionCounts*100)/4),2))+"%"
						if(round(((h4ConvictionCounts*100)/3),0)>10):
							breakoutSignal="Buy"
					if(l4ConvictionCounts >0 and l4Breakout=="sell"):
						breakoutConviction=str(round(((l4ConvictionCounts*100)/4),2))+"%"
						if(round(((l4ConvictionCounts*100)/3),0)>10):
							breakoutSignal="Sell"

				if(breakoutSignal!="NA" or reversalSignal!="NA"):
					# tempTabular=cur_candle
					# tabularData.append(tempTabular)
					# print(tabulate(tabularData,headers="firstrow"))
					entryTime = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
					formatted_remarks=""
					for remark in remarks:
						formatted_remarks=formatted_remarks+remark+". "
					tempTabular = [process_sym,round(float(target),2),round(float(sl),2),round(float(entry),2),breakoutSignal,breakoutConviction,reversalSignal,reversalConviction,formatted_remarks,entryTime]
					tabularData2.append(tempTabular)
					try:
						insertQuery = "insert into trades(symbol,entrytime,bk_signal,bk_conv,rev_signal,rev_conv,cmp,target,sl,remarks) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
						insertValues=(process_sym,entryTime,breakoutSignal,breakoutConviction,reversalSignal,reversalConviction,round(float(entry),2),round(float(target),2),round(float(sl),2),formatted_remarks)
						mycursor.execute(insertQuery,insertValues)
						t.mydb.commit()
					except:
						print(mycursor.statement)
        #print(tabulate(tabularData2,headers="firstrow",tablefmt="pretty"))
		#time.sleep(900)
		print("Waking up...")

