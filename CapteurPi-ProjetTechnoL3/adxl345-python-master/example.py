# ADXL345 Python example 
#
# author:  Jonathan Williamson
# license: BSD, see LICENSE.txt included in this package
# 
# This is an example to show you how to use our ADXL345 Python library
# http://shop.pimoroni.com/products/adafruit-triple-axis-accelerometer

from adxl345 import ADXL345
import time
import json
import telnetlib

HOST = "192.138.43.120"
PORT = 7777
ID =2

adxl345 = ADXL345()

_json  = json.dumps({'type' :'request', 'request' : 'publish', 'peripheral' :  0, 'data' : '1'})
_json = json.loads(_json)
frequencestr = _json["data"]
frequence = int(frequencestr)


tn = telnetlib.Telnet(HOST,PORT)
_connect = '{"type" : "request", "request" : "connect", "peripheral" : '+str(ID)+'}'
parsed = json.loads(_connect)
tn.write(json.dumps(parsed, indent = 4).encode("ascii"))

def to_json(data) :
    h_json = '{"type" : "request", "request" : "publish", "peripheral" : 2, "data" : "'+str(data)+'"}'
    parsed = json.loads(h_json)
    print(parsed)
    return json.dumps(parsed, indent = 4)

while(True):
    time.sleep(frequence)
    axes = adxl345.getAxes(True)

    time.sleep(0.01)
    axes2 = adxl345.getAxes(True)
    
    x = axes2['x']-axes['x']
    y = axes2['y']-axes['y']
    z = axes2['z']-axes['z']
    h_json = '{"accelerometreX" : '+repr(x)+',"accelerometreY" : '+repr(y)+',"accelerometreZ" : '+repr(z)+'}'
    parsed = json.loads(h_json)
    json.dumps(parsed, indent = 4)
    _json = to_json(parsed)
    tn.write(_json.encode("ascii"))

    
   
