from microbit import pin1, pin2, pin0, button_a, button_b
from servo import Servo
from utime import sleep, sleep_ms

PERIODE_SERVO = 20
FRACTION_MIN = 0.6
FRACTION_MAX = 2.5

capteur_d = pin1
capteur_g = pin2
servo = Servo(pin0, PERIODE_SERVO, FRACTION_MIN, FRACTION_MAX)



def test_servo():
    while True: 
        # Start and stop using buttons
        if button_a.was_pressed():
            servo.stop()
            while not button_b.was_pressed() :
                pass
        servo.set_angle(0)
        sleep(1)
        servo.set_angle(90)
        sleep(1)
        servo.set_angle(180)
        sleep(1)

def test_capteur():
     print ([capteur_d.read_analog(), capteur_g.read_analog()])

def run():
    angle = 0
    while True: 
        
        # Start and stop using buttons
        if button_a.was_pressed():
            servo.stop()
            while not button_b.was_pressed() :
                pass
        
        if abs(capteur_g.read_analog() - capteur_d.read_analog() ) < 50:
            servo.stop()

        elif capteur_g.read_analog() > capteur_d.read_analog():
            angle = min(angle+1, 180)
            servo.set_angle(angle)
            
        elif capteur_g.read_analog() < capteur_d.read_analog():
            angle = max(angle-1, 0)
            servo.set_angle(angle)
            
        
        sleep_ms(1)
        print(angle)





run()

    
    



