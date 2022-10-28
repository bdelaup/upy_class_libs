from utime import sleep_ms
import machine
import micropython
from machine import PWM, Pin
import machine
from utime import sleep_ms
from time import ticks_ms, ticks_diff


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
        

        self._pin_channel_a.irq(trigger=sig_trigger, handler=self.signal_handler)
                
           
    def signal_handler(self, p):
        """ Actual implementation of interupt routine"""
        if self._pin_channel_b.value() == 0:
            self._counter -= self._dir        
        else :
            self._counter += self._dir

    @property
    def counter(self):
        return self._counter



class Motor:
    class MotorDirection(enumerate) :
        FORWARD = 1
        REVERSE = 0

    def __init__(self, pin_dir, pin_speed, duty_ratio = 65535, reverse_sense=False):
        self._pin_dir = pin_dir
        self._pin_dir.init(Pin.OUT)
        self._pin_dir.off()

        self._pin_speed = pin_speed
        self._pwm = PWM(self._pin_speed)
        self._pwm.duty_u16(0)
        self._pwm.freq(1000)    
        

        if reverse_sense:
            self._rev_sense = True
        else:
            self._rev_sense = False

        self._duty_ratio = duty_ratio
        self._dir = self.MotorDirection.FORWARD        
    
    def set_direction(self, dir):
        if dir != self.MotorDirection.FORWARD and dir != self.MotorDirection.REVERSE:
            return

        if self.MotorDirection.FORWARD == dir:
            if self._rev_sense:
                self._dir = self.MotorDirection.REVERSE
            else:
                self._dir = self.MotorDirection.FORWARD
        else :
            if self._rev_sense:
                self._dir = self.MotorDirection.FORWARD
            else:
                self._dir = self.MotorDirection.REVERSE
            
        if self._dir == self.MotorDirection.FORWARD:
            self._pin_dir.on()
        else:
            self._pin_dir.off()


    def set_speed(self, duty):
        if duty < 0 or duty > 100:
            return
        duty = round(duty/100 * self._duty_ratio)
        self._pwm.duty_u16(duty)

    def on(self, direction, duty):
        self.set_direction(direction)
        self.set_speed(duty)

    def off(self):
        self.set_speed(0)

class Filter:
    def __init__(self, kp=0):
        self._kp=kp
        self._order=0        
        self._proportional=0

    
    @property
    def kp(self):
        return self._kp

    @kp.setter
    def kp(self, val):
        self._kp = val

    @property
    def order(self):
        return self._order

    @order.setter
    def order(self, sp):
        self._order=sp
        
    def set_signal(self, value):
        """
        update the input signal value
        """
        epsilon = self._order-value
        
    def get_filtered_signal(self):
        """
        returns the filtered signal
        """
        return self._kp * epsilon

def ramp2(time):
    """time in s"""
    if time > 4:
        return None
    else:
        return  int(100 * time )
    
class Controller:
    def __init__(self, encoder, motor, pid):
        self._enc = encoder
        self._pid = pid
        self._mot = motor 
      
    def position_loop(self ):
        order_generator=ramp2
        ticks_start = ticks_ms()

        #dry run
        t =  (ticks_ms() - ticks_start) / 1000 # ms -> s
        self._pid.order = order_generator(t)
        position = self._enc.counter
        self._pid.set_signal(t, position)
        cmd = self._pid.get_driving_value()
        
        while(self._pid.set_point != None):

            position = self._enc.counter
            self._pid.set_signal(t, position)
            cmd = self._pid.get_filtered_signal()
                        
            if cmd >= 0:
                self._mot.on(Motor.MotorDirection.FORWARD, min(cmd,100))
            else :
                self._mot.on(Motor.MotorDirection.REVERSE, min(abs(cmd),100))
                
            t =  (ticks_ms() - ticks_start) / 1000 # ms -> s
            sleep_ms(10)
            self._pid.set_point = set_point_generator(t)
        self._mot.off()
              



def ramp2(time):
    """time in s"""
    if time > 4:
        return None
    else:
        return  int(100 * time )
    
def test_asservissement_ch2():
    pin_ch_a = Pin(21)
    pin_ch_b = Pin(20)
    encoder = Encoder(pin_ch_a, pin_ch_b,reverse_direction = False)

    pin_dir = Pin(6)
    pin_speed = Pin(7)
    motor = Motor(pin_dir, pin_speed,reverse_sense=True)
    motor.off()

    Kp = 1

    filter_ = Filter(Kp)

    controller = Controller(encoder, motor, filter_)

#     ramp_inc = generate_ramp(0, 100, 4)
#     plateau = generate_plateau(400,2)
#     ramp_dec = generate_ramp(400, -100, 4)

    controller.position_loop()
#     controller.position_loop(plateau)
#     controller.position_loop(ramp_dec)
    motor.off()

def generate_ramp(initial_position, rate, duration):
    def ramp(time):
        """time in s"""
        if time > duration:
            return None
        else:
            return  int(rate * time + initial_position)

    return lambda t : ramp(t)

# duration in ms
def generate_plateau(initial_position, duration):
    def plateau(time):
        """time in s"""
        if time > duration:
            return None
        else:
            return  int(initial_position)

    return lambda t : plateau(t)


if __name__=="__main__":
    test_asservissement_ch2()
