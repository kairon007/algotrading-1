import testdata as t
import datetime
import requests
import json
import time
from pprintpp import pprint as pp
mycursor = t.mydb.cursor()
sym='PNBHOUSING'+'.NS'
API_URL = "https://www.alphavantage.co/query" 
data = { "function": "TIME_SERIES_DAILY", 
            "symbol": sym,
            "outputsize" : "full",
            "datatype": "json", 
            "apikey": "01LSAIRK0QTB0QMN" } 
 response = requests.get(API_URL, data)
items = response.json()['Time Series (Daily)'].items()
keys = list(items)
#print(len(keys))
count =0
for key in keys:
    open_price = float(str(key[1]['1. open']))
    close_price = float(str(key[1]['4. close']))
    high_price = float(str(key[1]['2. high']))
    low_price = float(str(key[1]['3. low']))
    volume = int(str(key[1]['5. volume']))
    date1 = datetime.datetime.strptime(str(key[0]),'%Y-%m-%d')
    count = count+1
    #print(str(sym) +" "+ str(open_price) +" "+str(close_price)+" "+str(high_price)+" "+str(low_price)+" "+str(volume)+" "+str(date1))

    # sql = "INSERT INTO daily_ohlc (symbol,date1,open_price,close_price,high_price,low_price,volume) VALUES (%s,%s,%s,%s,%s,%s,%s)"
    # val=(sym,date1,open_price,close_price,high_price,low_price,volume)
    # mycursor.execute(sql,val)
    # t.mydb.commit()
    # print(mycursor.rowcount, "record inserted.")

print(count)    


