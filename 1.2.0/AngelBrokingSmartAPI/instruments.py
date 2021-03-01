import urllib.request
import  json
import testdata as t
# url1 = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
# with urllib.request.urlopen(url1) as url:
#     s = url.read()
# data = json.loads(s)
# with open('data.txt', 'w') as outfile:
#     json.dump(data, outfile)


mycursor = t.mydb.cursor()
symQuery = "select distinct symbol from algo_symbols"
mycursor.execute(symQuery)
symbols = mycursor.fetchall()

for sym in symbols:
    with open('data.txt') as json_file:
        data = json.load(json_file)
        for p in data:
            if(str(sym[0]).lower()+"-eq"==p['symbol'].lower()):
                symQuery = "update algo_symbols set token = '"+p['token']+"' where symbol='"+str(sym[0])+"'"
               # print (symQuery)
                mycursor.execute(symQuery)
                print(" Record updated for "+ str(sym[0])+" with token "+p['token'])
            # print('token: ' + p['token'])
            # print('symbol: ' + p['symbol'])
            # print('instrumenttype: ' + p['instrumenttype'])
            # print('')

t.mydb.commit();