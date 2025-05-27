import multiprocessing
import pygame
import time
from GameModel import GameModel
from GameView import GameView
from GameController import GameController
from BallTransferManager import BallTransferManager

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
PORT = 1000

def run_screen(screen_index):
    pygame.init()

    # Inicializa modelo, vista y controlador
    model = GameModel(screen_index, SCREEN_WIDTH, SCREEN_HEIGHT)
    view = GameView(screen_index, SCREEN_WIDTH, SCREEN_HEIGHT)
    controller = GameController(model, None)

    # Inicializa gestor de transferencia
    transfer_manager = BallTransferManager(
        screen_index,
        PORT,
        controller.handle_received_balls  # Callback para recibir bolas
    )
    controller.transfer_manager = transfer_manager

    clock = pygame.time.Clock()
    running = True

    # Bucle principal de juego
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        controller.update()
        view.draw(model.get_balls())
        clock.tick(60)

    print(f"[Pantalla {screen_index}] Esperando que las bolas terminen antes de cerrar...")
    transfer_manager.close()
    view.close()

if __name__ == "__main__":
    multiprocessing.set_start_method('spawn')

    # Crea los dos procesos para pantalla 0 y 1
    screen_0 = multiprocessing.Process(target=run_screen, args=(0,))
    screen_1 = multiprocessing.Process(target=run_screen, args=(1,))

    screen_0.start()
    time.sleep(1)  # Pausa para evitar que ambas pantallas conecten al mismo tiempo
    screen_1.start()

    screen_0.join()
    screen_1.join()

    print("Todas las pantallas se han cerrado. Fin del programa.")