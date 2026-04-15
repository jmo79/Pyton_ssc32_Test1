import serial
import time

ser = None # cariable global

def Robot_CommunicationStart():
    global ser
    ser = serial.Serial('COM1', 115200, timeout=1)
    
    time.sleep(2)  # laisse le temps à la carte de démarrer

def Robot_CommunicationStop():
    global ser
    ser.close()

def Robot_Mvt1(): 
    global ser
    # Déplacer le servo 0 à la position 1500 µs
    cmd = "#1P1800S250#2P1700S250#3P1000S250#4P1000S250#5P1000S250\r"
    ser.write(cmd.encode())
    print("Commande Mvt1 envoyée au servos")

def Robot_Mvt2():  
    global ser
    # Déplacer le servo 0 à la position 1500 µs
    cmd = "#1P1500S50#2P1500S50#3P1500S50#4P1500S50#5P1500S50\r"
    ser.write(cmd.encode())
    print("Commande Mvt2 envoyée au servos")