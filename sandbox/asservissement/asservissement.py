from utime import sleep_ms
import machine
import micropython

# Allocate memory for the case of an exception was rised in an IRQ
micropython.alloc_emergency_exception_buf(100)

class SoftEncoder:
    def __init__(self, reverse_direction = False):
        self._counter = 0
        if reverse_direction:
            self._dir = -1
        else:
            self._dir = 1

    @property
    def counter(self):
        return self._counter 
    
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
        self._encoder = SoftEncoder(reverse_direction)

        self._pin_channel_a = pin_channel_a
        self._pin_channel_a.init(machine.Pin.IN, pull_r)

        self._pin_channel_b = pin_channel_b
        self._pin_channel_b.init(machine.Pin.IN)
        
        if use_soft_interrupt_irq:
            self._pin_channel_a.irq(trigger=sig_trigger, handler=self.signal_soft_handler)
        else:
            self._pin_channel_a.irq(trigger=sig_trigger, handler=self.signal_handler)
                
        
    def signal_soft_handler(self, p):
        """
        First called by interrupt, then schedule the interrupt handler
        asap to avoid allocation problem in IRQ
        """ 
        micropython.schedule(self.signal_handler, None)
    
    def signal_handler(self, p):
        """ Actual implementation of interupt routine"""
        self._encoder.update(1, self._pin_channel_b.value())

    @property
    def counter(self):
        return self._encoder.counter    

def test_soft_encoder():
    encoder = SoftEncoder()
    encoder.update(0,1)
    encoder.update(0,1)
    encoder.update(0,1)
    assert(encoder.counter == 3)
    encoder.update(0,0)
    assert(encoder.counter == 2)
    print("Success")

def test_encoder():
    pin_channnel_a=machine.Pin(27)
    pin_channnel_b=machine.Pin(26)
    encoder = Encoder(pin_channnel_a, pin_channnel_b)

    while True:
        print(encoder.counter)
        sleep_ms(100)

if __name__=="__main__":
    test_soft_encoder()
    #test_encoder()