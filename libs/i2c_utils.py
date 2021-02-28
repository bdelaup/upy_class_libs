
"""I2C utils"""

from microbit import *

SENSOR_LIST = {
    0x19 : "micro:bit accelerometer", 
    0x1e : "micro:bit Magnetometer", 
    0x3e : "Grove LCD-data", 
    0x62 : "Grove LCD-RGB", 
    0x50 : " GrovePulsation"
    }
def scan_i2c_sensors():
    for address in i2c.scan():
        if address in SENSOR_LIST:
            print(address, " : ", SENSOR_LIST[address])
        else :
            print(address, " : Unknown")
