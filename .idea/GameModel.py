# GameModel.py
import random
import threading
from Ball import Ball

class GameModel:
    def __init__(self, screen_id, width, height, transfer_manager):
        """
        Initializes the game model for a given screen.

        :param screen_id: Identifier for the screen (0 or 1)
        :param width: Width of the screen
        :param height: Height of the screen
        :param transfer_manager: Manager responsible for sending balls to the other screen
        """
        self.screen_id = screen_id
        self.width = width
        self.height = height
        self.transfer_manager = transfer_manager
        self.balls = []
        self.lock = threading.Lock()

    def create_ball(self):
        """
        Create a new ball with random position and direction, and add it to the model.
        """
        ball_id = len(self.balls)
        x = random.randint(50, self.width - 50)
        y = random.randint(50, self.height - 50)
        dx = random.choice([-2, 2])
        dy = random.choice([-2, 2])
        color = random.choice(["red", "green", "blue", "yellow"])
        ball = Ball(ball_id, x, y, dx, dy, color)
        print(f"Bola {ball_id} iniciada en pantalla {self.screen_id}")
        with self.lock:
            self.balls.append(ball)

    def update_balls(self):
        """
        Updates the position of each ball and handles bouncing and transfer between screens.
        """
        with self.lock:
            new_balls = []
            for ball in self.balls:
                # Move the ball
                ball.update_position()

                # Bounce vertically (top/bottom)
                if ball.y <= 0 or ball.y >= self.height:
                    ball.dy *= -1

                # Handle cooldown period after transfer
                if ball.just_transferred > 0:
                    ball.just_transferred -= 1
                    new_balls.append(ball)
                    continue

                # Transfer logic when the ball leaves the screen horizontally
                if ball.x < 0:
                    if self.screen_id == 0:
                        ball.just_transferred = 10  # Prevent bouncing back immediately
                        self.transfer_manager.send_ball(ball, 1)
                    else:
                        ball.dx *= -1  # Bounce if it's the last screen
                        new_balls.append(ball)

                elif ball.x > self.width:
                    if self.screen_id == 1:
                        ball.just_transferred = 10
                        self.transfer_manager.send_ball(ball, 0)
                    else:
                        ball.dx *= -1
                        new_balls.append(ball)

                else:
                    # If the ball is within the screen horizontally, keep it
                    new_balls.append(ball)

            self.balls = new_balls

    def add_ball(self, ball):
        """
        Add a transferred ball to this model.

        :param ball: Ball object received from another screen
        """
        print(f"[Pantalla {self.screen_id}] Recibe bola transferida: {ball.to_dict()}")
        ball.just_transferred = 10  # Set cooldown to avoid immediate re-transfer
        with self.lock:
            self.balls.append(ball)

    def get_balls(self):
        """
        Return the current list of balls (thread-safe).
        """
        with self.lock:
            return list(self.balls)