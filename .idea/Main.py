from multiprocessing import Process, Manager, freeze_support
from GameController import start_game
from BallTransferManager import BallTransferManager
import time

manager = None  # referencia global

if __name__ == "__main__":
    freeze_support()
    manager = Manager()
    transfer_manager = BallTransferManager(manager)

    processes = []
    for game_id in (0, 1):
        p = Process(target=start_game, args=(game_id, transfer_manager))
        p.start()
        processes.append(p)

    try:
        while True:
            time.sleep(1)
            if not any(transfer_manager.active_games.values()):
                print("Todas las pantallas se han cerrado. Fin del programa.")
                break
    except KeyboardInterrupt:
        print("Interrupción manual. Cerrando procesos...")

    for p in processes:
        p.join()