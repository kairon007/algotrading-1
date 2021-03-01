import http.client
import mimetypes
conn = http.client.HTTPSConnection(
    "apiconnect.angelbroking.com"
    )
payload = "{\n\"clientcode\":\"D43726\",\n\"password\":\"Angel@1986\"\n}"
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'X-UserType': 'USER',
    'X-SourceID': 'WEB',
    'X-ClientLocalIP': '192.168.1.109',
    'X-ClientPublicIP': '203.194.98.1',
    'X-MACAddress': '28-C2-DD-58-9C-F7',
    'X-PrivateKey': 'tKace7Mp'
  }
conn.request(
    "POST", 
    "/rest/auth/angelbroking/user/v1/loginByPassword",
     payload,
     headers)

res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))