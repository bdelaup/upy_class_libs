from utime import sleep_ms, ticks_add
from machine import Pin
from machine import Timer
from time import ticks_ms, ticks_diff

from encoder import Encoder
from motor import Motor, test_motor_stop
from pid import Filter
from setpoint_generator import generate_plateau, generate_ramp

class Controler:
    def __init__(self, encoder, motor, pid):
        self._enc = encoder
        self._pid = pid
        self._mot = motor

        self._duration_timer = Timer()          
    
    def position_loop(self, set_point_generator):
        ticks_start = ticks_ms()

        #dry run
        t =  (ticks_ms() - ticks_start) / 1000 # ms -> s
        self._pid.set_point = set_point_generator(t)
        position = self._enc.counter
        self._pid.update(t, position)
        cmd = self._pid.get_driving_value()
    
        
        while(self._pid.set_point != None):
#             print ("time : ", t, "pos : ", position,"Cmd : ", cmd, "set_point : ", self._pid.set_point, "Epsi : ", self._pid._last_epsilon)
            position = self._enc.counter
            self._pid.update(t, position)
            cmd = self._pid.get_driving_value()
            
            
            if cmd >= 0:
                self._mot.on(Motor.MotorDirection.FORWARD, min(cmd,100))
            else :
                self._mot.on(Motor.MotorDirection.REVERSE, min(abs(cmd),100))
                
            t =  (ticks_ms() - ticks_start) / 1000 # ms -> s
            sleep_ms(10)
            self._pid.set_point = set_point_generator(t)
        self._mot.off()
        
    def position_step(self, ticks_start, set_point_generator):

        #dry run
        t =  (ticks_ms() - ticks_start) / 1000 # ms -> s
        self._pid.set_point = set_point_generator(t)

        if (self._pid.set_point != None):            
            position = self._enc.counter
            self._pid.update(t, position)
            cmd = self._pid.get_driving_value()            
            
            if cmd >= 0:
                self._mot.on(Motor.MotorDirection.FORWARD, min(cmd,100))
            else :
                self._mot.on(Motor.MotorDirection.REVERSE, min(abs(cmd),100))
            print ("Time : ", t, "pos : ", position,"Cmd : ", cmd, "set_point : ", self._pid.set_point, "Epsi : ", self._pid._last_epsilon)    
            return True
        else:
            return False

class ControlerMultiChannel:
    def __init__(self, ch1, ch2):
        self._ch1 = ch1
        self._ch2 = ch2
    
    def position_loop(self, set_point_generator_ch1, set_point_generator_ch2):
        ticks_start = ticks_ms()
        ret1 = True
        ret2 = True
        while (ret1==True and ret2==True):
#         while (ret1 == True):
            ret1 = self._ch1.position_step(ticks_start, set_point_generator_ch1)
            ret2 = self._ch2.position_step(ticks_start, set_point_generator_ch2)
            sleep_ms(10)
#             print ("Ret loop 1 : ", ret1, "Ret loop 2 : ", ret2)
        
            
            
def test_asservissement_2chan():
    ch1_pin_ch_a = Pin(19)
    ch1_pin_ch_b = Pin(18)
    ch1_encoder = Encoder(ch1_pin_ch_a, ch1_pin_ch_b,reverse_direction = False)

    ch1_pin_dir = Pin(8)
    ch1_pin_speed = Pin(9)
    ch1_motor = Motor(ch1_pin_dir, ch1_pin_speed,reverse_sense=True)
    ch1_motor.off()

    ch2_pin_ch_a = Pin(21)
    ch2_pin_ch_b = Pin(20)
    ch2_encoder = Encoder(ch2_pin_ch_a, ch2_pin_ch_b,reverse_direction = False)

    ch2_pin_dir = Pin(6)
    ch2_pin_speed = Pin(7)
    ch2_motor = Motor(ch2_pin_dir, ch2_pin_speed,reverse_sense=True)
    ch2_motor.off()

    Kp = 1
    Ki = 0
    Kd = 0
    ch1_filter = Filter(Kp, Ki, Kd)
    ch2_filter = Filter(Kp, Ki, Kd)

    ch1_controler = Controler(ch1_encoder, ch1_motor, ch1_filter)
    ch2_controler = Controler(ch2_encoder, ch2_motor, ch2_filter)

    dual_controler = ControlerMultiChannel(ch1_controler, ch2_controler)

