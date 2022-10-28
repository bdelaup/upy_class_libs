from utime import sleep_ms
import machine
import micropython
from machine import PWM, Pin
import machine
from machine import Timer
from utime import sleep_ms
from time import ticks_ms, ticks_diff, ticks_us


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
        
    def signal_soft_handler(self, p):
        """
        First called by interrupt, then schedule the interrupt handler
        asap to avoid allocation problem in IRQ
        """ 
        micropython.schedule(self.signal_handler, self._pin_channel_b.value())

    def signal_handler(self, p):
        """ Actual implementation of interupt routine"""
        if p == 0:
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
        self._epsilon = 0

    
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
#         print(self._order, value)
        self._epsilon = self._order-value
        
    def get_filtered_signal(self):
        """
        returns the filtered signal
        """
       
        return self._kp * self._epsilon

class Controller:
    def __init__(self, encoder, motor, pid):
        self._enc = encoder
        self._pid = pid
        self._mot = motor
        self._last_position = 0
        self._last_time_ms = 0
        self._ticks_start_us = 0
        self._set_point_generator = None
        self._status = None
      
#     def position_loop(self, order_generator):
#         ticks_start = ticks_ms()
# 
#         #dry run
#         t =  (ticks_ms() - ticks_start) / 1000 # ms -> s
#         self._pid.order = order_generator(t)
#         
#         while(self._pid.order != None):
#             
#             position = self._enc._counter
#             self._pid.set_signal(position)
#             cmd = self._pid.get_filtered_signal()
#                         
#             if cmd >= 0:
#                 self._mot.on(Motor.MotorDirection.FORWARD, min(cmd,100))
#             else :
#                 self._mot.on(Motor.MotorDirection.REVERSE, min(abs(cmd),100))
#             
# 
#             t =  (ticks_ms() - ticks_start) / 1000 # ms -> s
#             self._pid.order = order_generator(t)
#             
#             
#         self._mot.off()
        
#     def speed_step(self, ticks_start_us, set_point_generator):
#             position = self._enc._counter
#             self._pid.set_signal(position)
#             cmd = self._pid.get_filtered_signal()
#                         
#             if cmd >= 0:
#                 self._mot.on(Motor.MotorDirection.FORWARD, min(cmd,100))
#             else :
#                 self._mot.on(Motor.MotorDirection.REVERSE, min(abs(cmd),100))
#             
# 
#             t =  (ticks_ms() - ticks_start) / 1000 # ms -> s
#             self._pid.order = order_generator(t)
#             if self._pid.order == None:
#                 return False
#             else :
#                 return True
            
    def timer_soft_handler(self, p):
        """
        First called by interrupt, then schedule the interrupt handler
        asap to avoid allocation problem in IRQ
        """ 
        micropython.schedule(self.speed_step, None)

    def speed_loop(self, set_point_generator):
        ticks_start_us = ticks_us()
        self.speed_warmup(ticks_start_us, set_point_generator)
        
        self._ticks_start_us = ticks_start_us
        self._set_point_generator = set_point_generator
        

            
        timer = Timer(period=100, mode=Timer.PERIODIC, callback=self.timer_soft_handler)
        
        
        
        while self._status != False:            
            sleep_ms(1000)
 
        timer.deinit()
        self._mot.off()
    
    def speed_warmup(self,ticks_start_us, set_point_generator):
        current_time_us =  ticks_us() - self._ticks_start_us
        current_time_s = current_time_us / 1000000
        self._pid.order = set_point_generator(current_time_s)
        
        self._last_position = self._enc._counter
        self._last_time_us = current_time_us -1        
        
    def speed_step(self, _):
            current_time_us =  ticks_us() - self._ticks_start_us
            current_time_s = current_time_us / 1000000
            if (self._set_point_generator(current_time_s) == None):
                return False
            current_position = self._enc._counter
            current_time_us =  ticks_us() - self._ticks_start_us
            current_time_s = current_time_us / 1000000

            angular_speed_deg_us = (current_position - self._last_position) / ((current_time_us - self._last_time_us))
            angular_speed_deg_s = angular_speed_deg_us * 1000000
            self._pid.order = self._set_point_generator(current_time_s)
            self._pid.set_signal(angular_speed_deg_s)
            cmd = self._pid.get_filtered_signal()
            print (cmd, angular_speed_deg_s, current_time_us , current_position)
            
