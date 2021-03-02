from smartapi import SmartConnect #or from smartapi.smartConnect import SmartConnect
import testdata as t


smartApi =SmartConnect(api_key="tKace7Mp")
smartApi.generateSession("D43726","Angel@1986")
exchange = "NSE"
tradingsymbol = "SBIN-EQ"
symboltoken = 3045
data = smartApi.ltpData("NSE", "SBIN-EQ", "3045")
print(data)
