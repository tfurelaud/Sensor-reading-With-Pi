import json
import telnetlib
import time
import socket

HOST = "192.168.43.120"
PORT = 7777
ID = 2
SONAR = 0
LIGHT = 1

#Parse data to a JSON package to send to the bus
def to_json(data) :
    h_json = '{"type" : "request", "request" : "publish", "peripheral" : 2, "data" : "' + str(data) + '"}'
    parsed = json.loads(h_json)
    print(parsed)
    return json.dumps(parsed, indent = 4)

data =  '{"luminosite" : 15}'
d_parsed = json.loads(data)
json.dumps(d_parsed, indent = 4)
_json = to_json(d_parsed)


#print(_json);


tn = telnetlib.Telnet(HOST,PORT)
_connect = '{"type" : "request", "request" : "connect", "peripheral" : '+str(ID)+'}'
parsed = json.loads(_connect)
tn.write(json.dumps(parsed, indent = 4).encode("ascii"))
time.sleep(1)
tn.write(_json.encode("ascii"))