#             print(self._pid.order, angular_speed_deg_s, cmd)
            if cmd >= 0:
                self._mot.on(Motor.MotorDirection.FORWARD, min(cmd,100))
            else :
                self._mot.on(Motor.MotorDirection.REVERSE, min(abs(cmd),100))
                
            self._last_time_us =  ticks_us() - self._ticks_start_us
            self._last_position = self._enc._counter
            current_time_us =  ticks_us() - self._ticks_start_us
            current_time_s = current_time_us / 1000000
            self._pid.order = self._set_point_generator(current_time_s)
            if self._pid.order == None:
                self._status = False
                return False
            else :
                self._status = True
                return True
            
class ControlerMultiChannel:
    def __init__(self, ch1, ch2):
        self._ch1 = ch1
        self._ch2 = ch2
    
#     def position_loop(self, set_point_generator_ch1, set_point_generator_ch2):
#         ticks_start = ticks_ms()
#         ret1 = True
#         ret2 = True
#         while (ret1==True and ret2==True):
# #         while (ret1 == True):
#             ret1 = self._ch1.position_step(ticks_start, set_point_generator_ch1)
#             ret2 = self._ch2.position_step(ticks_start, set_point_generator_ch2)
#             sleep_ms(10)
# #             print ("Ret loop 1 : ", ret1, "Ret loop 2 : ", ret2)
#         
    def speed_loop(self, set_point_generator_ch1, set_point_generator_ch2):
        ticks_start_us = ticks_us()
        
        self._ch1.speed_warmup(ticks_start_us, set_point_generator_ch1)
        self._ch2.speed_warmup(ticks_start_us, set_point_generator_ch2)
        
        ret1 = True
        ret2 = True

        while (ret1==True and ret2==True):
            
            ret1 = self._ch1.speed_step(ticks_start_us, set_point_generator_ch1)
            ret2 = self._ch2.speed_step(ticks_start_us, set_point_generator_ch2)


def generate_ramp(initial_position, rate, duration):
    def ramp(time):
        """time in s"""
        if time > duration:
            return None
        else:
            return  round(rate * time + initial_position)

    return lambda t : ramp(t)

# duration in ms
def generate_plateau(initial_position, duration):
    def plateau(time):
        """time in s"""
#         print("time",time, "duration", duration)
        if time > duration:
            return None
        else:
            return  round(initial_position)

    return lambda t : plateau(t)

# def test_asservissement_ch2():
#     pin_ch_a = Pin(21)
#     pin_ch_b = Pin(20)
#     encoder = Encoder(pin_ch_a, pin_ch_b,reverse_direction = False)

#     pin_dir = Pin(6)
#     pin_speed = Pin(7)
#     motor = Motor(pin_dir, pin_speed,reverse_sense=True)
#     motor.off()

#     Kp = 1
#     Ki = 0
#     Kd = 0
#     filter_ = Filter(Kp)

#     Controller = Controller(encoder, motor, filter_)

#     ramp_inc = generate_ramp(0, 100, 4)
#     plateau = generate_plateau(400,2)
#     ramp_dec = generate_ramp(400, -100, 4)

#     Controller.position_loop(ramp_inc)
#     Controller.position_loop(plateau)
#     Controller.position_loop(ramp_dec)
#     motor.off()

def test_asservissement_ch2_speed():
    
    pin_ch_a = Pin(21)
    pin_ch_b = Pin(20)
    encoder = Encoder(pin_ch_a, pin_ch_b,reverse_direction = False)

    pin_dir = Pin(6)
    pin_speed = Pin(7)
    motor = Motor(pin_dir, pin_speed,reverse_sense=True)
    motor.off()

    Kp = 0.3
    filter = Filter(Kp)

    controller = Controller(encoder, motor, filter)

    ramp_inc = generate_ramp(0, 30, 1)
    plateau = generate_plateau(30,5)
    ramp_dec = generate_ramp(30, -30, 1)

    controller.speed_loop(ramp_inc)
    controller.speed_loop(plateau)
    controller.speed_loop(ramp_dec)
    
def test_encoder2():
    pin_channnel_a=machine.Pin(21)
    pin_channnel_b=machine.Pin(20)
    encoder = Encoder(pin_channnel_a, pin_channnel_b)

    while True:
        print("counter :", encoder.counter)
        sleep_ms(100)

def emergency_stop():
    pin_dir = machine.Pin(9)
    pin_speed = machine.Pin(8)
    motor = Motor(pin_speed, pin_dir)
    motor.off()
    
    pin_dir = machine.Pin(7)
    pin_speed = machine.Pin(6)
    motor = Motor(pin_speed, pin_dir)
    motor.off()
    sleep_ms(1000)

if __name__=="__main__":
    emergency_stop()
#     test_encoder2()
    
    test_asservissement_ch2_speed()
    # test_asservissement_ch2()
