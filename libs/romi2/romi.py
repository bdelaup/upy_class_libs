from utime import sleep_ms
import machine
import micropython
from machine import Pin
import machine
from machine import Timer
from utime import sleep_ms
from time import ticks_us
from filtre import Filter, Filter2, Filter3
from romi_tools import CircularBuffer, generate_ramp, generate_plateau
from encoder import Encoder
from motor import Motor


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
#         self._last_angular_speed_deg_s = 0

        self._print_speed_buffer = CircularBuffer(10, 0)        
        self._print_cmd = 0
        self._print_set_point = 0
        self._print_speed_av = 0
        
        self._loop_status = None
    
            
    def print_timer_soft_handler(self, p):
        """
        First called by interrupt, then schedule the interrupt handler
        asap to avoid allocation problem in IRQ
        """ 
        micropython.schedule(self.print_internals, None)
        
            
    def print_internals(self,_):
        print (\
#                     "cmd:", self._print_cmd \
                   "set_point", self._print_set_point\
#                    ,"speed:",angular_speed_deg_s \
                   ,"speed_av", self._print_speed_av\
#                    ,"time_us:", current_time_us  \
#                    ,"pos:", current_position\
#                    ,"delta_pos",delta_pos\
#                    ,"buffer",self._speed_buffer.buffer\
                   
            )
            
        
    def speed_loop(self, set_point_generator):
        # Manage printing
        print_timer = Timer( period=100, mode=Timer.PERIODIC, callback=self.print_timer_soft_handler)
        
        # Warm up variables
        self.warmup(set_point_generator)

        # Loop timer
        while self.speed_step() != False:            
            sleep_ms(1)

        print_timer.deinit()
        self._mot.off()
    
    def warmup(self, set_point_generator):
        self._ticks_start_us = ticks_us()
        self._last_angular_speed_deg_s=0
        self._last_time_us = self._ticks_start_us -1
        
        self._last_position = self._enc._counter
        self._set_point_generator = set_point_generator
            
    def speed_step(self):
        # Get current values
        current_position = self._enc._counter
        current_time_us =  ticks_us() - self._ticks_start_us
        current_time_s = current_time_us / 1000000
        
        # Get variations
        delta_pos = current_position - self._last_position
        delta_time_us = current_time_us - self._last_time_us
        
        # Compute speed
        angular_speed_deg_us = delta_pos / delta_time_us
        angular_speed_deg_s = 1000000 * angular_speed_deg_us
                
        self._pid.order = self._set_point_generator(current_time_s)
        if (self._pid.order == None):
            return False            
        
        self._pid.set_signal(angular_speed_deg_s, current_time_s)
        cmd = round(self._pid.get_filtered_signal())
        
        # Set motor speed
        if cmd >= 0:
            self._mot.on(Motor.MotorDirection.FORWARD, min(cmd,100))
        else :
            self._mot.on(Motor.MotorDirection.REVERSE, min(abs(cmd),100))
            
        # Store current values            
        self._last_time_us =  current_time_us
        self._last_position = current_position
        
        # Set display variables
        self._print_cmd = cmd
        self._print_set_point = self._pid.order
        self._print_speed_buffer.push(angular_speed_deg_s) 
        self._print_speed_av = self._print_speed_buffer.average

        return True
            
class DualChannelController:
    def __init__(self, left_channel, right_channel):
        self._lch = left_channel
        self._rch = right_channel
        
    def print_timer_cb(self, _):
        self._lch.print_timer_soft_handler(None)
        self._rch.print_timer_soft_handler(None)
        
    def speed_loop(self, set_point_generator_lch, set_point_generator_rch):
        # Manage printing
        print_timer = Timer( period=100, mode=Timer.PERIODIC, callback=self.print_timer_cb)

        # Warm up variables
        self._lch.warmup(set_point_generator_lch)
        self._rch.warmup(set_point_generator_rch)
        
        # Main loop
        rret = True
        lret = True
        while (rret==True and lret==True):
            sleep_ms(1)
            rret = self._lch.speed_step()
            sleep_ms(1)
            lret = self._rch.speed_step()

        self._lch._mot.off()
        self._rch._mot.off()
        print_timer.deinit()

def test_asservissement_ch2_right_speed():
    
    pin_ch_a = Pin(21)
    pin_ch_b = Pin(20)
    encoder = Encoder(pin_ch_a, pin_ch_b,reverse_direction = False)

    pin_dir = Pin(6)
    pin_speed = Pin(7)
    motor = Motor(pin_dir, pin_speed,reverse_sense=True)
    motor.off()

    filter = Filter3(kp=0.5, ki = 0.05, kd = 0.0001, average_nb_values = 2)

    controller = Controller(encoder, motor, filter)

    ramp_inc = generate_ramp(0, 300, 1)
    plateau = generate_plateau(300,5)
    ramp_dec = generate_ramp(300, -300, 1)

    controller.speed_loop(ramp_inc)
    controller.speed_loop(plateau)
    controller.speed_loop(ramp_dec)
    
def test_asservissement_ch1_left_speed():
    
    pin_ch_a = Pin(18)
    pin_ch_b = Pin(19)
    encoder = Encoder(pin_ch_a, pin_ch_b,reverse_direction = True)

    pin_dir = Pin(8)
    pin_speed = Pin(9)
    motor = Motor(pin_dir, pin_speed,reverse_sense=True)
    motor.off()

    filter = Filter3(kp=0.5, ki = 0.05, kd = 0.0001, average_nb_values = 2)

    controller = Controller(encoder, motor, filter)

    ramp_inc = generate_ramp(0, 20, 15)
    plateau = generate_plateau(300,5)
    ramp_dec = generate_ramp(300, -300, 1)

    controller.speed_loop(ramp_inc)
    controller.speed_loop(plateau)
    controller.speed_loop(ramp_dec)


