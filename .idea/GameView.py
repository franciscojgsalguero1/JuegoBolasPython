import pygame

class GameView:
    def __init__(self, screen_id, screen_width, screen_height):
        self.screen_id = screen_id
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.window = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption(f"Ball Game - Screen {screen_id}")
        self.font = pygame.font.SysFont(None, 24)

    def draw(self, balls):
        self.window.fill((0, 0, 0))
        for ball in balls:
            pygame.draw.circle(self.window, pygame.Color(ball.color), (int(ball.x), int(ball.y)), ball.radius)
        text = self.font.render(f"Balls: {len(balls)}", True, (255, 255, 255))
        self.window.blit(text, (10, 10))
        pygame.display.flip()

    def close(self):
        pygame.quit()