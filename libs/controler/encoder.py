from utime import sleep_ms
import machine
from time import ticks_ms
import micropython
from machine import Timer

# Allocate memory for the case of an exception was rised in an IRQ
micropython.alloc_emergency_exception_buf(100)

class SoftEncoder:
    def __init__(self, t, reverse_direction = False ):
        self._counter = 0

        self._speed = 0
        
        self._cnt_prev = 0
        self._tick_prev = t
        self._distance = 0
        self._duration = 1

        if reverse_direction:
            self._dir = -1
        else:
            self._dir = 1

    @property
    def counter(self):
        return self._counter 
    
    @property
    def speed(self):
        """ Pulse per ms """
        #print ("t =", self._duration, "d :", self._distance)
        return self._distance / self._duration * 1000
    
    def update_speed (self, tick):
        self._distance = self._counter - self._cnt_prev
        self._duration = tick - self._tick_prev
        self._tick_prev = tick
        self._cnt_prev = self._counter
    
    def update(self, channel_a, channel_b):
        if channel_b == 0:
            self._counter -= self._dir        
        else :
            self._counter += self._dir

class Encoder:
    """
    Scheduler is used for soft IRQ, unfortunately, on rp2 the deph is set to 8
    which appears to make lose signals
    """
    def __init__(self, pin_channel_a, pin_channel_b, reverse_direction = False, use_soft_interrupt_irq=False, sig_trigger=machine.Pin.IRQ_RISING, pull_r=None):
        # Initialise rising edge detection
        self._encoder = SoftEncoder(ticks_ms(), reverse_direction)

        self._pin_channel_a = pin_channel_a
        self._pin_channel_a.init(machine.Pin.IN, pull_r)

        self._pin_channel_b = pin_channel_b
        self._pin_channel_b.init(machine.Pin.IN)
        
        if use_soft_interrupt_irq:
            self._pin_channel_a.irq(trigger=sig_trigger, handler=self.signal_soft_handler)            
            self._timer = Timer(period=100, mode=Timer.PERIODIC, callback=self.timer_soft_handler)
        else:
            self._pin_channel_a.irq(trigger=sig_trigger, handler=self.signal_handler)
            self._timer = Timer(period=100, mode=Timer.PERIODIC, callback=self.timer_handler)
                
        
    def signal_soft_handler(self, p):
        """
        First called by interrupt, then schedule the interrupt handler
        asap to avoid allocation problem in IRQ
        """ 
        micropython.schedule(self.signal_handler, None)
    
    def signal_handler(self, p):
        """ Actual implementation of interupt routine"""
        self._encoder.update(1, self._pin_channel_b.value())

    def timer_soft_handler(self, p):
        """
        First called by interrupt, then schedule the interrupt handler
        asap to avoid allocation problem in IRQ
        """ 
        micropython.schedule(self.timer_handler, None)
    
    def timer_handler(self, p):
        """ Actual implementation of interupt routine"""
        self._encoder.update_speed(ticks_ms())

    @property
    def counter(self):
        return self._encoder.counter
    
    @property
    def speed(self):
        return self._encoder.speed

def test_soft_encoder():
    encoder = SoftEncoder(0)
    encoder.update(0,1)
    encoder.update(0,1)
    encoder.update(0,1)
    assert(encoder.counter == 3)
    encoder.update(0,0)
    assert(encoder.counter == 2)
    print("Success")

def test_soft_encoder_speed1():
    encoder = SoftEncoder(0)

    for _ in range(4) : encoder.update(0,1)
    encoder.update_speed(1)
    assert(encoder.speed == 4000)
    
    for _ in range(6) : encoder.update(0,1)
    encoder.update_speed(2)
    assert(encoder.speed == 6000)
    
    for _ in range(4) : encoder.update(0,0)
    encoder.update_speed(3)
    assert(encoder.speed == -4000)
    
    print("Success")  

def test_encoder1():
    pin_channnel_a=machine.Pin(21)
    pin_channnel_b=machine.Pin(20)
    encoder = Encoder(pin_channnel_a, pin_channnel_b)

    while True:
        print("counter :", encoder.counter, "speed : ", encoder.speed)
        sleep_ms(100)
        
def test_encoder2():
    pin_channnel_a=machine.Pin(18)
    pin_channnel_b=machine.Pin(19)
    encoder = Encoder(pin_channnel_a, pin_channnel_b)

    while True:
        print("counter :", encoder.counter, "speed : ", encoder.speed)
        sleep_ms(100)

if __name__=="__main__":
#     test_soft_encoder()
#     test_soft_encoder_speed1()
    test_encoder1()
#     test_encoder2()