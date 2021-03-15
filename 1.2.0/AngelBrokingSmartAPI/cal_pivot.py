import testdata as t
import datetime
import requests
import json
import time
from datetime import timedelta
from pprintpp import pprint as pp
import matplotlib.pyplot as plt 
import itertools
import collections
from tabulate import tabulate 
from prettytable import PrettyTable
import mysql
from datetime import datetime

mycursor = t.mydb.cursor()
sym_query = "select distinct symbol from algo_symbols"
mycursor.execute(sym_query)
records_sym = mycursor.fetchall()

for symbol in records_sym:
	sql_query = "select * from bhavcopy where symbol = '"+str(symbol[0]+"' order by timestamp desc limit 2")
	mycursor.execute(sql_query)
	records_raw = mycursor.fetchall()
	records = records_raw
	previous_cpt=[]
	count=0
	cpt_relationship=""
	x=PrettyTable()
	x.add_column("symbol",[str(symbol[0]),str(symbol[0]),str(symbol[0]),str(symbol[0]),str(symbol[0]),str(symbol[0]),str(symbol[0]),str(symbol[0]),str(symbol[0]),str(symbol[0]),str(symbol[0]),str(symbol[0]),str(symbol[0]),str(symbol[0]),str(symbol[0])])
	x.add_column("zone",["H5","H4","H3","H2","H1","L1","L2","L3","L4","L5","BC","PIVOT","TC","PIVOT WIDTH","CPT Relationship"])
	for row in reversed(records):
		date1=str(row[1]).split()
		high=row[4]
		low=row[5]
		close=row[3]
		range=high-low
		h5=(high/low)*close
		h4= close + (range * 1.1/2)
		h3=close + (range * 1.1/4)
		h2 = close + (range* 1.1/6)
		h1=close + (range * 1.1/ 12)
		l1= close - (range * 1.1/ 12)
		l2 =close - (range* 1.1/6)
		l3= close - (range *1.1/4)
		l4=close - (range *1.1/2)
		l5=close-(h5-close)
		bc=(low+high)/2
		pivot=(low+high+close)/3
		tc=(pivot-bc)+pivot
		width=(abs(tc-bc)/tc)*100
		if(bc > tc):
			temp=tc
			tc=bc
			bc=temp
		if (count >0):
			prev_bc=previous_cpt[0]
			prev_pivot=previous_cpt[1]
			prev_tc=previous_cpt[2]
			if (bc > prev_tc):
				cpt_relationship="HV"
			elif(tc>prev_tc and (pivot<prev_tc or bc<prev_tc) and bc>prev_bc):
				cpt_relationship= "OHV"
			elif(tc<prev_bc):
				cpt_relationship="LV"
			elif(bc<prev_bc and (pivot>prev_bc or tc>prev_bc ) and tc<prev_tc):
				cpt_relationship="OLV"
			elif(tc>prev_tc and bc<prev_bc):
				cpt_relationship = "Outside"
			elif(tc<prev_tc and bc>prev_bc):
				cpt_relationship="Inside"
		else:
			cpt_relationship="NA"
		previous_cpt= [bc,pivot,tc]	
		try:
			sqlquery = "insert into pivots(symbol,closingdate,cpt_relationship,bc,pivot,tc,cpr_width,l5,l4,l3,l2,l1,h1,h2,h3,h4,h5)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
			values=(str(symbol[0]),str(date1[0]),cpt_relationship,bc,pivot,tc,width,l5,l4,l3,l2,l1,h1,h2,h3,h4,h5)
			print(values)
			mycursor.execute(sqlquery,values)
			t.mydb.commit()
		except (mysql.connector.Error, mysql.connector.Warning) as e:
			print("Error while insert ",e)

		x.add_column(date1[0],[h5,h4,h3,h2,h1,l1,l2,l3,l4,l5,bc,pivot,tc,width,cpt_relationship])
		count=count+1
	#print(x)