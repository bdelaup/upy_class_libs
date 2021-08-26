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
    
    def position_loop(self, set_point_generator):
        ticks_start = ticks_ms()

        #dry run
        t =  (ticks_ms() - ticks_start) / 1000 # ms -> s
        self._pid.set_point = set_point_generator(t)
        position = self._enc.counter
        self._pid.update(t, position)
    
        
        while(self._pid.set_point != None):
            t =  (ticks_ms() - ticks_start) / 1000 # ms -> s
            self._pid.set_point = set_point_generator(t)

            position = self._enc.counter
            self._pid.update(t, position)
            cmd = self._pid.generate_driving_value()

            if cmd >= 0:
                self._mot.on(Motor.MotorDirection.FORWARD, cmd)
            else :
                self._mot.on(Motor.MotorDirection.REVERSE, abs(cmd))
            
            sleep_ms(1)


def test_asservissement():
    pin_ch_a = Pin(27)
    pin_ch_b = Pin(26)
    encoder = Encoder(pin_ch_a, pin_ch_b)

    pin_dir = Pin(8)
    pin_speed = Pin(9)
    motor = Motor(pin_dir, pin_speed)

    Kp = 3
    Ki = 0
    Kd = 0
    filter = Filter(Kp, Ki, Kd)

    controler = Controler(encoder, motor, filter)

    ramp_inc = generate_ramp(0, 10, 4)
    plateau = generate_plateau(40,2)
    ramp_dec = generate_ramp(40, -10, 4)

    controler.position_loop(ramp_inc)
    controler.position_loop(plateau)
    controler.position_loop(ramp_dec)

if __name__ == "__main__":
    test_asservissement()