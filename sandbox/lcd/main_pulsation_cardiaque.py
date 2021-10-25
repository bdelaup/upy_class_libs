# Initialisation de la carte
# Création de interface avec l'écran et le capteur
from initialisation import *
from time import sleep_ms
# from utime import sleep_ms

# Création des objets lcd et capteur
lcd = lcd_display(0)
# capteur = CapteurPulsation()

# Boucle infinie
while (True):
    # Lecture de la valeur de la pulsation
    val = 42 #capteur.lire_pulsation()

    # Effacement de l'écran LCD
    lcd.clear()

    # Ecriture du texte
    lcd.write(val)

    # On attend avant de rafraichir
    sleep_ms(1000)