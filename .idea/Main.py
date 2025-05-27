import pygame                      # Librería para gráficos y eventos
import time                        # Para hacer pausas
import multiprocessing             # Para lanzar procesos
from GameModel import GameModel
from GameView import GameView
from GameController import GameController
from BallTransferManager import BallTransferManager

# Dimensiones de la ventana de juego
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
# Puerto base para las conexiones por socket
PORT = 1000

# Función que representa una pantalla individual del juego
# Esta función puede ser lanzada por múltiples procesos
def run_screen(screen_index):
    # Inicializa pygame en este proceso
    pygame.init()

    # Inicializa el modelo, vista y controlador para esta pantalla
    model = GameModel(screen_index, SCREEN_WIDTH, SCREEN_HEIGHT)
    view = GameView(screen_index, SCREEN_WIDTH, SCREEN_HEIGHT)
    controller = GameController(model, None)

    # Crea el gestor de transferencia (envío/recepción de bolas entre pantallas)
    transfer_manager = BallTransferManager(
        screen_index,
        PORT,
        controller.handle_received_balls  # Callback que se llama cuando se reciben bolas
    )
    # Asigna el gestor al controlador
    controller.transfer_manager = transfer_manager

    # Crea un reloj para regular los FPS del juego
    clock = pygame.time.Clock()
    running = True

    # Bucle principal de ejecución de la pantalla
    while running:
        # Maneja eventos (como cerrar la ventana)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Actualiza lógica del juego
        controller.update()
        # Dibuja las bolas en la pantalla
        view.draw(model.get_balls())
        # Espera para mantener 60 FPS
        clock.tick(60)

    # Al cerrar la ventana, limpia recursos
    print(f"[Pantalla {screen_index}] Esperando que las bolas terminen antes de cerrar...")
    transfer_manager.close()
    view.close()

# Punto de entrada del archivo si se ejecuta directamente (no desde Launcher)
if __name__ == "__main__":
    multiprocessing.set_start_method('spawn')

    # Ejecuta ambas pantallas automáticamente si se ejecuta sin el Launcher
    screen_0 = multiprocessing.Process(target=run_screen, args=(0,))
    screen_1 = multiprocessing.Process(target=run_screen, args=(1,))

    screen_0.start()
    time.sleep(1)  # Espera para evitar colisiones de conexión
    screen_1.start()

    screen_0.join()
    screen_1.join()

    print("Todas las pantallas se han cerrado. Fin del programa.")