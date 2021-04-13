# Initialisation de la carte
# Création de interface avec l'écran et le capteur
from initialisation import *

# Création des objets lcd et capteur
lcd = afficheur_lcd()
capteur = CapteurPulsation()

# Boucle infinie
while (True):
    # Lecture de la valeur de la pulsation
    val = capteur.lire_pulsation()

    # Effacement de l'écran LCD
    lcd.clear()

    # Ecriture du texte
    lcd.write(val)

    # On attend avant de rafraichir
    sleep_ms(1000)