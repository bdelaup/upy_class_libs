# Initialisation de la carte
# Création de interface avec l'écran et le capteur
# from initialisation import *
# from time import sleep_ms
# # from utime import sleep_ms
# 
# # Création des objets lcd et capteur
# lcd = lcd_display(0)
# # capteur = CapteurPulsation()
# 
# # Boucle infinie
# while (True):
#     # Lecture de la valeur de la pulsation
#     val = 42 #capteur.lire_pulsation()
# 
#     # Effacement de l'écran LCD
#     lcd.clear()
# 
#     # Ecriture du texte
#     lcd.write(val)
# 
#     # On attend avant de rafraichir
#     sleep_ms(1000)
#     
from microbit import *
from micropython import const
from lcd import lcd_display
from i2c_utils import scan_i2c_sensors
from time import sleep_ms
import gc

# Parametrage 
OFFSET_WHEATSTONE_BRIDGE = const(297)
a = const(0.0687)
b = const(0.0018)

# Fin Parametrage 

#define LOAD_SENSOR_IN A3
DATA_SMOOTH_SIZE = const(50)
SAMPLE_TIME = const(20)

#define TXT_SIZE 16
#define WHITE_LINE " 


if __name__ == "__main__":
    lcd = lcd_display()
    lcd.write("Demarrage ...")
    sleep(1)

    scale_input = pin0
    scale_sensor_value = 0
    
    #read the analog in value. 
    #Sample several time to smooth the noise.
    while(True):
        for j in range (DATA_SMOOTH_SIZE):
            scale_sensor_value = scale_sensor_value + scale_input.read_analog()
            sleep_ms(SAMPLE_TIME);
        
        scale_sensor_value = scale_sensor_value / DATA_SMOOTH_SIZE;
        scale_sensor_value = scale_sensor_value - OFFSET_WHEATSTONE_BRIDGE;
        weight_kg = scale_sensor_value * a + b;

        print("poids_kg : ", "%.2f"%weight_kg, "scale_sensor_value : ", "%.2f"%scale_sensor_value);
        lcd.clear()

        lcd.write("%.2f"%weight_kg + "Kg")
        gc.collect()
