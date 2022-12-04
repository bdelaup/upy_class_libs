import machine
from romi import Encoder, Motor, Controller, Romi
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
    
def test_circular_buffer():
    buf = CircularBuffer(10, 0)
    for i in range(100):
        buf.push(i)
        print (buf.average)
    print(buf.buffer)
    
    
def test_contact():
    robot = Romi()
    while(True):
        print("L : ", robot.left_contact_state(), "R : ", robot.right_contact_state())
        sleep_ms(1000)
    
def test_command():
    robot = Romi()
    speed = 20
    robot.right_wheel_command(speed)
    robot.left_wheel_command(speed)
    sleep_ms(1000)
    robot.right_wheel_command(0)
    robot.left_wheel_command(0)
    sleep_ms(1000)
    robot.right_wheel_command(-speed)
    robot.left_wheel_command(-speed)
    sleep_ms(1000)
    robot.right_wheel_command(0)
    robot.left_wheel_command(0)
    
    
def test_detection():
    robot = Romi()
    speed = 20
    while (True):
        r_c = robot.left_contact_state()
        l_c = robot.right_contact_state()
        if r_c == False and l_c == False:
            robot.right_wheel_command(speed)
            robot.left_wheel_command(speed)            
        if r_c == True :
            robot.right_wheel_command(speed)
            robot.left_wheel_command(-speed)
            sleep_ms(1000)
        elif l_c == True :
            robot.right_wheel_command(-speed)
            robot.left_wheel_command(speed)
            sleep_ms(1000)
        
        sleep_ms(10)
            
    

if __name__=="__main__":
    test_detection()
    test_command()
    test_contact()
    test_motor_stop()
    test_encoder1()
