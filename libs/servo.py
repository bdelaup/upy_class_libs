from stiutils import *

class Servo:
    """Generic Servo class"""
    def __init__(self, pin, period_servo=20, time_min=0.6, time_max=2.5):
        self._pin = pin
        self._period_servo=period_servo
        self._time_min=time_min
        self._time_max=time_max
        self._pin.set_analog_period(self._period_servo)
    
    def set_angle(self, angle):
        mli = interpolate(
            angle, 
            [0, 180], 
            [self._time_min/self._period_servo*1024, self._time_max/self._period_servo*1024])
        self._pin.write_analog(int(mli))
    
    def stop(self):
        self._pin.write_digital(0)

        


def tests():
    class PinStub:
        def __init__(self):
            self.analog = 0
            self.period = 0

        def set_analog_period(self, p):
            self.period = p
        
        def write_analog(self, a):
            self.analog = a

    pin = PinStub()
    servo = Servo(pin, 10, 1, 2)

    servo.set_angle(0)
    assert pin.analog == 102

    servo.set_angle(180)
    assert pin.analog == 204

def test_microbit():
    from microbit import pin2, sleep
    servo = Servo(pin=pin2)
    while (True):
        servo.set_angle(30)
        sleep(1)
        servo.set_angle(90)
        sleep(1)
    

if __name__ == "__main__":
    #tests()
    test_microbit()
    