#     ramp_inc = generate_ramp(0, 100, 1)
    ramp_inc = generate_ramp(0, 100, 4)
    plateau = generate_plateau(400,2)
    ramp_dec = generate_ramp(400, -100, 4)

    dual_controler.position_loop(ramp_inc, ramp_inc)
    dual_controler.position_loop(plateau, plateau)
    dual_controler.position_loop(ramp_dec, ramp_dec)
    ch1_motor.off()
    ch1_motor.off()

def test_asservissement_ch1():
    pin_ch_a = Pin(19)
    pin_ch_b = Pin(18)
    encoder = Encoder(pin_ch_a, pin_ch_b,reverse_direction = False)

    pin_dir = Pin(8)
    pin_speed = Pin(9)
    motor = Motor(pin_dir, pin_speed,reverse_sense=True)
    motor.off()

    Kp = 1
    Ki = 0
    Kd = 0
    filter = Filter(Kp, Ki, Kd)

    controler = Controler(encoder, motor, filter)

    ramp_inc = generate_ramp(0, 100, 4)
    plateau = generate_plateau(400,2)
    ramp_dec = generate_ramp(400, -100, 4)

    controler.position_loop(ramp_inc)
    controler.position_loop(plateau)
    controler.position_loop(ramp_dec)
    motor.off()
    
    
def test_asservissement_ch2():
    pin_ch_a = Pin(21)
    pin_ch_b = Pin(20)
    encoder = Encoder(pin_ch_a, pin_ch_b,reverse_direction = False)

    pin_dir = Pin(6)
    pin_speed = Pin(7)
    motor = Motor(pin_dir, pin_speed,reverse_sense=True)
    motor.off()

    Kp = 1
    Ki = 0
    Kd = 0
    filter = Filter(Kp, Ki, Kd)

    controler = Controler(encoder, motor, filter)

    ramp_inc = generate_ramp(0, 100, 4)
    plateau = generate_plateau(400,2)
    ramp_dec = generate_ramp(400, -100, 4)

    controler.position_loop(ramp_inc)
    controler.position_loop(plateau)
    controler.position_loop(ramp_dec)
    motor.off()

def test_asservissement_ch1_2():
    
    pin_ch_a = Pin(19)
    pin_ch_b = Pin(18)
    encoder = Encoder(pin_ch_a, pin_ch_b,reverse_direction = False)

    pin_dir = Pin(8)
    pin_speed = Pin(9)
    motor = Motor(pin_dir, pin_speed,reverse_sense=True)
    motor.off()

    Kp = 1
    filter = Filter(Kp, 0, 0)

    controler = Controler(encoder, motor, filter)

    ramp_inc = generate_ramp(0, 100, 1)

    controler.position_loop(ramp_inc)
    
def test_asservissement_ch2_2():
    
    pin_ch_a = Pin(21)
    pin_ch_b = Pin(20)
    encoder = Encoder(pin_ch_a, pin_ch_b,reverse_direction = False)

    pin_dir = Pin(6)
    pin_speed = Pin(7)
    motor = Motor(pin_dir, pin_speed,reverse_sense=True)
    motor.off()

    Kp = 1
    filter = Filter(Kp, 0, 0)

    controler = Controler(encoder, motor, filter)

    ramp_inc = generate_ramp(0, 100, 1)

    controler.position_loop(ramp_inc)

if __name__ == "__main__":
#     test_asservissement_ch1_2()
#     print("---")
#     test_asservissement_ch2_2()
#     print("---")
#     test_asservissement_ch1()
#     print("---")
#     test_asservissement_ch2()
    print("---")
    test_asservissement_2chan()
    print("---")
    test_motor_stop()  

    