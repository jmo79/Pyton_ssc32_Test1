import tkinter as tk  # pour l'interface



def creer_interface(InterfaceActions):
    """Crée la fenêtre et le bouton"""
    root = tk.Tk()
    root.title("Interface SSC-32")
    root.geometry("300x200")


    # Bouton Manu
    bouton_manu = tk.Button(root, text="Manu", command=InterfaceActions["ModeManu"])
    bouton_manu.pack(padx=1, pady=1)

    # Bouton Auto
    bouton_auto = tk.Button(root, text="Auto", command=InterfaceActions["ModeAuto"])
    
    bouton_auto.pack(padx=10, pady=20)


    return root