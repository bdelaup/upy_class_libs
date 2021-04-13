import math
import time

from machine import ADC,Pin 


B = 4275 # B value of the thermistor
R0 = 100000 # R0 = 100k
 
class Thermometer:
    def __init__(self, pin_id, R0, B, precision = 10):
        self.pin = ADC(Pin(pin_id))
        self.R0 = R0
        self.B = B
        self.precision = precision
    
    def analog_to_temp(self, val):
        R = (2**self.precision / val - 1.0 )
        # print("R", R)
        # print("val", val)
        R = R*R0
        # print("R", R)
        # print ("2**self.precision", 2**self.precision)
        temperature = 1.0/(math.log(R/R0)/B+1/298.15)-273.15 # Convert to temperature via datasheet
        return temperature

    def get_temperature(self):
        val = self.pin.read_u16()
        temp = self.analog_to_temp(val)
        return temp
        
def temp(reading):
    R = 1023.0 / reading - 1.0
    R = R0*R 
    temperature = 1.0/(math.log(R/R0)/B+1/298.15)-273.15 # Convert to temperature via datasheet    
    return temperature
 
def test():
    meter = Thermometer(27, R0, B, 16) # Rp Pico is 12 bits
    while(True):
        time.sleep(1)
        print ("Temperateure : ", meter.get_temperature(), " degC")

if __name__ == "__main__":
    test()
