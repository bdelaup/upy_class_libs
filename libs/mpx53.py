import machine
import time

class MPX53:
    """
    High precision pressure sensor
    """
    def __init__(self, pin, adc_resolution = 16, amplication_factor=35, mpx53_vin = 3.3):
        # Relative to aquisition chain
        self.amplication_factor = amplication_factor
        self.mpx53_vin = mpx53_vin
        
        # Relative to ADC embedded on the SOC
        self.adc_resolution = adc_resolution
        self.adc_value_max = 2**self.adc_resolution
        self.adc = machine.ADC(pin)
        
    def get_digital_value(self):
        return self.adc.read_u16()
    
    def get_input_voltage(self):
        return self.get_digital_value()/self.adc_value_max * self.mpx53_vin
    
    def get_signal_voltage(self):
        return self.get_input_voltage()/self.amplication_factor
    
    def voltage_to_pressure_kpa(self,voltage):
        sensitivity = 1/1.2
        offset = -25
        return voltage*1000*sensitivity + offset
    
    @property
    def pressure(self):
        return self.voltage_to_pressure_kpa(self.get_signal_voltage())
        
    
if __name__ == "__main__":
    
    
    mpx = MPX53(27)
    
    while(True):
        print ("get_digital_value ", mpx.get_digital_value())
        print ("get_input_voltage", mpx.get_input_voltage()*1000, "mV")
        print ("get_signal_voltage", mpx.get_signal_voltage()*1000, "mV")
        print ("pressure", mpx.pressure)
        print("")
        time.sleep(1)
