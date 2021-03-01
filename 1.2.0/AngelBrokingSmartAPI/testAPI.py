from smartapi import SmartConnect #or from smartapi.smartConnect import SmartConnect
import testdata as t
#import smartapi.smartExceptions(for smartExceptions)

#create object of call
obj=SmartConnect(api_key="tKace7Mp")



#login api call

data = obj.generateSession("D43726","Angel@1986")
refreshToken= data['data']['refreshToken']

#fetch the feedtoken
feedToken=obj.getfeedToken()
print(feedToken)
print(refreshToken)
#fetch User Profile
userProfile= obj.getProfile(refreshToken)
