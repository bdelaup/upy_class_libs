import micropython
import machine

# Allocate memory for the case of an exception was rised in an IRQ
micropython.alloc_emergency_exception_buf(100)    
        

class Encoder:
    """
    Scheduler is used for soft IRQ, unfortunately, on rp2 the deph is set to 8
    which appears to make lose signals
    """
    def __init__(self, pin_channel_a, pin_channel_b, reverse_direction = False, use_soft_interrupt_irq=False, sig_trigger=machine.Pin.IRQ_RISING, pull_r=None):
        self._counter = 0

        if reverse_direction:
            self._dir = -1
        else:
            self._dir = 1
        
        # Initialise rising edge detection
        self._pin_channel_a = pin_channel_a
        self._pin_channel_a.init(machine.Pin.IN, pull_r)

        self._pin_channel_b = pin_channel_b
        self._pin_channel_b.init(machine.Pin.IN)
        

        self._pin_channel_a.irq(trigger=sig_trigger, handler=self.signal_soft_handler)
        
    def signal_soft_handler(self, _):
        """
        First called by interrupt, then schedule the interrupt handler
        asap to avoid allocation problem in IRQ
        """ 
        micropython.schedule(self.signal_handler, self._pin_channel_b.value())

    def signal_hard_handler(self, p):
        """ Actual implementation of interupt routine"""
        if p == 0:
            self._counter -= self._dir        
        else :
            self._counter += self._dir

    def signal_handler(self, _):
        """ Actual implementation of interupt routine"""
        if self._pin_channel_b.value() == 0:
            self._counter -= self._dir        
        else :
            self._counter += self._dir

    @property
    def counter(self):
        return self._counter