from utime import sleep_ms, ticks_add
from machine import Pin
from machine import Timer
from time import ticks_ms, ticks_diff

from encoder import Encoder
from motor import Motor
from pid import Filter
from setpoint_generator import generate_plateau, generate_ramp

class Controler:
    def __init__(self, encoder, motor, pid):
        self._enc = encoder
        self._pid = pid
        self._mot = motor

        self._duration_timer = Timer()
    
    def position_step(self, ticks_start, set_point_generator):

        #dry run
        t =  (ticks_ms() - ticks_start) / 1000 # ms -> s
        self._pid.set_point = set_point_generator(t)
        position = self._enc.counter
        self._pid.update(t, position)
        cmd = self._pid.get_driving_value()
    
        
        if (self._pid.set_point != None):
            position = self._enc.counter
            self._pid.update(t, position)
            cmd = self._pid.get_driving_value()            
            
            if cmd >= 0:
                self._mot.on(Motor.MotorDirection.FORWARD, min(cmd,100))
            else :
                self._mot.on(Motor.MotorDirection.REVERSE, min(abs(cmd),100))
        else:
            return None
                
    
    def position_loop(self, set_point_generator):
        ticks_start = ticks_ms()

        #dry run
        t =  (ticks_ms() - ticks_start) / 1000 # ms -> s
        self._pid.set_point = set_point_generator(t)
        position = self._enc.counter
        self._pid.update(t, position)
        cmd = self._pid.get_driving_value()
    
        
        while(self._pid.set_point != None):
            position = self._enc.counter
            self._pid.update(t, position)
            cmd = self._pid.get_driving_value()            
            
            if cmd >= 0:
                self._mot.on(Motor.MotorDirection.FORWARD, min(cmd,100))
            else :
                self._mot.on(Motor.MotorDirection.REVERSE, min(abs(cmd),100))
                
            t =  (ticks_ms() - ticks_start) / 1000 # ms -> s
            self._pid.set_point = set_point_generator(t)

class ControlerMultiChannel:
    def __init__(self, ch1, ch2):
        self._ch1 = ch1
        self._ch2 = ch2
    
    def position_loop(self, set_point_generator_ch1, set_point_generator_ch2):
        ticks_start = ticks_ms()
        ret1 = 1
        ret2 = 1
        while (ret1 != None and ret2!=None):
            ret1 = self._ch1.position_step(ticks_start, set_point_generator_ch1)
            ret2 = self._ch2.position_step(ticks_start, set_point_generator_ch2)
            


def test_asservissement():
    pin_ch_a = Pin(27)
    pin_ch_b = Pin(26)
    encoder = Encoder(pin_ch_a, pin_ch_b)

    pin_dir = Pin(8)
    pin_speed = Pin(9)
    motor = Motor(pin_dir, pin_speed)
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

def test_asservissement2():
    ch1_pin_ch_a = Pin(27)
    ch1_pin_ch_b = Pin(26)
    encoder1 = Encoder(ch1_pin_ch_a, ch1_pin_ch_b)

    ch1_pin_dir = Pin(9)
    ch1_pin_speed = Pin(8)
    motor1 = Motor(ch1_pin_dir, ch1_pin_speed)
    motor1.off()

    ch2_pin_ch_a = Pin(20)
    ch2_pin_ch_b = Pin(21)    
    encoder2 = Encoder(ch2_pin_ch_a, ch2_pin_ch_b)

    ch2_pin_dir = Pin(18)
    ch2_pin_speed = Pin(19)
    motor2 = Motor(ch2_pin_dir, ch2_pin_speed)
    motor2.off()

    Kp = 1
    Ki = 0
    Kd = 0
    filter = Filter(Kp, Ki, Kd)

    controler1 = Controler(encoder1, motor1, filter)
    controler2 = Controler(encoder2, motor2, filter)

    dual_controler = ControlerMultiChannel(controler1, controler2)

    ramp_inc = generate_ramp(0, 100, 4)
    plateau = generate_plateau(400,2)
    ramp_dec = generate_ramp(400, -100, 4)

    dual_controler.position_loop(ramp_inc)
    dual_controler.position_loop(plateau)
    dual_controler.position_loop(ramp_dec)
    motor1.off()
    motor2.off()

if __name__ == "__main__":
    # test_asservissement()
    test_asservissement2()