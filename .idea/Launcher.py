# Importa tkinter para crear una interfaz gráfica simple
import tkinter as tk
# Importa multiprocessing para lanzar pantallas como procesos separados
import multiprocessing
# Importa time para poder hacer pausas entre lanzamientos
import time
# Importa la función que lanza una pantalla individual desde tu Main.py
from Main import run_screen

# Lista global que almacena los procesos de pantallas activas
screen_processes = []

# Número máximo de pantallas que se pueden abrir
MAX_SCREENS = 2

# Función que se ejecuta cuando se presiona el botón "Abrir pantalla"
def open_new_screen():
    # Cuenta cuántas pantallas hay abiertas actualmente
    current_count = len(screen_processes)

    # Solo permite abrir una nueva si hay menos de 2
    if current_count < MAX_SCREENS:
        # Crea un nuevo proceso con el índice adecuado (0 o 1)
        p = multiprocessing.Process(target=run_screen, args=(current_count,))
        p.start()  # Inicia el proceso
        screen_processes.append(p)  # Guarda el proceso en la lista
        print(f"Pantalla {current_count} iniciada.")
        # Espera 1 segundo para evitar que ambas pantallas intenten conectar al mismo tiempo
        time.sleep(1)
    else:
        # Si ya hay 2 pantallas, no permite abrir más
        print("No se pueden abrir más de dos pantallas.")

# Función principal que lanza la ventana del lanzador
def main():
    # En Windows (y recomendable en general), se debe establecer el método 'spawn'
    multiprocessing.set_start_method('spawn')

    # Crea la ventana principal de la interfaz
    root = tk.Tk()
    root.title("Lanzador de pantallas")  # Título de la ventana
    root.geometry("300x150")             # Tamaño de la ventana

    # Etiqueta de instrucción
    label = tk.Label(root, text="Haz clic para abrir una nueva pantalla:")
    label.pack(pady=20)  # Espaciado vertical

    # Botón que al hacer clic llama a la función para abrir pantallas
    open_button = tk.Button(root, text="Abrir pantalla", command=open_new_screen)
    open_button.pack()

    # Permite cerrar la ventana normalmente
    root.protocol("WM_DELETE_WINDOW", root.quit)

    # Inicia el bucle principal de la interfaz gráfica
    root.mainloop()

    # Al cerrar la ventana, termina y espera cada proceso de pantalla
    for p in screen_processes:
        p.terminate()  # Detiene el proceso
        p.join()       # Espera a que termine completamente

# Ejecuta la función main si este archivo se ejecuta directamente
if __name__ == "__main__":
    main()