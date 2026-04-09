import tkinter as tk  # pour l'interface



def creer_interface(start_robot,stop_robot):
    """Crée la fenêtre et le bouton"""
    root = tk.Tk()
    root.title("Interface SSC-32")
    root.geometry("300x200")

    # Bouton Manu
    bouton_start = tk.Button(root, text="Manu", command=start_robot)
    bouton_start.pack(padx=1, pady=1)

    # Bouton Auto
    bouton_stop = tk.Button(root, text="Auto", command=stop_robot)
    bouton_stop.pack(padx=10, pady=20)


    return root