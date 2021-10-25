from microbit import *
from utime import sleep_ms


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