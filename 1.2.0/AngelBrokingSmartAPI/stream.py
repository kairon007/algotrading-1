from smartapi import WebSocket
from smartapi import SmartConnect
import testdata as t


obj=SmartConnect(api_key="tKace7Mp")
data = obj.generateSession("D43726","Angel@1986")
FEED_TOKEN=obj.getfeedToken() 
CLIENT_CODE="D43726"

mycursor = t.mydb.cursor()
symQuery = "select symbol,token from algo_symbols limit 3"
mycursor.execute(symQuery)
data = mycursor.fetchall()
token=""
for d in data:
	if(token==""):
		print("First time")
		token= token+"nse_cm|"+str(d[1])
	else:
		print("afterwards")
		token= token+"&nse_cm|"+str(d[1])


ss = WebSocket(FEED_TOKEN, CLIENT_CODE)
def on_tick(ws, tick):
	print("Ticks: {}".format(tick))

def on_connect(ws, response):
	ws.send_request(token)

def on_close(ws, code, reason):
	ws.stop()

# Assign the callbacks.
ss.on_ticks = on_tick
ss.on_connect = on_connect
ss.on_close = on_close

ss.connect( )