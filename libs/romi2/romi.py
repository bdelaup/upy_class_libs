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
        
#         self._display_freq = 10
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
            
    def speed_step_timer_soft_handler(self, p):
        """
        First called by interrupt, then schedule the interrupt handler
        asap to avoid allocation problem in IRQ
        """ 
        micropython.schedule(self.speed_step, None)
        
    def speed_loop(self, set_point_generator):
        # Manage printing
        print_timer = Timer( period=100, mode=Timer.PERIODIC, callback=self.print_timer_soft_handler)
        
        # Warm up variables
        self._ticks_start_us = ticks_us()
        self._last_angular_speed_deg_s=0
        self._last_time_us = self._ticks_start_us -1
        
        self._last_position = self._enc._counter
        self._set_point_generator = set_point_generator

        # Loop timer
        while self.speed_step() != False:            
            sleep_ms(1)

        print_timer.deinit()
        self._mot.off()
            
    def speed_step(self, _ = None):
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

    filter = Filter3(kp=0.5, ki = 0.05, kd = 0.0001, average_nb_values = 2)

    controller = Controller(encoder, motor, filter)

    ramp_inc = generate_ramp(0, 300, 1)
    plateau = generate_plateau(300,5)
    ramp_dec = generate_ramp(300, -300, 1)

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
#     test_circular_buffer()
    test_asservissement_ch2_speed()
    # test_asservissement_ch2()
