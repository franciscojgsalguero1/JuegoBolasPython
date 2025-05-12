import random
from Ball import Ball
from BallDTO import BallDTO

class GameModel:
    def __init__(self, game_id, transfer_manager):
        self.game_id = game_id
        self.transfer_manager = transfer_manager
        self.balls = []
        self.next_id = 0
        self.active = True

    def create_ball(self):
        dto = BallDTO(
            id=self.next_id,
            x=100,
            y=random.randint(50, 350),
            dx=random.choice([2, 3]),
            dy=random.choice([-2, 2]),
            color=random.choice(["red", "green", "blue", "yellow"])
        )
        self.next_id += 1
        ball = Ball(dto, self)
        self.balls.append(ball)
        ball.start()
        print(f"Bola {dto.id} iniciada en pantalla {self.game_id}")

    def destroy_balls(self):
        for ball in self.balls:
            ball.alive = False
        self.balls.clear()

    def receive_transferred_balls(self):
        transferred = self.transfer_manager.get_transferred_balls(self.game_id)
        for dto in transferred:
            print(f"[Pantalla {self.game_id}] Recibe bola transferida: {dto.__dict__}")
            ball = Ball(dto, self)
            self.balls.append(ball)
            ball.start()