def test_asservissement_ch1ch2_speed():
    # Left wheel
    l_pin_ch_a = Pin(18)
    l_pin_ch_b = Pin(19)
    l_encoder = Encoder(l_pin_ch_a, l_pin_ch_b,reverse_direction = True)
    
    l_pin_dir = Pin(8)
    l_pin_speed = Pin(9)
    l_motor = Motor(l_pin_dir, l_pin_speed,reverse_sense=True)
    l_motor.off()

    l_filter = Filter3(kp=0.5, ki = 0.05, kd = 0.0001, average_nb_values = 2)

    l_controller = Controller(l_encoder, l_motor, l_filter)
    
    # Right wheel
    r_pin_ch_a = Pin(21)
    r_pin_ch_b = Pin(20)
    r_encoder = Encoder(r_pin_ch_a, r_pin_ch_b,reverse_direction = False)
    
    r_pin_dir = Pin(6)
    r_pin_speed = Pin(7)
    r_motor = Motor(r_pin_dir, r_pin_speed,reverse_sense=True)
    r_motor.off()

    r_filter = Filter3(kp=0.5, ki = 0.05, kd = 0.0001, average_nb_values = 2)

    r_controller = Controller(r_encoder, r_motor, r_filter)
    
    # Both wheels
    lr_controller = DualChannelController(l_controller, r_controller)
    
    
    ramp_inc = generate_ramp(0, 20, 15)
    plateau = generate_plateau(50,5)
    ramp_dec = generate_ramp(50, -50, 1)    

    lr_controller.speed_loop(ramp_inc, ramp_inc)
    lr_controller.speed_loop(plateau, plateau)
    lr_controller.speed_loop(ramp_dec, ramp_dec)
    
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

class Romi:
    def __init__(self, kp_in=0.5, ki_in = 0.05, kd_in = 0.0001, l_contact = 27, r_contact = 28):
        # Left wheel
        l_pin_ch_a = Pin(18)
        l_pin_ch_b = Pin(19)
        self.l_encoder = Encoder(l_pin_ch_a, l_pin_ch_b,reverse_direction = True)
        
        l_pin_dir = Pin(8)
        l_pin_speed = Pin(9)
        self.l_motor = Motor(l_pin_dir, l_pin_speed,reverse_sense=True)
        self.l_motor.off()

        l_filter = Filter3(kp=kp_in, ki = ki_in, kd = kd_in, average_nb_values = 2)

        l_controller = Controller(self.l_encoder, self.l_motor, l_filter)
        
        # Right wheel
        r_pin_ch_a = Pin(21)
        r_pin_ch_b = Pin(20)
        self.r_encoder = Encoder(r_pin_ch_a, r_pin_ch_b,reverse_direction = False)
        
        r_pin_dir = Pin(6)
        r_pin_speed = Pin(7)
        self.r_motor = Motor(r_pin_dir, r_pin_speed,reverse_sense=True)
        self.r_motor.off()

        r_filter = Filter3(kp_in, ki = ki_in, kd = kd_in, average_nb_values = 2)

        r_controller = Controller(self.r_encoder, self.r_motor, r_filter)
        
        # Both wheels
        self.lr_controller = DualChannelController(l_controller, r_controller)
        
        # Contact        
        self.l_contact = Pin(l_contact, Pin.IN, Pin.PULL_DOWN)     
        self.r_contact = Pin(r_contact, Pin.IN, Pin.PULL_DOWN)
        
    # Asservissement
    def move(self, l_set_point, r_set_point):
        self.lr_controller.speed_loop(l_set_point, r_set_point)
               
    def right_wheel_command(self, s):
        if s == 0:
            self.r_motor.off()
#             print("s = 0")
        elif s > 0 :
#             print("s > 0", s)
            self.r_motor.on(Motor.MotorDirection.FORWARD,s)
        else :
#             print("s < 0", s, -s)
            self.r_motor.on(Motor.MotorDirection.REVERSE,-s)
            
    def left_wheel_command(self, s):
        if s == 0:
            self.l_motor.off()        
        elif s > 0 :   
            self.l_motor.on(Motor.MotorDirection.FORWARD,s)
        else :
            self.l_motor.on(Motor.MotorDirection.REVERSE,-s)

    def left_contact_state(self):        
        return self.l_contact.value() == 1
    
    def right_contact_state(self):
        return self.r_contact.value() == 1
    
    def left_coder_position(self):
        return self.l_encoder.counter
    
    def right_coder_position(self):
        return self.r_encoder.counter

        
if __name__=="__main__":
    emergency_stop()
#     test_asservissement_ch2_right_speed()
#     test_asservissement_ch1_left_speed()
#     test_asservissement_ch1ch2_speed()
    robot = Romi()
    
    ramp_inc = generate_ramp(0, 20, 15)
    plateau = generate_plateau(300,5)
    ramp_dec = generate_ramp(300, -300, 1)
    
    robot.move(ramp_inc, ramp_inc)
    robot.move(plateau, plateau)
    robot.move(ramp_dec, ramp_dec)
