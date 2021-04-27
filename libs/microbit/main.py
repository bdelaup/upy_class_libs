# Add your Python code here. E.g.
from microbit import *
from stepper_uln2003 import Driver, Command, Stepper, FULL_ROTATION, HALF_STEP

s1 = Stepper(HALF_STEP, pin13, pin14, pin15, pin16, delay=5)
# s2 = Stepper(HALF_STEP, microbit.pin6, microbit.pin5, microbit.pin4, microbit.pin3, delay=5)
#s1.step(FULL_ROTATION)
#s2.step(FULL_ROTATION)

print("starting")

runner = Driver()
print("runner ok")
#runner.run([Command(s1, FULL_ROTATION, 1), Command(s1, FULL_ROTATION/2, -1)])
print("Command end")
