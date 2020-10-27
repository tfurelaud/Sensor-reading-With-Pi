import json
import RPi.GPIO as GPIO
from adxl345 import ADXL345
import smbus
import time
import telnetlib
import socket

GPIO.setmode(GPIO.BCM)

#Set all variables that we'll need
HOST = "192.168.43.120"
PORT = 7777
ID = 2
Trig = 23
Echo = 24
pin_input = 18

adxl345 = ADXL345()

GPIO.setup(Trig,GPIO.OUT)
GPIO.setup(Echo,GPIO.IN)

GPIO.output(Trig, False)

adxl345 = ADXL345()

bus = smbus.SMBus(1)

#Parse data to a JSON package to send it to the bus
def to_json(data) :
    h_json = '{"type" : "request", "request" : "publish", "peripheral" : 2, "data" : "'+str(data)+'"}'
    parsed = json.loads(h_json)
    print(parsed)
    return json.dumps(parsed, indent = 4)


def get_luminosity (pin_input):
    count = 0
    MAX = 5000
    #Set up the pin as output to set it low
    GPIO.setup(pin_input, GPIO.OUT)
    GPIO.output(pin_input, GPIO.LOW)
    time.sleep(0.1)

    #Change the pin back to input and count until the pin goes high
    GPIO.setup(pin_input, GPIO.IN)
    while (GPIO.input(pin_input) != GPIO.HIGH):
        if count>=MAX:
            break
        count+=1

    #Return the value (not really accurate)
    return count

#Connecting to the BUS by sending a JSON package
tn = telnetlib.Telnet(HOST,PORT)
_connect = '{"type" : "request", "request" : "connect", "peripheral" : '+str(ID)+'}'
parsed = json.loads(_connect)
print(parsed)
tn.write(json.dumps(parsed, indent = 4).encode("ascii"))
time.sleep(1)

#Prentend to receive a JSON package from the BUS containing the frequency for the While(True)
_json  = json.dumps({'type' :'request', 'request' : 'publish', 'peripheral' :  0, 'data' : '0.5'})
_json = json.loads(_json)
frequencestr = _json["data"]
frequence = float(frequencestr)


bus.write_byte_data(0x68, 0x3E, 0x01)
bus.write_byte_data(0x68, 0x16, 0x18)

while True:
    time.sleep(float(frequence))

    #Sending the wave
    GPIO.output(Trig,True)
    time.sleep(0.01)
    GPIO.output(Trig,False)
    
    while GPIO.input(Echo)==0:
        start = time.time()

    #Waiting for the wave comes back
    while GPIO.input(Echo)==1:
        end = time.time()
    
    distance = round((end-start) *343*100/2)    #343m/s is the sound speed, *100 to get it in cm, /2 because the signal is going there and coming back 

    #Get the informations from the accelerometer a first time
    axes = adxl345.getAxes(True)
    time.sleep(0.01)
    axes2 = adxl345.getAxes(True)

    #Calculate the difference to know the acceleration
    x = axes2['x']-axes['x']
    y = axes2['y']-axes['y']
    z = axes2['z']-axes['z']

    print(" ------- ACCELERATION----------")
    print("Acceleration X :" + repr(x) + "g")
    print("Acceleration Y :" + repr(y) + "g")
    print("Acceleration Z :" + repr(z) + "g")
    print("\n")

    
    data = bus.read_i2c_block_data(0x68, 0x1D, 6)

    # Convert the data for the X axe
    xGyro1 = data[0] * 256 + data[1]
    if xGyro1 > 32767 :
            xGyro1 -= 65536
            
    # Convert the data for the Y axe
    yGyro1 = data[2] * 256 + data[3]
    if yGyro1 > 32767 :
            yGyro1 -= 65536

    # Convert the data for the Z axe
    zGyro1 = data[4] * 256 + data[5]
    if zGyro1 > 32767 :
            zGyro1 -= 65536

    time.sleep(0.01)
    data2 = bus.read_i2c_block_data(0x68, 0x1D, 6)

    # Do it a seconde time
    xGyro2 = data2[0] * 256 + data2[1]
    if xGyro2 > 32767 :
            xGyro2 -= 65536

    yGyro2 = data2[2] * 256 + data2[3]
    if yGyro2> 32767 :
            yGyro2 -= 65536

    zGyro2 = data2[4] * 256 + data2[5]
    if zGyro2 > 32767 :
            zGyro2 -= 65536

    #Calculate the difference to know the movement
    xGyro = xGyro2 - xGyro1
    yGyro = yGyro2 - yGyro1
    zGyro = zGyro2 - zGyro1

    print(" ------- ROTATION----------")
    print("X-Axis of Rotation : %d radians/s" %xGyro)
    print("Y-Axis of Rotation : %d radians/s" %yGyro)
    print("Z-Axis of Rotation : %d radians/s" %zGyro)
    print("\n")

    print(" ------- DISTANCE----------")
    #Don't print the distance if it's over 2000cm
    if(distance<2000):
        print("La distance est de :", distance,"cm")

    else:
        print("Distance supérieur à 20 mètres")
    print("\n")

    print(" ------- LUMINOSITE----------")
    lumi = get_luminosity(pin_input)
    #Get luminosity in percentage
    lumi = 100- (lumi/50)
    print("Pourcentage de lumière : " + repr(lumi) + "%")
    print("\n")
    
    
    #Form the data that we'll send to the bus
    to_send = '{"accelerometreX" : '+ repr(x) +',"accelerometreY" : ' + repr(y) + ',"accelerometreZ" : '+ repr(z) +', "gyroscopeX": '+ repr(xGyro)+',"gyroscopeX": '+repr(yGyro)+',"gyroscopeX": '+repr(zGyro)+', "SONAR" : '+repr(distance)+', "luminosite" : '+repr(lumi)+'}'  

    #Parsed the data and send it
    d_parsed = json.loads(to_send)
    json.dumps(d_parsed, indent = 4)
    _json = to_json(d_parsed)
    tn.write(_json.encode("ascii"))

    time.sleep(0.1)
   # print(tn.read_all())
         

GPIO.cleanup()
    
#https://tutorials-raspberrypi.com/raspberry-pi-ultrasonic-sensor-hc-sr04/ to get the tutorial
