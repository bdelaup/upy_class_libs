
# from micropbit import *
from lycee_utils.py import *
class KitronikMotorDriver :
     class MotorDirection(enumerate) :
        Forward = 1
        Reverse = 2

    class Motors(enumerate) :
        Motor1 = 1
        Motor2 = 2

    def motorOn(self, motor, direction, speed):
        self.MotorDirection.Forward


#     OutputVal = Math.clamp(0, 100, speed) * 10;

#         switch (motor) {
#             case Motors.Motor1: /*Motor 1 uses Pins 8 and 12*/
#                 switch (dir) {
#                     case MotorDirection.Forward:
#                         pins.analogWritePin(AnalogPin.P8, OutputVal);
#                         pins.digitalWritePin(DigitalPin.P12, 0); /*Write the low side digitally, to allow the 3rd PWM to be used if required elsewhere*/
#                         break
#                     case MotorDirection.Reverse:
#                         pins.analogWritePin(AnalogPin.P12, OutputVal);
#                         pins.digitalWritePin(DigitalPin.P8, 0);
#                         break
#                 }

#                 break;
#             case Motors.Motor2: /*Motor 2 uses Pins 0 and 16*/
#                 switch (dir) {
#                     case MotorDirection.Forward:
#                         pins.analogWritePin(AnalogPin.P0, OutputVal);
#                         pins.digitalWritePin(DigitalPin.P16, 0); /*Write the low side digitally, to allow the 3rd PWM to be used if required elsewhere*/
#                         break
#                     case MotorDirection.Reverse:
#                         pins.analogWritePin(AnalogPin.P16, OutputVal);
#                         pins.digitalWritePin(DigitalPin.P0, 0);
#                         break
#                 }

#                 break;
#         }
#     }
# 	/**
#      * Turns off the motor specified by eMotors
#      * @param motor :which motor to turn off
#      */
#     //% blockId=kitronik_motordriver_motor_off
#     //%block="turn off %motor"
#     export function motorOff(motor: Motors): void {
#         switch (motor) {
#             case Motors.Motor1:
#                 pins.digitalWritePin(DigitalPin.P8, 0);
#                 pins.digitalWritePin(DigitalPin.P12, 0);
#                 break
#             case Motors.Motor2:
#                 pins.digitalWritePin(DigitalPin.P0, 0);
#                 pins.digitalWritePin(DigitalPin.P16, 0);
#                 break
#         }
#     }
# }
