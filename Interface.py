import tkinter as tk  # pour l'interface



def creer_interface():
    """Crée la fenêtre et le bouton"""
    root = tk.Tk()
    root.title("Interface SSC-32")
    root.geometry("300x200")

    # Bouton Start
    bouton_start = tk.Button(root, text="Start", command=start_robot)
    bouton_start.pack(padx=10, pady=10)

    # Bouton Stop
    bouton_stop = tk.Button(root, text="Stop", command=stop_robot)
    bouton_stop.pack(padx=10, pady=10)


    return root