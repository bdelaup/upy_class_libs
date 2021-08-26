from machine import PWM, Pin
import machine
from utime import sleep_ms

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
        self._pwm.freq(1000)    
        self._pwm.duty_u16(0)

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
            print ("forward")
        else:
            self._pin_dir.off()
            print ("reverse")


    def set_speed(self, duty):
        if duty < 0 or duty > 100:
            return
        duty = round(duty/100 * self._duty_ratio)
        print (duty)
        self._pwm.duty_u16(duty)

    def on(self, direction, duty):
        self.set_direction(direction)
        self.set_speed(duty)

    def off(self):
        self.set_speed(0)

def test_motor():
    pin_dir = machine.Pin(9)
    pin_speed = machine.Pin(8)
    motor = Motor(pin_speed, pin_dir)
    motor.off()
    sleep_ms(5000)   
    for i in range (100):
        print(i)
        motor.on(motor.MotorDirection.FORWARD, i)
        sleep_ms(10)        
    
    for i in range (100):
        print(i)
        motor.on(motor.MotorDirection.FORWARD, 100 - i)
        sleep_ms(10)

    for i in range (100):
        print(i)
        motor.on(motor.MotorDirection.REVERSE, i)
        sleep_ms(10)
        
    for i in range (100):
        print(i)
        motor.on(motor.MotorDirection.REVERSE, 100 - i)
        sleep_ms(10)
        
    motor.off()
    sleep_ms(10000)            

            
if __name__=="__main__":
    test_motor()
    

