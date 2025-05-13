import pygame

class GameView:
    def __init__(self, screen_index, width, height):
        # Initialize screen properties
        self.screen_index = screen_index
        self.width = width
        self.height = height

        # Create the window with its size and title
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(f"Screen {screen_index}")

    def draw(self, balls):
        """Draw all balls and update the screen."""
        # Fill the background with black color
        self.screen.fill((0, 0, 0))

        # Draw each ball as a circle
        for ball in balls:
            pygame.draw.circle(self.screen, ball.color, (int(ball.x), int(ball.y)), ball.radius)

        # Refresh the screen
        pygame.display.flip()