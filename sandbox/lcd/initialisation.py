# Installation des bibliothèque contenant
# les sous programme tels que capteur ou ou lcd
from microbit import *
from lcd import lcd_display
from heartbeat import CapteurPulsation
from i2c_utils import scan_i2c_sensors
from time import sleep_ms


# i2c.init(freq=100000)

print("Initialisation effectuee ...")
scan_i2c_sensors()