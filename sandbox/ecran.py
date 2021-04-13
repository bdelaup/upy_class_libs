# (c) 2019 Christophe Gueneau
from microbit import *
import time

class afficheur_lcd():
    def __init__(self, delay=10, debug=False):
        self._delay = delay
        self._debug = debug
        self.set_register(0x00, 0)
        self.set_register(0x01, 0)
        self.set_register(0x08, 0xAA)
        self.disp_func = 0x04 | 0x08
        time.sleep_ms(50)
        self.cmd(0x20 | self.disp_func)
        time.sleep_us(4500)
        self.cmd(0x20 | self.disp_func)
        time.sleep_us(150)
        self.cmd(0x20 | self.disp_func)
        self.cmd(0x20 | self.disp_func)
        self.disp_ctrl = 0x04 | 0x00 | 0x00
        self.display1(True)
        self.clear()
        self.disp_mode = 0x02 | 0x00
        self.cmd(0x04 | self.disp_mode)
        time.sleep_ms(self._delay)
        self._r=0
        self._g=0
        self._b=0
        self._txt = ""
        self.set_register(0x04, 0)
        self.set_register(0x03, 0)
        self.set_register(0x02, 0)
        if (self._debug) :
            print("[debug] Ecran : initialisation terminee")

    def set_register(self, reg, val):
        val = bytes((reg, val))
        i2c.write(0x62, val)
        time.sleep_ms(self._delay)


    def color(self, r, g, b):
        if (self._debug) :
            print("[debug] Ecran : r=", r, " g=", g, " b=", b)

        if self._r != r:
            self._r = r
            self.set_register(0x04, r)

        if self._g != g:
            self._g = g
            self.set_register(0x03, g)

        if self._b != b:
            self._b = b
            self.set_register(0x02, b)

    def cmd(self, command):
        assert command >= 0 and command < 256
        val = bytes((0x80, command))
        i2c.write(0x3e, val)
        time.sleep_ms(self._delay)

    def write_char(self, c):
        assert c >= 0 and c < 256
        val = bytes((0x40, c))
        i2c.write(0x3e, val)
        time.sleep_ms(self._delay)

    def write(self, text):
        text = str(text)
        if (self._debug) :
            print("[debug] Ecran : ", text)
        for char in text:
            self.write_char(ord(char))

    def setCursor(self, col, row):
        col = (col | 0x80) if row == 0 else (col | 0xc0)
        self.cmd(col)

    def display1(self, state):
        if state:
            self.disp_ctrl |= 0x04
            self.cmd(0x08  | self.disp_ctrl)
        else:
            self.disp_ctrl &= ~0x04
            self.cmd(0x08  | self.disp_ctrl)

    def clear(self):
        if (self._debug) :
            print("[debug] Ecran : Clear")
        self.cmd(0x01)
        time.sleep_ms(2)