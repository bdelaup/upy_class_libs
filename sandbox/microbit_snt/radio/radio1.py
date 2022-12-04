import radio
import random
from microbit import display, Image, button_a, sleep, button_b


def radio_io():
    while True:
        # Button A sends a "flash" message.
        if button_a.was_pressed():
            radio.send('A')  # a-ha
            
        if button_b.was_pressed():
            radio.send('B')  # a-ha

        # Read any incoming messages.
        incoming = radio.receive()
        
        if incoming == 'A':
            print("<- A")
            
            display.scroll("A")
        
        if incoming == 'B':
            print("<- B")
            
            display.scroll("B")
        
        sleep(100)

