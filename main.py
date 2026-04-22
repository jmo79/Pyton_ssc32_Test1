#python -m compileall .
#python -m py_compile main.py

import time
import mTimer
from robot import *     #python -m py_compile main.py
from Interface import *

def SwithToManu():
    print("Ask to switch to Manu")

def SwithToAuto():
    print("Ask to switch to Manu")

InterfaceActions = {
    "ModeManu": SwithToManu,
    "ModeAuto": SwithToAuto,
}







numCyclage = 0

def ActionRobot():
 #   Robot_Mvt1()
 #   time.sleep(5)
 #   Robot_Mvt2()
    global numCyclage 
    numCyclage = 10 + numCyclage
    print ("cylage" + str(numCyclage))
    root.after(1000, ActionRobot)

print(mTimer.__file__)
print(dir(mTimer))
print("=== JE SUIS LE BON MAIN ===")

T1 = mTimer.create_ton(2000)
T1["Q"]= False;
T1["IN"]= True;


while T1["Q"] == False:
    mTimer.update_ton(T1,mTimer.now_ms())
    print("wait timer T1: " + str(T1["ET"]))


T2 = mTimer.TON(5000)
T2.IN = True

while T2.DN == False:
    T2.update()
    print("wait timer T2a: " + str(T2.ET))
T2.IN = False
T2.update()  
T2.PRE = 3500
T2.IN = True
while T2.DN == False:
    T2.update()
    print("wait timer T2b: " + str(T2.ET) )

   


"""





Robot_CommunicationStart()
# --- Appel de la fonction pour créer la fenêtre ---
root = creer_interface(InterfaceActions)

# --- Démarre la boucle principale ---
root.after(0, ActionRobot)
root.mainloop()

Robot_CommunicationStop()

"""


"""

#time.sleep(2)  # laisse le temps à la carte de démarrer
import tkinter as tk

# Crée la fenêtre principale
root = tk.Tk()  # T majuscule
root.title("Interface SSC-32")
root.geometry("300x150")  # largeur x hauteur

# Fonction pour le premier bouton
def bouton1_action():
    print("Bouton 1 cliqué !")

# Fonction pour le deuxième bouton
def bouton2_action():
    print("Bouton 2 cliqué !")

# Création des boutons
button1 = tk.Button(root, text="Bouton 1", command=bouton1_action)
button1.pack(pady=10)  # pack avec un peu d'espace vertical

button2 = tk.Button(root, text="Bouton 2", command=bouton2_action)
button2.pack(pady=10)

# Démarre la boucle principale de l'interface
root.mainloop()
"""
"""

# Déplacer le servo 0 à la position 1500 µs
cmd = "#1P1800S250#2P1700S250#3P1000S250#4P1000S250#5P1000S250\r"
#cmd = "#1P1500S50#2P1500S50#3P1500S50#4P1500S50#5P1500S50\r"
ser.write(cmd.encode())
print("Commande 1 envoyée au servos")


time.sleep(5)  # laisse le temps à la carte de démarrer

cmd = "#1P1500S250#2P1500S250#3P1500S250#4P1500S250#5P1500S250\r"
ser.write(cmd.encode())

print("Commande 2 envoyée au servos")
"""

