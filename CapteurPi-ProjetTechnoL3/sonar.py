import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

Trig = 23
Echo = 24

GPIO.setup(Trig,GPIO.OUT)
GPIO.setup(Echo,GPIO.IN)

GPIO.output(Trig, False)

while True:
    time.sleep(0.1)

    #sending the wave
    GPIO.output(Trig,True)
    time.sleep(0.01)
    GPIO.output(Trig,False)
    while GPIO.input(Echo)==0:
        start = time.time()

    #Waiting for the wave comes back
    while GPIO.input(Echo)==1:
        end = time.time()

    distance = round((end-start) *343*100/2)    #343m/s is the sound speed, *100 to get it in cm, /2 because the signal is going there and coming back 

    #Don't print the distance if it's over 2000cm
    if(distance<2000):
        print("La distance est de :", distance,"cm")

    else:
        print("Distance trop importante")

GPIO.cleanup()
    
#https://tutorials-raspberrypi.com/raspberry-pi-ultrasonic-sensor-hc-sr04/ to get the tutorial
