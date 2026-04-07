print("Hello SSC32 World!")

import serial
import time

# ⚠️ Remplace 'COM3' par le port réel de ta SSC-32
ser = serial.Serial('COM1', 2400, timeout=1)

time.sleep(2)  # laisse le temps à la carte de démarrer

# Déplacer le servo 0 à la position 1500 µs
cmd = "#1P1800S250#2P1700S250#3P1000S250#4P1000S250#5P1000S250\r"
#cmd = "#1P1500S50#2P1500S50#3P1500S50#4P1500S50#5P1500S50\r"
ser.write(cmd.encode())
print("Commande 1 envoyée au servos")


time.sleep(5)  # laisse le temps à la carte de démarrer

cmd = "#1P1500S250#2P1500S250#3P1500S250#4P1500S250#5P1500S250\r"
ser.write(cmd.encode())

print("Commande 2 envoyée au servos")

ser.close()