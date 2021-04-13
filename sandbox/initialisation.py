# Installation des bibliothèque contenant
# les sous programme tels que capteur ou ou lcd
from microbit import *
from ecran import afficheur_lcd
from capteur import scan_capteurs, CapteurPulsation
from utime import sleep_ms

i2c.init(freq=100000)

print("Initialisation effectuee ...")
#scan_capteurs()