import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

#Define the pin
pin_input = 18

#The light sensor is analog and cannot be read by the Raspberry Pi
#so we add a capacitor and calcul the amount of time to charge it
#depending on the light
def get_value (pin_input):
    count = 0

    #Set up the pin as output to set it low
    GPIO.setup(pin_input, GPIO.OUT)
    GPIO.output(pin_input, GPIO.LOW)
    time.sleep(0.1)

    #Change the pin back to input and count until the pin goes high
    GPIO.setup(pin_input, GPIO.IN)
    while (GPIO.input(pin_input) != GPIO.HIGH):
        if count>=2000:
            break
        count+=1

    #Return the value (not really accurate)
    return count

#Catch when script is interrupted and clean up correctly
try:
    #Main loop
    while True:
        print(100- (get_value(pin_input)/20))
except KeyboardInterrupt:
       GPIO.cleanup()
