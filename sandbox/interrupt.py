import machine
import time
from machine import Pin
import micropython

# Allocate memory for the case of an exception was rised in an IRQ
micropython.alloc_emergency_exception_buf(100)

class Counter:
    def __init__(self, pin, sampling_frequency=1):
        # Initialise rising edge detection
        self.counter = 0
        self.pin = pin
        self.sig_handler = self.sig_secondary_handler
        pin.init(machine.Pin.IN, machine.Pin.PULL_DOWN)
        pin.irq(trigger=machine.Pin.IRQ_RISING, handler=self.sig_primary_handler)
        
        # Initialise timer interrupt for signal frequency computation
        self.signal_frequency = 0
        self.sampling_frequency = sampling_frequency
        self.timer_handler = self.timer_secondary_handler    
        self.timer_device = machine.Timer()
        self.timer_device.init(freq = self.sampling_frequency, mode=machine.Timer.PERIODIC, callback = self.timer_primary_handler)
        
    def sig_primary_handler(self, p):
        """
        First called by interrupt, then schedule the interrupt handler
        asap to avoid allocation problem in IRQ
        """ 
        micropython.schedule(self.sig_handler, None)
    
    def sig_secondary_handler(self, p):
        """ Actual implementation of interupt routine"""
        self.counter +=1        
 
    def timer_primary_handler(self, p):
        """
        First called by interrupt, then schedule the interrupt handler
        asap to avoid allocation problem in IRQ
        """ 
        micropython.schedule(self.timer_handler, None)

    def timer_secondary_handler(self, p):
        """ Actual implementation of interupt routine"""
        self.signal_frequency = self.counter * self.sampling_frequency
        self.counter = 0
        #print("Frequency %d : ", self.signal_frequency)
    
    def get_counter(self):
        return self.counter
    
    def get_signal_frequency(self):
        return self.signal_frequency
     

cnt = 0
def btn_handler(pin):
    global cnt
    cnt += 1

def main1():

    btn = Pin(20, machine.Pin.IN, machine.Pin.PULL_DOWN)
    btn.irq(trigger=machine.Pin.IRQ_RISING, handler=btn_handler)    
    while (True):
        print (cnt)
        time.sleep(1)
        
def main2():
    # Watch pin 20 for rizing edge
    pin = Pin(20)
    # Compute signal frequency once per seconde (1hz)
    freq= 1
    #Create counter
    cnt = Counter(pin, freq)
    while (True):
        print ("Compteur : ", cnt.get_counter(), " frequency : ", cnt.get_signal_frequency())
        time.sleep(1)
        
def test_schedule(p):
    print("Schedule OK")
    
if __name__=="__main__":
    micropython.schedule(test_schedule, None)
    #main1()
    main2()
