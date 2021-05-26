# (c) Benoit Delaup 2021
# Creative common

import machine
import time
import micropython

# Allocate memory for the case of an exception was rised in an IRQ
micropython.alloc_emergency_exception_buf(100)

class Counter:
    def __init__(self, pin, sampling_frequency=1, use_soft_interrupt_irq=False, use_soft_interrupt_timer=True, sig_trigger=machine.Pin.IRQ_RISING, pull_r=None):
        """
        Scheduler is used for soft IRQ, unfortunately, on rp2 the deph is set to 8
        which appears to make lose signals
        """
        
        # Initialise rising edge detection
        self.counter = 0
        self.pin = pin
        self.sig_handler = self.sig_secondary_handler
        pin.init(machine.Pin.IN, pull_r)
        if use_soft_interrupt_irq:
            pin.irq(trigger=sig_trigger, handler=self.sig_primary_handler)
        else:
            pin.irq(trigger=sig_trigger, handler=self.sig_handler)
        
        # Initialise timer interrupt for signal frequency computation
        self.signal_frequency = 0
        self.sampling_frequency = sampling_frequency
        self.timer_handler = self.timer_secondary_handler    
        self.timer_device = machine.Timer()
        if use_soft_interrupt_timer:
            self.timer_device.init(freq = self.sampling_frequency, mode=machine.Timer.PERIODIC, callback = self.timer_primary_handler)
        else:
            self.timer_device.init(freq = self.sampling_frequency, mode=machine.Timer.PERIODIC, callback = self.timer_handler)
        
        
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
        
def test_btn():
    # Watch pin 20 for rizing edge button
    pin = machine.Pin(20)
    # Compute signal frequency once per seconde (1hz)
    freq= 1
    #Create counter
    cnt = Counter(pin, freq)
    while (True):
        print ("Compteur : ", cnt.get_counter(), " frequency : ", cnt.get_signal_frequency())
        time.sleep(1)

def test_geiger():
    TUBE_FACTOR_INDEX = const(151)
    # Watch pin 6 for rizing edge btn
    pin = machine.Pin(6)
    # Compute signal frequency once per seconde (1hz)
    freq= 1/12
    #Create counter
    cnt = Counter(pin, freq)
    while (True):
        print (cnt.get_counter(), " ticks", cnt.get_signal_frequency()/freq/TUBE_FACTOR_INDEX, "uScv")
        time.sleep(1)


if __name__=="__main__":
    #test_btn()
    test_geiger()
