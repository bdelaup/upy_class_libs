# LSM6DSOX Basic Example.
import time
from lsm6dsox import LSM6DSOX

from microbit import i2c

lsm = LSM6DSOX(i2c)

while True:
    print("Accelerometer: x:{:>8.3f} y:{:>8.3f} z:{:>8.3f}".format(*lsm.read_accel()))
    print("Gyroscope:     x:{:>8.3f} y:{:>8.3f} z:{:>8.3f}".format(*lsm.read_gyro()))
    print("")
    time.sleep_ms(100)