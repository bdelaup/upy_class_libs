import machine
from romi import Encoder, Motor, Controller
from time import sleep_ms

def test_motor_stop():
    pin_dir = machine.Pin(9)
    pin_speed = machine.Pin(8)
    motor = Motor(pin_speed, pin_dir)
    motor.off()
    
    pin_dir = machine.Pin(7)
    pin_speed = machine.Pin(6)
    motor = Motor(pin_speed, pin_dir)
    motor.off()   

def test_encoder1():
    pin_channnel_a=machine.Pin(21)
    pin_channnel_b=machine.Pin(20)
    encoder = Encoder(pin_channnel_a, pin_channnel_b)

    while True:
        print("counter :", encoder.counter)
        sleep_ms(100)
        
def test_encoder2():
    pin_channnel_a=machine.Pin(18)
    pin_channnel_b=machine.Pin(19)
    encoder = Encoder(pin_channnel_a, pin_channnel_b)

    while True:
        print("counter :", encoder.counter)
        sleep_ms(100)
        
def test_motor1():
    pin_dir = machine.Pin(6)
    pin_speed = machine.Pin(7)
    motor = Motor(pin_dir, pin_speed, reverse_sense = False)
    motor.off()
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

def test_motor2():
    pin_dir = machine.Pin(8)
    pin_speed = machine.Pin(9)
    motor = Motor(pin_dir, pin_speed, reverse_sense = False)
    motor.off()
    sleep_ms(1000)   
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

if __name__=="__main__":

    test_motor_stop()
    test_encoder1()
