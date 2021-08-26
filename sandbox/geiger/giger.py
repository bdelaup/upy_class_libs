

from interrupt_counter import Counter
import time

if __name__=="__main__":
    # Watch pin 20 for rizing edge
    pin = machine.Pin(6)
    # Compute signal frequency once per seconde (1hz)
    freq= 1/60
    #Create counter
    cnt = Counter(pin, freq)
    while (True):
        print ("Compteur : ", cnt.get_counter(), " frequency : ", cnt.get_signal_frequency())
        time.sleep(1)




from interrupt_counter import Counter
import time

# Initialise rising edge detection
counter = 0
def sig_secondary_handler(p):
    global counter
    counter +=1      


pin = machine.Pin(6)
pin.init(machine.Pin.IN, machine.Pin.IRQ_FALLING  )
pin.irq(trigger=machine.Pin.IRQ_RISING, handler=sig_secondary_handler)

  
while (True):
    print ("Compteur : ", counter)
    time.sleep(1)
    
    

from interrupt_counter import Counter
import time

# Initialise rising edge detection
counter = 0
def sig_secondary_handler(p):
    global counter
    counter +=1      


pin = machine.Pin(6)
pin.init(machine.Pin.IN)
pin.irq(trigger=machine.Pin.IRQ_RISING, handler=sig_secondary_handler)
# print (machine.Pin.IRQ_FALLING )
# print (machine.Pin.PULL_UP)
# print (machine.Pin.PULL_DOWN)
  
while (True):
    print ("Compteur : ", counter)
    time.sleep(1)
