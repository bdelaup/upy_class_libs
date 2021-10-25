import machine, ssd1306
i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(18))
oled = ssd1306.SSD1306_I2C(0, 128, 32, i2c, 0x3c)
oled.fill(0)
oled.text("Hello World", 0, 0)
oled.show()