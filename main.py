print("Hello SSC32 World!")

import serial
import time

# ⚠️ Remplace 'COM3' par le port réel de ta SSC-32
ser = serial.Serial('COM1', 2400, timeout=1)

time.sleep(2)  # laisse le temps à la carte de démarrer

# Déplacer le servo 0 à la position 1500 µs
cmd = "#1P1700S20\r"
ser.write(cmd.encode())

print("Commande envoyée au servo 1")

ser.close()