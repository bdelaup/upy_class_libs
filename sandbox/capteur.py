from microbit import *
from utime import sleep_ms

CAPTEUR_LIST = {0x19:"accelerometer", 0x1e : "Magnetometre", 0x3e:"LCD", 0x62:"RGB", 0x50:"Pulsation"}
def scan_capteurs():
    for adresse in i2c.scan():
        if adresse in CAPTEUR_LIST:
            print(adresse, " : ", CAPTEUR_LIST[adresse])
        else :
            print(adresse, " : inconnue")

class CapteurPulsation():
    def __init__(self, delay=10, debug=False):
        self._delay = delay
        self._debug = debug
        if (self._debug) :
            print("[debug] Pulsation : initialisation terminee")

    def lire_pulsation(self):
        ppm = i2c.read(0x50, 1, False)
        sleep_ms(self._delay)
        if (self._debug) :
            print("[debug] Pulsation : ", ppm)
        return ord(ppm)