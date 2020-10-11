import testdata as t
import datetime
import requests
import time
from datetime import timedelta 
from pytz import timezone
from pprintpp import pprint as pp

today = datetime.datetime.now()-timedelta(days=20)
today2=today.astimezone(timezone('US/Eastern'))
print("Date: ",today)
print("double converted Date 2: ",today2.astimezone(timezone('Asia/Kolkata')))