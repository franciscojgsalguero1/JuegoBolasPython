import multiprocessing
import pygame
import sys
from GameModel import GameModel
from GameView import GameView
from GameController import GameController
from BallTransferManager import BallTransferManager

def game_loop(screen_id, send_queues, recv_queues, model):
    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption(f"Screen {screen_id}")
    clock = pygame.time.Clock()

    view = GameView(screen, screen_id)
    controller = GameController(model)

    controller.create_ball(screen_id)

    transfer_manager = BallTransferManager(
        screen_id,
        send_queues,
        recv_queues,
        model.get_balls,
        model.set_balls
    )
    transfer_process = multiprocessing.Process(target=transfer_manager.run, args=(600,))
    transfer_process.start()

    try:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            balls = model.get_balls()
            for ball in balls:
                ball.move()
                ball.bounce(600, 400)

            model.set_balls(balls)
            view.draw(balls)
            clock.tick(60)

    finally:
        print(f"[Pantalla {screen_id}] Esperando que las bolas terminen antes de cerrar...")
        transfer_process.terminate()
        pygame.quit()

if __name__ == "__main__":
    model0 = GameModel()
    model1 = GameModel()

    queue_0_to_1 = multiprocessing.Queue()
    queue_1_to_0 = multiprocessing.Queue()

    p0 = multiprocessing.Process(target=game_loop, args=(0, {1: queue_0_to_1}, {0: queue_1_to_0}, model0))
    p1 = multiprocessing.Process(target=game_loop, args=(1, {0: queue_1_to_0}, {1: queue_0_to_1}, model1))

    p0.start()
    p1.start()

    p0.join()
    p1.join()
    print("Todas las pantallas se han cerrado. Fin del programa.")
