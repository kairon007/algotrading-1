from smartapi import WebSocket
from smartapi import SmartConnect
import testdata as t
from datetime import datetime
import os
from tabulate import tabulate 

obj=SmartConnect(api_key="tKace7Mp")
data = obj.generateSession("D43726","Angel@1986")
FEED_TOKEN=obj.getfeedToken() 
CLIENT_CODE="D43726"

mycursor = t.mydb.cursor()
symQuery = "select symbol,token from algo_symbols"
mycursor.execute(symQuery)
data = mycursor.fetchall()
token=""
symToken={}
tabulardata = [("Time","symbol","LTP")]
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
		os.system('cls')
		print(tabulate(tabulardata,headers="firstrow"))
				
	
def on_connect(ws, response):
	ws.send_request(token)

def on_close(ws, code, reason):
	ws.stop()

# Assign the callbacks.
ss.on_ticks = on_tick
ss.on_connect = on_connect
ss.on_close = on_close

ss.connect( )