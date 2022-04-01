
from microbit import *
# from lycee_utils.py import *

class KitronikMotorDriver :
    
    class MotorDirection(enumerate) :
        Forward = 1
        Reverse = 2

    class Motors(enumerate) :
        Motor1 = 1
        Motor2 = 2

    def __init__(self, pin_ch_A, pin_ch_B, scale=1024, direction = MotorDirection.Forward) -> None:
        if direction == self.MotorDirection.Forward:
            self._pin_ch_A = pin_ch_A
            self._pin_ch_B = pin_ch_B
        else :
            self._pin_ch_A = pin_ch_B
            self._pin_ch_B = pin_ch_A

        self._scale=scale
        self._direction=direction
        
    def motor_off(self):
        self._pin_ch_A.write_analog(0)
        self._pin_ch_B.write_analog(0)

    def set_speed(self, speed_ratio):
        speed = speed_ratio * 1024//100
        if speed > 0:
            self._pin_ch_A.write_analog(0)
            self._pin_ch_B.write_analog(speed)

        elif speed < 0:
            self._pin_ch_A.write_analog(abs(speed))
            self._pin_ch_B.write_analog(0)
        else:
            self._pin_ch_A.write_analog(0)
            self._pin_ch_B.write_analog(0)

def test():
    
    moteur = KitronikMotorDriver (pin8, pin12)
    moteur.motor_off()
    for i in range (100):
        moteur.set_speed(i)
        sleep(10)

    moteur.motor_off()
    sleep(1000)

    for i in range (100):
        moteur.set_speed(-i)
        sleep(10)
    moteur.motor_off()

if __name__=="__main__":
    test()