import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root",
  database="algo_trade"
)




stocks_to_scan ={'AUBANK','ADANIPOWER','ABCAPITAL','ABFRL','AJANTPHARM','ALKEM','ALBK','AMARAJABAT','AMBUJACEM','APOLLOHOSP','APOLLOTYRE','ASIANPAINT','AUROPHARMA','DMART','AXISBANK','BAJFINANCE','BAJAJFINSV','BALKRISIND','BANDHANBNK','BANKBARODA','BANKINDIA','BATAINDIA','BERGEPAINT','BHARATFORG','BHEL','BPCL','INFRATEL','BIOCON','BBTC','BOSCHLTD','BRITANNIA','CADILAHC','CANBK','CASTROLIND','CHOLAFIN','CIPLA','CUB','COALINDIA','COLPAL','CONCOR','COROMANDEL','CUMMINSIND','DLF','DABUR','DALBHARAT','DIVISLAB','DRREDDY','EDELWEISS','EICHERMOT','EMAMILTD','ENDURANCE','ENGINERSIN','ESCORTS','EXIDEIND','FEDERALBNK','FCONSUMER','FRETAIL','GAIL','GICRE','GLENMARK','GODREJAGRO','GODREJCP','GODREJPROP','GRASIM','GSPL','HEG','HCLTECH','HDFCAMC','HDFCBANK','HDFCLIFE','HAVELLS','HEROMOTOCO','HEXAWARE','HINDALCO','HINDPETRO','HINDUNILVR','HUDCO','HDFC','ICICIBANK','ICICIPRULI','IDBI','IDFCFIRSTB','ITC','IBVENTURES','INDHOTEL','IOC','IGL','INDUSINDBK','INFY','INDIGO','IPCALAB','JSWSTEEL','JINDALSTEL','JUBLFOOD','JUBILANT','KOTAKBANK','L&TFH','LTTS','LICHSGFIN','LTI','LT','MGL','M&MFIN','M&M','MANAPPURAM','MRPL','MARICO','MARUTI','MFSL','MINDTREE','MOTHERSUMI','MPHASIS','MUTHOOTFIN','NATCOPHARM','NBCC','NHPC','NTPC','NATIONALUM','NESTLEIND','OBEROIRLTY','OIL','OFSS','ORIENTBANK','PIIND','PETRONET','PFIZER','PIDILITIND','PEL','PFC','POWERGRID','PRESTIGE','PGHH','PNB','QUESS','RBLBANK','RECLTD','RAJESHEXPO','RELIANCE','RNAM','SBILIFE','SRF','SHREECEM','SRTRANSFIN','SIEMENS','SBIN','SAIL','STRTECH','SUNPHARMA','SUNTV','SYNGENE','TVSMOTOR','TATACHEM','TATAGLOBAL','TATAMTRDVR','TATAMOTORS','TATAPOWER','TATASTEEL','TECHM','NIACL','RAMCOCEM','TITAN','TORNTPHARM','TORNTPOWER','UPL','ULTRACEMCO','UNIONBANK','UBL','MCDOWELL-N','VGUARD','VARROC','VEDL','IDEA','VOLTAS','ZEEL'} 
