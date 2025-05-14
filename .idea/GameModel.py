import threading
import time
from Ball import Ball

class GameModel:
    def __init__(self, screen_index, screen_width, screen_height):
        self.screen_index = screen_index
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.balls = []
        self.ball_id_counter = 0
        self.lock = threading.Lock()
        self.received_time = {}

    def update_balls(self):
        now = time.time()
        with self.lock:
            for ball in self.balls[:]:  # Create a copy for iteration
                if not ball.transferring:
                    ball.move()
                    ball.check_wall_collision(self.screen_width, self.screen_height)
                else:
                    if ball.update_transfer(1/60):  # Assuming 60fps
                        self.balls.remove(ball)

            # Filter out balls that are being immediately retransferred
            self.balls = [ball for ball in self.balls if not self._is_immediate_retransfer(ball, now)]

    def _is_immediate_retransfer(self, ball, now):
        if ball.id in self.received_time:
            return now - self.received_time[ball.id] < 0.3  # Short cooldown
        return False

    def get_balls(self):
        with self.lock:
            return list(self.balls)

    def add_ball(self):
        with self.lock:
            ball = Ball(self.ball_id_counter, self.screen_width, self.screen_height)
            self.balls.append(ball)
            self.ball_id_counter += 1
            print(f"Ball {ball.id} created on screen {self.screen_index}")

    def get_balls_to_transfer(self):
        with self.lock:
            to_transfer = []
            for ball in self.balls:
                if ball.is_off_screen(self.screen_width) and not ball.transferring:
                    ball.start_transfer(self.screen_index)
                    to_transfer.append(ball)
            return to_transfer

    def add_received_ball(self, dto):
        with self.lock:
            ball = Ball.from_dto(dto)
            # Position ball at correct edge
            if ball.dx > 0:  # Coming from left
                ball.x = -ball.radius
            else:  # Coming from right
                ball.x = self.screen_width + ball.radius

            self.balls.append(ball)
            self.received_time[ball.id] = time.time()
            print(f"Ball {ball.id} received on screen {self.screen_index}")