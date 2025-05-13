import pygame
from Ball import Ball
from BallDTO import BallDTO
from BallTransferManager import BallTransferManager

class GameController:
    def __init__(self, screen_index, screen_count, model):
        # Save reference to model and screen configuration
        self.model = model
        self.screen_index = screen_index
        self.screen_count = screen_count

        # Time control for updates (frames per second)
        self.clock = pygame.time.Clock()

        # Flag to stop the game loop
        self.running = True

        # Initialize transfer manager for sending and receiving balls
        self.transfer_manager = BallTransferManager(
            screen_index,
            screen_count,
            self.receive_balls  # callback function to receive balls
        )

    def receive_balls(self, ball_dtos):
        """Callback function to receive transferred balls from another screen."""
        for dto in ball_dtos:
            ball = Ball.from_dto(dto)
            print(f"[Screen {self.screen_index}] Received transferred ball: {dto}")
            self.model.add_ball(ball)

    def update(self):
        """Update all game logic."""
        # Move each ball
        for ball in self.model.balls[:]:  # Work on a copy of the list
            ball.move()

            # Bounce off top and bottom walls
            if ball.y - ball.radius <= 0 or ball.y + ball.radius >= self.model.height:
                ball.dy *= -1

            # Determine if ball should transfer to another screen
            if self.screen_index > 0 and ball.x - ball.radius <= 0:
                # Transfer to previous screen (left)
                dto = ball.to_dto()
                self.model.remove_ball(ball)
                self.transfer_manager.send_balls([dto], self.screen_index - 1)
                print(f"Ball {ball.id} transferred from {self.screen_index} to {self.screen_index - 1}")
            elif self.screen_index < self.screen_count - 1 and ball.x + ball.radius >= self.model.width:
                # Transfer to next screen (right)
                dto = ball.to_dto()
                self.model.remove_ball(ball)
                self.transfer_manager.send_balls([dto], self.screen_index + 1)
                print(f"Ball {ball.id} transferred from {self.screen_index} to {self.screen_index + 1}")

    def handle_events(self):
        """Handle user input and system events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False  # Stop the main loop
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Add a new ball at mouse position when user clicks
                x, y = pygame.mouse.get_pos()
                ball = Ball(x, y)
                print(f"Ball {ball.id} started on screen {self.screen_index}")
                self.model.add_ball(ball)

    def run_step(self):
        """Execute a single game frame."""
        self.handle_events()
        self.update()
        return self.running

    def get_balls(self):
        """Return the list of balls currently in the model."""
        return self.model.balls

    def stop(self):
        """Stop the game loop and close the socket."""
        self.running = False
        self.transfer_manager.close()