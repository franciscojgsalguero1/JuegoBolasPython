import threading
from Ball import Ball
from BallDTO import BallDTO

class GameModel:
    def __init__(self, screen_index, screen_width, screen_height):
        self.screen_index = screen_index
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.balls = []
        self.ball_id_counter = 0
        self.lock = threading.Lock()
        self.just_received = {}

    def update_balls(self):
        with self.lock:
            for ball in self.balls:
                ball.move()
                ball.check_wall_collision(self.screen_width, self.screen_height)

    def get_balls(self):
        with self.lock:
            return list(self.balls)

    def add_ball(self):
        with self.lock:
            ball = Ball(self.ball_id_counter, self.screen_width, self.screen_height)
            ball.screen_index = self.screen_index
            self.balls.append(ball)
            self.ball_id_counter += 1
            print(f"Bola {ball.id} iniciada en pantalla {self.screen_index}")

    def add_received_ball(self, ball_dto):
        with self.lock:
            ball = Ball.from_dto(ball_dto)
            ball.screen_index = self.screen_index
            ball.x = 0 + ball.radius
            self.balls.append(ball)
            print(f"[Pantalla {self.screen_index}] Recibe bola transferida: {ball_dto}")

    def get_balls_to_transfer(self):
        with self.lock:
            to_transfer = []
            remaining = []
            for ball in self.balls:
                if self.screen_index == 0 and ball.x + ball.radius >= self.screen_width:
                    to_transfer.append(ball)
                else:
                    remaining.append(ball)
            self.balls = remaining
            return to_transfer