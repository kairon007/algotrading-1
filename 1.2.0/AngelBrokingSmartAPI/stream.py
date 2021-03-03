from smartapi import WebSocket
from smartapi import SmartConnect
import testdata as t
from datetime import datetime
import os
from tabulate import tabulate 

candleData={}
obj=SmartConnect(api_key="tKace7Mp")
data = obj.generateSession("D43726","Angel@1986")
FEED_TOKEN=obj.getfeedToken() 
CLIENT_CODE="D43726"
cur_candle=[]
mycursor = t.mydb.cursor()
symQuery = "select symbol,token from algo_symbols limit 10"
mycursor.execute(symQuery)
data = mycursor.fetchall()
token=""
symToken={}
tabulardata = [("Time","symbol","LTP")]
candle_start_times={"0","15","30","45"}
candle_start_seconds="1"
new_candle_flag = {}
start_program_flag=True


def form_candle(time,sym,ltp):
	if((str(time.minute) in candle_start_times and str(time.second)==candle_start_seconds and (new_candle_flag[sym]!="close")) or start_program_flag):
		temp=candleData[sym]
		sqlQuery = "insert into candle_data(symbol,closingtime,open,close,high,low)values(%s,%s,%s,%s,%s,%s)"
		values=(sym,time,temp[0],temp[1],temp[2],temp[3])
		mycursor.execute(sqlQuery,values)
		print["Record inserted for :"+sym]
		candleData={}
		candleData[sym] = [ltp,ltp,ltp,ltp]
		new_candle_flag[sym]="close"
		#asd
		start_program_flag=False

	else:
		#print("Continue the current candle")
	#tabular = [("symbol","time""open","close","high","low")]
	#candleData = {"symbol" , {open,close,high,low}}
		#keys = candleData.keys()
		insertData = candleData[sym]
		high=insertData[2]
		low=insertData[3]
		if(ltp < insertData[3]):
			low=ltp
		if(ltp > insertData[2]):
			high=ltp
		candleData[sym]=[insertData[0],insertData[1],high,low]
		if(str(time.minute) not in candle_start_times):
			new_candle_flag[sym]="open"

	#keys = candleData.keys()
	# for key in keys:
	# 	insertData = candleData[key]
	# 	tempTab = (key,time.minute,insertData[0],insertData[1],insertData[2],insertData[3])
	# 	tabular.append(tempTab)
	#os.system('cls')
	#print(tabulate(tabular,headers="firstrow"))



for d in data:
	if(token==""):
		token= token+"nse_cm|"+str(d[1])
		symToken[str(d[0])]=str(d[1])
	else:
		token= token+"&nse_cm|"+str(d[1])
		symToken[str(d[0])]=str(d[1])

#print(symToken)

ss = WebSocket(FEED_TOKEN, CLIENT_CODE)
def on_tick(ws, tick):
	if(datetime.now() >= t.starttime and datetime.now() <= t.endtime):
		for i in tick:
			tempData=[]
			dataItems = i.items()
			symboltick={}
			if(len(dataItems)==19):
				for records in dataItems:
					symboltick[(records[0].replace(" ",""))]=records[1].replace(" ","")
				cur_symbol = list(symToken.keys())[list(symToken.values()).index(symboltick["tk"])]
				tempData=(str(datetime.now().strftime("%H:%M:%S")),cur_symbol,str(symboltick["ltp"]))
				tabulardata.append(tempData)
				form_candle(datetime.now(),cur_symbol,float(symboltick["ltp"]))
		#os.system('cls')
		#print(tabulate(tabulardata,headers="firstrow"))
		
				
	
def on_connect(ws, response):
	ws.send_request(token)

def on_close(ws, code, reason):
	ws.stop()

# Assign the callbacks.
ss.on_ticks = on_tick
ss.on_connect = on_connect
ss.on_close = on_close

ss.connect( )


