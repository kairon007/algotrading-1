import StockData as t
import testdata as td

mycursor = td.mydb.cursor()
sym_query = "select distinct symbol from stockdatadaily"
mycursor.execute(sym_query)
records_sym = mycursor.fetchall()

for stock in records_sym:
	sql_query = "select * from cam_data where stockdatadaily = '"+str(stock[0]+"' order by date desc limit 2")
	mycursor.execute(sql_query)
	records_raw = mycursor.fetchall()
	records = records_raw
	count=0
	prev_bc=0
	prev_tc=0
	prev_pivot=0
	for row in reversed(records):
		if(count==0):
			date1=str(row[1]).split()
			high=row[4]
			low=row[5]
			close=row[3]
			prev_pivot = (high+low+close)/3
			prev_bc = (high+low)/2
			prev_tc= (prev_pivot-prev_bc)+prev_pivot
			if(prev_bc >prev_tc):
				temp=prev_tc
				prev_tc = prev_bc
				prev_bc = temp 
		else:
			date1=str(row[1]).split()
			high=row[4]
			low=row[5]
			close=row[3]
			tempStock = t.StockDetails(stock)
			tempStock.pivot = (high+low+close)/3
			tempStock.bc = (high+low)/2
			tempStock.tc= (tempStock.pivot-tempStock.bc)+tempStock.pivot
			tempStock.pivotWidth=(abs(tempStock.tc-tempStock.tc)/tempStock.bc)*100
			if(tempStock.bc > tempStock.tc):
				temp=tempStock.tc
				tempStock.tc = tempStock.bc
				tempStock.bc = temp 
			tempStock.R1= (2*tempStock.pivot)-low
			tempStock.R2=tempStock.pivot+(high-low)
			tempStock.R3=high+2*(tempStock.pivot-low)
			tempStock.S1=(2*tempStock.pivot)-high
			tempStock.S2=tempStock.pivot-(high-low)
			tempStock.S3=low-2*(high-tempStock.pivot)
			tempStock.H1=close + (high-low) * 1.1/12
			tempStock.H2=close + (high - low) * 1.1/6
			tempStock.H3=close + (high - low) * 1.1/4
			tempStock.H4=close + (high - low) * 1.1/2
			tempStock.H5=tempStock.H4 + 1.168 * (tempStock.H4 - tempStock.H3)
			tempStock.H6=tempStock.H4 + (high/low) * close
			tempStock.CS1=close - (high - low) * 1.1/12
			tempStock.CS2=close - (high - low) * 1.1/6
			tempStock.CS3=close - (high - low) * 1.1/4
			tempStock.CS4=close - (high - low) * 1.1/2
			tempStock.CS5=tempStock.CS4 - 1.168 * (tempStock.CS3 - tempStock.CS4)
			tempStock.CS6=close - (tempStock.H6 - close)
			if (tempStock.bc > prev_tc):
				tempStock.cptRelationship="HV"
			elif(tempStock.tc>prev_tc and (tempStock.pivot<prev_tc or tempStock.bc<prev_tc) and tempStock.bc>prev_bc):
				tempStock.cptRelationship= "OHV"
			elif(tempStock.tc<prev_bc):
				tempStock.cptRelationship="LV"
			elif(tempStock.bc<prev_bc and (tempStock.pivot>prev_bc or tempStock.tc>prev_bc ) and tempStock.tc<prev_tc):
				tempStock.cptRelationship="OLV"
			elif(tempStock.tc>prev_tc and tempStock.bc<prev_bc):
				tempStock.cptRelationship = "Outside"
			elif(tempStock.tc<prev_tc and tempStock.bc>prev_bc):
				tempStock.cptRelationship="Inside"
			elif:
				tempStock.cptRelationship="NA"
			stocks.append(tempStock)


for stockData in stocks:

	# print("Stock name  : " , stockData.name , " Stock open Price : ",stockData.openPrice)
	print(tempStock)