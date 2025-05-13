import time
from Ball import Ball

class BallTransferManager:
    def __init__(self, screen_id, send_queues, recv_queues, get_balls_func, set_balls_func):
        self.screen_id = screen_id
        self.send_queues = send_queues
        self.recv_queues = recv_queues
        self.get_balls = get_balls_func
        self.set_balls = set_balls_func

    def run(self, width):
        while True:
            time.sleep(0.01)

            balls = self.get_balls()
            remaining_balls = []
            balls_to_transfer = {0: [], 1: []}

            for ball in balls:
                if ball.should_transfer(width):
                    dest_screen_id = 1 - self.screen_id
                    ball.last_transfer_time = time.time()
                    balls_to_transfer[dest_screen_id].append(ball.to_dto())
                    print(f"Bola {ball.id} transferida de {self.screen_id} a {dest_screen_id}")
                else:
                    remaining_balls.append(ball)

            self.set_balls(remaining_balls)

            for dest_id, dto_list in balls_to_transfer.items():
                if dto_list:
                    try:
                        self.send_queues[dest_id].put(dto_list)
                        print(f"[TransferManager] Enviando {len(dto_list)} bolas a pantalla {dest_id}")
                    except:
                        pass

            try:
                received_dtos = self.recv_queues[self.screen_id].get_nowait()
                if received_dtos:
                    new_balls = [Ball.from_dto(dto, self.screen_id) for dto in received_dtos]
                    print(f"[Pantalla {self.screen_id}] Recibe bola transferida: {received_dtos}")
                    self.set_balls(self.get_balls() + new_balls)
                    for ball in new_balls:
                        print(f"Bola {ball.id} iniciada en pantalla {self.screen_id}")
            except:
                pass
