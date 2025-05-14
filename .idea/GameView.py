import pygame

class GameView:
    def __init__(self, screen_id, screen_width, screen_height):
        self.screen_id = screen_id
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.window = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption(f"Ball Game - Screen {screen_id}")
        self.font = pygame.font.SysFont('Arial', 24)
        try:
            pygame.mixer.init()
            self.transfer_sound = pygame.mixer.Sound("transfer.wav")
        except:
            print("Could not load transfer sound")
            self.transfer_sound = None

    def draw(self, balls):
        self.window.fill((0, 0, 0))  # Clear screen with black

        for ball in balls:
            if ball.transferring:
                # On sending screen (origin screen)
                if ball.origin_screen == self.screen_id:
                    # Draw shrinking ball
                    current_radius = int(ball.radius * (1 - ball.transfer_progress))
                    if current_radius > 0:
                        pygame.draw.circle(self.window, ball.color,
                                           (int(ball.x), int(ball.y)),
                                           current_radius)
                # On receiving screen
                else:
                    # Draw growing ball at the edge
                    current_radius = int(ball.radius * ball.transfer_progress)
                    if current_radius > 0:
                        if ball.dx > 0:  # Coming from left
                            x = int(current_radius)
                        else:  # Coming from right
                            x = int(self.screen_width - current_radius)

                        pygame.draw.circle(self.window, ball.color,
                                           (x, int(ball.y)),
                                           current_radius)

                        # Play sound at start of transfer
                        if ball.transfer_progress < 0.1 and self.transfer_sound:
                            self.transfer_sound.play()
            else:
                # Normal ball rendering
                pygame.draw.circle(self.window, ball.color,
                                   (int(ball.x), int(ball.y)),
                                   ball.radius)

        # Draw ball counter
        text = self.font.render(f"Balls: {len(balls)}", True, (255, 255, 255))
        self.window.blit(text, (10, 10))

        pygame.display.flip()

    def close(self):
        pygame.quit()