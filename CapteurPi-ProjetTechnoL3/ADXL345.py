#import the adxl345 module
from adxl345 import ADXL345
import time

#create ADXL345 object
adxl345 = ADXL345()

#get axes as g
while(True):
    time.sleep(1)
    axes = adxl345.getAxes(True)
    # to get axes as ms^2 use
    #axes = accel.getAxes(False)

    #put axes into variables for the first time
    x1 = axes['x']
    y1 = axes['y']
    z1 = axes['z']

    #stop the program for the IMU to move
    time.sleep(0.001)

    #put axes into variables for the second time
    axes2 = adxl345.getAxes(True)
    x2 = axes2['x']
    y2 = axes2['y']
    z2 = axes2['z']

    #calculate the difference 
    x = x2-x1
    y = y2-y1
    z = z2-z1
    
    #print axes
    print (x2-x1)
    print (y2-y1)
    print (z2-z1)
