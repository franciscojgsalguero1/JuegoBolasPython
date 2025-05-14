import pygame
import multiprocessing
import time
import sys
from BallTransferManager import BallTransferManager
from GameController import GameController
from GameModel import GameModel
from GameView import GameView

def game_process(screen_index, width, height, connections):
    pygame.init()
    model = GameModel(screen_index, width, height)
    transfer_manager = BallTransferManager(screen_index, connections)
    controller = GameController(model, transfer_manager)
    view = GameView(screen_index, width, height)
    clock = pygame.time.Clock()

    while controller.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                controller.stop()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    controller.add_ball()

        controller.update()
        balls = model.get_balls()
        view.draw(balls)

        received_dto = transfer_manager.receive_balls()
        if received_dto:
            controller.handle_received_balls(received_dto)

        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    width, height = 600, 400
    conn1, conn2 = multiprocessing.Pipe()
    connections = [conn1, conn2]

    p1 = multiprocessing.Process(target=game_process, args=(0, width, height, connections))
    p2 = multiprocessing.Process(target=game_process, args=(1, width, height, connections))

    p1.start()
    p2.start()

    p1.join()
    p2.join()